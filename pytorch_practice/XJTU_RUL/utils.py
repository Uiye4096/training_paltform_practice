import pandas as pd
import numpy as np
import random
import torch

# =============================================================
# utils.py —— 工具函数
# =============================================================
# 这个文件的作用：
#   提供数据读取、特征提取、归一化等通用函数，
#   被 dataset.py / train.py / evaluate.py 调用。
#
# ──────────────────────────────────────────────────────────────
# 【1. 数据读取】
#
# def load_bearing_csv(csv_path):
#   """
#   读取单个轴承某一时刻的振动 CSV 文件。
#   XJTU-SY 格式：每个文件两列（水平加速度 / 垂直加速度），
#                 共 32768 行（约 1.28 s 的数据）。
#   参数：csv_path —— CSV 文件的完整路径（字符串）
#   返回：shape = (32768, 2) 的 numpy 数组
#   提示：用 pandas.read_csv() 或 numpy.loadtxt()
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【2. RUL 标签生成（线性退化假设）】
#
# def generate_rul_labels(total_files, rul_max=1.0):
#   """
#   为一条轴承寿命中的所有时刻生成 RUL 标签。
#   假设退化是线性的：第 0 个文件 RUL=1.0，最后一个文件 RUL=0.0。
#   参数：total_files —— 该轴承共有多少个 CSV 文件
#         rul_max     —— RUL 最大值（归一化时用 1.0）
#   返回：shape = (total_files,) 的 numpy 数组，值从 1.0 线性降至 0.0
#   提示：用 numpy.linspace()
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【3. 滑动窗口切片】
#
# def sliding_window(signal, window_size, stride):
#   """
#   对一段一维（或多维）信号做滑动窗口采样。
#   参数：signal      —— numpy 数组，shape = (N,) 或 (N, C)
#         window_size —— 窗口长度（采样点数）
#         stride      —— 步长
#   返回：shape = (num_windows, window_size) 或 (num_windows, window_size, C)
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【4. 归一化】
#
# def normalize(data, mean=None, std=None):
#   """
#   对数据做 Z-score 标准化。
#   如果传入 mean/std，则用给定值（测试集用训练集的统计量）；
#   否则在 data 自身上计算。
#   返回：(normalized_data, mean, std)
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【5. 设置随机种子（可复现）】
#
# def set_seed(seed):
#   """
#   同时设置 Python / NumPy / PyTorch 的随机种子。
#   提示：需要 import random, numpy, torch
#         torch.backends.cudnn.deterministic = True
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【可选：6. 时域 / 频域特征提取（如果不想用原始信号）】
#
# def extract_time_features(segment):
#   """
#   从一个窗口片段提取常用时域特征：
#   均值、标准差、峭度、峰峰值、有效值(RMS)、波形因子等。
#   返回：shape = (num_features,) 的 numpy 数组
#   """
#   pass
#
# def extract_freq_features(segment, sample_rate):
#   """
#   对片段做 FFT，提取频域特征（幅值谱、主频等）。
#   参数：sample_rate —— 采样率（Hz）
#   返回：shape = (num_freq_features,) 的 numpy 数组
#   """
#   pass
# =============================================================



def load_bearing_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df.values

def generate_rul_labels(total_files, rul_max=1.0):
    return np.linspace(rul_max, 0.0, total_files)

def generate_window(signal, window_size, stride):
    windows = []
    for i in range(0, len(signal) - window_size + 1, stride):
        windows.append(signal[i:i + window_size])
    return np.array(windows) #np array接受python列表，嵌套列表，另一个numpy数组，或者更高级别的numpy数组作为输入

def normalize(data, mean=None, std=None): #这里传入的data也是一个numpy数组
    if mean is None:
        mean = data.mean()
    if std is None:    
        std = data.std()
    return (data - mean) / std, mean, std

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
