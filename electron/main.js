const TabGroup = require('electron-tabs');
const dragula = require('dragula');
const {ipcRenderer} = require('electron');

const tabInfo = {
    title: 'Home',
    src: './app.html',
    webviewAttributes: {
        'nodeintegration': true
    },
    icon: 'fa fa-home',
    visible: true,
    closable: false,
    active: true,
    ready: tab => {
        // Open dev tools for webview
        // let webview = tab.webview;
        // if (!!webview) {
        //     webview.addEventListener('dom-ready', () => {
        //         webview.openDevTools({mode: 'detach'});
        //     })
        // }
    }
};

const tabGroup = new TabGroup({
    newTab: tabInfo,
    closeButtonText: '&#x2715;',
    ready: tabGroup => {
        dragula([tabGroup.tabContainer], {
            direction: 'horizontal'
        });
    }
});

tabGroup.addTab();

ipcRenderer.on('tabs-channel', (event, arg) => {
    if(arg === 'create') {
        tabGroup.addTab();
    }
});
