# =============================================================
# config.py —— 全局超参数 & 路径配置
# =============================================================
# 这个文件的作用：
#   把所有"可调节的数字/路径"集中在一处，
#   其他文件只需 import config，不需要到处硬编码数字。
#
# 你需要在这里定义：
#
# 【路径配置】
#   DATA_ROOT     : XJTU-SY 数据集的根目录路径（字符串）
#   CHECKPOINT_DIR: 保存模型权重文件的目录
#   LOG_DIR       : TensorBoard 日志目录
#
# 【数据预处理参数】
#   SAMPLE_RATE   : 采样频率（XJTU-SY 固定为 25.6 kHz）
#   WINDOW_SIZE   : 每个样本截取的采样点数（滑动窗口长度），例如 2048
#   STRIDE        : 滑动窗口步长（控制样本重叠程度）
#   CHANNELS      : 使用几个通道（水平/垂直振动，即 1 或 2）
#
# 【RUL 标签参数】
#   RUL_MAX       : 最大 RUL（线性退化假设下等于总寿命采样次数）
#                   也可以设为 1，表示把 RUL 归一化到 [0, 1]
#
# 【模型超参数】
#   CNN_FILTERS   : 各 Conv1d 层的输出通道数，例如 [32, 64, 128]
#   CNN_KERNEL    : 卷积核大小
#   LSTM_HIDDEN   : LSTM 隐藏层维度
#   LSTM_LAYERS   : LSTM 堆叠层数
#   DROPOUT       : Dropout 概率（防止过拟合）
#
# 【训练超参数】
#   EPOCHS        : 训练轮数
#   BATCH_SIZE    : 每批样本数
#   LR            : 初始学习率
#   WEIGHT_DECAY  : 优化器 L2 正则化系数
#   LR_STEP       : 学习率衰减的 epoch 间隔（StepLR）
#   LR_GAMMA      : 学习率衰减因子
#
# 【数据划分】
#   TRAIN_BEARINGS: 用于训练的轴承编号列表，例如 ['Bearing1_1', 'Bearing1_2']
#   TEST_BEARINGS : 用于测试的轴承编号列表
#
# 【其他】
#   SEED          : 随机种子，保证实验可复现
#   DEVICE        : 'cuda' 或 'cpu'（可用 torch.cuda.is_available() 自动判断）
# =============================================================


import argparse

def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--data_root', type=str, default='XJTU-SY', help='XJTU-SY 数据集的根目录路径')
    parser.add_argument('--check_point_dir', type=str, default='checkpoints', help='保存模型权重文件的目录')
    parser.add_argument('--log_dir', type=str, default='logs', help='TensorBoard 日志目录')

    parser.add_argument('--sample_rate', type=int, default=25600, help='采样频率')
    parser.add_argument('--window_size', type=int, default=2048, help='窗口大小')
    parser.add_argument('--stride', type=int, default=1024, help='滑动窗口步长')
    parser.add_argument('--channels', type=int, default=1, help='使用几个通道')

    parser.add_argument('--rul_max', type=int, default=100, help='最大 RUL')

    parser.add_argument('--cnn_filters', type=int, default=[32, 64, 128], nargs='+', help='CNN 过滤器数量')
    parser.add_argument('--cnn_kernel', type=int, default=3, help='CNN 卷积核大小')
    parser.add_argument('--cnn_padding', type=int, default=1, help='CNN 卷积核 padding')
    parser.add_argument('--lstm_hidden', type=int, default=64, help='LSTM 隐藏层大小')
    parser.add_argument('--lstm_layers', type=int, default=2, help='LSTM 层数')
    parser.add_argument('--dropout', type=float, default=0.5, help='Dropout 概率')

    parser.add_argument('--epochs', type=int, default=100, help='训练轮数')
    parser.add_argument('--batch_size', type=int, default=32, help='批次大小')
    parser.add_argument('--lr', type=float, default=1e-3, help='学习率')
    parser.add_argument('--weight_decay', type=float, default=1e-4, help='权重衰减')
    parser.add_argument('--lr_step', type=int, default=10, help='学习率衰减的 epoch 间隔')
    parser.add_argument('--lr_gamma', type=float, default=0.5, help='学习率衰减因子')

    parser.add_argument('--train_bearings', type=str, nargs='+', default=['Bearing1_1', 'Bearing1_2'], help='训练轴承')
    parser.add_argument('--test_bearings', type=str, nargs='+', default=['Bearing1_3'], help='测试轴承')

    parser.add_argument('--seed', type=int, default=42, help='随机种子')
    parser.add_argument('--device', type=str, default='mps', help='设备')

    return parser.parse_args()