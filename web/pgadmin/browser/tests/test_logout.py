##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
import pytest
from grappa import should

from regression.python_test_utils import test_utils


@pytest.mark.skip_if_not_in_server_mode
class TestLogout(object):
    def test_success(self, request, context_of_tests):
        """
        When trying to logout
        And the credential are correct
        It returns "Specified user does not exist" error
        """
        http_client = context_of_tests['test_client']
        response = http_client.get('/logout')
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))
        response.data.decode('utf8') | should.contain('Redirecting...')
