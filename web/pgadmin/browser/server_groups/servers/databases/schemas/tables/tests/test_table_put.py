##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json
import uuid

import pytest
from grappa import should

from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.utils.base_test_generator import PostgresVersion
from regression.python_test_utils import test_utils as utils
from . import utils as tables_utils


class TestTablePut:
    def set_up(self, context_of_tests):
        self.url = '/browser/table/obj/'

        self.tester = context_of_tests['test_client']

        self.server = context_of_tests['server']
        self.server_data = context_of_tests['server_information']
        self.db_name = self.server_data['db_name']
        self.server_id = self.server_data['server_id']
        self.db_id = self.server_data['db_id']
        self.schema_id = self.server_data['schema_id']
        self.schema_name = self.server_data['schema_name']
        self.schema_response = schema_utils.verify_schemas(
            self.server,
            self.db_name,
            self.schema_name
        )

        if not self.schema_response:
            raise Exception("Could not find the schema to update table.")

        self.table_name = "test_table_put_%s" % (str(uuid.uuid4())[1:8])

    def set_up_partition_and_mode(self, partition_type,
                                  mode):

        self.table_id = tables_utils.create_table_for_partition(
            self.server,
            self.db_name,
            self.schema_name,
            self.table_name,
            'partitioned',
            partition_type)

        table_response = tables_utils.verify_table(self.server, self.db_name,
                                                   self.table_id)

        if not table_response:
            raise Exception("Could not find the table to update.")

        self.data = {"id": self.table_id}
        tables_utils.set_partition_data(
            self.server, self.db_name, self.schema_name, self.table_name,
            partition_type, self.data, mode)

    @pytest.mark.usefixtures('require_database_connection')
    def test_table_put(self, context_of_tests):
        """
        When the table put request is sent to the backend
        it returns 200 status
        """

        self.set_up(context_of_tests)

        self.table_id = tables_utils.create_table(
            self.server, self.db_name,
            self.schema_name,
            self.table_name)

        table_response = tables_utils.verify_table(self.server, self.db_name,
                                                   self.table_id)

        if not table_response:
            raise Exception("Could not find the table to update.")

        data = {
            "description": "This is test comment for table",
            "id": self.table_id
        }

        response = self.tester.put(
            self.url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' +
            str(self.db_id) + '/' +
            str(self.schema_id) + '/' +
            str(self.table_id),
            data=json.dumps(data), follow_redirects=True)

        response.status_code | should.be.equal.to(200)

    @pytest.mark.usefixtures('require_database_connection')
    @pytest.mark.parametrize(
        'partition_type, mode', [
            (
                'range',
                'create'
            ),
            (
                'list',
                'create'
            ),
            (
                'range',
                'detach'
            ),
            (
                'list',
                'detach'
            ),
            (
                'range',
                'attach'
            ),
            (
                'list',
                'attach'
            )
        ]
    )
    @pytest.mark.skip_if_postgres_version({'below_version':
                                           PostgresVersion.v10},
                                          "Event triggers are not supported "
                                          "by PG10 ")
    def test_table_put_partitioned(self,
                                   context_of_tests,
                                   partition_type,
                                   mode):
        """
        When the table put request is sent to
        a partition table
        it returns 200 status
        """

        self.set_up(context_of_tests)

        self.set_up_partition_and_mode(partition_type, mode)

        response = self.tester.put(
            self.url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' +
            str(self.db_id) + '/' +
            str(self.schema_id) + '/' +
            str(self.table_id),
            data=json.dumps(self.data), follow_redirects=True)

        response.status_code | should.be.equal.to(200)
