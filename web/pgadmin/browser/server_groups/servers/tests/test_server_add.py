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

from pgadmin.utils.base_test_generator import BaseTestGenerator
from regression.python_test_utils import test_utils as utils


class TestServersAdd:
    def test_server_add(self, request, context_of_tests):
        """
        When sending post request to server url
        It returns 200 status code
        """

        request.addfinalizer(self.tearDown)

        url = "/browser/server/obj/{0}/".format(utils.SERVER_GROUP)

        self.tester = context_of_tests['test_client']
        server = context_of_tests['server']

        response = self.tester.post(url, data=json.dumps(server),
                                    content_type='html/json')
        response.status_code | should.equal(200)

        response_data = json.loads(response.data.decode('utf-8'))
        self.server_id = response_data['node']['_id']
        server_dict = {"server_id": int(self.server_id)}
        utils.write_node_info("sid", server_dict)

    def tearDown(self):
        utils.delete_server_with_api(self.tester, self.server_id)
