import ocrModule.Ocr as ocr
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import split
import vertical
import horizontal
import config
from config import img_path, txtpath, outcomepath
from keras_master import predict
import warnings
import sys


def cv2AddChineseText(img, text, position, textColor=(0, 0, 0), textSize=15):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


if __name__ == '__main__':
    ocrRes = ocr.createRequest(img_path)

    with open(txtpath, 'w') as file:
        for line in ocrRes:
            file.write(line)

    with open(txtpath, 'r') as file:
        # 读取文件内容到一个字符串
        ocr_content_raw = file.read()
        print('api返回字数:', len(ocr_content_raw))
        ocr_content_store = ocr_content_raw

    # 投影法图像分割
    img_bgr = cv2.imread(img_path, 1)
    if not img_bgr is None:
        img = img_bgr.copy()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 二值化
        t, binary = cv2.threshold(
            img_gray, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    else:
        print("couldn't read image!")
    lines = horizontal.get_horizonal(binary)
    height, width = binary.shape
    ordinats = []
    char_num = 0
    print('投影分割行数：', len(lines))

    for line in lines:
        img_hor = binary[line[0]:line[1], :]
        h_list = vertical.get_vertical_all(img_hor)  # 第一趟
        char_num += len(h_list)
        for x_ordinate in h_list:
            ordinats.append((x_ordinate, line))
    print("first scan,num of char:", len(ordinats))

    char_width = split.get_inform(ordinats)
    print(char_width)

    ordinats_Zen = []
    char_num_Zen = 0
    row_num = 0  # 行数
    for line in lines:
        img_hor = binary[line[0]:line[1], :]
        try:
            h_list_Zen = vertical.get_vertical_Zen(
                img_hor, char_width, ocrRes[row_num])  # 第二趟
        except:
            warnings.warn('fucked!', UserWarning)
            break
        row_chr_num = len(h_list_Zen)  # 本行字数
        i = 0
        for x_ordinate in h_list_Zen:
            ordinate = (x_ordinate, line)
            ordinats_Zen.append(ordinate)

            # 神经网络检查行中和行末
            if i == row_chr_num//2 or i == row_chr_num-1:
                probability = predict.compare(img_path, ((ordinate[0][0], ordinate[1][0]), (
                    ordinate[0][1], ordinate[1][1])), ocrRes[row_num][i])
                if probability < 0.4:
                    # warnings.warn("警告：切割可能发生错误", UserWarning)
                    print("警告：切割可能发生错误")
            # 打印字符框
            cv2.rectangle(img_bgr, (ordinate[0][0], ordinate[1][0]),
                          (ordinate[0][1], ordinate[1][1]), (255, 0, 0), 1)
            # 打印文字
            try:
                img_bgr = cv2AddChineseText(img_bgr, ocrRes[row_num][i], ((
                    ordinate[0][0]+ordinate[0][1])//2, ordinate[1][0]-(ordinate[0][1]-ordinate[0][0])//2))
            except IndexError:
                pass
            i += 1
        row_num += 1
    print("second scan,num of char:", len(ordinats_Zen))

    # 显示和存储图片
    # cv2.imshow('outcome',img_cut)
    # cv2.waitKey(0)
    cv2.imwrite(outcomepath, img_bgr)
