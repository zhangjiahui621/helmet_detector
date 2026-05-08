"""安全帽佩戴检测 —— 单图分析入口。"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2

import config
from detector import Detector


def analyze(image_path: str) -> None:
    path = Path(image_path)
    if not path.exists():
        print(f"[错误] 文件不存在: {path}")
        return
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}:
        print(f"[错误] 不支持的图片格式: {path.suffix}")
        return

    print(f"正在分析: {path.name}")

    detector = Detector()
    dets = detector.detect(str(path))
    with_helmets = dets["with_helmets"]
    without_helmets = dets["without_helmets"]

    total = len(with_helmets) + len(without_helmets)
    if total == 0:
        print("未检测到人员。")
        return

    print(f"检测到 {len(with_helmets)} 人已佩戴, {len(without_helmets)} 人未佩戴\n")

    img = cv2.imread(str(path))

    for box in with_helmets:
        x1, y1, x2, y2 = (int(v) for v in box)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, "HELMET OK", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    for box in without_helmets:
        x1, y1, x2, y2 = (int(v) for v in box)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(img, "NO HELMET", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 保存标注图
    output_dir = Path(config.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"result_{path.name}"
    cv2.imwrite(str(out_path), img)

    print(f"\n结果: {len(with_helmets)}/{total} 人已佩戴安全帽")
    if without_helmets:
        print(f"违规: {len(without_helmets)} 人未佩戴安全帽")
    print(f"标注图已保存: {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python main.py <图片路径>")
        sys.exit(1)
    analyze(sys.argv[1])
