import cv2
import numpy as np
import time
import argparse

def detect_motion(video_path=None, min_area=500, show_window=True):
    """
    检测视频中的运动，并输出移动物体的位置信息（bounding box）

    参数:
        video_path: 视频文件路径，或 None 表示使用摄像头
        min_area:   忽略小于此面积的噪声轮廓（像素）
        show_window: 是否实时显示带框的画面
    """
    # 初始化视频源
    if video_path is None:
        cap = cv2.VideoCapture(0)  # 0 = 默认摄像头
        print("使用摄像头进行实时运动检测...")
    else:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"无法打开视频文件: {video_path}")
            return
        print(f"处理视频文件: {video_path}")

    # 使用MOG2背景减法器（对光照变化、阴影有较好鲁棒性）
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=500,          # 背景历史帧数
        varThreshold=50,      # 方差阈值（越小越敏感）
        detectShadows=True    # 检测阴影
    )

    frame_count = 0
    motion_detected_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("视频结束或读取失败")
            break

        frame_count += 1

        # 预处理：缩小画面加速 + 灰度
        small_frame = cv2.resize(frame, (640, 480))  # 可调大小，平衡速度与精度
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)  # 去噪

        # 背景减法 → 前景掩码
        fg_mask = bg_subtractor.apply(gray)

        # 形态学处理：去除小噪声 + 连接断开的区域
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_DILATE, kernel)

        # 查找轮廓
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        positions = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area:
                continue  # 忽略小噪声

            motion_detected = True
            # 计算外接矩形（bounding box）
            x, y, w, h = cv2.boundingRect(cnt)
            # 还原到原始画面尺寸（如果resize过）
            scale_x = frame.shape[1] / small_frame.shape[1]
            scale_y = frame.shape[0] / small_frame.shape[0]
            x, y, w, h = int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)

            positions.append({
                "frame": frame_count,
                "timestamp": time.time(),
                "bbox": [x, y, x + w, y + h],  # [left, top, right, bottom]
                "area": area,
                "center": (x + w//2, y + h//2)
            })

            if show_window:
                # 在原始画面上画框（红色）
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                cv2.putText(frame, f"Area: {int(area)}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        if motion_detected:
            motion_detected_frames += 1
            print(f"[帧 {frame_count}] 检测到运动！位置信息：")
            for pos in positions:
                print(f"  - 中心点: {pos['center']}, 框: {pos['bbox']}, 面积: {pos['area']}")
        else:
            if frame_count % 30 == 0:  # 每秒约打印一次（假设30fps）
                print(f"[帧 {frame_count}] 无明显运动")

        if show_window:
            cv2.imshow("Motion Detection", frame)
            # cv2.imshow("Foreground Mask", fg_mask)  # 可选：看前景掩码

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    print(f"\n处理完成。共 {frame_count} 帧，检测到运动的帧数: {motion_detected_frames}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频/摄像头运动检测 + 位置输出")
    parser.add_argument("--video", type=str, default=None, help="视频文件路径（可选，默认为摄像头）")
    parser.add_argument("--min_area", type=int, default=500, help="最小运动面积阈值")
    parser.add_argument("--no_window", action="store_true", help="不显示窗口（后台运行）")

    args = parser.parse_args()

    detect_motion(
        video_path=args.video,
        min_area=args.min_area,
        show_window=not args.no_window
    )