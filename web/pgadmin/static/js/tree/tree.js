//////////////////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////////////////
export class TreeNode {
  constructor(id, data, parent) {
    this.id = id;
    this.data = data;
    this.parentNode = parent;
    this.path = this.id;
    if (parent !== null && parent !== undefined && parent.path !== undefined) {
      this.path = parent.path + '.' + id;
    }
    this.children = [];
  }

  hasParent() {
    return this.parentNode !== null && this.parentNode !== undefined ;
  }

  parent() {
    return this.parentNode;
  }

  getData() {
    return Object.assign({}, this.data);
  }
}

export class Tree {
  constructor() {
    this.rootNode = new TreeNode(undefined, {});
    this.aciTreeApi = undefined;
  }

  addNewNode(id, data, path) {
    const parent = this.findNode(path);
    return this.createOrUpdateNode(id, data, parent);
  }

  findNode(path) {
    if (path.length === 0) {
      return this.rootNode;
    }
    return findInTree(this.rootNode, path.join('.'));
  }

  findNodeByDomElement(domElement) {
    return this.findNode(this.translateTreeNodeIdFromACITree(domElement));
  }

  register($treeJQuery) {
    $treeJQuery.on('acitree', function (event, api, item, eventName) {
      if (api.isItem(item)) {
        if (eventName === 'added') {
          const id = api.getId(item);
          const data = api.itemData(item);
          const parentId = this.translateTreeNodeIdFromACITree(api.parent(item));
          this.addNewNode(id, data, parentId);
        }
      }
    }.bind(this));
    this.aciTreeApi = $treeJQuery.aciTree('api');
  }

  createOrUpdateNode(id, data, parent) {
    const oldNode = this.findNode([parent.path, id]);
    if (oldNode !== null) {
      oldNode.data = Object.assign({}, data);
      return oldNode;
    }

    const node = new TreeNode(id, data, parent);
    if (parent === this.rootNode) {
      node.parentNode = null;
    }
    parent.children.push(node);
    return node;
  }

  translateTreeNodeIdFromACITree(aciTreeNode) {
    let currentTreeNode = aciTreeNode;
    let path = [];
    while (currentTreeNode !== null && currentTreeNode !== undefined && currentTreeNode.length > 0) {
      path.unshift(this.aciTreeApi.getId(currentTreeNode));
      if (this.aciTreeApi.hasParent(currentTreeNode)) {
        currentTreeNode = this.aciTreeApi.parent(currentTreeNode);
      } else {
        break;
      }
    }
    return path;
  }
}

export let tree = new Tree();

function findInTree(rootNode, path) {
  if (path === null) {
    return rootNode;
  }
  return (function findInNode(currentNode) {
    for (let i = 0, length = currentNode.children.length; i < length; i++) {
      const calculatedNode = findInNode(currentNode.children[i]);
      if (calculatedNode !== null) {
        return calculatedNode;
      }
    }

    if (currentNode.path === path) {
      return currentNode;
    } else {
      return null;
    }
  })(rootNode);
}
