/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

import {Tree} from "../../../pgadmin/static/js/tree/tree";

export class TreeFake extends Tree {
  constructor() {
    super();
    this.aciTreeToOurTreeTranslator = {};
  }

  addNewNode(id, data, path) {
    this.aciTreeToOurTreeTranslator[id] = path.concat(id);
    return super.addNewNode(id, data, path);
  }

  hasParent(aciTreeNode) {
    return this.translateTreeNodeIdFromACITree(aciTreeNode).length > 1;
  }

  parent(aciTreeNode) {
    if (this.hasParent(aciTreeNode)) {
      let path = this.translateTreeNodeIdFromACITree(aciTreeNode);
      return [{id: this.findNode(path).parent().id}];
    }

    return null;
  }

  translateTreeNodeIdFromACITree(aciTreeNode) {
    return this.aciTreeToOurTreeTranslator[aciTreeNode[0].id];
  }

  itemData(aciTreeNode) {
    let path = this.translateTreeNodeIdFromACITree(aciTreeNode);
    return this.findNode(path).getData();
  }
}
