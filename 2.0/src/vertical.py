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

def get_vertical_all(binary):
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
        ordinate = (i[0], i[-1])
        chars.append(ordinate)
    return chars

def check_if_more(lis,start,char_width,old_length):
    dist_to_check=char_width[1]//2-1#如果已经切割的字符过窄，就要检查是否是左右结构类的情况，向后继续检查
    i=start
    to_be_add,j=add_row_until_blank(lis,start)
    width=j-i+old_length

    #如果下一个字符的距离超出阈值，则不应该添加
    if j-len(to_be_add)-i>dist_to_check:
        return 0

    #如果添加该部分后字符过长，则不应该添加
    if width> 1.2*char_width[1]:
        return 0
    
    return 1

def add_row_until_blank(lis,start):#从任意位置开始，扫描至非空列，添加至数组直到到遇到空列
    i=start
    res=[]
    while i<len(lis):
        if lis[i]>0:
            first_black=i
            while i<len(lis):
                if lis[i]>0:
                    res.append(i)
                else:
                    return res,i
                i+=1
        else:
            i+=1
    return res,i

def get_vvList_Zen(list_data,char_width):
    #取出list中像素存在的区间
    vv_list=list()
    v_list=list()

    total_row = len(list_data)
    row_num = 0

    while row_num<total_row:
        v_list,row_num=add_row_until_blank(list_data,row_num)
        if row_num>=total_row:
            break
        
        #分裂检查
        is_more=check_if_more(list_data,row_num,char_width,len(v_list))
        if is_more:
            while is_more:
                to_be_add,row_num=add_row_until_blank(list_data,row_num)
                if row_num>=total_row:
                    break    
                v_list+=to_be_add
                is_more=check_if_more(list_data,row_num,char_width,len(v_list))
        #添加字符
        if v_list:
            vv_list.append(v_list)
            v_list=[]
        
        row_num+=1

    return vv_list

def get_vertical_Zen(binary,char_width):
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
    vv_list=get_vvList_Zen(ver_list,char_width)
    chars=[]
    for i in vv_list:
        #print(i)
        ordinate = (i[0], i[-1])
        chars.append(ordinate)
    return chars


