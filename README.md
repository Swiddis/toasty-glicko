# Toasty Glicko

This small script is used for running a content difficulty rating system for language learners.
Google Forms input is piped into Google Sheets,
which this script processes to produce difficulty ratings with Glicko-2.

Currently it's very small, mostly thrown together during a 1-night hackathon.
It doesn't have any fancy auto-polling set up, it runs best with an hourly schedule in Cron.

## Setting Up

Install requirements, and run the script:

```sh
$ pip install -r requirements.txt
...
$ python3 main.py
...
Ratings Updated!
```
