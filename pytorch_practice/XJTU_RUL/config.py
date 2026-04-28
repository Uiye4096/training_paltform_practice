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