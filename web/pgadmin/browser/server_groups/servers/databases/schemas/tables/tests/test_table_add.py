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
from pgadmin.utils import server_utils as server_utils
from regression.python_test_utils import test_utils as utils


class TestTableAdd:
    def set_up(self, context_of_tests):
        self.tester = context_of_tests['test_client']
        self.server = context_of_tests['server']
        server_data = context_of_tests['server_information']

        db_name = server_data['db_name']
        self.server_id = server_data['server_id']
        self.db_id = server_data['db_id']
        self.schema_id = server_data['schema_id']
        schema_name = server_data['schema_name']
        self.server_id = server_data['server_id']
        schema_response = schema_utils.verify_schemas(self.server,
                                                      db_name,
                                                      schema_name)
        if not schema_response:
            raise Exception("Could not find the schema to add a table.")

        db_user = self.server["username"]
        table_name = "test_table_add_%s" % (str(uuid.uuid4())[1:8])
        self.data = {
            "check_constraint": [],
            "coll_inherits": "[]",
            "columns": [
                {
                    "name": "empno",
                    "cltype": "numeric",
                    "attacl": [],
                    "is_primary_key": False,
                    "attoptions": [],
                    "seclabels": []
                },
                {
                    "name": "empname",
                    "cltype": "character[]",
                    "attacl": [],
                    "is_primary_key": False,
                    "attoptions": [],
                    "seclabels": []
                },
                {"name": "DOJ",
                 "cltype": "date",
                 "attacl": [],
                 "is_primary_key": False,
                 "attoptions": [],
                 "seclabels": []
                 }
            ],
            "exclude_constraint": [],
            "fillfactor": "",
            "hastoasttable": True,
            "like_constraints": True,
            "like_default_value": True,
            "like_relation": "pg_catalog.pg_namespace",
            "name": table_name,
            "primary_key": [],
            "relacl": [
                {
                    "grantee": db_user,
                    "grantor": db_user,
                    "privileges":
                        [
                            {
                                "privilege_type": "a",
                                "privilege": True,
                                "with_grant": True
                            },
                            {
                                "privilege_type": "r",
                                "privilege": True,
                                "with_grant": False
                            },
                            {
                                "privilege_type": "w",
                                "privilege": True,
                                "with_grant": False
                            }
                        ]
                }
            ],
            "relhasoids": True,
            "relowner": db_user,
            "schema": schema_name,
            "seclabels": [],
            "spcname": "pg_default",
            "unique_constraint": [],
            "vacuum_table": [
                {
                    "name": "autovacuum_analyze_scale_factor"
                },
                {
                    "name": "autovacuum_analyze_threshold"
                },
                {
                    "name": "autovacuum_freeze_max_age"
                },
                {
                    "name": "autovacuum_vacuum_cost_delay"
                },
                {
                    "name": "autovacuum_vacuum_cost_limit"
                },
                {
                    "name": "autovacuum_vacuum_scale_factor"
                },
                {
                    "name": "autovacuum_vacuum_threshold"
                },
                {
                    "name": "autovacuum_freeze_min_age"
                },
                {
                    "name": "autovacuum_freeze_table_age"
                }
            ],
            "vacuum_toast": [
                {
                    "name": "autovacuum_freeze_max_age"
                },
                {
                    "name": "autovacuum_vacuum_cost_delay"
                },
                {
                    "name": "autovacuum_vacuum_cost_limit"
                },
                {
                    "name": "autovacuum_vacuum_scale_factor"
                },
                {
                    "name": "autovacuum_vacuum_threshold"
                },
                {
                    "name": "autovacuum_freeze_min_age"
                },
                {
                    "name": "autovacuum_freeze_table_age"
                }
            ]
        }

    @pytest.mark.usefixtures('require_database_connection')
    def test_table_add(self, context_of_tests):
        """
        When the table add request is sent to the backend
        it returns 200 status
        """

        url = '/browser/table/obj/'

        self.set_up(context_of_tests)

        response = self.tester.post(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(self.db_id) +
            '/' + str(self.schema_id) + '/',
            data=json.dumps(self.data),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)

    @pytest.mark.usefixtures('require_database_connection')
    def test_table_add_range_partitioned(self, context_of_tests):
        """
        When the range-partitioned table add request is sent to the backend
        it returns 200 status
        """

        url = '/browser/table/obj/'
        server_min_version = 100000
        partition_type = 'range'

        self.set_up(context_of_tests)

        server_con = server_utils.connect_server(self, self.server_id)
        server_con['info'] | \
            should.be.equal.to('Server connected.',
                               msg='Could not connect to server to add'
                               'partitioned table.')

        if server_con['data']['version'] < server_min_version:
            message = 'Partitioned table are not supported by ' \
                      'PPAS/PG 10.0 and below.'
            pytest.skip(message)

        self.data['partition_type'] = partition_type
        self.data['is_partitioned'] = True
        self.data['partitions'] = \
            [{'values_from': "'2010-01-01'",
              'values_to': "'2010-12-31'",
              'is_attach': False,
              'partition_name': 'emp_2010'
              },
             {'values_from': "'2011-01-01'",
              'values_to': "'2011-12-31'",
              'is_attach': False,
              'partition_name': 'emp_2011'
              }]

        self.data['partition_keys'] = \
            [{'key_type': 'column', 'pt_column': 'DOJ'}]

        response = self.tester.post(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(self.db_id) +
            '/' + str(self.schema_id) + '/',
            data=json.dumps(self.data),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)

    @pytest.mark.usefixtures('require_database_connection')
    def test_table_add_list_partitioned(self, context_of_tests):
        """
        When the list-partitioned table add request is sent to the backend
        it returns 200 status
        """

        url = '/browser/table/obj/'
        server_min_version = 100000
        partition_type = 'list'

        self.set_up(context_of_tests)

        server_con = server_utils.connect_server(self, self.server_id)
        server_con['info'] | \
            should.be.equal.to('Server connected.',
                               msg='Could not connect to server to add'
                                   'partitioned table.')

        if server_con['data']['version'] < server_min_version:
            message = 'Partitioned table are not supported by ' \
                      'PPAS/PG 10.0 and below.'
            pytest.skip(message)

        self.data['partition_type'] = partition_type
        self.data['is_partitioned'] = True
        self.data['partitions'] = \
            [{'values_in': "'2012-01-01', '2012-12-31'",
              'is_attach': False,
              'partition_name': 'emp_2012'
              },
             {'values_in': "'2013-01-01', '2013-12-31'",
              'is_attach': False,
              'partition_name': 'emp_2013'
              }]

        self.data['partition_keys'] = \
            [{'key_type': 'column', 'pt_column': 'DOJ'}]

        response = self.tester.post(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id) + '/' + str(self.db_id) +
            '/' + str(self.schema_id) + '/',
            data=json.dumps(self.data),
            content_type='html/json')

        response.status_code | should.be.equal.to(200)
