import cv2
import numpy as np

if __name__ == "__main__":
    # 测试 OpenCV 是否安装成功
    print("OpenCV 版本:", cv2.__version__)
    print(cv2.__file__)

    # 创建一个简单的测试图像 (黑色图像)
    img = cv2.imread('test_image.jpg')  # 如果有图像文件，可以测试读取
    if img is None:
        print("未找到测试图像，创建空白图像进行测试。")
        img = cv2.imread('')  # 或者使用 numpy 创建
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        print("创建了 100x100 的黑色图像。")

    # 转换颜色空间作为测试
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("图像转换为灰度成功。")

    # 保存测试图像
    cv2.imwrite('output_test.jpg', gray)
    print("灰度图像已保存为 output_test.jpg")

    print("OpenCV 测试完成！")

if __name__ == "__main__":
    main()
