# CNNLSTM 模型设计笔记

## 完整信息流

```
原始信号 (batch, 1, window_size)
    ↓ CNN 特征提取
(batch, 128, seq_len/8)   ← 128个特征，序列长度缩短8倍（3次MaxPool1d(2)）
    ↓ permute(0, 2, 1)
(batch, seq_len/8, 128)   ← 转换为LSTM期望的格式
    ↓ LSTM
(batch, seq_len/8, lstm_hidden)
    ↓ dropout + [:, -1, :]
(batch, lstm_hidden)       ← 只取最后一个时间步
    ↓ fc
(batch, 1) → squeeze → (batch,)
```

---

## 设计决策

### 1. 为什么要 `permute(0, 2, 1)`？

CNN 和 LSTM 对数据维度的约定不同：

- **CNN** 的格式：`(batch, channels, length)` — 把数据看成"多通道信号"
- **LSTM**（batch_first=True）的格式：`(batch, seq_len, features)` — 把数据看成"时间序列，每个时刻一个特征向量"

CNN输出 `(batch, 128, 12)` 直接传给LSTM，LSTM会误认为序列长度=128，特征数=12，与实际语义相反，必须转置。

### 2. 为什么 LSTM 返回元组，要用 `x, _ = self.lstm(x)`？

`nn.LSTM` 返回 `(output, (h_n, c_n))`：
- `output`：所有时刻的输出，形状 `(batch, seq_len, hidden)`
- `h_n, c_n`：最后时刻的隐藏状态和细胞状态

隐状态在 Seq2Seq 等任务中需要传递给 decoder，但 RUL 预测不需要，用 `_` 丢弃即可。

### 3. 为什么只取最后一个时间步 `x[:, -1, :]`？

取决于任务类型：

| 任务 | 需要什么 |
|------|---------|
| 序列标注（NER）| 所有时刻的输出 `(batch, seq_len, hidden)` |
| 分类 / RUL 预测 | 最后一个时刻的输出 `(batch, hidden)` |

RUL 预测只需要输出一个标量，LSTM 逐时刻处理后，最后一步的隐状态已经综合了所有历史信息，代表当前最新的机器状态，用它来预测剩余寿命。

---

## 总结

| 步骤 | 原因 |
|------|------|
| `permute(0, 2, 1)` | CNN 和 LSTM 的维度约定不同 |
| `x, _ = lstm(x)` | LSTM 返回了不需要的隐状态 |
| `x[:, -1, :]` | RUL 只关心最新时刻的机器状态 |

**核心思想**：CNN 把原始信号转化为特征 → LSTM 追踪这些特征的时间演变 → 取最新时刻的状态预测寿命。
