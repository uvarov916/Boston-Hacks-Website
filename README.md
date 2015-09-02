# Boston Hacks website

Boston Hacks is Boston University's top hackathon. For 24 hours on October 31 to November 1, 2015, 500 students will come to Boston University, form teams around a problem or idea, and collaboratively code a unique solution from scratch.

Visit Boston Hacks at https://bostonhacks.io

## Requirements

You'll need to have the following items installed before continuing.

  * [Node.js](http://nodejs.org): Use the installer provided on the NodeJS website.
  * [Gulp](http://gulpjs.com/)
  * [Bower](http://bower.io): Run `[sudo] npm install -g bower`
  * Get pip
  * [Flask](http://flask.pocoo.org/docs/0.10/) Run `pip install Flask`
  * `pip install requests`
  * Add MLH credentials, client_id and client_secret, to creds.py `vim creds.py`

## How to start

```bash
git clone git@github.com:uvarovis/Boston-Hacks-Website.git
npm install && bower install
curl -O https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install Flask
pip install requests
# Add MLH credentials to creds.py
vim creds.py
```

While you're working on your project, run:

`gulp watch`

And you're set!

## creds.py

```
client_id = ''
client_secret = ''
```

### How to run

```
python __init__.py
```