# 工地安全帽佩戴检测系统

基于 YOLOv8 的安全帽佩戴检测工具。对输入图片帧进行逐帧分析，自动识别未佩戴安全帽的工人，保存违规证据并生成检测报告。

## 功能

- 使用 YOLOv8 模型检测图片中的工人和安全帽
- 通过 IoU（交并比）判断工人是否佩戴安全帽
- 自动保存违规帧并绘制红色标注框
- 生成违规检测日志报告

## 项目结构

```
helmet_detector/
├── main.py              # 入口脚本
├── config.py            # 配置参数（模型路径、阈值等）
├── detector.py          # YOLO 检测器封装
├── analyzer.py          # 逐帧分析与违规记录
├── iou_utils.py         # IoU 计算工具
├── requirements.txt     # Python 依赖
├── input_frames/        # 输入图片目录（按文件名排序模拟视频帧）
└── output_violations/   # 违规帧输出目录
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备模型

默认使用 `yolov8n.pt`（COCO 80 类，可检测 person）。首次运行时会自动下载。

若需检测安全帽，请替换为自定义训练的模型，并在 `config.py` 中修改：

```python
MODEL_PATH = "best_helmet.pt"
```

### 3. 放入图片

将待检测的图片帧放入 `input_frames/` 目录，支持 `.jpg`、`.jpeg`、`.png`、`.bmp`、`.webp` 格式。文件按名称排序逐帧处理。

### 4. 运行检测

```bash
python main.py
```

运行后：
- 违规帧图片（含红色标注）保存到 `output_violations/`
- 违规记录写入 `violations.log`

## 配置说明

在 `config.py` 中可调整以下参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `IMAGE_DIR` | `input_frames` | 输入图片文件夹 |
| `OUTPUT_DIR` | `output_violations` | 违规帧保存目录 |
| `LOG_FILE` | `violations.log` | 违规日志文件 |
| `MODEL_PATH` | `yolov8n.pt` | YOLO 模型路径 |
| `CONF_THRESHOLD` | `0.5` | 检测置信度阈值 |
| `IOU_THRESHOLD` | `0.05` | IoU 阈值，低于此值视为未佩戴 |
| `IMG_SIZE` | `640` | YOLO 推理分辨率 |

## 检测原理

1. 对每帧图片使用 YOLO 模型检测所有工人（person）和安全帽（helmet）的边界框
2. 对每个工人的边界框，计算其与所有安全帽边界框的最大 IoU
3. 若最大 IoU 低于设定阈值（默认 0.05），则判定该工人未佩戴安全帽
4. 将违规帧复制到输出目录并绘制红色标注框，同时记录日志
