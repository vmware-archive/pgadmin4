##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
from grappa import should

from pgadmin.utils.base_test_generator import BaseTestGenerator
from regression.python_test_utils import test_utils as utils


class TestServerDelete:
    def test_server_delete(self, request, context_of_tests):
        """
        When sending delete request to server url
        It returns 200 status code
        """

        request.addfinalizer(self.tearDown)

        url = "/browser/server/obj/{0}/".format(utils.SERVER_GROUP)

        server = context_of_tests['server']
        self.server_id = utils.create_server(server)
        self.tester = context_of_tests['test_client']

        if not self.server_id:
            raise Exception("No server to delete!!!")

        server_dict = {"server_id": self.server_id}
        utils.write_node_info("sid", server_dict)

        response = self.tester.delete(url + str(self.server_id))
        response.status_code | should.equal(200)

    def tearDown(self):
        utils.delete_server_with_api(self.tester, self.server_id)
