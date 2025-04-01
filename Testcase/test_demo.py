import allure
from playwright.sync_api import Playwright


@allure.feature("综合媒体模块")  # 功能模块
@allure.story("正常登录流程")  # 用户故事
@allure.severity(allure.severity_level.CRITICAL)  # 优先级
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    context = browser.new_context()
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
    page.get_by_text("媒体信息").click()
    page.get_by_text("大牌资源管理").click()
    page.get_by_role("button", name="展开").click()
    page.locator("div:nth-child(5) > .el-form-item > .el-form-item__content > .el-select > .select-trigger > .el-select__tags > .el-select__input").click()
    page.get_by_text("龙门架（K）").click()
    page.locator("div:nth-child(5) > .el-form-item > .el-form-item__content > .el-select > .select-trigger > .el-select__tags > .el-select__input").click()
    page.get_by_role("button", name="查询").click()
    page.goto("https://gscm.gzyyrj.cn/#/resourceManagement/brandManagement/index")
    page.close()

    # ---------------------
    context.close()
    browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
