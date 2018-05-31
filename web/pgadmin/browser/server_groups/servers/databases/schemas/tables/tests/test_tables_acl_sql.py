##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import os

import pytest
from grappa import should

from regression.python_test_utils import test_utils
from regression.python_test_utils.template_helper import file_as_template


@pytest.mark.database
class TestTablesAclSql:
    def test_execute_acl_sql(self, context_of_tests):
        """
        When all parameters are present
        It executes the query that retrieves the ACL for a table
        """
        server = context_of_tests['server']
        with test_utils.Database(server) as (connection, database_name):
            test_utils.create_table(server, database_name, 'test_table')

            if connection.server_version < 90100:
                versions_to_test = ['default']
            else:
                versions_to_test = ['9.1_plus']

            cursor = connection.cursor()
            cursor.execute('GRANT SELECT ON test_table TO PUBLIC')
            cursor = connection.cursor()
            cursor.execute(
                'SELECT oid FROM pg_class WHERE relname=\'test_table\'')
            table_id = cursor.fetchone()[0]

            for version in versions_to_test:
                template_file = self.get_template_file(version, 'acl.sql')
                template = file_as_template(template_file)
                public_schema_id = 2200
                sql = template.render(scid=public_schema_id,
                                      tid=table_id)

                cursor = connection.cursor()
                cursor.execute(sql)
                fetch_result = cursor.fetchall()

                public_acls = list(
                    filter(lambda acl: acl[1] == 'PUBLIC', fetch_result)
                )
                public_acls | should.have.length(1)

                new_acl_map = dict(
                    zip(map(lambda column: column.name, cursor.description),
                        public_acls[0])
                )

                new_acl_map['grantee'] | should.be.equal.to('PUBLIC')
                new_acl_map['grantor'] | should.be.equal.to(server['username'])
                new_acl_map['deftype'] | should.be.equal.to('relacl')
                new_acl_map['privileges'] | should.be.equal.to(['r'])
                new_acl_map['grantable'] | should.be.equal.to([False])

    @staticmethod
    def get_template_file(version, filename):
        return os.path.join(
            os.path.dirname(__file__), '..', 'templates', 'table', 'sql',
            version, filename
        )
