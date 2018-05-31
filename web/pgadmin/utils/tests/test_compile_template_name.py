#######################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from grappa import should

from pgadmin.utils.compile_template_name import compile_template_name
from pgadmin.utils.base_test_generator import BaseTestGenerator


class TestCompileTemplateName(BaseTestGenerator):
    scenarios = [
        (
            'When server is Postgres and version is 10, it returns the path '
            'to the postgres template',
            dict(
                server_type='pg',
                version=100000,
                expected_return_value='some/prefix/#100000#/some_file.sql'
            )
        ),
        (
            'When server is GreenPlum and version is 5, it returns the path '
            'to the GreenPlum template',
            dict(
                server_type='gpdb',
                version=80323,
                expected_return_value='some/prefix/#gpdb#80323#/some_file.sql'
            )
        ),
    ]

    def test_all(self, args, kwargs):
        self._expand_test_object(kwargs)
        result = compile_template_name(
            'some/prefix', 'some_file.sql', self.server_type, self.version
        )
        result | should.be.equal.to(self.expected_return_value)
