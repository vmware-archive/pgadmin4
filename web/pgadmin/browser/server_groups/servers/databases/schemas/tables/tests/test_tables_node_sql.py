##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import os
import sys

import pytest
from grappa import should

from regression.python_test_utils import test_utils
from regression.python_test_utils.template_helper import file_as_template

if sys.version_info[0] >= 3:
    long = int


@pytest.mark.database
class TestTablesNodeSql:
    def test_retrieval_of_all_table_node(self, context_of_tests):
        """
        When all parameters are present
        It executes a query in the database to retrieve all table names
        """
        server = context_of_tests['server']

        with test_utils.Database(server) as (connection, database_name):
            test_utils.create_table(server, database_name, 'test_table')

            if connection.server_version < 90100:
                versions_to_test = ['default']
            else:
                versions_to_test = ['9.1_plus']

            for version in versions_to_test:
                template_file = self.get_template_file(
                    version,
                    'nodes.sql')
                template = file_as_template(template_file)
                public_schema_id = 2200
                sql = template.render(scid=public_schema_id)

                cursor = connection.cursor()
                cursor.execute(sql)
                fetch_result = cursor.fetchall()

                first_row = {}
                for index, description in enumerate(cursor.description):
                    first_row[description.name] = fetch_result[0][index]

                oid = first_row['oid']
                name = first_row['name']
                triggercount = first_row['triggercount']
                has_enable_triggers = first_row['has_enable_triggers']

                long(oid) | should.not_be.none
                name | should.be.equal.to('test_table')
                # triggercount is sometimes returned as a
                # string for some reason
                long(triggercount) | should.be.equal.to(0)
                long(has_enable_triggers) | should.not_be.none

    @staticmethod
    def get_template_file(version, filename):
        return os.path.join(
            os.path.dirname(__file__), '..', 'templates', 'table', 'sql',
            version, filename
        )
