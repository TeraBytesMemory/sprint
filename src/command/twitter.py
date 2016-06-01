#!/usr/bin/env python
# coding: utf-8

import twitter as tw
from math import cos
from datetime import datetime
from urllib.request import urlopen, pathname2url
import json

from .command import Command
from .utils import timeout

class Twitter(Command):

    def __init__(self, data):
        token = '3132998455-VhvyIApFRecDu6e7Ro6bzu02nNtKV7ClOEXeeSZ'
        token_key = 'U1EbBib9gV3yG9pAAUZ42BzlYDxklFGvLEr0wSwxxUjld'
        consumer_key = 'rN94BWPXYM2gPkQ8O5fmZ6sul'
        consumer_secret = 'CUpuN2QpLYdAWQXSwGcIBWM3qlJctud0t8fmRQagv1YJ2XEV3u'

        super().__init__(data)

        self.auth = tw.OAuth(token, token_key, consumer_key, consumer_secret)

        self._add_option('-m', float, '100')
        self._add_option('--meter', float, '0')

        self._add_option('-e', float, '0')
        self._add_option('--expand', float, '0')

        self._add_option('-w', float, '5')
        self._add_option('--wait', float, '0')

        self._add_option('--country', bool)
        self._add_option('--admin', bool)
        self._add_option('--city', bool)

        parse_result = self._parse_option()

        self.meter = parse_result['--meter'] or parse_result['-m']
        self.expand = parse_result['--expand'] or parse_result['-e']
        self.wait_time = parse_result['--wait'] or parse_result['-w']

        self.filter = []
        self.filter += ['country'] if parse_result['--country'] else []
        self.filter += ['admin'] if parse_result['--admin'] else []
        self.filter += ['city'] if parse_result['--city'] else []
        if not self.filter:
            self.filter = ['country', 'admin', 'city']

    def run(self):
        try:
            lng, lat = float(self.data[1]), float(self.data[2])
            box = self._gen_box_from_meter(lng, lat, self.meter)
        except (ValueError, IndexError):
            loc_name = ' '.join(self.data[1:])
            box = self._get_box_from_loc_name(loc_name)

        yield from self._traffic(box, self.wait_time)

    def _traffic(self, sq_loc, timeout_sec):
        yield {
            "data": "tweet start streaming ..."
        }

        start_time = datetime.now()
        result = []

        query = ",".join(map(str, sq_loc))
        itr = self._tweet_from_loc(query)

        try:
            with timeout(int(timeout_sec)):
                for i in itr:
                    if i['place']['place_type'] in self.filter:
                        result.append(i)
        except TimeoutError:
            now = datetime.now()

        result = ['@{user}: {tweet} in {loc} ({place_type})'
                  .format(**{
                      'user': r['user']['screen_name'],
                      'tweet': r['text'],
                      'loc': r['place']['name'],
                      'place_type': r['place']['place_type']
                  }) for r in result]

        yield {
            'data': 'tweet get {num} tweet{s} in {time} sec'
            .format(**{
                'num': len(result),
                's': 's' if len(result) > 1 else '',
                'time': (now - start_time).seconds
            })
        }

        for r in result:
            yield {
                'data': r
            }

    def _get_stream(self):
        return tw.TwitterStream(auth=self.auth)

    def _tweet_from_loc(self, loc_var):
        st_client = self._get_stream()
        return st_client.statuses.filter(locations=loc_var)

    def _gen_box_from_meter(self, lng: float, lat: float, meter):
        # http://oshiete.goo.ne.jp/qa/141526.html
        var_lng, var_lat = self._meter_to_geo(lng, lat, meter)

        result = [lng - var_lng,
                  lat - var_lat,
                  lng + var_lng,
                  lat + var_lat]

        return result

    def _get_box_from_loc_name(self, loc_name):
        loc_name = pathname2url(loc_name)
        api_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}'
        api_url = api_url.format(loc_name)

        req = urlopen(api_url)
        body = ''.join(map(lambda x: x.decode('utf-8'), req.readlines()))

        result = json.loads(body)['results'][0]
        geo_box = result['geometry']['bounds']

        box = [geo_box['southwest']['lng'],
               geo_box['southwest']['lat'],
               geo_box['northeast']['lng'],
               geo_box['northeast']['lat']]

        if self.expand:
            mid = [(box[2] - box[0]) / 2 + box[0],
                   (box[3] - box[1]) / 2 + box[1]]
            var_lng, var_lat = self._meter_to_geo(mid[0], mid[1], self.expand)
            box[0] -= var_lng
            box[1] -= var_lat
            box[2] += var_lng
            box[3] += var_lat

        return box

    def _meter_to_geo(self, lng: float, lat: float, meter):
        var_lng = meter / (1850 * 60)
        var_lat = meter / (1850 * 60 * cos(lng))

        return var_lng, var_lat

    @classmethod
    def command(cls):
        return 'twitter'
