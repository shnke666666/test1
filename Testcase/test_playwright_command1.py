import re

import allure
from playwright.sync_api import Playwright, expect


@allure.feature("综合媒体模块")  # 功能模块
@allure.story("正常登录流程")  # 用户故事
@allure.severity(allure.severity_level.CRITICAL)  # 优先级
def run(playwright: Playwright):
    browser = playwright.chromium.launch(channel="chrome", headless=False, args=['--start-maximized'])
    context = browser.new_context(
        no_viewport=True  # 禁用窗口大小
    )
    page = context.new_page()
    page.goto("https://gscm.gzyyrj.cn/")
    page.goto("https://gscm.gzyyrj.cn/#/")
    page.goto("https://gscm.gzyyrj.cn/#/login?redirect=/&params={}")
    page.get_by_placeholder("请输入用户名").click()
    page.get_by_placeholder("请输入用户名").fill("admin")
    page.get_by_placeholder("请输入用户名").press("Tab")
    page.get_by_placeholder("请输入密码").fill("123456")
    page.get_by_placeholder("请输入密码").press("Enter")
    page.get_by_text("资源管理", exact=True).click()
    page.locator("div").filter(has_text=re.compile(r"^媒体信息$")).click()
    page.get_by_text("大牌资源管理").click()
    page.get_by_role("button", name="展开").click()
    page.locator("div:nth-child(10) > .el-form-item > .el-form-item__content > .el-select > .select-trigger > .el-select__tags > .el-select__input").click()
    page.locator("li").filter(has_text="已建设").click()
    page.get_by_role("button", name="查询").click()
    jianshe = page.get_by_role("row", name="1 YW-L001 云梧 楼顶牌（L） K114+300-").get_by_role("paragraph").first  #列表第一行数据的建设状态
    expect(jianshe).to_have_text('已建设')   #断言
    page.goto("https://gscm.gzyyrj.cn/#/resourceManagement/brandManagement/index")
    page.close()

    # ---------------------
    context.close()
    browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
