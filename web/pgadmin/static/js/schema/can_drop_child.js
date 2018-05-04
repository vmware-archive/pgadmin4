/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

export function canDropChild(pgBrowser, itemData, item) {
  let node = pgBrowser.treeMenu.findNodeByDomElement(item);

  if (node.anyParent((parent) => parent.getData()._type === 'catalog')) {
    return false;
  }

  return true;
}
