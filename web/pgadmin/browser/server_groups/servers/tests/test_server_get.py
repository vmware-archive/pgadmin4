##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

from grappa import should

from regression.python_test_utils import test_utils as utils


class TestServersGet:
    def test_server_get(self, request, context_of_tests):
        """
        When sending get request to server url
        It returns 200 status code
        """

        request.addfinalizer(self.tearDown)

        url = '/browser/server/obj/'

        self.server_id = utils.create_server(context_of_tests['server'])
        if not self.server_id:
            raise Exception("Server not found to test GET API")

        server_dict = {"server_id": self.server_id}
        utils.write_node_info("sid", server_dict)
        self.tester = context_of_tests['test_client']

        response = self.tester.get(
            url + str(utils.SERVER_GROUP) + '/' +
            str(self.server_id),
            follow_redirects=True)

        response.status_code | should.be.equal.to(200)

    def tearDown(self):
        utils.delete_server_with_api(self.tester, self.server_id)
