# =============================================================
# dataset.py —— Dataset 定义 & DataLoader 构建
# =============================================================
# 这个文件的作用：
#   定义 PyTorch Dataset，把原始轴承数据变成 (sample, label) 对，
#   再包成 DataLoader 提供给训练循环使用。
#
# ──────────────────────────────────────────────────────────────
# 【步骤 1：import 必要库】
#   from torch.utils.data import Dataset, DataLoader
#   import os, numpy, torch
#   from utils import load_bearing_csv, generate_rul_labels, sliding_window, normalize
#   import config
#
# ──────────────────────────────────────────────────────────────
# 【步骤 2：定义 BearingDataset 类，继承 torch.utils.data.Dataset】
#
# class BearingDataset(Dataset):
#
#   def __init__(self, bearing_dirs, window_size, stride, mean=None, std=None):
#     """
#     参数：
#       bearing_dirs —— 轴承文件夹路径列表，每个文件夹内含若干 CSV 文件
#                       例如 ['data/XJTU-SY/Bearing1_1', 'data/XJTU-SY/Bearing1_2']
#       window_size  —— 滑动窗口长度
#       stride       —— 滑动窗口步长
#       mean / std   —— 若不为 None，用这组统计量归一化（测试集场景）
#
#     你需要做的事情（按顺序）：
#       1. 遍历每个 bearing_dir
#          a. 用 sorted(os.listdir()) 拿到该文件夹下所有 CSV 文件（注意按时间顺序排序！）
#          b. 调用 generate_rul_labels() 生成该轴承所有时刻的 RUL 标签
#          c. 对每个 CSV 文件：
#             - 调用 load_bearing_csv() 读取振动信号
#             - 调用 sliding_window() 切成若干片段
#             - 每个片段对应的 RUL 就是该 CSV 文件的标签（保持对应关系！）
#       2. 把所有片段 concat 成一个大的 numpy 数组 self.samples
#          把所有标签 concat 成 self.labels
#       3. 归一化 self.samples：
#          - 若 mean/std 为 None，在 self.samples 上计算并保存
#          - 否则直接用传入的 mean/std
#       4. 转成 torch.FloatTensor
#
#     提示：self.samples 的最终 shape 应为 (N, C, window_size)
#           其中 N=总片段数，C=通道数（1 或 2），window_size=窗口长度
#           CNN 期望输入格式就是 (batch, channels, length)
#     """
#     pass
#
#   def __len__(self):
#     # 返回样本总数
#     pass
#
#   def __getitem__(self, idx):
#     # 返回第 idx 个样本和对应的 RUL 标签
#     # 返回类型应为 (torch.FloatTensor, torch.FloatTensor)
#     pass
#
# ──────────────────────────────────────────────────────────────
# 【步骤 3：构建 DataLoader 的工厂函数】
#
# def get_dataloaders(train_dirs, test_dirs):
#   """
#   利用上面的 BearingDataset 构建训练集和测试集的 DataLoader。
#   注意：
#     - 用训练集的 mean/std 来归一化测试集（避免数据泄露）
#     - 训练集 DataLoader shuffle=True；测试集 shuffle=False
#     - batch_size / window_size / stride 从 config 读取
#   返回：(train_loader, test_loader)
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【调试入口（可选）】
# if __name__ == '__main__':
#   # 在这里临时测试：打印 dataset 长度、第一个样本的 shape 和 label 值
#   pass
# =============================================================
