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
        let hierarchy = {
          id: 'root',
          children: [
            {
              id: 'level2',
              data: {_type: 'schema'},
            },
          ],
        };

        tree = TreeFake.build(hierarchy);
        ourBrowser = {treeMenu: tree};
      });

      it('returns true', () => {
        expect(canCreate(ourBrowser, 'coll-table', [{id: 'level2'}], data)).toBe(true);
      });
    });

    context('has ancestor with type schema', () => {
      beforeEach(() => {

        let hierarchy = {
          id: 'root',
          children: [
            {
              id: 'level2',
              data: {_type: 'schema'},
              children: [
                {
                  id: 'level3',
                  data: {_type: 'database'},
                },
              ],
            },
          ],
        };

        tree = TreeFake.build(hierarchy);
        ourBrowser = {treeMenu: tree};
      });

      it('returns true', () => {
        expect(canCreate(ourBrowser, 'coll-table', [{id: 'level3'}], data)).toBe(true);
      });
    });

    context('when type is not "coll-table"', () => {
      beforeEach(() => {
        let hierarchy = {
          id: 'root',
          children: [
            {
              id: 'level2',
              data: {_type: 'database'},
            },
          ],
        };

        tree = TreeFake.build(hierarchy);
        ourBrowser = {treeMenu: tree};
      });

      it('returns true', () => {
        expect(canCreate(ourBrowser, 'coll-table', [{id: 'level2'}], data)).toBe(true);
      });
    });

    context('when type is "coll-table"', () => {
      context('when parent type is "catalog"', () => {
        beforeEach(() => {
          let hierarchy = {
            id: 'root',
            children: [
              {
                id: 'level2',
                data: {_type: 'catalog'},
                children: [
                  {
                    id: 'level3',
                    data: {_type: 'coll-table'},
                  },
                ],
              },
            ],
          };

          tree = TreeFake.build(hierarchy);
          ourBrowser = {treeMenu: tree};
        });

        it('returns false', () => {
          expect(canCreate(ourBrowser, 'coll-table', [{id: 'level3'}], data)).toBe(false);
        });
      });

      context('when parent type is not "catalog"', () => {
        beforeEach(() => {
          let hierarchy = {
            id: 'root',
            children: [
              {
                id: 'level2',
                data: {_type: 'database'},
                children: [
                  {
                    id: 'level3',
                    data: {_type: 'coll-table'},
                  },
                ],
              },
            ],
          };

          tree = TreeFake.build(hierarchy);
          ourBrowser = {treeMenu: tree};
        });

        it('returns false', () => {
          expect(canCreate(ourBrowser, 'coll-table', [{id: 'level3'}], data)).toBe(true);
        });
      });
    });
  });
});
