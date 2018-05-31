##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json

from grappa import should

from regression.test_setup import config_data


class TestServerGroupNode:
    def test_server_group_node(self, context_of_tests):
        """
        When a get request is made to the server group endpoint
        It returns status 200 and the server group
        """

        url = '/browser/server_group/obj/'
        http_client = context_of_tests['test_client']

        server_group_id = config_data['server_group']
        response = http_client.get(url + str(server_group_id),
                                   content_type='html/json')

        response.status_code | should.equal(200)
        response_data = json.loads(response.data.decode('utf8'))
        response_data['id'] | should.equal(server_group_id)
