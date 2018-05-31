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

import config
from regression.python_test_utils import test_utils as utils
from regression.test_setup import config_data as tconfig


class TestGravatarImageDisplay(object):
    @pytest.mark.skip_if_not_in_server_mode
    def test_gravatar_image_display(self, request, context_of_tests):
        """
        When user login
        It displays the gravatar
        """
        http_client = context_of_tests['test_client']
        utils.logout_tester_account(http_client)
        request.addfinalizer(lambda: utils.login_tester_account(http_client))

        response = http_client.post(
            '/login', data=dict(
                email=tconfig['pgAdmin4_login_credentials']['login_username'],
                password=tconfig['pgAdmin4_login_credentials'][
                    'login_password']
            ),
            follow_redirects=True
        )
        gravatar_information = 'Gravatar image for {0}'.format(
            tconfig['pgAdmin4_login_credentials']['login_username']
        )
        if config.SHOW_GRAVATAR_IMAGE:
            response.data.decode('utf8') | should.contain(gravatar_information)
        else:
            response.data.decode('utf8') | should.not_contain(
                gravatar_information)
