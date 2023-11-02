import horizontal
import vertical
import split
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt



img_path='/home/walkiiiy/Zensplit/2.1/src/rawpic/test.png'#设置图像路径，必须是相对路径且不能有中文

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


if __name__=='__main__':

    with open('/home/walkiiiy/Zensplit/2.1/src/ocr_outcome.txt', 'r') as file:
        # 读取文件内容到一个字符串
        ocr_content_raw = file.read()
    #预处理ocr内容
    ocr_content=''
    for c in ocr_content_raw:
        if ord(c)!=10 and ord(c)!=12288 and ord(c)!=8194 and c!='\n'and c!='\r'and c!='\t':
            ocr_content+=c
    ocr_content_store=ocr_content

    #投影法图像分割
    img_bgr=cv2.imread(img_path,1)
    if not img_bgr is None:
        img=img_bgr.copy()
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #二值化
        t,binary=cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    else:
        print("couldn't read image!")
    lines=horizontal.get_horizonal(binary)
    height,width=binary.shape
    ordinats=[]
    char_num=0
    for line in lines:
        img_hor=binary[line[0]:line[1],:]
        h_list=vertical.get_vertical_all(img_hor)#第一趟
        char_num+=len(h_list)
        for x_ordinate in h_list:
            ordinats.append((x_ordinate,line))
    print("first scan,num of char:",len(ordinats))
    #print(ordinats)

    char_width=split.get_inform(ordinats)
    print(char_width)
    
    ordinats_Zen=[]
    char_num_Zen=0
    row_num=0#行数
    for line in lines:
        img_hor=binary[line[0]:line[1],:]
        h_list_Zen=vertical.get_vertical_Zen(img_hor,char_width,ocr_content)#第二趟
        row_chr_num=len(h_list_Zen)#本行字数
        for x_ordinate in h_list_Zen:
            ordinats_Zen.append((x_ordinate,line))
        row_num+=1
        print("第%d行%d字"%(row_num,row_chr_num))
        print("本行切割的字符：",ocr_content[:row_chr_num])
        ocr_content=ocr_content[row_chr_num:]#更新ocr字符串 
        print("本行坐标",h_list_Zen)
    print("second scan,num of char:",len(ordinats_Zen))
    #print(ordinats_Zen)

    #用所得坐标切割每个字符
    img_cut=img_bgr
    for ordinate in ordinats_Zen:
        cv2.rectangle(img_cut, (ordinate[0][0], ordinate[1][0]), (ordinate[0][1], ordinate[1][1]), (255, 0, 0), 1)
    
    #在对应位置打印信息
    i=0
    for ordinate in ordinats_Zen:
        img_cut=cv2AddChineseText(img_cut,ocr_content_store[i],((ordinate[0][0]+ordinate[0][1])//2, ordinate[1][0]-(ordinate[0][1]-ordinate[0][0])//2))
        i+=1
    #显示和存储图片
    # cv2.imshow('outcome',img_cut)
    # cv2.waitKey(0)
    cv2.imwrite("/home/walkiiiy/Zensplit/2.1/src/outcome/outcome.jpg", img_cut)
    



