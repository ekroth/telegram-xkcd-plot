# Telegram XKCD Plot Bot

## Usage
- Create venv
`virtualenv --system-site-packages venv`
- Source environment
`source venv/bin/activate`
- Install dependencies
`pip install -r requirements.txt`
- Run
`python main.py`

## Issues
`matplotlib` might fail on OSX, export the following:
```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```
