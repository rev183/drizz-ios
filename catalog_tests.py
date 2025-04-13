import os

from datetime import datetime
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from constants import SERVER_URL_BASE
from helper.desired_capabilities import get_desired_capabilities
from openai_helper import generate_steps, find_element_in_xml
from steps import AppiumPlan

BUNDLE_ID = 'com.example.apple-samplecode.UICatalog'

class TestCatalog(object):

    def setup_method(self):
        capabilities = get_desired_capabilities('UIKitCatalog.app')
        capabilities.update(
            {
                'bundleId': BUNDLE_ID,
                'nativeWebTap': True,
                'no_reset': True,
                'full_context': True
            }
        )
        self.driver = webdriver.Remote(SERVER_URL_BASE, options=AppiumOptions().load_capabilities(capabilities))

        # Fresh iOS 18.2 simulator may not show up the webview context with "safari"
        # after a fresh simlator instance creation.
        # Re-launch the process could be a workaround in my debugging.
        self.driver.activate_app(BUNDLE_ID)

    def teardown_method(self) -> None:
        self.driver.terminate_app(BUNDLE_ID)
        print(f'Testing done')
        # self.driver.quit()

    def perform_steps(self, plan: AppiumPlan):
        formatted_time = datetime.now().strftime("%d%m%Y%H%M")
        plan_id = f'plan-{formatted_time}'
        plan_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), f'./output/{plan_id}'))
        if not os.path.exists(plan_dir):
            os.makedirs(plan_dir)
        for index, step in enumerate(plan.steps):
            if (step.action == 'navigate' or step.action == 'tap') and len(step.inputs) > 0:
                xml_source = self.driver.execute_script("mobile: source", {"format": "xml"})
                out = find_element_in_xml(xml_source, step)
                element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, out)
                print(f'Step {index} element desc - {out}')
                print(f'Element found: {element}')
                element.click()
            elif step.action == 'screenshot':
                filename = os.path.join(plan_dir, f'ss-step-{index}.png')
                self.driver.save_screenshot(filename)
            else:
                print(f'Can\'t handle step: {step}')

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
    appium_plan = generate_steps(
        """
        1. go to toolbars screen
        2. Click on button
        3. take screenshot
        """
    )
    test = TestCatalog()
    test.setup_method()
    test.perform_steps(appium_plan)
    # for i, step in enumerate(appium_plan.steps):
    #     if len(step.inputs) > 0:
    #       element = find_element_in_xml(xml_example, step)
    #       print(f'Step {i} - {element}')

