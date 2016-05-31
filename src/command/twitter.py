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

        self.yahoo_api_key = 'dj0zaiZpPVRBTTdlUTlncmVLTiZzPWNvbnN1bWVyc2VjcmV0Jng9MGQ-'

        self.auth = tw.OAuth(token,
                             token_key,
                             consumer_key,
                             consumer_secret)

        super().__init__(data)

        self.meter = 100

    def run(self):
        try:
            lat, lng = float(self.data[1]), float(self.data[2])
            box = self._gen_box_from_meter(lat, lng, self.meter)
        except (ValueError, IndexError):
            loc_name = self.data[1]
            box = self._get_box_from_loc_name(loc_name)

        yield from self._traffic(box)


    def _traffic(self, box, timeout_sec=5):
        yield {
            "data": "tweet start streaming ..."
        }

        start_time = datetime.now()
        result = []

        query = ",".join(map(str, box))
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

    def _gen_box_from_meter(self, lat: float, lng: float, meter):
        # http://oshiete.goo.ne.jp/qa/141526.html
        var_lat = meter / (1850 * 60)
        var_lng = meter / (1850 * 60 * cos(lng))

        result = [lng - var_lng,
                  lat - var_lat,
                  lng + var_lng,
                  lat + var_lat]

        return result

    def _get_box_from_loc_name(self, loc_name, box=True):
        loc_name = pathname2url(loc_name)
        api_url = 'http://geo.search.olp.yahooapis.jp/OpenLocalPlatform/V1/geoCoder?appid={0}&q={1}'
        api_url = api_url.format(self.yahoo_api_key, loc_name)

        req = urlopen(api_url)
        body = ''.join(map(lambda x: x.decode('utf-8'), req.readlines()))

        soup = BeautifulSoup(body).ydf
        geo = soup.feature

        if box:
            box = geo.find('boundingbox').get_text()
            box.replace(' ', ',')

            return box.split(',')
        else:
            coord = geo.find('coordinates').get_text()
            lng, lat = (float(v) for v in coord.split(','))
            return lng, lat

    @classmethod
    def command(cls):
        return 'twitter'


def large_than(loc1: list, loc2: list):
    pass
