##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
from regression.feature_utils.base_feature_test import BaseFeatureTest
from regression.python_test_utils import test_utils


class TestTableDdl(BaseFeatureTest):
    def test_table_ddl(self, driver):
        self.driver = driver

        self.setUp()

        connection = test_utils.get_db_connection(
            self.server['db'],
            self.server['username'],
            self.server['db_password'],
            self.server['host'],
            self.server['port'],
            self.server['sslmode']
        )
        test_utils.drop_database(connection, "acceptance_test_db")

        test_utils.create_database(self.server, "acceptance_test_db")

        self.page.add_server(self.server)

        test_utils.create_table(
            self.server, "acceptance_test_db", "test_table")

        self.page.toggle_open_server(self.server['name'])
        self.page.toggle_open_tree_item('Databases')
        self.page.toggle_open_tree_item('acceptance_test_db')
        self.page.toggle_open_tree_item('Schemas')
        self.page.toggle_open_tree_item('public')
        self.page.toggle_open_tree_item('Tables')
        self.page.select_tree_item('test_table')
        self.page.click_tab("SQL")

        self.page.find_by_xpath(
            "//*[contains(@class,'CodeMirror-lines') and "
            "contains(.,'CREATE TABLE public.test_table')]")

        self.page.remove_server(self.server)
        connection = test_utils.get_db_connection(
            self.server['db'],
            self.server['username'],
            self.server['db_password'],
            self.server['host'],
            self.server['port'],
            self.server['sslmode']
        )
        test_utils.drop_database(connection, "acceptance_test_db")
