

import cv2
import numpy as np

img_path = "anqi.jpg"   # 换成你图片路径
img = cv2.imread(img_path)
if img is None:
    print("读取失败")
    exit()

# ---------- 1. 计算“与纯白的距离”，做软alpha ----------
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 越接近白色，距离越小 → alpha越小（越透明）
diff = 255 - gray
# 把距离映射到 0~255，20 是灵敏度：越大越不容易透明
alpha = np.clip(diff / 20 * 255, 0, 255).astype(np.uint8)

# ---------- 2. 形态学：把衣服上小白洞补掉，背景保持干净 ----------
# 先二值化：白背景=0，衣服=255
_, mask = cv2.threshold(alpha, 240, 255, cv2.THRESH_BINARY)
# 闭运算：填小洞；开运算：去背景噪点
kernel = np.ones((3, 3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)  # 补洞
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)   # 去噪

# ---------- 3. 边缘羽化，避免锯齿硬边 ----------
alpha = cv2.GaussianBlur(mask, (3, 3), 0)

# ---------- 4. 合成 BGRA 并保存 ----------
b, g, r = cv2.split(img)
rgba = cv2.merge((b, g, r, alpha))
cv2.imwrite(r"D:\opencv\pythonProject\qita\anqi.png", rgba)

print("完成：fixed_transparent.png")