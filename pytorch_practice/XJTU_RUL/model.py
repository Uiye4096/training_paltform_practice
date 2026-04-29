# =============================================================
# model.py —— CNN-LSTM RUL 预测网络
# =============================================================
# 这个文件的作用：
#   定义网络结构。整体思路：
#     原始振动信号 (batch, C, L)
#       → [CNN 特征提取器]  逐步提取局部模式，输出特征序列
#       → [LSTM 时序建模]   捕捉退化趋势在时间轴上的演变
#       → [全连接回归头]    输出一个标量：预测的 RUL 值
#
# ──────────────────────────────────────────────────────────────
# 【步骤 1：import】
#   import torch
#   import torch.nn as nn
#   import config
#
# ──────────────────────────────────────────────────────────────
# 【步骤 2：定义 CNN 特征提取器（子模块）】
#
# class CNNExtractor(nn.Module):
#   """
#   由若干个 Conv1d Block 叠加而成，每个 Block 包含：
#     Conv1d → BatchNorm1d → ReLU → MaxPool1d
#
#   输入：(batch, in_channels, signal_length)
#   输出：(batch, last_filter_size, reduced_length)
#         其中 reduced_length 因为 MaxPool 会比 signal_length 小很多
#
#   提示：
#     - nn.Conv1d(in_channels, out_channels, kernel_size, padding=kernel_size//2)
#       padding=kernel_size//2 可以让长度不因卷积缩小（same padding）
#     - nn.BatchNorm1d 让训练更稳定
#     - nn.MaxPool1d(2) 每次把长度减半
#     - 过滤器数量参考 config.CNN_FILTERS
#   """
#   def __init__(self, in_channels):
#     super().__init__()
#     # 在这里用 nn.Sequential 或手动定义各层
#     pass
#
#   def forward(self, x):
#     # x: (batch, in_channels, L)
#     # 返回: (batch, last_filter_size, L')
#     pass
#
# ──────────────────────────────────────────────────────────────
# 【步骤 3：定义完整的 CNN-LSTM 网络】
#
# class CNNLSTM(nn.Module):
#   """
#   完整的 RUL 预测网络。
#
#   forward 数据流：
#     x: (batch, C, L)               ← 输入
#       → CNNExtractor                → (batch, F, L')
#       → permute(0, 2, 1)           → (batch, L', F)  ← LSTM 期望 (batch, seq, feature)
#       → nn.LSTM(F, hidden, layers) → output: (batch, L', hidden)
#       → 取最后一个时间步 output[:, -1, :]  → (batch, hidden)
#       → nn.Dropout
#       → nn.Linear(hidden, 1)       → (batch, 1)
#       → squeeze(-1)                → (batch,)        ← 最终预测的 RUL
#
#   参数全从 config 读取：
#     CHANNELS, CNN_FILTERS, CNN_KERNEL, LSTM_HIDDEN, LSTM_LAYERS, DROPOUT
#   """
#   def __init__(self):
#     super().__init__()
#     # 1. 实例化 CNNExtractor
#     # 2. 实例化 nn.LSTM
#     #    注意：batch_first=True（让第一维是 batch）
#     # 3. 实例化 nn.Dropout
#     # 4. 实例化 nn.Linear 输出 1 个值
#     pass
#
#   def forward(self, x):
#     pass
#
# ──────────────────────────────────────────────────────────────
# 【调试入口（可选）】
# if __name__ == '__main__':
#   # 构造一个假输入，验证网络能跑通且输出 shape 正确
#   # model = CNNLSTM()
#   # dummy = torch.randn(8, config.CHANNELS, config.WINDOW_SIZE)
#   # out = model(dummy)
#   # print(out.shape)  # 应该是 torch.Size([8])
#   pass
# =============================================================

import torch
import torch.nn as nn
import config

args = config.get_args()

class CNNExtractor(nn.Module):
    def __init__(self, in_channels):
        super().__init__()
        # TODO: 实现CNN提取器
        args = config.get_args()
        filters = args.cnn_filters
        kernel_size = args.cnn_kernel
        
        layers = []
        for out_channels in filters:
            layers.append(nn.Conv1d(in_channels, out_channels, kernel_size, padding=kernel_size//2))
            layers.append(nn.BatchNorm1d(out_channels))
            layers.append(nn.ReLU())
            layers.append(nn.MaxPool1d(2))
            in_channels = out_channels

        self.net = nn.Sequential(*layers) #需要解包，把layers当中的内容拆开变成独立的元素传入sequential

    def forward(self, x):
        return self.net(x)

class CNNLSTM(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.input_size = input_size
        self.cnn = CNNExtractor(input_size)
        self.lstm = nn.LSTM(args.cnn_filters[-1], args.lstm_hidden, args.lstm_layers, batch_first=True)
        self.dropout = nn.Dropout(args.dropout)
        self.fc = nn.Linear(args.lstm_hidden, 1)
        
    def forward(self, x):
        x = self.cnn(x) # (batch, channels, seq_len)
        x = x.permute(0, 2, 1) # (batch, seq_len, channels)
        x, _ = self.lstm(x) # 丢弃隐藏状态
        x = self.dropout(x)
        x = x[:, -1, :] # 取最后一个时间步
        x = self.fc(x)
        return x










