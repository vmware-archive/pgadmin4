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

from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from regression.python_test_utils import test_utils as utils
from . import utils as tables_utils


class TestTableDelete:
    @pytest.mark.usefixtures('require_database_connection')
    def test_table_delete(self, context_of_tests):
        """
        When the table delete request is sent to the backend
        it returns 200 status
        """

        url = '/browser/table/obj/'

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
            raise Exception("Could not find the schema to delete a table.")

        table_name = "test_table_delete_%s" % (str(uuid.uuid4())[1:8])
        table_id = tables_utils.create_table(server, db_name,
                                             schema_name,
                                             table_name)

        table_response = tables_utils.verify_table(server, db_name,
                                                   table_id)
        if not table_response:
            raise Exception("Could not find the table to delete.")

        response = http_client.delete(url + str(utils.SERVER_GROUP) +
                                      '/' + str(server_id) + '/' +
                                      str(db_id) + '/' +
                                      str(schema_id) + '/' +
                                      str(table_id),
                                      follow_redirects=True)

        response.status_code | should.be.equal.to(200)
