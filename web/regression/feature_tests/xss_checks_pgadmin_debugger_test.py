##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
import pytest
from grappa import should
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from regression.feature_utils.base_feature_test import BaseFeatureTest
from regression.python_test_utils import test_utils


class TestCheckDebuggerForXss(BaseFeatureTest):
    def test_check_debugger_for_xss(self, driver):
        """
        Tests to check if Debugger is vulnerable to XSS.
        """
        self.driver = driver

        self.setUp()

        with test_utils.Database(self.server) as (connection, _):
            if connection.server_version < 90100:
                pytest.skip(
                    "Functions tree node is not present in pgAdmin below "
                    "PG v9.1"
                )

        # Some test function is needed for debugger
        test_utils.create_debug_function(
            self.server, "postgres", "a_test_function"
        )

        self.page.wait_for_spinner_to_disappear()
        self.page.add_server(self.server)
        self._function_node_expandable()
        self._debug_function()

        self.page.remove_server(self.server)
        test_utils.drop_debug_function(self.server, "postgres",
                                       "a_test_function")

    def _function_node_expandable(self):
        self.page.toggle_open_server(self.server['name'])
        self.page.toggle_open_tree_item('Databases')
        self.page.toggle_open_tree_item('postgres')
        self.page.toggle_open_tree_item('Schemas')
        self.page.toggle_open_tree_item('public')
        self.page.toggle_open_tree_item('Functions')
        self.page.select_tree_item("a_test_function()")

    def _debug_function(self):
        self.page.driver.find_element_by_link_text("Object").click()
        ActionChains(
            self.page.driver
        ).move_to_element(
            self.page.driver.find_element_by_link_text("Debugging")
        ).perform()
        self.page.driver.find_element_by_link_text("Debug").click()

        # We need to check if debugger plugin is installed or not
        try:
            wait = WebDriverWait(self.page.driver, 2)
            is_error = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'alertify') and "
                           "not(contains(@class, 'ajs-hidden'))]//div["
                           "contains(@class,'ajs-header')]")
            ))

        except TimeoutException as e:
            is_error = None

        # If debugger plugin is not found
        if is_error and is_error.text == "Debugger Error":
            self.page.click_modal('OK')
            pytest.skip(
                "Please make sure that debugger plugin is properly configured"
            )
        else:
            self.page.driver.switch_to.frame(
                self.page.driver.find_element_by_tag_name('iframe')
            )

            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(.,'Hello, pgAdmin4')]"))
            )
            self.page.click_element(
                self.page.driver.find_elements_by_xpath("//button")[2]
            )

            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//td[contains(@class,'test_function') and "
                           "contains(.,'Hello, pgAdmin4')]"))
            )

            # Only this tab is vulnerable rest are BackGrid & Code Mirror
            # control which are already tested in Query tool test case
            self.page.click_tab("Messages")
            source_code = self.page.find_by_xpath(
                "//*[@id='messages']"
            ).get_attribute('innerHTML')

            escaped_characters = \
                'NOTICE:  &lt;img src="x" onerror="console.log(1)"&gt;'
            source_code | should.contain(
                escaped_characters,
                msg="Debugger might be vulnerable to XSS "
            )

            self._close_debugger()

    def _close_debugger(self):
        self.page.driver.switch_to_default_content()
        self.page.click_element(
            self.page.find_by_xpath(
                "//*[@id='dockerContainer']/div/div[3]/div/div[2]/div[1]")
        )
