# Telegram XKCD Plot Bot

## Usage
- Install `virtualenv`
`pip install virtualenv`
- Create venv
`virtualenv venv`
- Install dependencies
`pip install -r requirements.txt`
- Source environment
`source venv/bin/activate`
- Run
`python main.py`

## Issues
`matplotlib` might fail on OSX, export the following:
```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```
