import os
import cv2
import numpy as np

if __name__ == '__main__':
    while True:
        imagesdir_address = input("请输入图片文件夹路径：")
        # 创建目录
        output_dir = os.path.join(imagesdir_address, 'temp')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filenames = os.listdir(imagesdir_address)
        row = 100000
        column = 1000000
        for image in filenames:
            image_address = os.path.join(imagesdir_address, image)
            if image != 'temp':
                try:
                    img = cv2.imdecode(np.fromfile((image_address), dtype=np.uint8), -1)
                    if img.shape[0] < row:
                        row = img.shape[0]
                    if img.shape[1] < column:
                        column = img.shape[1]
                except:
                    pass
        print("最小尺寸为：", [row, column])
        print("开始进行图片对齐...")
        for image in filenames:
            image_address = os.path.join(imagesdir_address, image)
            if image != 'temp':
                try:
                    img = cv2.imdecode(np.fromfile((image_address), dtype=np.uint8), -1)
                    new_img = img[:row, :column]
                    extension = image.split(".")[-1]
                    print("正在处理：", image_address)
                    cv2.imencode("." + extension, new_img)[1].tofile(output_dir + '/' + image)
                except:
                    pass
        print("处理完毕，图片生成路径为：", output_dir)
        next_act = input("回车继续，输入exit退出...\n")
        if next_act == "exit":
            break
