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


class ClientTestBaseClass(BaseTestGenerator):
    def response_to_json(self, response):
        return json.loads(
            response.get_data(as_text=True).replace('\n', ''))

    def assert_node_json(self, json_response,
                         _type, module_name, inode, icon_class, label):
        assert_json_values_from_response(
            json_response,
            _type, module_name, inode, icon_class, label)


def convert_response_to_json(response):
    return json.loads(
        response.data.decode('utf-8').replace('\n', ''))


def assert_json_values_from_response(json_response,
                                     _type, module_name, inode, icon_class,
                                     label):
    """
    This function only works for JSON objects that look like:
        { node:
          {
            module: '',
            inode: '',
            icon: '',
            label: '',
            id: ''
          }
        }
    """
    (json_response | should.have.key('node') > should.have.key('_type') >
     should.be.equal.to(_type)
     )
    (json_response |
     should.have.key('node') >
     should.have.key('module') >
     should.be.equal.to(module_name)
     )
    (json_response |
     should.have.key('node') >
     should.have.key('inode') >
     should.be.equal.to(inode)
     )
    (json_response |
     should.have.key('node') >
     should.have.key('icon') >
     should.match(icon_class)
     )
    json_response | should.have.key('node') > should.have.key('_pid')
    (json_response |
     should.have.key('node') >
     should.have.key('label') >
     should.be.equal.to(label)
     )
    json_response | should.have.key('node') > should.have.key('_id')
    (json_response |
     should.have.key('node') >
     should.have.key('id') >
     should.be.equal.to(_type + '/' + str(json_response['node']['_id'])))
