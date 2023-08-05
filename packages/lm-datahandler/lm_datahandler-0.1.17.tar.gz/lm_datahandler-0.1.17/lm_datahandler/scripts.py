import os.path
from lm_datahandler.data_download.data_download import download_lm_data_from_server
from lm_datahandler.datahandler import DataHandler
import sys


def download_and_full_analyse(download_params):
    data_save_path = download_params["save_path"]
    data_list = download_lm_data_from_server(download_params, data_save_path)

    analysis_save_path = download_params["analysis_save_path"]

    show_plots = download_params["show_plots"]

    local_datas_full_analyse(data_save_path, data_list, analysis_save_path=analysis_save_path, show_plots=show_plots)


def local_datas_full_analyse(data_path, data_names, analysis_save_path=None, show_plots=False):
    assert os.path.exists(data_path), "The input dir path does not exist."

    if analysis_save_path is None:
        analysis_save_path = data_path
    else:
        if not os.path.exists(analysis_save_path):
            os.mkdir(analysis_save_path)
    for i, data_name in enumerate(data_names):
        if not os.path.exists(os.path.join(data_path, data_name)):
            print("data: \"{}\" not found, skipped.".format(data_name))
            continue
        try:

            data_handler = DataHandler()

            temp_data_path = os.path.join(data_path, data_name)

            data_analysis_save_path = os.path.join(analysis_save_path, data_name)

            if not os.path.exists(data_analysis_save_path):
                os.mkdir(data_analysis_save_path)
            sleep_fig_save_path = os.path.join(data_analysis_save_path, "sleep_fig.png")
            slow_wave_stim_sham_plot = os.path.join(data_analysis_save_path, "sw_stim_sham_fig.png")

            analysis_results_save_path = os.path.join(data_analysis_save_path, "analysis_results.xlsx")

            # 数据加载
            data_handler.load_data(data_name=data_name, data_path=temp_data_path)

            # 绘制慢波增强对比图，并保存
            data_handler.plot_sw_stim_sham(savefig=slow_wave_stim_sham_plot)

            # 进行睡眠分期，计算睡眠指标，绘制睡眠综合情况图，并保存
            data_handler.preprocess().sleep_staging().compute_sleep_variables().plot_sleep_data(
                savefig=sleep_fig_save_path)

            # spindle检测和慢波检测，并导出结果成excel
            data_handler.sw_detect().spindle_detect()
            data_handler.export_analysis_result_to_xlsx(analysis_results_save_path, sw_results=True, sp_results=True,
                                                        sleep_variables=True)

            if show_plots:
                data_handler.show_plots()

        except AssertionError as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("AssertionError: {}".format(e))
            print("File: {}".format(exc_traceback.tb_frame.f_code.co_filename))
            print("Line Number: {}".format(exc_traceback.tb_lineno))
            print("当前数据出错，将跳过当前数据.")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Unknown Error: {}".format(e))
            print("File: {}".format(exc_traceback.tb_frame.f_code.co_filename))
            print("Line Number: {}".format(exc_traceback.tb_lineno))
            print("当前数据出错，将跳过当前数据.")
        finally:

            continue



if __name__ == '__main__':
    # day = '20230621'
    # download_param = {
    #     # 刺激范式：1. 手动刺激，2. 音频刺激，3. N3闭环刺激，4. 纯记录模式，5. 记录模式， 6. 音频刺激
    #     'paradigms': None,
    #     # 用户手机号
    #     'phones': [18786181504],
    #     # 基座mac
    #     'macs': None,
    #     # 服务版本
    #     'serviceVersions': None,
    #     # 睡眠主观评分，1~5，-1表示未评分
    #     'sleepScores': None,
    #     # 停止类型， 0. 断连超时, 1. 用户手动, 2. 头贴放到基座上停止, 3. 关机指令触发, 4. 低电量, 5. 崩溃
    #     'stopTypes': None,
    #     # 时间范围，以停止记录的时间为准
    #     'dateRange': None,
    #     # 数据时长范围
    #     'dataLengthRange': [60 * 1, 60 * 12],
    #     # 翻身次数范围
    #     'turnoverCountRange': None,
    #     # 刺激次数范围
    #     'stimulationCountRange': None,
    #     # 下载保存路径
    #     'save_path': os.path.join('E:/dataset/x7_data_by_days/data', day),
    #     # 分析结果保存路径（为None表示保存在数据下载路径中）
    #     'analysis_save_path': os.path.join('E:/dataset/x7_data_by_days/analysis', day),
    #     'show_plots': True
    # }
    # download_and_full_analyse(download_param)
    data_path = r"E:\dataset\SHUPL_students\data\18_13688433900_LXY"
    data_names = []
    for i in os.listdir(data_path):
        if os.path.isdir(os.path.join(data_path, i)):
            data_names.append(i)

    # data_names = ['19914786512_0504-23_15_52_0505-06_12_47_4',
    #               '19914786512_0505-23_28_44_0506-07_03_13_4',
    #               '19914786512_0507-00_52_20_0507-07_43_33_4',
    #               '19914786512_0508-00_25_09_0508-07_45_17_4']
    local_datas_full_analyse(data_path, data_names, r"E:\dataset\SHUPL_students\analysis\18_13688433900_LXY")
