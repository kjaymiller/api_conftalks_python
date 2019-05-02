"""Schedule Emails That will Go Out that Day"""
from mongo import db, jsonify_results

import maya
import requests


collection = db['events']

def mongo_dates_between(key, days=1):
    today = maya.now()
    return {
        key: {
            "$gt": today.add(days=-days).datetime(), 
            "$lt": today.add(days=days).datetime(),
            }
        }

@jsonify_results
def get_upcoming_emails():
    today = maya.now()
    todays_events = collection.find({
        "$or": [
            mongo_dates_between('event_start'),
            mongo_dates_between('event_end')
            ]
        })
    return todays_events


if __name__=="__main__":
    print(get_upcoming_emails())
    
