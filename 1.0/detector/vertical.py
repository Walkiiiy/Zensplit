import numpy as np
import setdict
import cv2

char_dict = setdict.dic_init()
f=open('pp_string.txt','r')
pp_string=f.read()
f.close()

def char_check(char_num):
    try:
        if char_dict[pp_string[char_num]]=='1':#如果是左右结构的字，flag=2时分割
            return 1
        elif char_dict[pp_string[char_num]]=='8':#如果是英文字母，flag=1时分割
            return 2
        else:
            return 1
    except KeyError or IndexError as e:
        return 1

def get_vvList(list_data,char_num):
    #取出list中像素存在的区间
    vv_list=list()
    v_list=list()

    total_row = len(list_data)
    row_num = 0

    while row_num<total_row:
        mode = char_check(char_num)
        char_num += 1
        flag = 0  # defult设置为连续两列空相素才允许分割，解决二值化部分像素缺失问题

        if mode==1:
            while row_num<total_row:
                if list_data[row_num]>0 :
                    v_list.append(row_num)
                    if flag>0:
                        flag=0
                else:
                    flag+=1
                    if v_list and flag==2:
                        vv_list.append(v_list)
                        #list的clear与[]有区别
                        v_list=[]
                        flag=0
                        row_num+=1
                        break
                row_num+=1

        elif mode==2:
            while row_num<total_row:
                if list_data[row_num] > 0 :
                    v_list.append(row_num)
                else:
                    if v_list :
                        vv_list.append(v_list)
                        # list的clear与[]有区别
                        v_list = []
                        flag = 0
                        row_num += 1
                        break
                row_num += 1

    return vv_list

def get_vertical(binary,charnum):

    rows,cols=binary.shape
    ver_list=[0]*cols
    for j in range(cols):
        for i in range(rows):
            if binary.item(i,j)==0:
                ver_list[j]=ver_list[j]+1
        #if (ver_list[j]<minimum and ver_list[j]>0):#统计行所含像素个数最少的列所含的像素个数，用做误差值
            #minimum=ver_list[j]
    '''
    对ver_list中的元素进行筛选，可以去除一些噪点
    '''
    ver_arr=np.array(ver_list)
    ver_arr[np.where(ver_arr<1)]=0
    ver_list=ver_arr.tolist()

    #绘制垂直投影
    img_white=np.ones(shape=(rows,cols),dtype=np.uint8)*255
    for j in range(cols):
        pt1=(j,rows-1)
        pt2=(j,rows-1-ver_list[j])
        cv2.line(img_white,pt1,pt2,(0,),1)

    cv2.imshow('垂直投影',img_white)
    cv2.waitKey(0)

    #切割单一字符
    vv_list=get_vvList(ver_list,charnum)
    chars=[]
    for i in vv_list:
        #img_ver=binary[:,i[0]:i[-1]]
        #cv2.imshow('单一字符',img_ver)
        #cv2.waitKey(0)
        ordinate = (i[0], i[-1])
        chars.append(ordinate)
    return chars


if __name__=='__main__':
    print(char_dict)
    print(char_check(0))
    print(pp_string)