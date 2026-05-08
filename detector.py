"""YOLO 检测器封装。"""

from __future__ import annotations

import config
from ultralytics import YOLO


class Detector:
    """对 YOLO 模型的轻量封装，返回按类别分组的检测结果。"""

    def __init__(self, model_path: str | None = None):
        path = model_path or config.MODEL_PATH
        self.model = YOLO(path)

        # 构建类别名称 → ID 的映射（全部小写）
        self._name_to_id: dict[str, int] = {}
        for cls_id, name in self.model.names.items():
            self._name_to_id[name.lower().strip()] = cls_id

    # ── 公共接口 ───────────────────────────────────────

    def detect(self, image_path: str):
        """对单张图片执行检测，返回按类别分组的边界框列表。

        Returns:
            {
                "with_helmets":    [[x1,y1,x2,y2], ...],
                "without_helmets": [[x1,y1,x2,y2], ...],
            }
        """
        results = self.model.predict(
            source=image_path,
            conf=config.CONF_THRESHOLD,
            imgsz=config.IMG_SIZE,
            verbose=False,
        )
        result = results[0]

        # 查找类别 ID
        with_id = self._name_to_id.get(config.WITH_HELMET_CLASS.lower())
        without_id = self._name_to_id.get(config.WITHOUT_HELMET_CLASS.lower())

        with_helmets: list[list[float]] = []
        without_helmets: list[list[float]] = []

        for box in result.boxes:
            cls_id = int(box.cls[0])
            xyxy = box.xyxy[0].tolist()
            if cls_id == with_id:
                with_helmets.append(xyxy)
            elif cls_id == without_id:
                without_helmets.append(xyxy)

        return {"with_helmets": with_helmets, "without_helmets": without_helmets}
