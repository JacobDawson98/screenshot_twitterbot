# Futurama Screens

Tweets random Futurama screenshots every hour. Automated using cron.

## Set up
  * Requires python3
  * Install required dependencies using `pip3 install -r requirements/base.txt`
  * Screenshots are kept in public/screens. When a screenshot is tweeted it is moved to public/screens/used.
  * twitterbot.py requires keys and secrets from the file .env kept in the root project directory.

## Default .env
```
API_KEY=<api key>
API_SECRET=<api secret>
OAUTH_TOKEN=<oauth token>
OAUTH_TOKEN_SECRET=<oauth token secret>
```
