# capture_image.py
import cv2
import os
from Logger import log
def capture_image():
    # 打开摄像头
    import time
    log.info("capture_image")
    time.sleep(10)  # 程序会暂停执行 10 秒

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        return False

    # 读取一帧
    ret, frame = cap.read()
    if not ret:
        print("无法捕捉图像")
        return False

    # 保存图片到当前目录
    image_path = os.path.join(os.getcwd(), "captured_image.jpg")
    cv2.imwrite(image_path, frame)

    # 释放摄像头资源
    cap.release()

    print(f"图片已保存到: {image_path}")
    return True

if __name__ == "__main__":
    capture_image()
