##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
import copy
import json

from grappa import should

from regression.python_test_utils import test_utils as utils


class TestServersWithSSHTunnelAdd:
    def test_server_using_tunnel_with_password(self,
                                               request,
                                               context_of_tests):
        """
        When sending a post request to add server
        using ssh tunnel with password
        It returns 200 status code
        """

        request.addfinalizer(self.tearDown)

        url = "/browser/server/obj/{0}/".format(utils.SERVER_GROUP)

        self.server = copy.deepcopy(context_of_tests['server'])
        self.tester = context_of_tests['test_client']
        self.server['use_ssh_tunnel'] = 1
        self.server['tunnel_host'] = '127.0.0.1'
        self.server['tunnel_port'] = 22
        self.server['tunnel_username'] = 'user'
        self.server['tunnel_authentication'] = 0

        response = self.tester.post(
            url,
            data=json.dumps(self.server),
            content_type='html/json'
        )

        response.status_code | should.equal(200)

        response_data = json.loads(response.data.decode('utf-8'))
        self.server_id = response_data['node']['_id']

    def test_server_using_tunnel_with_id_file(self,
                                              request,
                                              context_of_tests):
        """
        When sending a post request to add server
        using ssh tunnel with an identity file
        It returns 200 status code
        """

        request.addfinalizer(self.tearDown)

        url = "/browser/server/obj/{0}/".format(utils.SERVER_GROUP)

        self.server = copy.deepcopy(context_of_tests['server'])
        self.tester = context_of_tests['test_client']
        self.server['use_ssh_tunnel'] = 1
        self.server['tunnel_host'] = '127.0.0.1'
        self.server['tunnel_port'] = 22
        self.server['tunnel_username'] = 'user'
        self.server['tunnel_authentication'] = 1
        self.server['tunnel_identity_file'] = 'pkey_rsa'

        response = self.tester.post(
            url,
            data=json.dumps(self.server),
            content_type='html/json'
        )

        response.status_code | should.equal(200)

        response_data = json.loads(response.data.decode('utf-8'))
        self.server_id = response_data['node']['_id']

    def tearDown(self):
        utils.delete_server_with_api(self.tester, self.server_id)
