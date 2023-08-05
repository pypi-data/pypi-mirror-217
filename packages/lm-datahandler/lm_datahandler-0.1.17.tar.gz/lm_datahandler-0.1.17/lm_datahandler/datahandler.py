import logging
import os
import sys
import pandas as pd
from scipy.io import savemat

from lm_datahandler.data_load import data_loader
from lm_datahandler.functions.biomarker import sw_detect, spindles_detect
from lm_datahandler.functions.feature_extract import RSCFeature, WearDectectFeature
from lm_datahandler.functions.sleep_staging import sleep_staging_with_features
from lm_datahandler.functions.wear_detect import wear_detect_with_features
import matplotlib.pyplot as plt
import seaborn as sns
from lm_datahandler.plots.sleep_staging_plot import plot_spectrogram, plot_avg_diff_acc, plot_sleep_staging_result, \
    plot_sleep_posture
from lm_datahandler.plots.stim_plot import plot_stim_sham_sw
from lm_datahandler.functions.sleep_variable_compute import *
from lm_datahandler.preprocess.filter import eeg_filter
from lm_datahandler.functions.posture_analyse import sleep_posture_analyse


class DataHandler(object):
    def __init__(self):

        self.sleep_postures = None
        self.raw_sti = None
        self.data_name = None
        self.logger = None
        self.sleep_variables = None
        self.seconds = None
        self.sp_df = None
        self.sleep_staging_result = None
        self.acc = None
        self.eeg = None
        self.biomarker = None
        self.features = pd.DataFrame({})
        self.supported_features = {}
        self.sf_eeg = 500
        self.sf_acc = 50
        self.epoch_len = 15
        self.sw_df = None

        self.set_logger()

    def set_logger(self):
        self.logger = logging.getLogger("LM Data Handler")
        self.logger.setLevel("INFO")
        # 创建一个handler，用于输出日志到控制台
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s: %(message)s'
        )
        # 将formatter添加到handler
        console_handler.setFormatter(formatter)
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        # 将handler添加到logger
        self.logger.addHandler(console_handler)

    def load_data_file(self, data_name, eeg_path, acc_path, ble_path, sti_path, person_info=None):
        assert data_name is not None, "Please check the data name and retry."

        self.data_name = data_name
        self.raw_eeg, self.eeg, self.raw_acc, self.acc, self.raw_sti, self.disconnections, self.total_time, self.start_time, self.package_loss_rate, self.disconnect_rate = data_loader.load_data(
            eeg_path, acc_path, sti_path, ble_path, logger=self.logger)

        eeg_sec = -1
        acc_sec = -1
        if self.eeg is not None and self.raw_eeg is not None:
            self.eeg = (self.eeg[0] - 32767) / 65536 * 2.5 * 1000 * 1000 / 100
            self.raw_eeg = self.raw_eeg[0]
            self.eeg = np.squeeze(self.eeg)
            eeg_sec = self.eeg.shape[0] // self.sf_eeg
            self.seconds = eeg_sec

        if self.acc is not None and self.raw_acc is not None:
            self.acc = self.acc - 32767
            self.acc = np.squeeze(self.acc)
            acc_sec = self.acc.shape[1] // self.sf_acc

        if eeg_sec != -1 and acc_sec != -1:
            assert eeg_sec == acc_sec, "EEG length have to be consistent with ACC."

        if self.eeg is not None:
            self.eeg = self.eeg[:self.seconds * self.sf_eeg]
        if self.acc is not None:
            self.acc = self.acc[:self.seconds * self.sf_acc]
        self.logger.info("Data loaded, {} total seconds".format(self.seconds))

        self.features['meta'] = {'male': 1, 'age': 30, 'data_type': 0, 'h/w': 0}
        if person_info is not None:
            if person_info['male'] is not None:
                self.features['meta']['male'] = person_info['male']
            if person_info['age'] is not None:
                self.features['meta']['age'] = person_info['age']
            if person_info['data_type'] is not None:
                self.features['meta']['data_type'] = person_info['data_type']
            if person_info['height'] is not None and person_info['weight'] is not None:
                self.features['meta']['h/w'] = person_info['height'] / person_info['weight']
        return self

    def load_data(self, data_name, data_path, person_info=None):
        assert data_name is not None, "Please check the data name and retry!"
        self.data_name = data_name
        eeg_path = None
        acc_path = None
        sti_path = None
        ble_path = None
        for file in os.listdir(data_path):
            if file.endswith(".eeg"):
                eeg_path = os.path.join(data_path, file)
            if file.endswith(".acc"):
                acc_path = os.path.join(data_path, file)
            if file.endswith(".sti"):
                sti_path = os.path.join(data_path, file)
            if file.endswith(".ble"):
                ble_path = os.path.join(data_path, file)
        self.load_data_file(data_name, eeg_path, acc_path, ble_path, sti_path, person_info)
        return self

    def save_data_to_mat(self, mat_path):
        if self.eeg is None:
            self.logger.info("Please load EEG data first.")
        if self.acc is None:
            self.logger.info("Please load ACC data first.")
        savemat(mat_path, {'EEG_total': self.eeg, 'ACC': self.acc, 'package_loss_rate': self.package_loss_rate,
                           'disconnect_rate': -1 if self.disconnect_rate is None else self.disconnect_rate})

    def load_hypno(self, hypno):
        hypno = np.asarray(hypno)
        if np.shape(hypno.shape) != 1 or hypno.shape[0] <= 0:
            self.logger.error("Format of hypno is incorrect, please check hypno is one-dimension array!")
            return
        if self.sleep_staging_result is not None and hypno.shape[0] != self.sleep_staging_result.shape[0]:
            self.logger.error("The length of hypno is not consistent with loaded EEG, please check!")
            return
        self.hypno = hypno
        return self

    def tailor_operation(self, tailor_type="drop_tail", tailor_param=None):
        if tailor_type == "no":
            return

        start_sec = None
        end_sec = None
        if tailor_type == "drop_tail":
            start_sec = 0
            end_sec = self.seconds // self.epoch_len * self.epoch_len
        if tailor_type == "custom" and tailor_param is not None:
            start_sec = tailor_param['start_sec']
            end_sec = tailor_param['end_sec']
            assert start_sec is not None and end_sec is not None, "tailor_param is a dict consist of start_sec and end_sec, please check!"
        if self.eeg is not None:
            self.eeg = self.eeg[start_sec * self.sf_eeg:end_sec * self.sf_eeg]
        if self.acc is not None:
            self.acc = self.acc[:, start_sec * self.sf_acc:end_sec * self.sf_acc]
        self.seconds = end_sec - start_sec
        self.logger.info(
            "Loaded data is clipped to a multiple of the window length, {} total seconds".format(self.seconds))

    def preprocess(self, filter_param={'highpass': 0.5, 'lowpass': None, 'bandstop': [[49, 51]]},
                   tailor_type="drop_tail", tailor_param=None):
        self.tailor_operation(tailor_type, tailor_param)

        self.highpass = filter_param['highpass']
        self.bandstop = filter_param['bandstop']
        self.lowpass = filter_param['lowpass']

        self.eeg = eeg_filter(self.eeg, self.sf_eeg, self.highpass, 3, self.lowpass, 3, self.bandstop, 3)
        log_info = "EEG filtered: "
        if self.highpass is not None:
            log_info += "Highpass: {} Hz".format(self.highpass)
        if self.lowpass is not None:
            log_info += ", Lowpass: {} Hz".format(self.lowpass)
        if self.bandstop is not None:
            log_info += ", Bandstop: {} Hz.".format(self.bandstop)
        self.logger.info(log_info)
        return self

    # def feature_extract(self, feature_names={}):
    #     unsupoort_features = feature_names - self.supported_features
    #     if len(unsupoort_features) > 0:
    #         self.logger.warning("{}/{} input features are not support: ".format(len(unsupoort_features), len(feature_names),
    #                                                                         unsupoort_features))

    def wear_detect(self, model_path=None):
        if model_path is not None:
            self.logger.info("Wear detect model is set, please make sure the features are corresponded.")
        person_info = dict(age=30, male=1, datatype=0)
        epochs = self.eeg.shape[0] // (self.sf_eeg * self.epoch_len)
        input_eeg = self.eeg[0:epochs * self.sf_eeg * self.epoch_len].reshape(-1, self.sf_eeg)
        wear_detect_features = WearDectectFeature(person_info, input_eeg, self.sf_eeg, context_mode=3).get_features()
        wear_detect_res = wear_detect_with_features(features=wear_detect_features, model_path=model_path)

        wear_detect_res = wear_detect_res.reshape([-1, 15])
        wear_detect_res = np.sum(wear_detect_res, axis=1)
        wear_detect_res[wear_detect_res <= 15 * 0.5] = 0
        wear_detect_res[wear_detect_res > 15 * 0.5] = 1

        return wear_detect_res

    def sleep_staging(self, use_acc=False, use_time=False, context_mode=2, model_path=None):
        if self.eeg is None:
            self.logger.info("The EEG data is not loaded, please load EEG first.")
        self.logger.info("Sleep staging started.")
        epochs = self.eeg.shape[0] // (self.sf_eeg * self.epoch_len)
        input_eeg = self.eeg[0:epochs * self.sf_eeg * self.epoch_len].reshape(-1, self.sf_eeg * self.epoch_len)
        # data = np.load('E:/dataset/x7_disorder/npzData/20230511_19145647867.npz')
        # input_eeg = data['x'].reshape(-1, 500*15)
        # epochs = 1800
        input_acc = None
        if use_acc and self.acc is not None:
            acc = self.acc[:, 0:epochs * self.sf_acc * self.epoch_len]
            # acc = data['acc']
            accx = acc[0, :].reshape(-1, 1, 750)
            accy = acc[1, :].reshape(-1, 1, 750)
            accz = acc[2, :].reshape(-1, 1, 750)
            input_acc = np.concatenate([accx, accy, accz], axis=1)

        self.features = RSCFeature(self.features['meta'], raw_eeg=input_eeg, raw_acc=input_acc,
                                   sf_eeg=self.sf_eeg, sf_acc=self.sf_acc).get_features()
        self.logger.info("Feature extraction finished.")
        predictions, pp_predictions = sleep_staging_with_features(self.features, use_acc=use_acc, use_time=use_time,
                                                                  context_mode=context_mode, model_path=model_path)

        wear_detect_res = self.wear_detect()
        pp_predictions[wear_detect_res == 0] = 4
        self.sleep_staging_result = pp_predictions
        self.logger.info("Sleep staging finished.")
        return self

    def plot_sleep_data(self, plot_spectral=True, plot_acc=True, plot_staging=True, plot_variables=True, savefig=None):
        if self.sleep_staging_result is None:
            self.logger.info("Sleep staging result is none, auto sleep staging will run first!")
        if self.acc is None:
            plot_acc = False
            self.logger.info("The ACC is not loaded, ACC plot will be skipped.")
        if plot_variables and self.sleep_variables is None:
            self.logger.info(
                "Sleep variables is none, and will computed first. If you don't want it, just change \"plot_variables\" to False.")
            self.compute_sleep_variables()

        subplot_count = 0 + 2 * plot_acc + plot_spectral + plot_staging
        fig, ax = plt.subplots(subplot_count, 1, figsize=(16, subplot_count * 4))
        fig.subplots_adjust(hspace=0.5)
        if subplot_count == 1:
            ax = [ax]

        i = 0
        if plot_spectral:
            plot_spectrogram(fig, ax[i], self.eeg, self.start_time, self.sf_eeg)
            i += 1
        if plot_acc:
            plot_avg_diff_acc(fig, ax[i], self.acc, self.start_time, self.sf_acc)
            i += 1
            if self.sleep_postures is None:
                self.sleep_postures = sleep_posture_analyse(self.acc)
            plot_sleep_posture(fig, ax[i], self.sleep_postures, self.start_time, self.sf_acc)
            i += 1
        if plot_staging:
            if self.sleep_staging_result is None:
                self.logger.info("The sleep staging result is None, auto sleep staging will run first!")
                self.sleep_staging()
            variables = None
            if plot_variables:
                variables = self.sleep_variables
                if variables is None:
                    self.logger.info("The sleep variables is None, sleep variables will be computed first.")
                    self.compute_sleep_variables()
                    variables = self.sleep_variables
            plot_sleep_staging_result(fig, ax[i], self.sleep_staging_result, variables, self.start_time)

        if savefig is not None:
            plt.savefig(savefig, dpi=300, bbox_inches='tight')
            self.logger.info("The sleep data plot is saved as {}".format(savefig))
        return self

    def compute_sleep_variables(self, hypno=None):

        if hypno is not None:
            self.logger.info("Sleep variables will be computed by the giving hypno instead of the loaded data!")
        else:
            if self.sleep_staging_result is None:
                self.logger.info("Sleep variables are based on sleep staging result, auto sleep staging will run first!")
                self.sleep_staging()
            hypno = np.copy(self.sleep_staging_result)


        tst = tst_compute(hypno, self.epoch_len)
        sl = sl_compute(hypno, self.epoch_len)
        if sl == -1:
            self.logger.info("No continuous sleep epochs are detected!")
            se = 0.0
            arousal_time = np.asarray([])
            arousal_count = 0
            waso = 0
            gu = -1
        else:
            gu = get_up_time_compute(hypno, self.epoch_len)
            se = se_compute(hypno)
            arousal_count, arousal_time = arousal_time_compute(hypno, self.epoch_len, sleep_range=[sl, gu])
            waso = arousal_time.shape[0] * self.epoch_len

        if sl >= 0 and gu >= 0 and gu + sl <= hypno.shape[0] * 15:
            sl_index = sl // 15
            gu_index = (hypno.shape[0] - gu//15)
            sleep_hypno = hypno[sl_index: gu_index]
            rem_hypno = np.where(sleep_hypno == 2)[0].shape[0] * 15
            n12_hypno = np.where(sleep_hypno == 1)[0].shape[0] * 15
            n3_hypno = np.where(sleep_hypno == 0)[0].shape[0] * 15
        else:
            rem_hypno = -1
            n12_hypno = -1
            n3_hypno = -1
        self.sleep_variables = {
            "TST": tst,
            "SOL": sl,
            "GU": gu,
            "WASO": waso,
            "SE": se,
            "AR": arousal_count,
            "ART": arousal_time,
            "N3": n3_hypno,
            "N12": n12_hypno,
            "REM": rem_hypno,
            "HYPNO": str(hypno.tolist())
        }
        print(
            "TST:\t{} s\nSOL:\t{} s\nSE:\t\t{}%\nWASO:\t{} s\nAR:\t\t{}".format(tst, sl, se * 100, waso, arousal_count))

        return self

    def get_sleep_variables(self):
        if self.sleep_variables is None:
            self.logger.error("Sleep variables are None, please run compute_sleep_variables first.")
        return self.sleep_variables

    def spindle_detect(self, hypno_mask=(0, 1), freq_sp=(12, 15), freq_broad=(1, 30), duration=(0.5, 2),
                       min_distance=100,
                       thresh_rel_pow=0.2, thresh_corr=0.65, thresh_rms=1.5):
        self.logger.info("Spindle detect start.")

        mask = None
        if hypno_mask is not None:
            if self.sleep_staging_result is None:
                self.logger.info(
                    "Sleep staging result is need for spindle detection, auto sleep staging will run first!")
                self.sleep_staging()
            mask = np.in1d(self.sleep_staging_result, hypno_mask)
            mask = np.repeat(mask, self.sf_eeg * self.epoch_len)

        self.sp_df = spindles_detect(self.eeg, mask=mask, freq_sp=freq_sp, freq_broad=freq_broad,
                                     duration=duration,
                                     min_distance=min_distance, thresh_rel_pow=thresh_rel_pow, thresh_rms=thresh_rms,
                                     thresh_corr=thresh_corr)
        logging.getLogger("").isEnabledFor(logging.WARNING)
        if self.biomarker is None:
            self.biomarker = np.zeros(self.eeg.shape[0])
        for row in np.arange(self.sp_df.shape[0]):
            self.biomarker[self.sp_df['Start_Index'][row]:self.sp_df['End_Index'][row]] = 1
        self.logger.info("Spindle detect finished.")
        # print(self.sp_df)
        return self

    def sw_detect(self, hypno_mask=(0, 1), freq_sw=(0.3, 1.5), dur_neg=(0.3, 1.5), dur_pos=(0.1, 1), amp_neg=(40, 200),
                  amp_pos=(10, 150), amp_ptp=(75, 350), coupling=False, coupling_params=None):
        self.logger.info("Slow-wave detect start.")
        mask = None
        if hypno_mask is not None:
            if self.sleep_staging_result is None:
                self.logger.info(
                    "Sleep staging result is need for slow-wave detection, auto sleep staging will run first!")
                self.sleep_staging()
            mask = np.in1d(self.sleep_staging_result, hypno_mask)
            mask = np.repeat(mask, self.sf_eeg * self.epoch_len)

        self.sw_df = sw_detect(self.eeg, sf=self.sf_eeg, mask=mask, freq_sw=freq_sw, dur_neg=dur_neg,
                               dur_pos=dur_pos,
                               amp_neg=amp_neg, amp_pos=amp_pos, amp_ptp=amp_ptp, coupling=coupling,
                               coupling_params=coupling_params)
        if self.biomarker is None:
            self.biomarker = np.zeros(self.eeg.shape[0])
        for row in np.arange(self.sw_df.shape[0]):
            self.biomarker[self.sw_df['Start_Index'][row]:self.sw_df['End_Index'][row]] = 2
        self.logger.info("Slow-wave detect finished.")
        # print(self.sw_df)
        return self

    def export_sp_results(self, save_file=None):
        if self.sp_df is None:
            self.logger.info("The spindle detection result is None, spindle detection will run first.")
            self.spindle_detect()
        if save_file is None:
            self.logger.info("File save path is not configured, default saved to ./saved_files/{}".format(
                "spindle_result_" + self.data_name + ".csv"))
            if not os.path.exists("../saved_file"):
                os.mkdir("../saved_file")
            self.sp_df.to_csv("./saved_file/" + "spindle_result_" + self.data_name + ".csv")
        else:
            self.sp_df.to_csv(save_file)
            self.logger.info("Save file to {}.".format(save_file))

        return self

    def export_sw_results(self, save_file=None):
        if self.sw_df is None:
            self.logger.info("The slow-wave detection result is None, slow-wave detection will run first.")
            self.sw_detect()
        if save_file is None:
            self.logger.info("File save path is not configured, default saved to ./saved_files/{}".format(
                "slow_wave_result_" + self.data_name + ".csv"))
            if not os.path.exists("../saved_file"):
                os.mkdir("../saved_file")
            self.sw_df.to_csv("./saved_file/" + "slow_wave_result_" + self.data_name + ".csv")
        else:
            self.sw_df.to_csv(save_file)
            self.logger.info("Save file to {}.".format(save_file))
        return self

    def plot_sp_results_by_id(self, sp_index, range=5000, savefig=None):
        if self.sp_df is None:
            self.logger.info("You have not run spindle detect, spindle detect will run first!")
            self.spindle_detect()
        if self.sp_df.size < sp_index or sp_index <= 0:
            self.logger.error("The input sp_index is invalid, please check!")
        sp = self.sp_df.iloc[sp_index]
        mid = (sp["Start_Index"] + sp["End_Index"]) // 2
        min_index = max(mid - range / 2, 0)
        max_index = min(mid + range / 2, self.eeg.shape[0])
        self.plot_sp_results_by_range(start_index=min_index, end_index=max_index,
                                      title="spindle detection result: No.{}".format(sp_index), savefig=savefig)
        if savefig is not None:
            self.logger.info("The spindle plot is saved to {}".format(savefig))
        return self

    def plot_sp_results_by_range(self, start_index, end_index, title=None, savefig=None):
        if end_index - start_index > 8000:
            self.logger.error("For best view, please make sure the sample size is around 5000, plot is skipped.")
            return
        if self.sp_df is None:
            self.logger.info("You have not run spindle detect, spindle detect will run first!")
            self.spindle_detect()
        start_index = int(start_index)
        end_index = int(end_index)
        mask = self.biomarker[start_index: end_index]
        data = self.eeg[start_index: end_index]
        mask[mask != 1] = np.nan
        times = np.arange(start_index, end_index) / self.sf_eeg
        plt.figure(figsize=(14, 4))
        plt.plot(times, data, 'k')
        plt.plot(times, mask * data, 'indianred')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude (uV)')
        plt.xlim([times[0], times[-1]])
        if title is None:
            plt.title(
                "spindle detect result between [{}s, {}s]".format(start_index / self.sf_eeg, end_index / self.sf_eeg))
        else:
            plt.title(title)
        sns.despine()
        if savefig is not None:
            plt.savefig(savefig, dpi=300, bbox_inches='tight')
        return self

    def plot_sw_results_by_id(self, sw_index, range=5000, savefig=None):
        if self.sw_df is None:
            self.logger.info("You have not run slow wave detect, slow wave detect will run first!")
            self.sw_detect()
        if self.sw_df.size < sw_index or sw_index <= 0:
            self.logger.error("The input sp_index is invalid, please check!")
        sw = self.sw_df.iloc[sw_index]
        mid = (sw["Start_Index"] + sw["End_Index"]) // 2
        min_index = max(mid - range / 2, 0)
        max_index = min(mid + range / 2, self.eeg.shape[0])
        self.plot_sw_results_by_range(start_index=min_index, end_index=max_index,
                                      title="slow wave result: No.{}".format(sw_index), savefig=savefig)
        if savefig is not None:
            self.logger.info("The slow-wave plot is saved as {}".format(savefig))
        return self

    def plot_sw_results_by_range(self, start_index, end_index, title=None, savefig=None):
        if self.sw_df is None:
            self.logger.info("You have not run slow wave detect, slow wave detect will run first!")
            self.sw_detect()

        if end_index - start_index > 8000:
            self.logger.error("For best view, please make sure the sample size is around 5000!")
            return
        start_index = int(start_index)
        end_index = int(end_index)
        mask = self.biomarker[start_index: end_index]
        data = self.eeg[start_index: end_index]
        mask[mask != 2] = np.nan
        mask[mask == 2] = 1
        times = np.arange(start_index, end_index) / self.sf_eeg
        plt.figure(figsize=(14, 4))
        plt.plot(times, data, 'k')
        plt.plot(times, mask * data, 'indianred')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude (uV)')
        plt.xlim([times[0], times[-1]])
        if title is None:
            plt.title("slow wave result between [{}s, {}s]".format(start_index / self.sf_eeg, end_index / self.sf_eeg))
        else:
            plt.title(title)
        sns.despine()
        if savefig is not None:
            plt.savefig(savefig, dpi=300, bbox_inches='tight')
        return self

    def plot_sw_stim_sham(self, savefig=None):
        if self.raw_sti is None:
            self.logger.error(
                "The sti indexs is None, please make sure the .sti file is loaded before plot sw stim vs sham.")
            return self
        if self.raw_sti.shape[0] < 10:
            self.logger.error(
                "The count of stim/sham points is less than expected, slow-wave stim sham plot will be skipped.")
            return self
        eeg_copy = np.copy(self.raw_eeg)
        plot_stim_sham_sw(eeg_copy, self.raw_sti, self.sf_eeg, savefig)

    def export_analysis_result_to_xlsx(self, save_path, sw_results=True, sp_results=True, sleep_variables=True):
        if save_path is None:
            self.logger.warning("Analysis results save path is None, xlsx file will not be saved, please check.")
            return self
        sheet_count = 0

        if sw_results:
            df_sw = self.sw_df
            sheet_count += 1

        if sp_results:
            df_sp = self.sp_df
            sheet_count += 1

        if sleep_variables:
            sleep_variables_df = {
                "data_name": [self.data_name],
                "TST(H)": [self.sleep_variables["TST"]/3600],
                "SOL(H)": [self.sleep_variables["SOL"]/3600],
                "GU(H)": [self.sleep_variables["GU"]/3600],
                "WASO(M)": [self.sleep_variables["WASO"]/60],
                "SE(%)": [self.sleep_variables["SE"] * 100],
                "AR": [self.sleep_variables["AR"]],
                "N3(H)": [self.sleep_variables["N3"]/3600],
                "N12(H)": [self.sleep_variables["N12"]/3600],
                "REM(H)": [self.sleep_variables["REM"]/3600],
                "Hypno": [self.sleep_variables["HYPNO"]]
            }

            df_sv = pd.DataFrame(sleep_variables_df)
            sheet_count += 1
        if sheet_count == 0:
            self.logger.info("At least one sheet is needed to export analysis result xlsx.")
            return self

        with pd.ExcelWriter(save_path) as writer:
            if df_sw is not None:
                df_sw.to_excel(writer, sheet_name='slow-wave results')
            else:
                self.logger.warning("Slow-wave detect result is None, please make sure slow-wave detection is done.")
            if df_sp is not None:
                df_sp.to_excel(writer, sheet_name='spindle results')
            else:
                self.logger.warning("Spindle detect result is None, please make sure spindle detection is done.")
            if df_sv is not None:
                df_sv.to_excel(writer, sheet_name='sleep variables')
            else:
                self.logger.warning("Sleep variables result is None, please make sure sleep variable is computed.")
        return self

    def show_plots(self):
        plt.show()


if __name__ == '__main__':
    data_handler = DataHandler()
    data_handler.load_data(data_name="20230620_15900563129", data_path=r"E:\dataset\dev_test_data\20230620_15900563129")

    data_handler.plot_sw_stim_sham()
    data_handler.preprocess().sleep_staging().compute_sleep_variables().plot_sleep_data()

    data_handler.show_plots()
