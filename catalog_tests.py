import os

from datetime import datetime
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from helper.constants import SERVER_URL_BASE
from helper.desired_capabilities import get_desired_capabilities

BUNDLE_ID = 'com.example.apple-samplecode.UICatalog'

class TestCatalog(object):

    def setup_method(self):
        capabilities = get_desired_capabilities('UIKitCatalog.app')
        capabilities.update(
            {
                'bundleId': BUNDLE_ID,
                'nativeWebTap': True,
            }
        )
        self.driver = webdriver.Remote(SERVER_URL_BASE, options=AppiumOptions().load_capabilities(capabilities))

        # Fresh iOS 18.2 simulator may not show up the webview context with "safari"
        # after a fresh simlator instance creation.
        # Re-launch the process could be a workaround in my debugging.
        self.driver.activate_app(BUNDLE_ID)

    def teardown_method(self) -> None:
        self.driver.terminate_app(BUNDLE_ID)
        # self.driver.quit()

    def test_ui(self):
        element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'Buttons')
        element.click()
        # Create the output folder if it doesn't exist
        current_time = datetime.now()

        formatted_time = current_time.strftime("%d%m%Y%H%M")
        screenshot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), './output/screenshots'))
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        filename = os.path.join(screenshot_dir, f'test-{formatted_time}.png')
        self.driver.save_screenshot(filename)
        xml_source = self.driver.execute_script("mobile: source", {"format": "xml"})
        xml_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), './output/xmls'))
        if not os.path.exists(xml_dir):
            os.makedirs(xml_dir)
        xml_file = os.path.join(xml_dir, f'test-{formatted_time}.xml')
        with open(xml_file, 'w') as fd:
            fd.write(xml_source)
        print(xml_file)


if __name__ == '__main__':
    test = TestCatalog()
    test.setup_method()
    test.test_ui()
    test.teardown_method()



