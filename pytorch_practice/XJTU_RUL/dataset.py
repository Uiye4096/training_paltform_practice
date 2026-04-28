from torch.utils.data import Dataset, DataLoader
import os, torch
import numpy as np
from utils import load_bearing_csv, generate_rul_labels, generate_window, normalize
import config

class BearingDataset(Dataset):
    def __init__(self, bearing_dirs, window_size, stride, mean=None, std=None):
        all_samples = []
        all_labels = []
        
        for bearing_dir in bearing_dirs:
            csv_files = sorted(os.listdir(bearing_dir)) #os来对它进行排序，listdir返回的是文件名列表
            rul_labels = generate_rul_labels(len(csv_files))

            for i, csv_file in enumerate(csv_files): #enumerate返回索引和文件名
                signal = load_bearing_csv(os.path.join(bearing_dir, csv_file)) #os.path查询了路径
                windows = generate_window(signal, window_size, stride)

                labels = np.full(len(windows), rul_labels[i]) #生成与窗口数量相同的标签

                all_samples.append(windows)
                all_labels.append(labels)

        self.samples = np.concatenate(all_samples)
        self.labels = np.concatenate(all_labels)

        self.samples, self.mean, self.std = normalize(self.samples, mean, std)

        self.samples = self.samples[:, np.newaxis, :]
        # 时序预测当中，对于每个shape，固定一般第一个数写样本数，
        # 第二个地方写样本每个店对应的通道数或者维度数，
        # 第三个地方写样本长度。所以为了符合这个张量形式，
        # 我们把原来的(N, L)变成 (N, 1, L)的数组形式

        self.samples = torch.FloatTensor(self.samples)
        self.labels = torch.FloatTensor(self.labels)

    # len 和 getitem 是 PyTorch Dataset 类的两个必要方法
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx], self.labels[idx]


def get_dataloaders(train_dirs, test_dirs):
    args = config.get_args()

    train_dataset = BearingDataset(train_dirs, args.window_size, args.stride)

    mean, std = train_dataset.mean, train_dataset.std

    test_dataset = BearingDataset(test_dirs, args.window_size, args.stride, mean, std)

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)

    return train_loader, test_loader

