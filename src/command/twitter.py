#!/usr/bin/env python
# coding: utf-8

import twitter as tw
from math import cos
from datetime import datetime
from urllib.request import urlopen, pathname2url
from bs4 import BeautifulSoup

from .command import Command


class Twitter(Command):

    def __init__(self, data):
        token = '3132998455-VhvyIApFRecDu6e7Ro6bzu02nNtKV7ClOEXeeSZ'
        token_key = 'U1EbBib9gV3yG9pAAUZ42BzlYDxklFGvLEr0wSwxxUjld'
        consumer_key = 'rN94BWPXYM2gPkQ8O5fmZ6sul'
        consumer_secret = 'CUpuN2QpLYdAWQXSwGcIBWM3qlJctud0t8fmRQagv1YJ2XEV3u'

        super().__init__(data)

        self.auth = tw.OAuth(token, token_key, consumer_key, consumer_secret)
        self.meter = 100

    def run(self):
        try:
            lat, lng = float(self.data[1]), float(self.data[2])
        except (ValueError, IndexError):
            loc_name = self.data[1]
            lat, lng = self._get_topo_from_loc_name(loc_name)

        sq_loc = self._gen_sq_loc_from_meter(lat, lng, self.meter)

        yield from self._traffic(sq_loc)


    def _traffic(self, sq_loc, timeout_sec=5):
        yield {
            "data": "tweet start streaming ..."
        }

        start_time = datetime.now()
        result = []

        query = ",".join(map(str, sq_loc))
        itr = self._tweet_from_loc(query)

        for i in itr:
            result.append(i)
            now = datetime.now()
            if (now - start_time).seconds > timeout_sec:
                end_time = now
                break

        yield {
            'data': 'tweet get {num} tweet{s} in {time} sec'
            .format(**{
                'num': len(result),
                's': 's' if len(result) > 1 else '',
                'time': (now - start_time).seconds
            })
        }

        result = ['@{user}: {tweet} in {loc} ({place_type})'
                  .format(**{
                      'user': r['user']['screen_name'],
                      'tweet': r['text'],
                      'loc': r['place']['name'],
                      'place_type': r['place']['place_type']
                  }) for r in result]

        for r in result:
            yield {
                'data': r
            }

    def _get_stream(self):
        return tw.TwitterStream(auth=self.auth)

    def _tweet_from_loc(self, loc_var):
        st_client = self._get_stream()
        return st_client.statuses.filter(locations=loc_var)

    def _gen_sq_loc_from_meter(self, lat: float, lng: float, meter):
        # http://oshiete.goo.ne.jp/qa/141526.html
        var_lat = meter / (1850 * 60)
        var_lng = meter / (1850 * 60 * cos(lng))

        result = [lng - var_lng,
                  lat - var_lat,
                  lng + var_lng,
                  lat + var_lat]

        return result

    def _get_topo_from_loc_name(self, loc_name):
        loc_name = pathname2url(loc_name)
        api_url = 'http://www.geocoding.jp/api/?v=1.1&q={}'.format(loc_name)

        req = urlopen(api_url)
        body = ''.join(map(lambda x: x.decode('utf-8'), req.readlines()))
        soup = BeautifulSoup(body)

        lat = soup.find('lat').get_text()
        lng = soup.find('lng').get_text()

        return float(lat), float(lng)

    @classmethod
    def command(cls):
        return 'twitter'


def large_than(loc1: list, loc2: list):
    pass
