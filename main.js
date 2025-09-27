const {app, BrowserWindow} = require('electron')
//browserwindow generates a window (shocker)

let win = null;
const createWindow = () => {
    win = new BrowserWindow({
        //window properties
        width: 1200,
        height: 900,
        resizable: true,
        webPreferences: {
            //gives front end access to things
            nodeIntegration: true       //gives access to node functions in front end
        }
    })
    win.loadFile("index.html");        //loads html file

    
}



app.whenReady().then(createWindow);