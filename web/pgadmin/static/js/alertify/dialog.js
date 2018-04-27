/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2018, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

import gettext from '../gettext';
import {sprintf} from 'sprintf-js';
import {DialogFactory} from './dialog_factory';
import Backform from '../backform.pgadmin';

export class Dialog {
  constructor(errorAlertTitle,
              dialogContainerSelector,
              pgBrowser, $, alertify, DialogModel,
              backform = Backform) {
    this.errorAlertTitle = errorAlertTitle;
    this.alertify = alertify;
    this.pgBrowser = pgBrowser;
    this.jquery = $;
    this.dialogModel = DialogModel;
    this.backform = backform;
    this.dialogContainerSelector = dialogContainerSelector;
  }

  retrieveAncestorOfTypeServer(item) {
    let serverInformation = null;
    let aciTreeItem = item || this.pgBrowser.treeMenu.selected();
    let treeNode = this.pgBrowser.treeMenu.findNodeByDomElement(aciTreeItem);

    while (treeNode) {
      const node_data = treeNode.getData();
      if (node_data._type === 'server') {
        serverInformation = node_data;
        break;
      }

      if (treeNode.hasParent()) {
        treeNode = treeNode.parent();
      } else {
        this.alertify.alert(
          gettext(this.errorAlertTitle),
          gettext('Please select server or child node from the browser tree.')
        );
        break;
      }
    }
    return serverInformation;
  }

  hasBinariesConfiguration(serverInformation) {
    const module = 'paths';
    let preference_name = 'pg_bin_dir';
    let msg = gettext('Please configure the PostgreSQL Binary Path in the Preferences dialog.');

    if ((serverInformation.type && serverInformation.type === 'ppas') ||
      serverInformation.server_type === 'ppas') {
      preference_name = 'ppas_bin_dir';
      msg = gettext('Please configure the EDB Advanced Server Binary Path in the Preferences dialog.');
    }
    const preference = this.pgBrowser.get_preference(module, preference_name);

    if (preference) {
      if (!preference.value) {
        this.alertify.alert(gettext('Configuration required'), msg);
        return false;
      }
    } else {
      this.alertify.alert(
        gettext(this.errorAlertTitle),
        sprintf(gettext('Failed to load preference %s of module %s'), preference_name, module)
      );
      return false;
    }
    return true;
  }

  dialogName() {
    return undefined;
  }

  createOrGetDialog(dialogTitle, typeOfDialog) {
    const dialogName = this.dialogName(typeOfDialog);

    if (!this.alertify[dialogName]) {
      const self = this;
      this.alertify.dialog(dialogName, function factory() {
        return self.dialogFactory(dialogTitle, typeOfDialog);
      });
    }
    return this.alertify[dialogName];
  }

  dialogFactory(dialogTitle, typeOfDialog) {
    const factory = new DialogFactory(
      this.pgBrowser,
      this.jquery,
      this.alertify,
      this.dialogModel,
      this.backform,
      this.dialogContainerSelector);
    return factory.create(dialogTitle, typeOfDialog);
  }
}
