/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

import {canDropChild} from '../../../pgadmin/browser/server_groups/servers/databases/schemas/static/js/can_drop_child';
import {TreeFake} from '../tree/tree_fake';

let context = describe;

describe('can_drop_child', () => {

  let browser;
  let itemData;
  let item;

  beforeEach(() => {
    browser = {
      treeMenu: new TreeFake(),
    };
    item = [];
    browser.treeMenu.addNewNode('node1', {_type: 'schema'}, [{id: 'node1'}], []);
    browser.treeMenu.addNewNode('node1.1', {_type: 'database'}, [{id: 'node1.1'}], ['node1']);
    browser.treeMenu.addNewNode('node2', {_type: 'catalog'}, [{id: 'node2'}], []);
    browser.treeMenu.addNewNode('node2.1', {_type: 'table'}, [{id: 'node2.1'}], ['node2']);
    browser.treeMenu.addNewNode('node3', {_type: 'function'}, [{id: 'node3'}], []);
    browser.treeMenu.addNewNode('node3.1', {_type: 'procedure'}, [{id: 'node3.1'}], ['node3']);
  });

  context('when current node is of the type schema', () => {
    beforeEach(() => {
      itemData = {
        _type: 'schema',
      };
      item = [{id: 'node1'}];
    });

    it('returns true', () => {
      let bool = canDropChild(browser, itemData, item);
      expect(bool).toBe(true);
    });
  });

  context('when a parent of the current node is a schema', () => {
    it('returns true', () => {
      itemData = {
        _type: 'database',
      };
      item = [{id: 'node1.1'}];
      let bool = canDropChild(browser, itemData, item);
      expect(bool).toBe(true);
    });
  });

  context('when a parent of the current node is a catalog', () => {
    it('returns false', () => {
      itemData= {
        _type: 'table',
      };
      item = [{id: 'node2.1'}];

      let bool = canDropChild(browser, itemData, item);
      expect(bool).toBe(false);
    });
  });

  context('when a parent of the current node is not catalog nor schema', () => {
    it('returns true', () => {
      itemData = {
        _type: 'procedure',
      };
      item = [{id: 'node3.1'}];

      let bool = canDropChild(browser, itemData, item);
      expect(bool).toBe(true);
    });
  });
});
