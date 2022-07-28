# Install
## Python 3.9
https://www.python.org/downloads/release/python-3913/

## PIP 
For easy installation of other requirements below 
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```
 
## Node & npm
https://nodejs.org/en/download/

## PicoSDK
From https://www.picotech.com/downloads, download "Discontinued Products" > "PicoScope 2207A" > "Software" > "PicoSDK (64-bit) for Windows" 
```bash
pip install picosdk
pip install picoscope
```

## Python Libraries 
```bash
pip install matplotlib
pip install pandas
pip install scipy
```

# Run
```bash
# Install dependencies
npm install
# Run the app
npm start
```

# App Packaging
```bash
npm run package-win
```

# Files
- `package.json` - Points to the app's main file and lists its details and dependencies.
- `main.js` - Starts the app and creates a browser window to render HTML. This is the app's **main process**.
- `index.html` - A web page to render. This is the app's **renderer process**.

You can learn more about each of these components within the [Quick Start Guide](https://electronjs.org/docs/latest/tutorial/quick-start).
