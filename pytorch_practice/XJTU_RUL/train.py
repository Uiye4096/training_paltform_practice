# =============================================================
# train.py —— 训练循环
# =============================================================
# 这个文件的作用：
#   把 dataset / model / optimizer / loss 组装起来，
#   循环执行"前向传播 → 计算损失 → 反向传播 → 更新权重"，
#   并记录每个 epoch 的训练/验证损失，保存最优模型。
#
# ──────────────────────────────────────────────────────────────
# 【步骤 1：import】
#   import torch
#   import torch.nn as nn
#   from torch.optim import Adam（或 SGD）
#   from torch.optim.lr_scheduler import StepLR（可选）
#   from torch.utils.tensorboard import SummaryWriter（可选，用于可视化）
#   import os
#   import config
#   from dataset import get_dataloaders
#   from model import CNNLSTM
#   from utils import set_seed
#
# ──────────────────────────────────────────────────────────────
# 【步骤 2：train_one_epoch 函数】
#
# def train_one_epoch(model, loader, optimizer, criterion, device):
#   """
#   跑完训练集一遍，返回平均损失。
#
#   伪代码：
#     model.train()                          ← 开启 Dropout / BN 训练模式
#     total_loss = 0
#     for x, y in loader:
#       x, y = x.to(device), y.to(device)
#       optimizer.zero_grad()                ← 清空上一步的梯度
#       pred = model(x)                      ← 前向传播
#       loss = criterion(pred, y)            ← 计算损失（MSELoss）
#       loss.backward()                      ← 反向传播，计算梯度
#       optimizer.step()                     ← 用梯度更新权重
#       total_loss += loss.item()
#     return total_loss / len(loader)
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【步骤 3：evaluate 函数（在验证/测试集上跑一遍）】
#
# def evaluate(model, loader, criterion, device):
#   """
#   model.eval() + torch.no_grad()，返回平均损失。
#   提示：torch.no_grad() 关闭梯度计算，节省内存，加快速度。
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【步骤 4：主训练流程】
#
# def main():
#   # 1. 设置随机种子
#   # 2. 确定 device（cuda / cpu）
#   # 3. 调用 get_dataloaders() 得到 train_loader, test_loader
#   # 4. 实例化 model，并 .to(device)
#   # 5. 定义损失函数：nn.MSELoss()
#   #    （可选：nn.HuberLoss() 对异常值更鲁棒）
#   # 6. 定义优化器：Adam(model.parameters(), lr=config.LR, weight_decay=...)
#   # 7. 定义学习率调度器（可选）：StepLR
#   # 8. 创建保存目录：os.makedirs(config.CHECKPOINT_DIR, exist_ok=True)
#   # 9. （可选）创建 TensorBoard SummaryWriter
#
#   # 10. 训练循环：
#   #   best_val_loss = float('inf')
#   #   for epoch in range(config.EPOCHS):
#   #     train_loss = train_one_epoch(...)
#   #     val_loss   = evaluate(...)
#   #     scheduler.step()（如果用了调度器）
#   #
#   #     打印：f"Epoch {epoch+1}/{EPOCHS} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}"
#   #
#   #     如果 val_loss < best_val_loss：
#   #       保存模型权重：torch.save(model.state_dict(), path)
#   #       更新 best_val_loss
#   #
#   #     （可选）SummaryWriter 记录损失曲线
#   pass
#
# if __name__ == '__main__':
#   main()
#
# ──────────────────────────────────────────────────────────────
# 【知识点提示】
#
# Q: optimizer.zero_grad() 为什么要放在最前面？
#   A: PyTorch 的梯度是累加的，每次更新前必须手动清零，否则梯度会叠加。
#
# Q: model.train() 和 model.eval() 有什么区别？
#   A: train() 开启 Dropout 随机失活和 BatchNorm 用 batch 统计量；
#      eval()  关闭 Dropout，BatchNorm 用运行均值/方差。
#
# Q: torch.no_grad() 的作用？
#   A: 关闭自动微分图的构建，推理时节省约 50% 显存，速度更快。
# =============================================================
