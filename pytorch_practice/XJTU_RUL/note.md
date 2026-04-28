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
