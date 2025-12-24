# Ask Me Anything

Ask me anything application built with Flask and Flask-SocketIO

## Get Started
### Clone Project
```bash
git clone https://github.com/mohits-git/ask-me-anything
## navigate to the directory
# cd ask-me-anything
```
### With Docker Locally
1. Build
   ```bash
   docker build -t ask-me-anything .
   ```
2. Run
   ```bash
   docker run -p 5000:5000 ask-me-anything:latest
   ```
### Locally with python
1. Setup venv
   ```bash
   # create venv
   python -m venv .venv

   # activate venv
   source .venv/bin/activate

   ## to deactivate
   deactivate
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Start server
   ```bash
   ## development only
   flask --app "main:main()" run --debug
   # or
   python src/main.py

   ## production
   gunicorn --bind 127.0.0.1:5000 --worker-class eventlet -w 1 'main:main()'
   ```
> Open project in browser at [`http://localhost:5000`](http://localhost:5000)

## Features
- Create a AMA session with TTL or Live
- Share the AMA session link to anyone
- Protect the session via password to answer the asked question
- Ask and answer questions live anonymously
- End live sessions anytime.
- Sessions expires as per specified expiry time
