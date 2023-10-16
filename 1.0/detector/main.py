import horizontal
import vertical
import cv2
import setstring
from tools.infer import predict_system
#需要将paddle所在的包为源文件夹

#特殊字符：省略号/姚/比/左右结构(旧、三点水、口字旁)/门/们/小/训/全体/"/英文字符

img_path='rawpic/finaltest.png'#设置图像路径，必须是相对路径且不能有中文
if __name__=='__main__':

    predict_system.set_dir(img_path)#ppocr初始化
    predict_system.run_ppocr()
    pp_string=setstring.str_init().strip()
    f=open('pp_string.txt','w')
    f.write(pp_string)
    f.close()
    print('\npp识别字符串：',pp_string,'\n长度：',len(pp_string))

    #投影法图像分割
    img_bgr=cv2.imread(img_path,1)
    if not img_bgr is None:
        img=img_bgr.copy()
        img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #二值化
        t,binary=cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)

    lines=horizontal.get_horizonal(binary)
    #print(lines)
    height,width=binary.shape
    chars=[]
    ordinats=[]
    char_num=0
    for line in lines:
        img_hor=binary[line[0]:line[1],:]
        h_list=vertical.get_vertical(img_hor,char_num)
        char_num+=len(h_list)
        for x_ordinate in h_list:
            ordinats.append((x_ordinate,line))
    print(len(ordinats))
    img_cut=img_bgr#用所得坐标切割每个字符
    for ordinate in ordinats:
        cv2.rectangle(img_cut, (ordinate[0][0], ordinate[1][0]), (ordinate[0][1], ordinate[1][1]), (255, 0, 0), 1)
    cv2.imwrite("outcome/outcome.jpg", img_cut)
    #cv2.imshow('cut',img_cut)
    #cv2.waitKey(0)


    i=35
    while i<35:
        print(pp_string[i])
        i+=1



