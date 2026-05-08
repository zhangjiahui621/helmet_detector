"""项目配置参数。"""

# ── 路径 ──────────────────────────────────────────────
IMAGE_DIR = "input_frames"           # 输入图片文件夹（按文件名排序模拟视频帧）
OUTPUT_DIR = "output_violations"     # 违规帧保存目录
LOG_FILE = "violations.log"          # 违规记录日志

# ── 模型 ──────────────────────────────────────────────
# 默认使用 yolov8n（COCO 80类，可检测 person）。
# 若要检测安全帽，请替换为自定义训练模型，例如：
#   MODEL_PATH = "best_helmet.pt"
MODEL_PATH = "best_helmet.pt"

# 安全帽检测模型的类别名称
WITH_HELMET_CLASS = "with helmet"
WITHOUT_HELMET_CLASS = "without helmet"

# ── 检测参数 ───────────────────────────────────────────
CONF_THRESHOLD = 0.4                 # 检测置信度阈值
IOU_THRESHOLD = 0.05                 # 工人-安全帽 IoU 阈值；低于此值视为未佩戴
IMG_SIZE = 640                       # YOLO 推理分辨率
