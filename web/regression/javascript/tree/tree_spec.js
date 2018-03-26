//////////////////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////////////////

import {Tree, TreeNode} from "../../../pgadmin/static/js/tree/tree";
import {TreeFake} from "./tree_fake";

const context = describe;

const treeTests = (treeClass) => {
  let tree;
  beforeEach(() => {
    tree = new treeClass();
  });

  describe('#addNewNode', () => {
    describe('when add a new root element', () => {
      beforeEach(() => {
        tree.addNewNode('some new node', {data: 'interesting'}, []);
      });

      it('can be retrieved', () => {
        const node = tree.findNode(['some new node']);
        expect(node.data).toEqual({data: 'interesting'});
      });

      it('return false for #hasParent()', () => {
        const node = tree.findNode(['some new node']);
        expect(node.hasParent()).toBe(false);
      });

      it('return null for #parent()', () => {
        const node = tree.findNode(['some new node']);
        expect(node.parent()).toBeNull();
      });
    });

    describe('when add a new element as a child', () => {
      let parentNode;
      beforeEach(() => {
        parentNode = tree.addNewNode('parent node', {data: 'parent data'}, []);
        tree.addNewNode('some new node', {data: 'interesting'}, ['parent' +
        ' node']);
      });

      it('can be retrieved', () => {
        const node = tree.findNode(['parent node', 'some new node']);
        expect(node.data).toEqual({data: 'interesting'});
      });

      it('return true for #hasParent()', () => {
        const node = tree.findNode(['parent node', 'some new node']);
        expect(node.hasParent()).toBe(true);
      });

      it('return "parent node" object for #parent()', () => {
        const node = tree.findNode(['parent node', 'some new node']);
        expect(node.parent()).toEqual(parentNode);
      });
    });

    describe('when add an element that already exists under a parent', () => {
      let parentNode;
      beforeEach(() => {
        parentNode = tree.addNewNode('parent node', {data: 'parent data'}, []);
        tree.addNewNode('some new node', {data: 'interesting'}, ['parent' +
        ' node']);
      });

      it('does not add a new child', () => {
        tree.addNewNode('some new node', {data: 'interesting 1'}, ['parent' +
        ' node']);
        const parentNode = tree.findNode(['parent node']);
        expect(parentNode.children.length).toBe(1);
      });

      it('updates the existing node data', () => {
        tree.addNewNode('some new node', {data: 'interesting 1'}, ['parent' +
        ' node']);
        const node = tree.findNode(['parent node', 'some new node']);
        expect(node.data).toEqual({data: 'interesting 1'});
      });
    });
  });

  describe('#translateTreeNodeIdFromACITree', () => {
    let aciTreeApi;
    beforeEach(() => {
      aciTreeApi = jasmine.createSpyObj('ACITreeApi', [
        'hasParent',
        'parent',
        'getId',
      ]);

      aciTreeApi.getId.and.callFake((node) => {
        return node[0].id;
      });
      tree.aciTreeApi = aciTreeApi;
    });

    describe('When tree as a single level', () => {
      beforeEach(() => {
        aciTreeApi.hasParent.and.returnValue(false);
      });

      it('returns an array with the ID of the first level', () => {
        let node = [{
          id: 'some id',
        }];
        tree.addNewNode('some id', {}, []);

        expect(tree.translateTreeNodeIdFromACITree(node)).toEqual(['some id']);
      });
    });

    describe('When tree as a 2 levels', () => {
      describe('When we try to retrieve the node in the second level', () => {
        it('returns an array with the ID of the first level and second level', () => {
          aciTreeApi.hasParent.and.returnValues(true, false);
          aciTreeApi.parent.and.returnValue([{
            id: 'parent id'
          }]);
          let node = [{
            id: 'some id',
          }];

          tree.addNewNode('parent id', {}, []);
          tree.addNewNode('some id', {}, ['parent id']);

          expect(tree.translateTreeNodeIdFromACITree(node))
            .toEqual(['parent id', 'some id']);
        });
      });
    });
  });
};

describe('tree tests', () => {
  describe('TreeNode', () => {
    describe('#hasParent', () => {
      context('parent is null', () => {
        it('returns false', () => {
          let treeNode = new TreeNode('123', {}, null);
          expect(treeNode.hasParent()).toBe(false);
        });
      });
      context('parent is undefined', () => {
        it('returns false', () => {
          let treeNode = new TreeNode('123', {}, undefined);
          expect(treeNode.hasParent()).toBe(false);
        });
      });
      context('parent exists', () => {
        it('returns true', () => {
          let parentNode = new TreeNode('456', {}, undefined);
          let treeNode = new TreeNode('123', {}, parentNode);
          expect(treeNode.hasParent()).toBe(true);
        });
      });
    });
  });

  describe('Tree', () => {
    treeTests(Tree);
  });

  describe('TreeFake', () => {
    treeTests(TreeFake);

    describe('#hasParent', () => {
      context('tree contains multiple levels', () => {
        let tree;
        beforeEach(() => {
          tree = new TreeFake();
          tree.addNewNode('level1', {data: 'interesting'}, []);
          tree.addNewNode('level2', {data: 'interesting'}, ['level1']);
        });

        context('node is at the first level', () => {
          it('returns false', () => {
            expect(tree.hasParent([{id: 'level1'}])).toBe(false);
          });
        });

        context('node is at the second level', () => {
          it('returns true', () => {
            expect(tree.hasParent([{id: 'level2'}])).toBe(true);
          });
        });
      });
    });

    describe('#parent', () => {
      let tree;
      beforeEach(() => {
        tree = new TreeFake();
        tree.addNewNode('level1', {data: 'interesting'}, []);
        tree.addNewNode('level2', {data: 'interesting'}, ['level1']);
      });

      context('node is the root', () => {
        it('returns null', () => {
          expect(tree.parent([{id: 'level1'}])).toBeNull();
        });
      });

      context('node is not root', () => {
        it('returns root element', () => {
          expect(tree.parent([{id: 'level2'}])).toEqual([{id: 'level1'}]);
        });
      });
    });

    describe('#itemData', () => {
      let tree;
      beforeEach(() => {
        tree = new TreeFake();
        tree.addNewNode('level1', {data: 'interesting'}, []);
        tree.addNewNode('level2', {data: 'expected data'}, ['level1']);
      });

      context('retrieve data from the node', () => {
        it('return the node data', () => {
          expect(tree.itemData([{id: 'level2'}])).toEqual({data: 'expected' +
            ' data'})
        });
      });
    });
  });
});

