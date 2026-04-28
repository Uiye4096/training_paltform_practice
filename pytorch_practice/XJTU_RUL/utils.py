import pandas as pd
import numpy as np
import random
import torch

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
