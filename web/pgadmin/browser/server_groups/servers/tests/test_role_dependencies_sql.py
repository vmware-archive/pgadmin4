##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
import os

from grappa import should

from regression.python_test_utils import test_utils
from regression.python_test_utils.template_helper import file_as_template


class TestRoleDependenciesSql:
    def test_role_dependencies(self, request, context_of_tests):
        """
        It verifies the role dependencies sql file
        """
        request.addfinalizer(self.tearDown)

        self.server = context_of_tests['server']

        with test_utils.Database(self.server) \
                as (connection, database_name):
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "CREATE ROLE testpgadmin LOGIN PASSWORD '%s'"
                    % self.server['db_password'])
            except Exception as exception:
                print(exception)
            connection.commit()

        server_with_modified_user = self.server.copy()
        server_with_modified_user['username'] = "testpgadmin"

        with test_utils.Database(self.server) \
                as (connection, database_name):
            test_utils.create_table(
                server_with_modified_user,
                database_name,
                "test_new_role_table"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT pg_class.oid AS table_id "
                           "FROM pg_class "
                           "WHERE pg_class.relname='test_new_role_table'")
            table_id = cursor.fetchone()[0]

            template_file = os.path.join(
                os.path.dirname(__file__),
                "..",
                "templates",
                "depends",
                "sql",
                'default',
                'role_dependencies.sql')
            template = file_as_template(template_file)
            sql = template.render(
                where_clause="WHERE dep.objid=%s::oid" % table_id)

            cursor.execute(sql)

            fetch_result = cursor.fetchall()

            fetch_result | should.have.length.of(1)

            first_row = {}
            for index, description in enumerate(cursor.description):
                first_row[description.name] = fetch_result[0][index]

            first_row['deptype'] | should.equal('o')

    def tearDown(self):
        with test_utils.Database(self.server) as (connection, database_name):
            cursor = connection.cursor()
            cursor.execute("DROP ROLE testpgadmin")
            connection.commit()
