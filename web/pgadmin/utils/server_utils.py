##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from __future__ import print_function

import json

import config
from regression.python_test_utils.test_utils import login_tester_account

SERVER_URL = '/browser/server/obj/'
SERVER_CONNECT_URL = '/browser/server/connect/'
DUMMY_SERVER_GROUP = 10000


def connect_server(self, server_id):
    """
    This function used to connect added server
    :param self: class object of server's test class
    :type self: class
    :param server_id: server id
    :type server_id: str
    """
    return client_connect_server(self.tester, server_id,
                                 self.server['db_password'])


def client_connect_server(client, server_id, password):
    """
    This function used to connect added server
    :param client: Flask Test client
    :param server_id: server id
    :param password: password to the database
    :type server_id: str
    """
    response = client.post(SERVER_CONNECT_URL + str(DUMMY_SERVER_GROUP) +
                           '/' + str(server_id),
                           data=dict(password=password),
                           follow_redirects=True)

    if response.status_code == 401 and config.SERVER_MODE:
        login_tester_account(client)
        response = client.post(SERVER_CONNECT_URL + str(DUMMY_SERVER_GROUP) +
                               '/' + str(server_id),
                               data=dict(password=password),
                               follow_redirects=True)

    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf-8'))
    return response_data
