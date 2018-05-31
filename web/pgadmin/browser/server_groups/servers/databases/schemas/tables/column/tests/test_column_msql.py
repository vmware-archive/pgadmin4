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

from pgadmin.browser.server_groups.servers.databases.schemas.tables.tests \
    import utils as tables_utils
from pgadmin.browser.server_groups.servers.databases.schemas.tests import \
    utils as schema_utils
from pgadmin.browser.server_groups.servers.databases.tests import utils as \
    database_utils
from regression import parent_node_dict
from regression.python_test_utils import test_utils as utils
from . import utils as columns_utils

try:
    from urllib.parse import urlencode
except ImportError as e:
    from urllib import urlencode


class TestColumGetMsql:
    """
    When the column get request is send to the backend
    for a msql column
    it returns 200 status,
    """
    @pytest.mark.parametrize(
        'data_type, expected_res,'
        'old_len, new_len, old_precision, new_precision', [
            (
                'timestamp(3) with time zone[]',
                'ALTER TABLE {schema}.{table}\n    ALTER COLUMN '
                '{column} TYPE timestamp({len}) with time zone [];',
                None,
                6,
                None,
                None,
            ),
            (
                'timestamp(4) with time zone',
                'ALTER TABLE {schema}.{table}\n    ALTER COLUMN '
                '{column} TYPE timestamp({len}) with time zone ;',
                None,
                7,
                None,
                None,
            ),
            (
                'numeric(5,2)[]',
                'ALTER TABLE {schema}.{table}\n    ALTER COLUMN '
                '{column} TYPE numeric ({len}, {precision})[];',
                5,
                None,
                None,
                4,
            ),
            (
                'numeric(6,3)',
                'ALTER TABLE {schema}.{table}\n    ALTER COLUMN '
                '{column} TYPE numeric ({len}, {precision});',
                6,
                None,
                None,
                5,
            ),
            (
                'numeric(6,3)[]',
                'ALTER TABLE {schema}.{table}\n    ALTER COLUMN '
                '{column} TYPE numeric ({len}, {precision})[];',
                None,
                8,
                3,
                None,
            ),
            (
                'numeric(6,4)',
                'ALTER TABLE {schema}.{table}\n    ALTER COLUMN '
                '{column} TYPE numeric ({len}, {precision});',
                None,
                8,
                4,
                None,
            ),
            (
                'numeric(10,5)[]',
                'ALTER TABLE {schema}.{table}\n    ALTER COLUMN '
                '{column} TYPE numeric ({len}, {precision})[];',
                None,
                15,
                None,
                8,
            ),
            (
                'numeric(12,6)',
                'ALTER TABLE {schema}.{table}\n    ALTER COLUMN '
                '{column} TYPE numeric ({len}, {precision});',
                None,
                14,
                None,
                9,
            )
        ]
    )
    def test_column_put(
        self,
        request,
        context_of_tests,
        data_type,
        expected_res,
        old_len,
        new_len,
        old_precision,
        new_precision
    ):
        request.addfinalizer(self.tearDown)

        url = '/browser/column/msql/'

        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']
        self.server_data = parent_node_dict['database'][-1]
        self.server_id = self.server_data['server_id']
        self.db_id = self.server_data['db_id']
        self.db_name = self.server_data['db_name']

        self.schema_info = parent_node_dict['schema'][-1]
        self.schema_name = self.schema_info['schema_name']
        self.schema_id = self.schema_info['schema_id']

        db_con = database_utils.connect_database(self,
                                                 utils.SERVER_GROUP,
                                                 self.server_id,
                                                 self.db_id)
        if not db_con["info"] == "Database connected.":
            raise Exception("Could not connect to database.")

        schema_response = schema_utils.verify_schemas(self.server,
                                                      self.db_name,
                                                      self.schema_name)
        if not schema_response:
            raise Exception("Could not find the schema.")

        self.table_name = "table_column_%s" % (str(uuid.uuid4())[1:8])
        self.table_id = tables_utils.create_table(self.server, self.db_name,
                                                  self.schema_name,
                                                  self.table_name)

        column_name = "test_column_get_msql_%s" % (str(uuid.uuid4())[1:8])
        column_id = columns_utils.create_column(self.server,
                                                self.db_name,
                                                self.schema_name,
                                                self.table_name,
                                                column_name,
                                                data_type)
        col_response = columns_utils.verify_column(self.server, self.db_name,
                                                   column_name)
        if not col_response:
            raise Exception("Could not find the column to update.")

        data = {"attnum": column_id}

        expected_len = None
        expected_precision = None

        if new_len is not None:
            data["attlen"] = new_len
            expected_len = new_len
        elif old_len is not None:
            expected_len = old_len

        if new_precision is not None:
            data["attprecision"] = new_precision
            expected_precision = new_precision
        elif old_precision is not None:
            expected_precision = old_precision

        response = self.tester.get(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' +
            str(self.db_id) + '/' +
            str(self.schema_id) + '/' +
            str(self.table_id) + '/' +
            str(column_id) + '?' +
            urlencode(data),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)
        response_data = json.loads(response.data.decode('utf-8'))
        response_data['data'] | should.be.equal.to(
            expected_res.format(
                **dict(
                    [('schema', self.schema_name),
                     ('table', self.table_name),
                     ('column', column_name),
                     ('len', expected_len),
                     ('precision', expected_precision)
                     ]
                )
            )
        )

    def tearDown(self):
        database_utils.client_disconnect_database(self.tester, self.server_id,
                                                  self.db_id)
