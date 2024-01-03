import base64
import requests
from ocrModule.utils.AuthV3Util import addAuthParams
import json
# 您的应用ID
APP_KEY = '3a8bd3bc44136041'
# 您的应用密钥
APP_SECRET = 'pyjt4OKx2YjjaMWSMUE9UkPy4VDndKdx'


def createRequest(PATH):
    '''
    设置OCR请求的参数
    '''
    lang_type = 'zh-CHS'  # 中文识别
    detect_type = '10012'  # 通用文字识别
    angle = '0'       # 不进行360角度识别
    column = 'onecolumn'      # 不按多列识别
    rotate = 'donot_rotate'      # 不获取文字旋转角度
    doc_type = 'json'
    image_type = '1'

    img = readFileAsBase64(PATH)
    data = {'img': img, 'langType': lang_type, 'detectType': detect_type, 'angle': angle,
            'column': column, 'rotate': rotate, 'docType': doc_type, 'imageType': image_type}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/ocrapi', header, data, 'post')
    originRes = str(res.content, 'utf-8')
    # 将响应字符串解析为 JSON 对象
    ocr_response_json = json.loads(originRes)

    # 使用解析后的 JSON 对象
    line_res = extract_text_by_line(ocr_response_json)
    print('api返回行数:', len(line_res))
    return line_res


def extract_text_by_line(ocr_response):
    lines = []
    for region in ocr_response['Result']['regions']:
        for line in region['lines']:
            lines.append(line['text'])
    return lines


# def parseResponse(response):
#     '''
#     解析OCR返回的响应，提取文本内容
#     '''
#     result = json.loads(response)
#     text_content = []

#     if 'Result' in result and 'regions' in result['Result']:
#         for region in result['Result']['regions']:
#             for line in region['lines']:
#                 text_content.append(line['text'])

#     return '\n'.join(text_content)


def doCall(url, header, params, method):
    if method == 'get':
        return requests.get(url, params=params, headers=header)
    elif method == 'post':
        return requests.post(url, data=params, headers=header)


def readFileAsBase64(path):
    with open(path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode('utf-8')


if __name__ == '__main__':
    res = createRequest('/home/walkiiiy/Zensplit/2.3/src/rawpic/photo1.png')
    # for line in res:
    #     print(line)
    print('api返回行数:', len(res))
