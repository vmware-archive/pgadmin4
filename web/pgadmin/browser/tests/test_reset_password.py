##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import uuid

import pytest
from grappa import should

from regression.python_test_utils.test_utils import login_tester_account
from regression.python_test_utils.test_utils import logout_tester_account
from regression.test_setup import config_data


@pytest.mark.skip_if_not_in_server_mode
class TestResetPassword(object):
    def test_empty_email(self, request, context_of_tests):
        """
        When trying to reset the password
        And email is empty
        It returns "Email not provided" error
        """
        http_client = context_of_tests['test_client']

        logout_tester_account(http_client)
        request.addfinalizer(lambda: login_tester_account(http_client))

        response = http_client.get('/browser/reset_password')
        response.data.decode('utf-8') | should.contain(
            'Recover pgAdmin 4 Password')
        response = http_client.post(
            '/browser/reset_password', data=dict(email=''),
            follow_redirects=True)
        response.data.decode('utf-8') | should.contain('Email not provided')

    def test_user_not_found(self, request, context_of_tests):
        """
        When trying to reset the password
        And user is not found
        It returns "Specified user does not exist" error
        """
        http_client = context_of_tests['test_client']

        logout_tester_account(http_client)
        request.addfinalizer(lambda: login_tester_account(http_client))

        response = http_client.get('/browser/reset_password')
        response.data.decode('utf-8') | should.contain(
            'Recover pgAdmin 4 Password')
        response = http_client.post(
            '/browser/reset_password', data=dict(
                email=str(uuid.uuid4())[1:8] + '@xyz.com'),
            follow_redirects=True)
        response.data.decode('utf-8') | should.contain(
            'Specified user does not exist')

    @pytest.mark.xfail(reason='Test previously failing, issue inside http '
                              'test client')
    def test_success(self, request, context_of_tests):
        """
        When trying to reset the password
        And user exists
        It returns success
        """
        http_client = context_of_tests['test_client']

        logout_tester_account(http_client)
        request.addfinalizer(lambda: login_tester_account(http_client))

        response = http_client.get('/browser/reset_password')
        response.data.decode('utf-8') | should.contain(
            'Recover pgAdmin 4 Password')
        response = http_client.post(
            '/browser/reset_password', data=dict(
                email=config_data['pgAdmin4_login_credentials']),
            follow_redirects=True)
        response.data.decode('utf-8') | should.contain('pgAdmin 4')
