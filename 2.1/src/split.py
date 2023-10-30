#对初次投影法扫描得到的列表处理，分离字符和标点，分别求平均。
import numpy as np
def split_char_punctuation():
    pass 
def get_inform(ordinates):#获取标准的：字的宽度，字符间距,字与符号间距，
    widths=[]
    for ordinate in ordinates:
        width=ordinate[0][1]-ordinate[0][0]
        widths.append(width)
    mid_width=np.median(widths)
    max_char_width=max(widths)
    long_expection=0
    #去除可能出现的特别长的连续像素（破折号）
    while max_char_width>=2*mid_width:
        long_expection=max_char_width
        widths.remove(max_char_width)
        max_char_width=max(widths)
    min_char_width=mid_width-(max_char_width-mid_width)
    char_width=(min_char_width,mid_width,max_char_width)
    #print("char width",char_width)

    i=0
    dists=[]
    while i<len(ordinates)-1:
        if(ordinates[i+1][1]==ordinates[i][1]):
            dist=ordinates[i+1][0][0]-ordinates[i][0][1]
            dists.append(dist)
        i+=1
    #print(dists)

    return char_width