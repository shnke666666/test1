import os

import allure
from playwright.sync_api import Playwright


@allure.feature("综合媒体模块")  # 功能模块
@allure.story("正常登录流程")  # 用户故事
@allure.severity(allure.severity_level.CRITICAL)  # 优先级
def run( playwright: Playwright):
    browser = playwright.chromium.launch(channel="chrome", headless=False)  # slow_mo:慢动作模式，用于调试模式   , slow_mo=1000
    context = browser.new_context(
        # record_har_path="debug.har"  # 保存调试追踪,page.pause()开启调试模式后可见效果
    )
    page = context.new_page()
    # page.pause()  # 开启调试模式
    page.goto("https://gscm.gzyyrj.cn/")
    page.goto("https://gscm.gzyyrj.cn/#/")
    page.goto("https://gscm.gzyyrj.cn/#/login?redirect=/&params={}")
    page.get_by_placeholder("请输入用户名").click()
    page.get_by_placeholder("请输入用户名").fill("admin")
    page.screenshot(path=os.path.join(os.environ["SCREENSHOT_DIR"], "1.png"), full_page=True)   #截图
    page.get_by_placeholder("请输入用户名").press("Tab")
    page.get_by_placeholder("请输入密码").fill("123456")
    page.screenshot(path=os.path.join(os.environ["SCREENSHOT_DIR"], "2.png"), full_page=True)  # 截图
    page.get_by_role("button", name="登 录").click()
    page.get_by_text("资源管理", exact=True).click()
    page.get_by_text("媒体信息").click()
    page.screenshot(path=os.path.join(os.environ["SCREENSHOT_DIR"], "3.png"), full_page=True)  # 截图
    page.get_by_text("综合媒体管理").click()
    page.get_by_role("button", name="展开").click()
    page.locator(".el-input__suffix-inner > .el-icon > svg").first.click()
    page.locator("li").filter(has_text="包亭").click()
    page.get_by_role("button", name="查询").click()
    page.goto("https://gscm.gzyyrj.cn/#/resourceManagement/mediaInfo/comprehensive/index")
    page.close()

    # ---------------------
    context.close()
    browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
