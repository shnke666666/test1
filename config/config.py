import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)

# 测试数据目录
DATA_DIR = os.path.join(BASE_DIR, "Data")
# print(DATA_DIR)

# 测试报告目录
REPORT_DIR = os.path.join(BASE_DIR, "report")
# print(REPORT_DIR)

# 截图保存目录
SCREENSHOT_DIR = os.path.join(REPORT_DIR, "screenshots")
# print(SCREENSHOT_DIR)

# 浏览器配置
BROWSER_CONFIG = {
    "headless": False,  # 是否使用无头模式
    "slow_mo": 50,      # 操作延迟时间
    "viewport": {"width": 1920, "height": 1080}  # 视窗大小
}

# 测试环境URL
BASE_URL = "https://gscm.gzyyrj.cn/"  # 替换为实际的测试环境URL