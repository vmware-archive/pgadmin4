//////////////////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////////////////

export class TreeNode {
  constructor(id, data, domNode, parent) {
    this.id = id;
    this.data = data;
    this.setParent(parent);
    this.children = [];
    this.domNode = domNode;
  }

  hasParent() {
    return this.parentNode !== null && this.parentNode !== undefined;
  }

  parent() {
    return this.parentNode;
  }

  setParent(parent) {
    this.parentNode = parent;
    this.path = this.id;
    if (parent !== null && parent !== undefined && parent.path !== undefined) {
      this.path = parent.path + '.' + this.id;
    }
  }

  getData() {
    if (this.data === undefined) {
      return undefined;
    } else if (this.data === null) {
      return null;
    }
    return Object.assign({}, this.data);
  }

  getHtmlIdentifier() {
    return this.domNode;
  }

  reload(tree) {
    this.unload(tree);
    tree.aciTreeApi.setInode(this.domNode);
    tree.aciTreeApi.deselect(this.domNode);
    setTimeout(() => {
      tree.selectNode(this.domNode);
    }, 0);
  }

  unload(tree) {
    this.children = [];
    tree.aciTreeApi.unload(this.domNode);
  }

  anyParent(condition) {
    let node = this;

    while (node.hasParent()) {
      node = node.parent();
      if (condition(node)) {
        return true;
      }
    }

    return false;
  }

  anyFamilyMember(condition) {
    if(condition(this)) {
      return true;
    }

    return this.anyParent(condition);
  }
}

export class Tree {
  constructor() {
    this.rootNode = new TreeNode(undefined, {});
    this.aciTreeApi = undefined;
  }

  addNewNode(id, data, domNode, parentPath) {
    const parent = this.findNode(parentPath);
    return this.createOrUpdateNode(id, data, parent, domNode);
  }

  findNode(path) {
    if (path === null || path === undefined || path.length === 0) {
      return this.rootNode;
    }
    return findInTree(this.rootNode, path.join('.'));
  }

  findNodeByDomElement(domElement) {
    const path = this.translateTreeNodeIdFromACITree(domElement);
    if(!path || !path[0]) {
      return undefined;
    }

    return this.findNode(path);
  }

  selected() {
    return this.aciTreeApi.selected();
  }

  selectNode(aciTreeIdentifier) {
    this.aciTreeApi.select(aciTreeIdentifier);
  }

  register($treeJQuery) {
    $treeJQuery.on('acitree', function (event, api, item, eventName) {
      if (api.isItem(item)) {
        if (eventName === 'added') {
          const id = api.getId(item);
          const data = api.itemData(item);
          const parentId = this.translateTreeNodeIdFromACITree(api.parent(item));
          this.addNewNode(id, data, item, parentId);
        }
      }
    }.bind(this));
    this.aciTreeApi = $treeJQuery.aciTree('api');
  }

  createOrUpdateNode(id, data, parent, domNode) {
    let oldNodePath = [id];
    if(parent !== null && parent !== undefined) {
      oldNodePath = [parent.path, id];
    }
    const oldNode = this.findNode(oldNodePath);
    if (oldNode !== null) {
      oldNode.data = Object.assign({}, data);
      return oldNode;
    }

    const node = new TreeNode(id, data, domNode, parent);
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
