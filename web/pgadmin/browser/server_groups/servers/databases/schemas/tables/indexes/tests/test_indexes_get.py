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

from pgadmin.browser.server_groups.servers.databases.schemas.tables.column. \
    tests import utils as columns_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tables.tests \
    import utils as tables_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.utils.tests_helper import convert_response_to_json
from regression.python_test_utils import test_utils as utils
from . import utils as indexes_utils


class TestIndexesGet:
    @pytest.mark.usefixtures('require_database_connection')
    def test_index_get(self, context_of_tests):
        """
        When the index GET request is send to the backend
        it returns 200 status
        """
        http_client = context_of_tests['test_client']
        server = context_of_tests['server']
        server_data = context_of_tests['server_information']

        db_name = server_data["db_name"]
        server_id = server_data["server_id"]
        db_id = server_data["db_id"]
        schema_id = server_data["schema_id"]
        schema_name = server_data["schema_name"]
        schema_response = schema_utils.verify_schemas(server,
                                                      db_name,
                                                      schema_name)
        if not schema_response:
            raise Exception("Could not find the schema to add a table.")
        table_name = "table_column_%s" % (str(uuid.uuid4())[1:8])
        table_id = tables_utils.create_table(server,
                                             db_name,
                                             schema_name,
                                             table_name)
        column_name = "test_column_delete_%s" % (str(uuid.uuid4())[1:8])
        columns_utils.create_column(server,
                                    db_name,
                                    schema_name,
                                    table_name,
                                    column_name)
        index_name = "test_index_delete_%s" % (str(uuid.uuid4())[1:8])
        index_id = indexes_utils.create_index(server,
                                              db_name,
                                              schema_name,
                                              table_name,
                                              index_name,
                                              column_name)

        url = '/browser/index/obj/'
        response = http_client.get(
            "{0}{1}/{2}/{3}/{4}/{5}/{6}".format(url, utils.SERVER_GROUP,
                                                server_id, db_id,
                                                schema_id, table_id,
                                                index_id),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        json_response = convert_response_to_json(response)
        json_response | should.have.key('indnatts') > should.be.equal.to(1)
        json_response | should.have.key('conoid') > should.be.none
        json_response | should.have.key('indisprimary') > should.be.false
        json_response | should.have.key('cols')
        json_response | should.have.key('tabname') > should.be.equal.to(
            table_name)
        json_response | should.have.key('indkey') > should.be.equal.to('4')
        json_response | should.have.key('indisclustered') > should.be.false
        json_response | should.have.key('condeferred') > should.be.none
        json_response | should.have.key('amname') > should.be.equal.to('btree')
        json_response | should.have.key('contype') > should.be.none
        json_response | should.have.key('indrelid')
        json_response | should.have.key('oid')
        json_response | should.have.key('is_sys_idx') > should.be.false
        json_response | should.have.key('description') > should.be.none
        json_response | should.have.key('nspname') > should.be.equal.to(
            schema_name)
        json_response | should.have.key('condeferrable') > should.be.none
        json_response | should.have.key('spcname')
        json_response | should.have.key('name') > should.be.equal.to(
            index_name)
        json_response | should.have.key('indclass')
        json_response | should.have.key('indisvalid') > should.be.true
        json_response | should.have.key('indconstraint') > should.be.none
        json_response | should.have.key('indisunique') > should.be.false
        json_response | should.have.key('fillfactor') > should.be.none
        json_response | should.have.key('spcoid')

        json_response | should.have.key('columns') > should.have.length(1)
        json_response['columns'][0] | should.have.key('op_class') > should.be \
            .none
        json_response['columns'][0] | should.have.key('colname') > should.be \
            .equal.to(column_name)
        json_response['columns'][0] | should.have.key('collspcname')
