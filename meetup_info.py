#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import json
from datetime import datetime, timedelta

import pytz


class Meetup(object):

    def __init__(self):
        self._duration = 0
        self._date = ''
        self.name = ''
        self.venue_name = ''
        self.venue_address = ''
        self.fee = 0
        self.rsvp = 0
        self.attended = 0
        self.event_url = ''

    def __repr__(self):
        return '{date},"{name}","{venue_name}","{venue_address}",{fee},{rsvp},{attended},"{duration}","{event_url}"'.format(
            **self.to_dict())

    def to_dict(self):
        return {
            'date': self.date,
            'duration': self.duration,
            'name': self.name,
            'venue_name': self.venue_name,
            'venue_address': self.venue_address,
            'fee': self.fee,
            'rsvp': self.rsvp,
            'attended': self.attended,
            'event_url': self.event_url
        }

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, epoch_date):
        epoch_date = epoch_date / 1000.0
        self._date = datetime.fromtimestamp(epoch_date, pytz.utc)
        self._date = self._date.strftime('%Y_%m_%d_%H:%M')

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration_ms):
        self._duration = timedelta(milliseconds=duration_ms)


def main(json_file, csv_file):
    """Import json data create csv"""
    meetups = []
    with open(json_file) as f:
        json_data = json.load(f)
    raw_meetups = json_data['results']
    for raw_meetup in raw_meetups:
        meetup = Meetup()
        meetup.date = raw_meetup['time']
        duration = raw_meetup.get('duration')
        if duration:
            meetup.duration = duration
        meetup.name = raw_meetup['name']
        venue = raw_meetup.get('venue')
        if venue:
            meetup.venue_name = raw_meetup['venue']['name']
            meetup.venue_address = raw_meetup['venue']['address_1']
        fee = raw_meetup.get('fee')
        if fee:
            meetup.fee = fee['amount']
        meetup.rsvp=raw_meetup['yes_rsvp_count']
        meetup.attended=raw_meetup['headcount']
        meetup.event_url=raw_meetup['event_url']
        meetups.append(meetup)
    with open(csv_file, 'w') as f:
        headers = "Date,Name,Venue Name,Venue Address,Fee,RSVP,Attended,Duration,Event URL"
        f.write('{}\n'.format(headers))
        for meetup in meetups:
            print(meetup)
            f.write('{}\n'.format(str(meetup)))

def _cli():
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            argument_default=argparse.SUPPRESS)
    parser.add_argument('-j', '--json_file', help="Load data from this file.")
    parser.add_argument('-c', '--csv_file', help="Load data from this file.")
    args = parser.parse_args()
    return vars(args)

if __name__ == '__main__':
    main(**_cli())

