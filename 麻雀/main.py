import cv2
import numpy as np

img = cv2.imread("humen.png")
temp = cv2.imread("2p.png")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)

# テンプレート画像の高さ・幅
h, w = temp.shape

# テンプレートマッチング（OpenCVで実装）
match = cv2.matchTemplate(gray, temp, cv2.TM_SQDIFF)
min_value, max_value, min_pt, max_pt = cv2.minMaxLoc(match)
pt = min_pt

# テンプレートマッチングの結果を出力
cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 0, 200), 3)
cv2.imwrite("ssd1.png", img)

print("最後まで動いてる")