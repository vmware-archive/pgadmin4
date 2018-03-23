/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////


import {TreeFake} from "../tree/tree_fake";
import {menu_enabled} from "../../../pgadmin/static/js/backup/menu_utils";

const context = describe;

describe('backup#menuEnabled', () => {
  let ourBrowser;
  beforeEach(() => {
    const tree = new TreeFake();
    ourBrowser = {
      tree: tree,
    };
    tree.addNewNode('level1', {}, []);
    tree.addNewNode('level2', {}, []);
    tree.addNewNode('level2.1', null, ['level2']);
    tree.addNewNode('level3.1', {}, ['level2', 'level2.1']);
  });
  // menu_enabled.apply(ourBrowser, [itemData, item]
  context('parent data does not exist', () => {
    it('returns false', () => {
      expect(menu_enabled.apply(ourBrowser, [{}, [{id: 'level3.1'}]])).toBe(false);
    });
  });
});
