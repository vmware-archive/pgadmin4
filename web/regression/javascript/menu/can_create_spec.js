/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
/////////////////////////////////////////////////////////////

import {canCreate} from '../../../pgadmin/static/js/menu/can_create';
import {TreeFake} from '../tree/tree_fake';

const context = describe;

describe('#canCreate', () => {
  let ourBrowser;
  let data;
  let tree;

  beforeEach(() => {
    tree = new TreeFake();
    ourBrowser = {
      treeMenu: tree,
    };

    tree.addNewNode('level1', {}, undefined, []);
  });

  context('data is not null and check is false ', () => {
    beforeEach(() => {
      data = {action: 'create', check: false};
    });
    it('returns true', () => {
      expect(canCreate({}, {}, {}, data)).toBe(true);
    });
  });

  context('data is not null and check is true', () => {
    beforeEach(() => {
      data = {action: 'create', check: true};
    });

    context('is node with type schema', () => {
      beforeEach(() => {
        tree.addNewNode('level2', {_type: 'schema'}, [{id: 'level2'}], ['level1']);
      });

      it('returns true', () => {
        expect(canCreate(ourBrowser, 'coll-table', [{id: 'level2'}], data)).toBe(true);
      });
    });

    context('has ancestor with type schema', () => {
      beforeEach(() => {
        tree.addNewNode('level2', {_type: 'schema'}, undefined, ['level1']);
        tree.addNewNode('level3', {_type: 'database'}, [{id: 'level3'}], ['level1', 'level2']);
      });

      it('returns true', () => {
        expect(canCreate(ourBrowser, 'coll-table', [{id: 'level3'}], data)).toBe(true);
      });
    });

    context('when type is not "coll-table"', () => {
      beforeEach(() => {
        tree.addNewNode('level2', {_type: 'database'}, undefined, ['level1']);
      });

      it('returns true', () => {
        expect(canCreate(ourBrowser, 'coll-table', [{id: 'level2'}], data)).toBe(true);
      });
    });

    context('when type is "coll-table"', () => {
      context('when parent type is "catalog"', () => {
        beforeEach(() => {
          tree.addNewNode('level2', {_type: 'catalog'}, undefined, ['level1']);
          tree.addNewNode('level3', {_type: 'coll-table'}, [{id: 'level3'}], ['level1', 'level2']);
        });

        it('returns false', () => {
          expect(canCreate(ourBrowser, 'coll-table', [{id: 'level3'}], data)).toBe(false);
        });
      });

      context('when parent type is not "catalog"', () => {
        beforeEach(() => {
          tree.addNewNode('level2', {_type: 'database'}, undefined, ['level1']);
          tree.addNewNode('level3', {_type: 'coll-table'}, [{id: 'level3'}], ['level1', 'level2']);
        });

        it('returns false', () => {
          expect(canCreate(ourBrowser, 'coll-table', [{id: 'level3'}], data)).toBe(true);
        });
      });
    });
  });
});
