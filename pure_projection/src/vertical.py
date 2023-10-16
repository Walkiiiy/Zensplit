import numpy as np
import cv2
def get_vvList(list_data):
    #取出list中像素存在的区间
    vv_list=list()
    v_list=list()

    total_row = len(list_data)
    row_num = 0

    while row_num<total_row:
        flag = 0  # defult设置为连续两列空相素才允许分割，解决二值化部分像素缺失问题

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

    return vv_list

def get_vertical(binary):
    rows,cols=binary.shape#行，列
    ver_list=[0]*cols
    for j in range(cols):
        for i in range(rows):
            if binary.item(i,j)==0:
                ver_list[j]=ver_list[j]+1
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

    #切割单一字符
    vv_list=get_vvList(ver_list)
    chars=[]
    for i in vv_list:
        #img_ver=binary[:,i[0]:i[-1]]
        #cv2.imshow('单一字符',img_ver)
        #cv2.waitKey(0)
        ordinate = (i[0], i[-1])
        chars.append(ordinate)
    return chars


