import  re
def str_init():
    f = open("../PaddleOCR-release-2.6/tools/infer/inference_results/system_results.txt",encoding='utf-8')
    strs=''
    content=f.read()
    #print(content)
    f.close()
    pattern =r'(?<="transcription": ").*?(?=",)'
    matches = re.findall(pattern, content)
    # 输出匹配结果
    for match in matches:
        strs+=match
    #  可以打印出来瞅瞅
    return strs