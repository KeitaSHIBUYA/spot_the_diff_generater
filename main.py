import glob
import os

import change_color as col
import cv2
import easy
import hard
import normal
import processing

# for debug
mode_easy = "easy"
mode_normal = "normal"
mode_hard = "hard"

# 難易度入力
# print("難易度: [easy, normal, hard]")
# mode_input = input("難易度を入力してください:")

path_str = os.path.dirname(os.path.abspath(__file__))


def main(difficulty):
    if difficulty == "easy":
        easy.main()                # easy.pyの呼び出し
        
    elif difficulty == "normal":
        normal.main()              # normal.pyの呼び出し
        
    elif difficulty == "hard":
        hard.main()                # hard.pyの呼び出し
    
if __name__ == "__main__":
    # main(mode_easy)
    # main(mode_normal)
    main(mode_hard)
    # main(mode_input)