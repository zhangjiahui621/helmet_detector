"""逐帧分析：检测未佩戴安全帽的工人并记录。"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

import cv2

import config
from detector import Detector
from iou_utils import best_iou


class ViolationAnalyzer:
    """遍历图片帧，检测违规并保存证据。"""

    def __init__(self, detector: Detector | None = None):
        self.detector = detector or Detector()
        self.output_dir = Path(config.OUTPUT_DIR)
        self.log_path = Path(config.LOG_FILE)

    # ── 公共接口 ───────────────────────────────────────

    def run(self) -> list[dict]:
        """处理 IMAGE_DIR 下所有图片，返回违规记录列表。"""
        image_dir = Path(config.IMAGE_DIR)
        images = sorted(
            p for p in image_dir.iterdir()
            if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        )

        if not images:
            print(f"[WARN] {image_dir.resolve()} 中未找到图片。")
            return []

        self.output_dir.mkdir(parents=True, exist_ok=True)
        violations: list[dict] = []

        for idx, img_path in enumerate(images, start=1):
            dets = self.detector.detect(str(img_path))
            persons = dets["persons"]
            helmets = dets["helmets"]

            # 对每个工人检查是否存在重叠度足够高的安全帽
            for person_box in persons:
                iou = best_iou(person_box, helmets)
                if iou < config.IOU_THRESHOLD:
                    record = self._record(idx, img_path, person_box, iou)
                    violations.append(record)

        if violations:
            self._write_log(violations)
        print(f"\n检测完成：共 {len(images)} 帧，发现 {len(violations)} 条违规记录。")
        return violations

    # ── 内部方法 ───────────────────────────────────────

    def _record(self, frame_idx: int, img_path: Path,
                person_box: list[float], iou: float) -> dict:
        """保存违规帧并生成记录。"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        saved_name = f"violation_frame{frame_idx:04d}_{img_path.stem}.jpg"
        saved_path = self.output_dir / saved_name
        shutil.copy2(img_path, saved_path)

        # 在保存的图片上画框标注
        self._annotate(saved_path, person_box)

        record = {
            "frame_index": frame_idx,
            "source_file": img_path.name,
            "timestamp": timestamp,
            "iou": round(iou, 4),
            "saved_path": str(saved_path),
        }
        print(f"  [违规] 帧 {frame_idx} | IoU={iou:.4f} | "
              f"已保存 → {saved_name}")
        return record

    @staticmethod
    def _annotate(image_path: Path, person_box: list[float]) -> None:
        """在图片上绘制红色违规框。"""
        img = cv2.imread(str(image_path))
        if img is None:
            return
        x1, y1, x2, y2 = (int(v) for v in person_box)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(img, "NO HELMET", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imwrite(str(image_path), img)

    def _write_log(self, violations: list[dict]) -> None:
        """将违规记录写入日志文件。"""
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("安全帽佩戴违规检测报告\n")
            f.write(f"生成时间: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
            f.write("=" * 60 + "\n\n")
            for v in violations:
                f.write(
                    f"帧序号: {v['frame_index']}\n"
                    f"源文件: {v['source_file']}\n"
                    f"检测时间: {v['timestamp']}\n"
                    f"IoU值: {v['iou']}\n"
                    f"保存路径: {v['saved_path']}\n"
                    f"{'-' * 40}\n"
                )
        print(f"日志已写入: {self.log_path.resolve()}")
