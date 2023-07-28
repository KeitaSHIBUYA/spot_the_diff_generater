import cv2
import os
import numpy as np

bg_path = "/Users/keita/Documents/1F10180284_thesis/images/easy/01.png"
mask_path = "/Users/keita/Documents/1F10180284_thesis/images/easy/size/menu.png"
mask_path_2 = "/Users/keita/Documents/1F10180284_thesis/images/easy/size/sarad.png"
sheep = "/Users/keita/Documents/1F10180284_thesis/images/easy/add/sheep.png"

# print(isinstance(sheep, str))

img = cv2.imread(bg_path)
print(isinstance(img, np.ndarray))

range_dict = {
    "sheep.png":[[280, 0],
             [280, 50]],
    "circle.png":[[0, 0],
              [0, 0]],
    "menu.png":[[0, 0],
            [0, 0]],
    "sarad.png":[[0, 0],
             [0, 0]]
}

dict_key = os.path.basename(sheep)
# 拡張子なしの場合
# dict_key = os.path.splitext(os.path.basename(sheep))[0]

print(range_dict[dict_key][0][0], range_dict[dict_key][0][1])
print(range_dict[dict_key][1][0], range_dict[dict_key][1][1])


def fill(base_path, target_path):
    bg_img = cv2.imread(base_path)
    mask = cv2.imread(target_path, cv2.IMREAD_GRAYSCALE)
    h, w = bg_img.shape[:2]
    
    for i in range(h):
        for j in range(w):
            if mask[i, j] != 0:
                bg_img[i, j] = 255
                
    
    return bg_img
    
# image = fill(bg_path, mask_path_2)
# cv2.imshow('result', image)
# cv2.moveWindow("result", 2300, 000)
# cv2.waitKey(0)


'''
def click_pos(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        img2 = np.copy(img)
        cv2.circle(img2, center = (x, y), radius = 5, color = 255, thickness = -1)
        pos_str = '(x, y)=(' + str( x ) + ',' + str( y )+ ')'
        cv2.putText(img2, pos_str, (x + 10, y + 10),
                    cv2.FONT_HERSHEY_PLAIN, 2, 255, 2, cv2.LINE_AA)
        cv2.imshow('pos', img2)
        cv2.moveWindow('pos', 2300, 600)


# 表示
cv2.imshow('result', img)
cv2.setMouseCallback('result', click_pos)
cv2.moveWindow("result", 2300, 000)
cv2.waitKey(0)
'''

'''
### 中心座標から左上の座標を求める
def calc_UpperLeft_pos(fore_size, pos, scale):
    fore_w, fore_h = fore_size                              # 元画像の大きさ
    
    center = [(fore_w/2 + pos[0]), (fore_h/2 + pos[1])]
    print("center:", center)                                # for debug
    
    aw, ah = [fore_w*scale, fore_h*scale]                   # 拡大・縮小後の画像の大きさ
    
    pos_w_h = [center[0] - fore_w/2, center[1]-fore_h/2]    # 元の画像の左上の座標
    print("before:", pos_w_h)                               # for debug
    
    pos_aw_ah = [center[0]- aw/2, center[1]-ah/2]           # 拡大・縮小後の左上の座標
    print("new:", pos_aw_ah)                                # for debug
    
    return pos_aw_ah

# sample_back = np.array([564, 578])
sample_back = np.array([500, 500])
# sample_fore = np.array([90, 90])
sample_fore = np.array([100, 100])
# sample_pos = np.array([280, 20])
sample_pos = np.array([300, 50])

print(calc_UpperLeft_pos(sample_fore, sample_pos, 0.5))
'''