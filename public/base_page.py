import os
import time

import allure
from playwright.sync_api import Page

from config.config import SCREENSHOT_DIR


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def take_screenshot(self, name: str):
        print("开始截图")
        """截图并添加到allure报告"""
        # 确保截图目录存在
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

        # 生成截图文件名
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{name}.png")

        # 截图
        self.page.screenshot(path=screenshot_path, full_page=True)

        #生成时间戳
        now = time.strftime("%Y-%m-%d-%H_%M_%S")

        # 添加到allure报告
        allure.attach.file(
            screenshot_path,
            name=name + str(now),
            attachment_type=allure.attachment_type.PNG
        )

    def navigate(self, url: str):
        """导航到指定URL"""
        self.page.goto(url)
        self.take_screenshot(f"navigate_to_{url}")

    def click(self, selector: str):
        """点击元素"""
        self.page.click(selector)
        self.take_screenshot(f"click_{selector}")

    def dblclick(self, selector: str):
        """鼠标双击"""
        self.page.dblclick(selector)
        self.take_screenshot(f"dblclick_{selector}")

    def click_ringht(self, selector: str):
        """鼠标右击"""
        self.page.click(selector, button='right')
        self.take_screenshot(f"click_right_{selector}")

    def fill(self, selector: str, value: str):
        """填充输入框"""
        self.page.fill(selector, value)
        self.take_screenshot(f"fill_{selector}")

    def wait_for_selector(self, selector: str, timeout: int = 5000):
        """等待元素出现"""
        self.page.wait_for_selector(selector, timeout=timeout)
