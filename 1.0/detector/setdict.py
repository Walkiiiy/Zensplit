
def dic_init():
    f = open("结构字典（20000字）.txt",encoding='utf-8')
    dic=dict()
    for line in f.readlines():
        line = line.strip(',').strip('\n').strip(',')
        k = line.split(':')[0].strip('\'')
        v = line.split(':')[1].strip('\'')
        dic[k] = v
    f.close()
    #  可以打印出来瞅瞅
    return dic