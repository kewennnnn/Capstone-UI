# Install
## Python 3.9
https://www.python.org/downloads/release/python-3913/
 
## Node & npm
https://nodejs.org/en/download/

## PicoSDK
```bash
py -m  pip install picosdk
```
# Run
```bash
# Install dependencies
npm install
# Run the app
npm start
```
# Files
- `package.json` - Points to the app's main file and lists its details and dependencies.
- `main.js` - Starts the app and creates a browser window to render HTML. This is the app's **main process**.
- `index.html` - A web page to render. This is the app's **renderer process**.

You can learn more about each of these components within the [Quick Start Guide](https://electronjs.org/docs/latest/tutorial/quick-start).
