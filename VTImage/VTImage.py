import cv2
from PIL import Image
import numpy as np
import os

while True:
    path = input("请输入视频文件夹路径（程序会自动分析文件夹下所有的视频）：")
    while not os.path.exists(path):
        path = input("输入路径错误，请重新输入：")
    files = os.listdir(path)
    flag = 0
    for file in files:
        # 确保有mpg格式的视频
        if file.split(".")[-1] == "mpg":
            flag = 1
            break
    if flag:
        for file in files:
            if file.split(".")[-1] == "mpg":
                print("正在处理：", os.path.join(path, file))
                # 视频名称
                videoName = file.split(".")[0]
                # 帧保存的文件夹名
                videoframepath = os.path.join(path, videoName)
                if not os.path.exists(videoframepath):  # 判断是否存在文件夹如果不存在则创建为文件夹
                    os.makedirs(videoframepath)  # makedirs 创建文件时如果路径不存在会创建这个路径
                # 获取视频对象
                cap = cv2.VideoCapture(os.path.join(path, file))  # 获取视频对象
                # 判断是否打开
                isOpened = cap.isOpened
                # 视频信息获取
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                print("fps = ", fps)
                # sum用来判断当前已分析的总帧数
                sum = 0
                # seconds用来保存当前分析的秒数
                seconds = 0
                # timef保存一秒内的帧数
                timef = 0
                while (isOpened):
                    sum += 1
                    timef += 1
                    (frameState, frame) = cap.read()  # 记录每帧及获取状态
                    if frameState == True:
                        seconds = int((sum - 1) / fps)
                        # 格式转变，BGRtoRGB
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # 转变成Image
                        frame = Image.fromarray(np.uint8(frame))
                        frame = np.array(frame)
                        # RGBtoBGR满足opencv显示格式
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                        frameName = videoName + "-" + str(seconds) + "-" + str(timef) + ".png"
                        framePath = os.path.join(videoframepath, frameName)  # 存储路径
                        # cv2.imwrite(framePath, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
                        cv2.imencode('.png', frame)[1].tofile(framePath)
                        print(framePath + " 储存成功")  # 输出存储状态
                        if timef == fps:
                            timef = 0
                    elif frameState == False:
                        print("读帧完毕。")
                        break
                print(os.path.join(path, file) + "处理完毕！")
                cap.release()
    print("全部视频处理完毕。")
    operate = input("重新运行请按回车键，输入exit退出程序：")
    if operate == "exit":
        break