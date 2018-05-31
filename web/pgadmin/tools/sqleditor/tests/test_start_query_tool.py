##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
import sys

from grappa import should

from pgadmin.tools.sqleditor import StartRunningQuery

if sys.version_info < (3, 3):
    from mock import patch, ANY
else:
    from unittest.mock import patch, ANY


class TestStartQueryTool:
    """StartQueryTool"""

    @patch('pgadmin.tools.sqleditor.extract_sql_from_network_parameters')
    def test_all(self, extract_sql_from_network_parameters_mock,
                 context_of_tests):
        """
        When request is sent to the backend
        And the request parameters are correct
        It starts the execution of the query and return 200
        """
        http_client = context_of_tests['test_client']

        extract_sql_from_network_parameters_mock.return_value = \
            'transformed sql'

        with patch.object(StartRunningQuery,
                          'execute',
                          return_value='some result'
                          ) as StartRunningQuery_execute_mock:
            response = http_client.post(
                '/sqleditor/query_tool/start/1234',
                data='"some sql statement"'
            )

            response.status | should.be.equal.to('200 OK')
            response.data | should.be.equal.to(b'some result')

            StartRunningQuery_execute_mock \
                .assert_called_with('transformed sql', 1234, ANY, False)
            extract_sql_from_network_parameters_mock \
                .assert_called_with(b'"some sql statement"', ANY, ANY)
