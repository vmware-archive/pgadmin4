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

from regression.python_test_utils import test_utils
from regression.test_setup import config_data


@pytest.mark.skip_if_not_in_server_mode
class TestLogin(object):
    def test_incorrect_password(self, request, context_of_tests):
        """
        When trying to login
        And password is invalid
        It returns "Invalid password" error
        """
        http_client = context_of_tests['test_client']

        test_utils.logout_tester_account(http_client)
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))

        response = http_client.post(
            '/login',
            data=dict(
                email=config_data['pgAdmin4_login_credentials']
                ['login_username'],
                password=str(uuid.uuid4())[4:8]
            ),
            follow_redirects=True
        )
        response.data.decode('utf8') | should.contain('Invalid password')

    def test_empty_email(self, request, context_of_tests):
        """
        When trying to login
        And email is empty
        It returns "Email not provided" error
        """
        http_client = context_of_tests['test_client']

        test_utils.logout_tester_account(http_client)
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))

        response = http_client.post(
            '/login',
            data=dict(
                email='',
                password=str(uuid.uuid4())[4:8]
            ),
            follow_redirects=True
        )
        response.data.decode('utf8') | should.contain('Email not provided')

    def test_empty_password(self, request, context_of_tests):
        """
        When trying to login
        And password is empty
        It returns "Password not provided" error
        """
        http_client = context_of_tests['test_client']

        test_utils.logout_tester_account(http_client)
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))

        response = http_client.post(
            '/login',
            data=dict(
                email=str(uuid.uuid4())[4:8],
                password=''
            ),
            follow_redirects=True
        )
        response.data.decode('utf8') | should.contain('Password not provided')

    def test_user_not_found(self, request, context_of_tests):
        """
        When trying to login
        And the user does not exist
        It returns "Specified user does not exist" error
        """
        http_client = context_of_tests['test_client']

        test_utils.logout_tester_account(http_client)
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))

        response = http_client.post(
            '/login',
            data=dict(
                email=str(uuid.uuid4())[4:8] + '@xyz.com',
                password=str(uuid.uuid4())[4:8]
            ),
            follow_redirects=True
        )
        response.data.decode('utf8') | should.contain(
            'Specified user does not exist')

    def test_success(self, request, context_of_tests):
        """
        When trying to login
        And the credential are correct
        It returns "Specified user does not exist" error
        """
        http_client = context_of_tests['test_client']

        test_utils.logout_tester_account(http_client)
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))

        response = http_client.post(
            '/login',
            data=dict(
                email=config_data['pgAdmin4_login_credentials']
                ['login_username'],
                password=config_data['pgAdmin4_login_credentials']
                ['login_password']
            ),
            follow_redirects=True
        )
        response.data.decode('utf8') | should.contain(
            'Gravatar image for %s' % config_data['pgAdmin4_login_credentials']
                                                 ['login_username'])
