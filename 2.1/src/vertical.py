import numpy as np
import cv2
import string
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
    dist_to_check=char_width[1]//2+10#如果已经切割的字符过窄，就要检查是否是左右结构类的情况，向后继续检查
    i=start
    to_be_add,j=add_row_until_blank(lis,start)
    width=j-i+old_length

    #如果下一个字符的距离超出阈值，则不应该添加
    if j-len(to_be_add)-i>dist_to_check:
        return 0
    #如果添加该部分后字符过长，则不应该添加
    if width>=1.2*char_width[1]:
        return 0
    return 1

def add_row_until_blank(lis,start):#从任意位置开始，扫描至非空列，添加至数组直到到遇到空列
    i=start
    res=[]
    while i<len(lis):
        if lis[i]>0:
            while i<len(lis):
                if lis[i]>0:
                    res.append(i)
                else:
                    return res,i
                i+=1
        else:
            i+=1
    return res,i

def split_default(list_data,row_num,total_row,char_width):#适用于中文和大部分标点
    v_list,row_num=add_row_until_blank(list_data,row_num)    
    #分裂检查
    is_more=check_if_more(list_data,row_num,char_width,v_list[-1]-v_list[0])#传参oldlength时出错
    if is_more:
        while is_more:
            to_be_add,row_num=add_row_until_blank(list_data,row_num)
            if row_num>=total_row:
                break    
            v_list+=to_be_add
            is_more=check_if_more(list_data,row_num,char_width,v_list[-1]-v_list[0])
    if len(v_list)>=char_width[1]*2:#过长切半
        print("过长切半")
        row_num=(v_list[0]+row_num)//2
        v_list=v_list[:len(v_list)//2]
    return v_list,row_num

def split_by_range(list_data,row_num,char_width):#给定范围，过长切半，适用于字母数字和一些符号
    v_list,row_num=add_row_until_blank(list_data,row_num)    
    if len(v_list)>char_width[2]:#如果字符过长，直接切半
        row_num=(row_num+v_list[0])//2
        v_list=v_list[:row_num]
        return v_list,row_num
    if len(v_list)<char_width[0]:#如果字符过短，添加直到空白，然后如果过长就切半
        temp,row_num_new=add_row_until_blank(list_data,row_num)
        if row_num_new-v_list[0]>char_width[2]:
            row_num=(row_num_new+v_list[0])//2
        else:
            row_num=row_num_new
        v_list+=temp
    return v_list,row_num

def split_pure_projection(list_data,row_num):#纯投影法，遇到空列就切，适用于独立性强的标点
    v_list,row_num=add_row_until_blank(list_data,row_num)    
    return v_list,row_num

def check_if_end(list_data,row_num):#由于先进行字符种类判断，需要先判断该行是否结束
    if row_num>=len(list_data):
        return 0
    while row_num<len(list_data):
        if list_data[row_num]>0:
            return 0
        row_num+=1
    return 1

def get_vvList_Zen(list_data,char_width,ocr_content):
    #预处理字宽度
    char_width_ch=char_width
    char_width_eng_low=(char_width[1]*0.2,char_width[1]*0.475,char_width[1]*0.7)
    char_width_eng_up=(char_width[1]*0.4,char_width[1]*0.55,char_width[1]*0.8)
    # char_width_num=(char_width[1]*0.3,char_width[1]*0.425,char_width[1]*0.55)
    char_width_dash=(char_width[1]*0.4,0,char_width[1]*0.6)#中间值在这里没有用了
    char_width_brackets=(char_width[1]*0.1,0,char_width[1]*0.4)#括号
    char_width_slash=(char_width[1]*0.3,0,char_width[1]*0.6)#斜杠
    #取出list中像素存在的区间
    vv_list=list()
    v_list=list()

    total_row = len(list_data)
    row_num = 0
    char_num=0
    while row_num<total_row:
        if row_num>=total_row:
            break
        if char_num>=len(ocr_content):
            break
        if ocr_content[char_num] in string.ascii_lowercase:
            v_list,row_num=split_by_range(list_data,row_num,char_width_eng_low)
        elif ocr_content[char_num] in string.ascii_uppercase:
            v_list,row_num=split_by_range(list_data,row_num,char_width_eng_up)
        elif ocr_content[char_num] in string.digits:#数字进行纯投影
            v_list,row_num=split_pure_projection(list_data,row_num)
        elif ocr_content[char_num] =='-' or ocr_content[char_num] =='-' or ocr_content[char_num] =='_':
            v_list,row_num=split_by_range(list_data,row_num,char_width_dash)
        elif ocr_content[char_num] =='(' or ocr_content[char_num] ==')' or ocr_content[char_num] =='{' or ocr_content[char_num] =='}'or ocr_content[char_num] =='（' or ocr_content[char_num] =='）':
            v_list,row_num=split_by_range(list_data,row_num,char_width_brackets)
        elif ocr_content[char_num] =='/' or ocr_content[char_num] =='\\' :
            v_list,row_num=split_by_range(list_data,row_num,char_width_slash)
        elif ocr_content[char_num] =='.' or ocr_content[char_num] =='《' :
            v_list,row_num=split_pure_projection(list_data,row_num)
        else:
            v_list,row_num=split_default(list_data,row_num,total_row,char_width_ch)

        #添加字符
        if v_list:
            vv_list.append(v_list)
            v_list=[]
        
        row_num+=1
        char_num+=1
        
        is_end=check_if_end(list_data,row_num)
        if is_end:
            break
    return vv_list

def get_vertical_Zen(binary,char_width,ocr_content):
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
    vv_list=get_vvList_Zen(ver_list,char_width,ocr_content)
    chars=[]
    for i in vv_list:
        #print(i)
        ordinate = (i[0], i[-1])
        chars.append(ordinate)
    return chars


