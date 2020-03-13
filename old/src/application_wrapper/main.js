'use strict';

let { app, BrowserWindow } = require('electron');

app.on('ready', function() {
    let mainWindow = new BrowserWindow();
    mainWindow.loadURL('file://' + __dirname + '/app/index.html');
});