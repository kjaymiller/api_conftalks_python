"""Schedule Emails That will Go Out that Day"""
from mongo import db, jsonify
from mail import send_event_email

import maya
import os


collection = db['events']

def mongo_dates_between(date_range=1):
    today = maya.now()
    between = {
            "$gt": today.add(days=-date_range).datetime(), 
            "$lt": today.add(days=date_range).datetime(),
        }
    return between

@jsonify
def get_upcoming_emails():
    todays_events = collection.find({
        "$or": [
            {'start_date': mongo_dates_between()},
            {'end_date': mongo_dates_between()},
            ]
        })
    return todays_events


if __name__=="__main__":
    upcoming_emails = get_upcoming_emails()
    print(upcoming_emails)

    for email in upcoming_emails:
        for user in email['subscribers']:
            print(user)
            send_event_email(user)    

