##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import uuid

import pytest
from grappa import should

from pgadmin.browser.server_groups.servers.databases.schemas.functions.tests \
    import utils as trigger_funcs_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tables.tests \
    import utils as tables_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from regression.python_test_utils import test_utils as utils
from . import utils as triggers_utils


@pytest.mark.skip_databases(['gpdb'])
class TestTriggersGet:

    @pytest.mark.usefixtures('require_database_connection')
    def test_trigger_get(self, context_of_tests):
        """
        When sending get request to trigger endpoint
        it returns 200 status
        """

        url = '/browser/trigger/obj/'
        http_client = context_of_tests['test_client']
        server = context_of_tests['server']
        server_data = context_of_tests['server_information']

        db_name = server_data['db_name']
        server_id = server_data['server_id']
        db_id = server_data['db_id']
        schema_id = server_data['schema_id']
        schema_name = server_data['schema_name']

        schema_response = schema_utils.verify_schemas(server,
                                                      db_name,
                                                      schema_name)
        if not schema_response:
            raise Exception("Could not find the schema to add a trigger.")
        table_name = "table_trigger_%s" % (str(uuid.uuid4())[1:8])
        table_id = tables_utils.create_table(server, db_name,
                                             schema_name,
                                             table_name)
        func_name = "trigger_func_add_%s" % str(uuid.uuid4())[1:8]
        trigger_funcs_utils.create_trigger_function_with_trigger(
            server, db_name, schema_name, func_name)

        trigger_name = "test_trigger_add_%s" % (str(uuid.uuid4())[1:8])
        trigger_id = triggers_utils.create_trigger(server,
                                                   db_name,
                                                   schema_name,
                                                   table_name,
                                                   trigger_name,
                                                   func_name)
        response = http_client.get(
            "{0}{1}/{2}/{3}/{4}/{5}/{6}".format(url, utils.SERVER_GROUP,
                                                server_id, db_id,
                                                schema_id, table_id,
                                                trigger_id),
            follow_redirects=True
        )

        response.status_code | should.equal(200)
