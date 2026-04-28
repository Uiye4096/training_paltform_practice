# config.py 学习笔记

## argparse 最小结构

```python
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=64)
    return parser.parse_args()
```

1. `ArgumentParser()` — 创建接收员
2. `add_argument(...)` — 声明期待的参数
3. `parse_args()` — 读取命令行，打包返回

调用：`args = get_args()`，访问：`args.batch_size`

---

## add_argument 常用参数

| 参数 | 作用 | 例子 |
|------|------|------|
| `type=` | 把字符串转成对应类型 | `int`, `float`, `str` |
| `default=` | 没传时的默认值 | `default=64` |
| `help=` | `--help` 时显示的说明 | `help='批次大小'` |
| `required=True` | 必须从命令行传入，不能只靠默认值 | - |

---

## 传列表参数：`nargs='+'`

argparse 默认每个参数只接收一个值。要接收列表，用 `nargs='+'`：

```python
parser.add_argument('--cnn_filters', type=int, nargs='+', default=[32, 64, 128])
```

命令行传入：
```bash
python train.py --cnn_filters 32 64 128
```

`args.cnn_filters` 结果直接是 `[32, 64, 128]`，无需手动解析。

> `nargs='+'` = 接收一个或多个值，自动组成列表。

---

## 命名规范

- argparse 参数名用 **小写 + 下划线**（snake_case），例如 `--checkpoint_dir`
- 不要混用驼峰，`--checkPoint_dir` 会变成 `args.checkPoint_dir`，不符合 Python 约定

---

## 路径默认值风格

三个路径要统一，要么全部绝对路径，要么全部相对路径：

```python
# 推荐：相对路径，跨机器可用
parser.add_argument('--data_root',      type=str, default='./data/XJTU-SY')
parser.add_argument('--checkpoint_dir', type=str, default='./checkpoints')
parser.add_argument('--log_dir',        type=str, default='./logs')
```

---

## config.py 设计选择

### 为什么用 config.py 而不是把 argparse 写在 train.py

项目是**多入口结构**（`train.py` + `evaluate.py`），参数定义必须在两者都能 import 的中立位置。  
把 argparse 放 `train.py` 会导致 `evaluate.py` 无法复用，只能重复定义。

### config.py 的职责

```
config.py  ←  定义所有参数 + 默认值（get_args 函数）
train.py   ←  from config import get_args; args = get_args()
evaluate.py←  from config import get_args; args = get_args()
```

---

## np.array() 接受的输入

| 输入类型 | 例子 |
|------|------|
| Python 列表 | `[1, 2, 3]` → 1D 数组 |
| 嵌套列表 | `[[1,2],[3,4]]` → 2D 数组 |
| 另一个 numpy 数组 | 复制一份 |
| list of numpy arrays | 自动堆叠成更高维数组 |

滑动窗口场景：`windows` 是嵌套列表，`np.array(windows)` 直接得到 shape `(num_windows, window_size)` 的二维数组。

---

## numpy mean/std 的 axis 参数

```python
data = np.array([[1, 2, 3],
                 [4, 5, 6]])  # shape (2, 3)

data.mean()        # 所有元素均值 → 标量 3.5
data.mean(axis=0)  # 每列的均值  → shape (3,)  [2.5, 3.5, 4.5]
data.mean(axis=1)  # 每行的均值  → shape (2,)  [2.0, 5.0]
```

**项目中的选择：** 振动信号两列（水平/垂直）量纲相同，用 `data.mean()`（全局标量）即可，实现简单。  
若两列量纲不同，改用 `data.mean(axis=0)` 按列分别归一化。

---

## set_seed：为什么要同时设置五个随机源

深度学习里有五个**互相独立**的随机数生成器，必须全部固定才能保证实验可复现：

```python
import random, numpy as np, torch

def set_seed(seed):
    random.seed(seed)                        # Python 内置 random
    np.random.seed(seed)                     # NumPy 随机数
    torch.manual_seed(seed)                  # PyTorch CPU
    torch.cuda.manual_seed(seed)             # 当前 GPU
    torch.cuda.manual_seed_all(seed)         # 所有 GPU（多卡）
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

| 随机源 | 管什么 |
|------|------|
| `random` | Python 内置随机操作 |
| `np.random` | numpy 的 shuffle、choice、randn 等 |
| `torch.manual_seed` | 权重初始化、dropout（CPU） |
| `torch.cuda.manual_seed` | 单卡 GPU 随机操作 |
| `torch.cuda.manual_seed_all` | 多卡 GPU 随机操作 |

---

## cudnn.deterministic 和 cudnn.benchmark

cuDNN 有自动寻优模式：第一次运行时测试多种卷积算法，找最快的那个。

```python
torch.backends.cudnn.benchmark = False      # 关闭自动寻优（否则结果不可复现）
torch.backends.cudnn.deterministic = True   # 强制用确定性算法
```

- `benchmark = True`：速度更快，但结果不可复现
- `benchmark = False` + `deterministic = True`：牺牲少量速度，换取完全可复现

**两行必须同时写**，否则 benchmark 的寻优会绕过 deterministic 的限制。

---

## 参考：iTSF 项目的做法

iTSF 是**单入口结构**，argparse 直接写在 `run.py`，通过 `--is_training 0/1` 控制训练/测试，  
Scripts 目录下的 `.sh` 文件充当实验配置快照。

```bash
python run.py \
    --is_training 1 \
    --model_id smoke_test \
    --batch_size 4 \
    ...
```
