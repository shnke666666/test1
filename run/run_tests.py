import importlib.util
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import sync_playwright

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent

# 导入配置
sys.path.append(str(ROOT_DIR))
from config.config import REPORT_DIR, SCREENSHOT_DIR

def clean_report_dir():
    """清理报告目录"""
    if os.path.exists(REPORT_DIR):
        for file in os.listdir(REPORT_DIR):
            file_path = os.path.join(REPORT_DIR, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"清理文件 {file_path} 时出错: {e}")

def check_testcase_dir():
    """检查测试用例目录是否存在"""
    testcase_dir = ROOT_DIR / "Testcase"
    if not testcase_dir.exists():
        print(f"错误: 测试用例目录不存在: {testcase_dir}")
        print("请确保项目根目录下存在 Testcase 目录")
        return False
    return True

def add_screenshots_to_report():
    """将截图添加到allure报告中"""
    if SCREENSHOT_DIR.exists():
        print(f"正在添加截图，截图目录: {SCREENSHOT_DIR}")
        for screenshot in sorted(SCREENSHOT_DIR.glob("*.png")):
            try:
                allure.attach.file(
                    str(screenshot),
                    name=f"测试截图_{screenshot.stem}",
                    attachment_type=AttachmentType.PNG
                )
                print(f"成功添加截图: {screenshot.name}")
            except Exception as e:
                print(f"添加截图 {screenshot.name} 时出错: {e}")
    else:
        print(f"截图目录不存在: {SCREENSHOT_DIR}")

def run_recorded_script(script_path):
    """运行录制的脚本"""
    try:
        print(f"正在运行录制脚本: {script_path}")
        # 动态导入录制的脚本
        spec = importlib.util.spec_from_file_location("recorded_script", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 如果脚本中有run函数，直接运行
        if hasattr(module, 'run'):
            with sync_playwright() as playwright:
                try:
                    # 执行录制脚本
                    result = module.run(playwright)
                    
                    # 添加截图到报告
                    add_screenshots_to_report()
                    
                    return result
                except Exception as e:
                    allure.attach(
                        str(e),
                        name="执行错误",
                        attachment_type=AttachmentType.TEXT
                    )
                    raise
            return True
        else:
            print("未找到run函数")
        return False
    except Exception as e:
        print(f"运行录制脚本时出错: {e}")
        allure.attach(
            str(e),
            name="录制脚本执行错误",
            attachment_type=AttachmentType.TEXT
        )
        return False

def get_recorded_scripts():
    """获取所有录制脚本"""
    testcase_dir = ROOT_DIR / "Testcase"
    recorded_scripts = []
    
    # 遍历Testcase目录下的所有Python文件
    for file in testcase_dir.glob("test_*.py"):
        if file.name != "__init__.py":  # 排除__init__.py文件
            recorded_scripts.append(file)
    
    return recorded_scripts

class TestRecordedScripts:
    """测试录制脚本的测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前的准备工作"""
        # 确保报告目录存在
        os.makedirs(REPORT_DIR, exist_ok=True)
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        yield
        # 测试后的清理工作
        pass
    
    @pytest.mark.parametrize("script_path", get_recorded_scripts())
    def test_recorded_script(self, script_path):
        """测试录制脚本"""
        with allure.step(f"执行录制脚本 - {script_path.name}"):
            allure.dynamic.suite("手动执行测试套件")
            allure.dynamic.title(f"{script_path.name} 执行结果")
            allure.dynamic.description(f"脚本路径: {script_path}")
            
            # 执行录制脚本
            if run_recorded_script(script_path):
                print(f"{script_path.name} 执行成功")
                allure.attach(f"{script_path.name} 执行成功", name="执行结果", attachment_type=AttachmentType.TEXT)
            else:
                print(f"{script_path.name} 执行失败")
                allure.attach(f"{script_path.name} 执行失败", name="执行结果", attachment_type=AttachmentType.TEXT)
                pytest.fail(f"{script_path.name} 执行失败")

def run_tests():
    """运行测试用例并生成报告"""
    try:
        # 检查测试用例目录
        if not check_testcase_dir():
            sys.exit(1)

        # 创建时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 清理旧的报告
        clean_report_dir()
        
        print("开始执行测试用例...")
        print(f"测试用例目录: {ROOT_DIR / 'Testcase'}")
        start_time = time.time()
        
        # 切换到项目根目录
        os.chdir(ROOT_DIR)
        
        # 使用pytest-allure生成报告
        allure_results_dir = os.path.join(REPORT_DIR, "allure-results")
        print(f"\n运行测试用例，结果将保存到: {allure_results_dir}")
        
        # 运行pytest
        pytest.main([
            "-v",
            "--alluredir", allure_results_dir,
            "--clean-alluredir",
            __file__
        ])
        
        # 检查allure结果目录
        if os.path.exists(allure_results_dir):
            print(f"Allure结果目录已创建: {allure_results_dir}")
            print(f"目录内容: {os.listdir(allure_results_dir)}")
        else:
            print(f"警告: Allure结果目录未创建: {allure_results_dir}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n测试执行完成！")
        print(f"总耗时: {duration:.2f} 秒")
        print(f"测试报告位置: {os.path.abspath(REPORT_DIR)}")
        print("使用 'allure serve report/allure-results' 查看测试报告")
        
    except Exception as e:
        print(f"执行测试时出错: {e}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")
        allure.attach(
            traceback.format_exc(),
            name="测试执行错误",
            attachment_type=AttachmentType.TEXT
        )
        sys.exit(1)

if __name__ == "__main__":
    # 设置环境变量，确保Allure结果目录正确
    os.environ["ALLURE_RESULTS_DIR"] = os.path.join(REPORT_DIR, "allure-results")
    # 设置环境变量，确保截图目录正确
    os.environ["SCREENSHOT_DIR"] = str(SCREENSHOT_DIR)
    run_tests()

