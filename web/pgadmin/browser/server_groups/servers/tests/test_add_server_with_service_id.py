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

from regression.python_test_utils import test_utils as utils


class TestServersWithServiceIDAdd:
    def test_server_with_id_add(self, request, context_of_tests):
        """
        When sending a post request to add server with service id
        It returns 200 status code
        """

        request.addfinalizer(self.tearDown)

        url = "/browser/server/obj/{0}/".format(utils.SERVER_GROUP)

        server = context_of_tests['server']
        server['service'] = "TestDB"
        self.tester = context_of_tests['test_client']

        response = self.tester.post(
            url,
            data=json.dumps(server),
            content_type='html/json'
        )

        response.status_code | should.equal(200)
        response_data = json.loads(response.data.decode('utf-8'))
        self.server_id = response_data['node']['_id']

    def tearDown(self):
        utils.delete_server_with_api(self.tester, self.server_id)
