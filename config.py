"""项目配置参数。"""

# ── 路径 ──────────────────────────────────────────────
IMAGE_DIR = "input_frames"           # 输入图片文件夹（按文件名排序模拟视频帧）
OUTPUT_DIR = "output_violations"     # 违规帧保存目录
LOG_FILE = "violations.log"          # 违规记录日志

# ── 模型 ──────────────────────────────────────────────
MODEL_PATH = "best_helmet.pt"

# 安全帽检测模型的类别名称
WITH_HELMET_CLASS = "with helmet"
WITHOUT_HELMET_CLASS = "without helmet"

# ── 检测参数 ───────────────────────────────────────────
CONF_THRESHOLD = 0.4                 # 检测置信度阈值
IMG_SIZE = 640                       # YOLO 推理分辨率
