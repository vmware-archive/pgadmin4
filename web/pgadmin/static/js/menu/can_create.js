/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
/////////////////////////////////////////////////////////////

export function canCreate(pgBrowser, childOfCatalogType, item, data) {
  //If check is false then , we will allow create menu
  if (data && data.check === false) {
    return true;
  }

  let node = pgBrowser.treeMenu.findNodeByDomElement(item);

  if (node.anyFamilyMember(parentCatalogOfTableChild.bind(null, childOfCatalogType))) {
    return false;
  }

  return true;
}

function parentCatalogOfTableChild(arg, node) {
  if (arg === node.getData()._type) {
    if (node.hasParent()) {

      let parent = node.parent();
      if ('catalog' === parent.getData()._type) {
        return true;
      }
    }
  }

  return false;
}
