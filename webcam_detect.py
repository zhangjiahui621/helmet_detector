"""安全帽佩戴检测 —— 摄像头实时检测。"""

from __future__ import annotations

import cv2

import config
from detector import Detector


def run_webcam(camera_id: int = 0) -> None:
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"[错误] 无法打开摄像头 (ID={camera_id})")
        return

    print("摄像头已打开，按 Q 键退出")

    detector = Detector()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[错误] 无法读取画面")
            break

        # 临时保存当前帧用于检测
        tmp_path = "_tmp_frame.jpg"
        cv2.imwrite(tmp_path, frame)

        dets = detector.detect(tmp_path)
        with_helmets = dets["with_helmets"]
        without_helmets = dets["without_helmets"]

        # 绘制标注框
        for box in with_helmets:
            x1, y1, x2, y2 = (int(v) for v in box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "HELMET OK", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        for box in without_helmets:
            x1, y1, x2, y2 = (int(v) for v in box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, "NO HELMET", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # 显示状态文字
        status = f"With: {len(with_helmets)}  Without: {len(without_helmets)}"
        cv2.putText(frame, status, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Helmet Detection - Press Q to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("已退出")


if __name__ == "__main__":
    run_webcam()
