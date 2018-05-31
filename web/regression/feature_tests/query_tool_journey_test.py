##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import pyperclip
from grappa import should
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from regression.feature_utils.base_feature_test import BaseFeatureTest
from regression.python_test_utils import test_utils


class TestQueryToolJourney(BaseFeatureTest):
    def test_table_ddl(self, driver):
        """
        Tests the path through the query tool
        """
        self.driver = driver

        self.setUp()

        connection = test_utils.get_db_connection(
            self.server['db'],
            self.server['username'],
            self.server['db_password'],
            self.server['host'],
            self.server['port']
        )
        test_utils.drop_database(connection, "acceptance_test_db")
        test_utils.create_database(self.server, "acceptance_test_db")
        test_utils.create_table(
            self.server, "acceptance_test_db", "test_table")
        self.page.add_server(self.server)

        self._navigate_to_query_tool()

        self._execute_query(
            "SELECT * FROM test_table ORDER BY value"
        )

        self._test_copies_rows()
        self._test_copies_columns()
        self._test_history_tab()

        self.page.close_query_tool()
        self.page.remove_server(self.server)

        connection = test_utils.get_db_connection(self.server['db'],
                                                  self.server['username'],
                                                  self.server['db_password'],
                                                  self.server['host'],
                                                  self.server['port'])
        test_utils.drop_database(connection, "acceptance_test_db")

    def _test_copies_rows(self):
        pyperclip.copy("old clipboard contents")
        self.page.driver.switch_to.default_content()
        self.page.driver.switch_to_frame(
            self.page.driver.find_element_by_tag_name("iframe"))
        self.page.find_by_xpath(
            "//*[contains(@class, 'slick-row')]/*[1]").click()
        self.page.find_by_xpath("//*[@id='btn-copy-row']").click()

        pyperclip.paste() | should.equal('"Some-Name"\t"6"\t"some info"')

    def _test_copies_columns(self):
        pyperclip.copy("old clipboard contents")

        self.page.driver.switch_to.default_content()
        self.page.driver.switch_to_frame(
            self.page.driver.find_element_by_tag_name("iframe"))
        self.page.find_by_xpath(
            "//*[@data-test='output-column-header' and "
            "contains(., 'some_column')]"
        ).click()
        self.page.find_by_xpath("//*[@id='btn-copy-row']").click()

        pyperclip.paste() | should.contain('"Some-Name"')
        pyperclip.paste() | should.contain('"Some-Other-Name"')
        pyperclip.paste() | should.contain('"Yet-Another-Name"')

    def _test_history_tab(self):
        self.__clear_query_tool()
        editor_input = self.page.find_by_id("output-panel")
        self.page.click_element(editor_input)
        self._execute_query("SELECT * FROM table_that_doesnt_exist")

        self.page.click_tab("Query History")
        selected_history_entry = self.page.find_by_css_selector(
            "#query_list .selected")
        selected_history_entry.text | should.contain(
            "SELECT * FROM table_that_doesnt_exist")
        failed_history_detail_pane = self.page.find_by_id("query_detail")

        failed_history_detail_pane.text | should.contain(
            "Error Message relation \"table_that_doesnt_exist\" "
            "does not exist")
        ActionChains(self.page.driver) \
            .send_keys(Keys.ARROW_DOWN) \
            .perform()
        selected_history_entry = self.page.find_by_css_selector(
            "#query_list .selected")
        selected_history_entry.text | should.contain(
            "SELECT * FROM test_table ORDER BY value")
        selected_history_detail_pane = self.page.find_by_id("query_detail")
        selected_history_detail_pane.text | should.contain(
            "SELECT * FROM test_table ORDER BY value")
        newly_selected_history_entry = self.page.find_by_xpath(
            "//*[@id='query_list']/ul/li[2]")
        self.page.click_element(newly_selected_history_entry)
        selected_history_detail_pane = self.page.find_by_id("query_detail")
        selected_history_detail_pane.text | should.contain(
            "SELECT * FROM table_that_doesnt_exist")

        self.__clear_query_tool()

        self.page.click_element(editor_input)

        self.page.fill_codemirror_area_with("SELECT * FROM hats")
        for _ in range(15):
            self.page.find_by_id("btn-flash").click()
            self.page.wait_for_query_tool_loading_indicator_to_disappear()

        self.page.click_tab("Query History")

        query_we_need_to_scroll_to = self.page.find_by_xpath(
            "//*[@id='query_list']/ul/li[17]")

        self.page.click_element(query_we_need_to_scroll_to)

        for _ in range(17):
            ActionChains(self.page.driver) \
                .send_keys(Keys.ARROW_DOWN) \
                .perform()

        self._assert_clickable(query_we_need_to_scroll_to)

        self.__clear_query_tool()
        self.page.click_element(editor_input)
        self.page.fill_codemirror_area_with("SELECT * FROM hats")
        for _ in range(15):
            self.page.find_by_id("btn-flash").click()
            self.page.wait_for_query_tool_loading_indicator_to_disappear()

        self.page.click_tab("History")
        query_we_need_to_scroll_to = self.page.find_by_xpath(
            "//*[@id='query_list']/ul/li[17]"
        )
        for _ in range(17):
            ActionChains(self.page.driver) \
                .send_keys(Keys.ARROW_DOWN) \
                .perform()
        self._assert_clickable(query_we_need_to_scroll_to)

    def __clear_query_tool(self):
        self.page.click_element(
            self.page.find_by_xpath("//*[@id='btn-clear-dropdown']")
        )
        ActionChains(self.driver) \
            .move_to_element(self.page.find_by_xpath("//*[@id='btn-clear']")) \
            .perform()
        self.page.click_element(
            self.page.find_by_xpath("//*[@id='btn-clear']")
        )
        self.page.click_modal('Yes')

    def _navigate_to_query_tool(self):
        self.page.toggle_open_tree_item(self.server['name'])
        self.page.toggle_open_tree_item('Databases')
        self.page.toggle_open_tree_item('acceptance_test_db')
        self.page.open_query_tool()

    def _execute_query(self, query):
        self.page.fill_codemirror_area_with(query)
        self.page.find_by_id("btn-flash").click()

    def _assert_clickable(self, element):
        self.page.click_element(element)
