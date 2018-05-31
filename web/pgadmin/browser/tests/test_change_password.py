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

from regression.python_test_utils import test_utils
from regression.test_setup import config_data


@pytest.mark.skip_if_not_in_server_mode
class TestChangePassword(object):
    def test_incorrect_password(self, request, context_of_tests):
        """
        When trying to change the password
        And the confirmation password does not match
        It returns "Passwords do not match" error
        """
        http_client = context_of_tests['test_client']
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))

        response = http_client.post(
            '/browser/change_password',
            data=dict(
                password=config_data['pgAdmin4_login_credentials']
                ['login_password'],
                new_password=str(uuid.uuid4())[4:8],
                new_password_confirm=str(uuid.uuid4())[4:8]
            ),
            follow_redirects=True
        )
        response.data.decode('utf-8') | should.contain(
            'Passwords do not match')

    def test_minimum_length(self, request, context_of_tests):
        """
        When trying to change the password
        And has less then 6 characters
        It returns "Password not provided" error
        """
        http_client = context_of_tests['test_client']
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))

        response = http_client.post(
            '/browser/change_password',
            data=dict(
                password=config_data['pgAdmin4_login_credentials']
                ['login_password'],
                new_password='pgadm',
                new_password_confirm='pgadm'
            ),
            follow_redirects=True
        )
        response.data.decode('utf-8') | should.contain(
            'Password must be at least 6 characters')

    def test_no_new_password_provided(self, request, context_of_tests):
        """
        When trying to change the password
        And password and confirmation password are empty
        It returns "Password not provided" error
        """
        http_client = context_of_tests['test_client']
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))

        response = http_client.post(
            '/browser/change_password',
            data=dict(
                password=config_data['pgAdmin4_login_credentials']
                ['login_password'],
                new_password='',
                new_password_confirm=''
            ),
            follow_redirects=True
        )
        response.data.decode('utf-8') | should.contain(
            'Password not provided')

    def test_current_password_is_incorrect(self, request, context_of_tests):
        """
        When trying to change the password
        And current password provided is not correct
        It returns "Invalid password" error
        """
        http_client = context_of_tests['test_client']
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))

        response = http_client.post(
            '/browser/change_password',
            data=dict(
                password=str(uuid.uuid4())[4:8],
                new_password='asdfasdf',
                new_password_confirm='asdfasdf'
            ),
            follow_redirects=True
        )
        response.data.decode('utf-8') | should.contain(
            'Invalid password')

    @pytest.mark.xfail(reason='Test previously failing, the login does not go '
                       'through successfuly')
    def test_success(self, request, context_of_tests):
        """
        When trying to change the password
        And everything is correct
        It returns changes the password
        """
        http_client = context_of_tests['test_client']
        request.addfinalizer(lambda: test_utils
                             .login_tester_account(http_client))
        response = http_client.post(
            '/user_management/user/',
            data=dict(
                email=config_data['pgAdmin4_test_user_credentials']
                ['login_username'] + '1',
                newPassword=config_data['pgAdmin4_test_user_credentials']
                ['login_password'],
                confirmPassword=config_data['pgAdmin4_test_user_credentials']
                ['login_password'],
                active=1,
                role="2"
            ),
            follow_redirects=True
        )

        json.loads(response.data.decode('utf-8')) | should.have.key('id')
        user_id = json.loads(response.data.decode('utf-8'))['id']
        # Logout the Administrator before login normal user
        test_utils.logout_tester_account(http_client)
        response = http_client.post(
            '/login',
            data=dict(
                email=config_data['pgAdmin4_test_user_credentials']
                ['login_username'] + '1',
                password=config_data['pgAdmin4_test_user_credentials']
                ['login_password']
            ),
            follow_redirects=True
        )
        response.status_code | should.be.equal(200)
        response = http_client.get(
            '/browser/change_password', follow_redirects=True
        )
        response.data.decode('utf-8') | should.contain(
            'pgAdmin 4 Password Change')
        # test the 'change password' test case
        response = http_client.post(
            '/browser/change_password',
            data=dict(
                password=config_data['pgAdmin4_test_user_credentials']
                ['login_password'],
                new_password='asdfasdf',
                new_password_confirm='asdfasdf'
            ),
            follow_redirects=True
        )
        response.data.decode('utf-8') | should.contain(
            'You successfully changed your password')
        # Delete the normal user after changing it's password
        test_utils.logout_tester_account(http_client)
        # Login the Administrator before deleting normal user
        test_utils.login_tester_account(http_client)
        response = http_client.delete(
            '/user_management/user/' + str(user_id),
            follow_redirects=True
        )
        response.status_code | should.be.equal(200)
