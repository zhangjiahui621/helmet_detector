"""边界框 IoU（交并比）计算工具。"""

from __future__ import annotations


def compute_iou(box_a: list[float], box_b: list[float]) -> float:
    """计算两个 [x1, y1, x2, y2] 边界框的 IoU。

    Returns:
        IoU 值，范围 [0.0, 1.0]。
    """
    x1 = max(box_a[0], box_b[0])
    y1 = max(box_a[1], box_b[1])
    x2 = min(box_a[2], box_b[2])
    y2 = min(box_a[3], box_b[3])

    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)

    area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
    union = area_a + area_b - inter

    if union <= 0:
        return 0.0
    return inter / union


def best_iou(person_box: list[float], helmet_boxes: list[list[float]]) -> float:
    """返回一个人框与所有安全帽框之间的最大 IoU。

    Args:
        person_box: 单个 [x1, y1, x2, y2]。
        helmet_boxes: 多个 [x1, y1, x2, y2] 的列表。

    Returns:
        最大 IoU；若 helmet_boxes 为空则返回 0.0。
    """
    if not helmet_boxes:
        return 0.0
    return max(compute_iou(person_box, h) for h in helmet_boxes)
