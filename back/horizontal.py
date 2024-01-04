import numpy as np


def get_vvList(list_data):
    # 取出list中像素存在的区间
    vv_list = list()
    v_list = list()
    for index, i in enumerate(list_data):
        if i > 0:
            v_list.append(index)  # v_list记录含有效像素列或行所在的坐标值，每个字对应一个
        else:
            if v_list:
                vv_list.append(v_list)
                # list的clear与[]有区别
                v_list = []
    return vv_list


def get_horizonal(binary):
    rows, cols = binary.shape

    ver_list = [0]*rows
    for j in range(rows):
        for i in range(cols):
            if binary.item(j, i) == 0:
                ver_list[j] = ver_list[j]+1
    '''
    对ver_list中的元素进行筛选，可以去除一些噪点
    '''
    ver_arr = np.array(ver_list)
    ver_arr[np.where(ver_arr < 1)] = 0
    ver_list = ver_arr.tolist()

    # 绘制水平投影
    '''
    img_white=np.ones(shape=(rows,cols),dtype=np.uint8)*255
    for j in range(rows):
        pt1=(cols-1,j)
        pt2=(cols-1-ver_list[j],j)
        cv2.line(img_white,pt1,pt2,(0,),1)
    cv2.imshow('水平投影',img_white)
    cv2.waitKey(0)
    '''
    # 切割行字符
    vv_list = get_vvList(ver_list)
    lines = []
    for i in vv_list:
        # img_hor=binary[i[0]:i[-1],:]
        # cv2.imshow('单行字符',img_hor)
        # cv2.waitKey(0)
        if i[-1] - i[0] > 3:
            ordinate = (i[0], i[-1])
            lines.append(ordinate)
    return lines
