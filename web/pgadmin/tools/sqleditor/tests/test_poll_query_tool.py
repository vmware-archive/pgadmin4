##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json

from grappa import should

from pgadmin.browser.server_groups.servers.databases.tests import utils as \
    database_utils
from regression.python_test_utils import test_utils as utils


class TestPollQueryTool:
    def test_poll_and_have_2_notices(self, context_of_tests):
        """
        When query tool poll to check on the query with 2 notices
        It returns messages saying polling is checking
        """
        database_info = context_of_tests["server_information"]
        server_id = database_info["server_id"]
        db_id = database_info["db_id"]

        http_client = context_of_tests['test_client']
        server = context_of_tests['server']

        db_con = database_utils.client_connect_database(
            http_client,
            utils.SERVER_GROUP,
            server_id,
            db_id,
            server['db_password'])
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to the database.")

        url = '/datagrid/initialize/query_tool/{0}/{1}/{2}'.format(
            utils.SERVER_GROUP, server_id, db_id)
        response = http_client.post(url)
        response.status_code | should.be.equal(200)

        response_data = json.loads(response.data.decode('utf-8'))
        trans_id = response_data['data']['gridTransId']

        sql = """
DROP TABLE IF EXISTS test_for_notices;

DO $$
BEGIN
    RAISE NOTICE 'Hello, world!';
END $$;

SELECT 'CHECKING POLLING';
"""
        expected_message = """NOTICE:  table "test_for_notices" does not exist, skipping
NOTICE:  Hello, world!
"""
        expected_result = 'CHECKING POLLING'

        url = '/sqleditor/query_tool/start/{0}'.format(trans_id)
        response = http_client.post(url, data=json.dumps({"sql": sql}),
                                    content_type='html/json')

        response.status_code | should.be.equal(200)

        url = '/sqleditor/poll/{0}'.format(trans_id)
        response = http_client.get(url)
        response.status_code | should.be.equal(200)

        response_data = json.loads(response.data.decode('utf-8'))

        response_data['data']['additional_messages'] | should.be.equal(
            expected_message
        )

        expected_result | should.be.equal(
            response_data['data']['result'][0][0])

        database_utils.client_disconnect_database(http_client, server_id,
                                                  db_id)

    def test_poll_and_have_1000_notices(self, context_of_tests):
        """
        When query tool poll to check on the query with 1000 notices
        It returns messages saying polling is checking for long messages
        """
        database_info = context_of_tests["server_information"]
        server_id = database_info["server_id"]
        db_id = database_info["db_id"]

        http_client = context_of_tests['test_client']
        server = context_of_tests['server']

        db_con = database_utils.client_connect_database(
            http_client,
            utils.SERVER_GROUP,
            server_id,
            db_id,
            server['db_password'])
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to the database.")

        url = '/datagrid/initialize/query_tool/{0}/{1}/{2}'.format(
            utils.SERVER_GROUP, server_id, db_id)
        response = http_client.post(url)
        response.status_code | should.be.equal(200)

        response_data = json.loads(response.data.decode('utf-8'))
        trans_id = response_data['data']['gridTransId']

        sql = """
DO $$
BEGIN
    FOR i in 1..1000 LOOP
        RAISE NOTICE 'Count is %', i;
    END LOOP;
END $$;

SELECT 'CHECKING POLLING FOR LONG MESSAGES';
"""
        expected_message = "\n".join(["NOTICE:  Count is {0}".format(i)
                                      for i in range(1, 1001)]) + "\n"
        expected_result = 'CHECKING POLLING FOR LONG MESSAGES'

        url = '/sqleditor/query_tool/start/{0}'.format(trans_id)
        response = http_client.post(url, data=json.dumps({"sql": sql}),
                                    content_type='html/json')

        response.status_code | should.be.equal(200)

        url = '/sqleditor/poll/{0}'.format(trans_id)
        response = http_client.get(url)
        response.status_code | should.be.equal(200)

        response_data = json.loads(response.data.decode('utf-8'))

        response_data['data']['additional_messages'] | should.be.equal(
            expected_message
        )

        expected_result | should.be.equal(
            response_data['data']['result'][0][0])

        database_utils.client_disconnect_database(http_client, server_id,
                                                  db_id)

    def test_poll_and_have_no_notices(self, context_of_tests):
        """
        When query tool poll to check on the query with no notices
        It returns messages saying polling is checking without messages
        """
        database_info = context_of_tests["server_information"]
        server_id = database_info["server_id"]
        db_id = database_info["db_id"]

        http_client = context_of_tests['test_client']
        server = context_of_tests['server']

        db_con = database_utils.client_connect_database(
            http_client,
            utils.SERVER_GROUP,
            server_id,
            db_id,
            server['db_password'])
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to the database.")

        url = '/datagrid/initialize/query_tool/{0}/{1}/{2}'.format(
            utils.SERVER_GROUP, server_id, db_id)
        response = http_client.post(url)
        response.status_code | should.be.equal(200)

        response_data = json.loads(response.data.decode('utf-8'))
        trans_id = response_data['data']['gridTransId']

        sql = "SELECT 'CHECKING POLLING WITHOUT MESSAGES';"
        expected_result = 'CHECKING POLLING WITHOUT MESSAGES'

        url = '/sqleditor/query_tool/start/{0}'.format(trans_id)
        response = http_client.post(url, data=json.dumps({"sql": sql}),
                                    content_type='html/json')

        response.status_code | should.be.equal(200)

        url = '/sqleditor/poll/{0}'.format(trans_id)
        response = http_client.get(url)
        response.status_code | should.be.equal(200)

        response_data = json.loads(response.data.decode('utf-8'))

        response_data['data']['additional_messages'] | should.be.none

        expected_result | should.be.equal(
            response_data['data']['result'][0][0])

        database_utils.client_disconnect_database(http_client, server_id,
                                                  db_id)
