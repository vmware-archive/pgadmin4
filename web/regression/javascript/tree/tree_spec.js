//////////////////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////////////////

import {Tree} from "../../../pgadmin/static/js/tree/tree";

describe('tree#', () => {
  let tree;
  beforeEach(() => {
    tree = new Tree();
  });

  describe('addNewNode', () => {
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

          expect(tree.translateTreeNodeIdFromACITree(node))
            .toEqual(['parent id', 'some id']);
        });
      });
    });
  });
});
