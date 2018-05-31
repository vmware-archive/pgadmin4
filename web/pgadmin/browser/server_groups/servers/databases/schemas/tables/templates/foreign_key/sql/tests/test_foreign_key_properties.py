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

from grappa import should

from pgadmin.utils.driver import DriverRegistry
from regression.python_test_utils.template_helper import file_as_template

DriverRegistry.load_drivers()
from regression.python_test_utils import test_utils

if sys.version_info[0] >= 3:
    long = int


class TestColumnForeignKeyGetConstraintCols:
    def test_column_foreign_keys(self, context_of_tests):
        """
        When there are no foreign key properties on the column
        it returns an empty result
        """

        server = context_of_tests['server']

        with test_utils.Database(server) as (connection, database_name):
            test_utils.create_table(server, database_name, "test_table")

            cursor = connection.cursor()
            cursor.execute("SELECT pg_class.oid as table_id, "
                           "pg_attribute.attnum as column_id "
                           "FROM pg_class join pg_attribute on "
                           "attrelid=pg_class.oid "
                           "where pg_class.relname='test_table'"
                           " and pg_attribute.attname = 'some_column'")
            table_id, column_id = cursor.fetchone()

            if connection.server_version < 90100:
                versions_to_test = 'default'
            else:
                versions_to_test = '9.1_plus'

            template_file = os.path.join(
                os.path.dirname(__file__), "..", versions_to_test,
                "properties.sql"
            )
            template = file_as_template(template_file)

            sql = template.render(
                tid=table_id,
                cid=column_id)

            cursor = connection.cursor()
            cursor.execute(sql)
            fetch_result = cursor.fetchall()

            fetch_result | should.have.length.of(0)
