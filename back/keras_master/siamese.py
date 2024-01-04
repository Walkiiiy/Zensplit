from utils.utils import (cvtColor, letterbox_image, preprocess_input,
                         show_config)
from nets.siamese import siamese
from PIL import Image
from keras import backend as K
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from config import modelPath


# ---------------------------------------------------#
#   使用自己训练好的模型预测需要修改model_path参数
# ---------------------------------------------------#
class Siamese(object):
    _defaults = {
        # -----------------------------------------------------#
        #   使用自己训练好的模型进行预测一定要修改model_path
        #   model_path指向logs文件夹下的权值文件
        # -----------------------------------------------------#
        # 此处路径需要修改
        "model_path": modelPath,
        # -----------------------------------------------------#
        #   输入图片的大小。
        # -----------------------------------------------------#
        "input_shape": [105, 105],
        # --------------------------------------------------------------------#
        #   该变量用于控制是否使用letterbox_image对输入图像进行不失真的resize
        #   否则对图像进行CenterCrop
        # --------------------------------------------------------------------#
        "letterbox_image": False,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    # ---------------------------------------------------#
    #   初始化Siamese
    # ---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():

            setattr(self, name, value)
        self.sess = tf.compat.v1.keras.backend.get_session()

        self.generate()

        show_config(**self._defaults)

    # ---------------------------------------------------#
    #   载入模型
    # ---------------------------------------------------#
    def generate(self):
        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith(
            '.h5'), 'Keras model or weights must be a .h5 file.'
        # ---------------------------#
        #   载入模型与权值
        # ---------------------------#
        self.model = siamese([self.input_shape[0], self.input_shape[1], 3])
        self.model.load_weights(self.model_path)
        print('{} model loaded.'.format(model_path))

    # ---------------------------------------------------#
    #   检测图片
    # ---------------------------------------------------#
    def detect_image(self, image_1, image_2):
        # ---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        # ---------------------------------------------------------#
        image_1 = cvtColor(image_1)
        image_2 = cvtColor(image_2)

        # ---------------------------------------------------#
        #   对输入图像进行不失真的resize
        # ---------------------------------------------------#
        image_1 = letterbox_image(
            image_1, [self.input_shape[1], self.input_shape[0]], self.letterbox_image)
        image_2 = letterbox_image(
            image_2, [self.input_shape[1], self.input_shape[0]], self.letterbox_image)

        # ---------------------------------------------------------#
        #   归一化+添加上batch_size维度
        # ---------------------------------------------------------#
        photo1 = np.expand_dims(preprocess_input(
            np.array(image_1, np.float32)), 0)
        photo2 = np.expand_dims(preprocess_input(
            np.array(image_2, np.float32)), 0)

        # ---------------------------------------------------#
        #   获得预测结果，output输出为概率
        # ---------------------------------------------------#
        output = self.model.predict([photo1, photo2])[0]

        return output

    def close_session(self):
        self.sess.close()
