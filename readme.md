基于多种方案的字符切割技术
* pure——projection纯投影法
* 1.0 粗糙的ocr字符结构与字典匹配
* 2.0 基于动态宽度标准调整算法，适用于全中文（最好是公文）的理想环境
* 2.1 结合理想的ocr结果，根据不同种类进行不同的切割模式
* 2.3 引入了ocrapi，并结合ocr行字数信息进行更准确的切割
