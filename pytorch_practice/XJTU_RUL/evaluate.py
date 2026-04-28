# =============================================================
# evaluate.py —— 模型评估 & 结果可视化
# =============================================================
# 这个文件的作用：
#   加载训练好的模型权重，在测试集上做推理，
#   计算评估指标，并画出预测 RUL vs 真实 RUL 曲线。
#
# ──────────────────────────────────────────────────────────────
# 【步骤 1：import】
#   import torch
#   import numpy as np
#   import matplotlib.pyplot as plt
#   from sklearn.metrics import mean_absolute_error, mean_squared_error
#   import config
#   from dataset import get_dataloaders
#   from model import CNNLSTM
#
# ──────────────────────────────────────────────────────────────
# 【步骤 2：收集预测值与真实值】
#
# def get_predictions(model, loader, device):
#   """
#   在整个测试 loader 上做推理，收集所有预测值和真实标签。
#   提示：
#     model.eval() + torch.no_grad()
#     把每个 batch 的 pred / label .cpu().numpy() 存进列表
#     最后 np.concatenate 拼成一维数组
#   返回：(preds, labels)，均为 shape=(N,) 的 numpy 数组
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【步骤 3：计算评估指标】
#
# def compute_metrics(preds, labels):
#   """
#   计算并打印：
#     MAE  (Mean Absolute Error)       ← sklearn.metrics.mean_absolute_error
#     RMSE (Root Mean Squared Error)   ← np.sqrt(mean_squared_error(...))
#     MAPE (Mean Absolute Percentage Error, %)
#          ← np.mean(np.abs((preds - labels) / (labels + 1e-8))) * 100
#          （分母加 1e-8 防止除以零）
#   返回：字典 {'MAE': ..., 'RMSE': ..., 'MAPE': ...}
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【步骤 4：可视化】
#
# def plot_rul_curve(preds, labels, save_path=None):
#   """
#   绘制预测 RUL 与真实 RUL 随时间变化的对比曲线。
#   图例：一条蓝色实线（真实值），一条橙色虚线（预测值）。
#   x 轴：样本序号（时间索引）
#   y 轴：RUL 值
#
#   提示：
#     plt.figure(figsize=(12, 5))
#     plt.plot(labels, label='True RUL')
#     plt.plot(preds,  label='Pred RUL', linestyle='--')
#     plt.xlabel / ylabel / title / legend
#     if save_path: plt.savefig(save_path, dpi=150)
#     plt.show()
#   """
#   pass
#
# ──────────────────────────────────────────────────────────────
# 【步骤 5：主评估流程】
#
# def main():
#   # 1. 确定 device
#   # 2. 加载模型结构，并用 model.load_state_dict(torch.load(...)) 加载权重
#   # 3. 调用 get_dataloaders() 只取 test_loader
#   # 4. 调用 get_predictions() 得到 preds, labels
#   # 5. 调用 compute_metrics() 打印指标
#   # 6. 调用 plot_rul_curve() 可视化
#   pass
#
# if __name__ == '__main__':
#   main()
#
# ──────────────────────────────────────────────────────────────
# 【知识点提示】
#
# Q: 为什么要用 RMSE 而不只是 MSE？
#   A: RMSE 与原始 RUL 的量纲相同，更直观；MSE 是其平方，数值偏大。
#
# Q: MAPE 的局限性？
#   A: 当真实值接近 0（寿命末期），MAPE 会非常大甚至无穷，
#      所以要在分母加一个小量，或改用 sMAPE。
# =============================================================
