import numpy as np
from PIL import Image
from siamese import Siamese
from config import predict_imgFolderPath

model = Siamese()


def compare(img_path, position, char):
    image_1_raw = Image.open(img_path)  # 优化？
    image_1_rgba = image_1_raw.crop(
        (position[0][0], position[0][1], position[1][0], position[1][1]))
    image_1 = Image.new('RGB', image_1_rgba.size, (255, 255, 255))
    # 粘贴使用alpha通道作为掩码的RGBA图像到背景上
    if image_1_rgba.mode == 'RGBA':
        # 如果图像是RGBA格式，使用alpha通道
        alpha_channel = image_1_rgba.split()[3]
    else:
        # 如果图像不是RGBA格式，使用一个全白的alpha通道
        alpha_channel = Image.new(
            'L', image_1_rgba.size, 255)  # 创建一个全白的alpha通道

    image_1.paste(image_1_rgba, mask=alpha_channel)

    try:
        # 此处路径需要修改
        image_2 = Image.open(predict_imgFolderPath+char+'.png')
    except:
        print('no image!')
        return 0

    probability = model.detect_image(image_1, image_2)
    print(char, probability)
    return probability
