import allure
import pytest
from playwright.sync_api import Playwright, sync_playwright

from config.config import SCREENSHOT_DIR


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    """创建Playwright实例"""
    with sync_playwright() as p:
        yield p



@pytest.fixture(scope="function")
def auto_screenshot(page, request):
    """测试失败时自动截图"""
    yield
    if request.node.rep_call.failed:
        test_name = request.node.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = SCREENSHOT_DIR / f"{test_name}_{timestamp}.png"
        page.screenshot(path=str(screenshot_path))
        allure.attach.file(
            str(screenshot_path),
            name=f"失败截图_{test_name}",
            attachment_type=allure.attachment_type.PNG
        )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)