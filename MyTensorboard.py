from torch.utils.tensorboard import SummaryWriter
import numpy as np
from PIL import Image

writer = SummaryWriter("pytorch_practice/data/dataset/logs")
image_path = "pytorch_practice/data/dataset/train/ants_image/0013035.jpg"
img_PIL = Image.open(image_path)
img_array = np.array(img_PIL)
print(img_array.shape)

writer.add_image("test", img_array, 1, dataformats="HWC")

#numpy型读取图片-opencv

# for i in range(100):
#     writer.add_scalar("y=2x", 2 * i, i) #一定要记得改tag，不然会写到同一个事件里面，如果发生了就删掉logs中的文件并重新开始进程。

writer.close()
