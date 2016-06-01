#!/usr/bin/env python
# coding: utf-8

import twitter as tw
from math import cos
from datetime import datetime
from urllib.request import urlopen, pathname2url
from bs4 import BeautifulSoup

from .command import Command
from .utils import timeout

class Twitter(Command):

    def __init__(self, data):
        token = '3132998455-VhvyIApFRecDu6e7Ro6bzu02nNtKV7ClOEXeeSZ'
        token_key = 'U1EbBib9gV3yG9pAAUZ42BzlYDxklFGvLEr0wSwxxUjld'
        consumer_key = 'rN94BWPXYM2gPkQ8O5fmZ6sul'
        consumer_secret = 'CUpuN2QpLYdAWQXSwGcIBWM3qlJctud0t8fmRQagv1YJ2XEV3u'

        self.yahoo_api_key = 'dj0zaiZpPVRBTTdlUTlncmVLTiZzPWNvbnN1bWVyc2VjcmV0Jng9MGQ-'

        super().__init__(data)

        self.auth = tw.OAuth(token, token_key, consumer_key, consumer_secret)

        self._add_option('-m', float, '100')
        self._add_option('--meter', float, '0')

        self._add_option('-w', float, '5')
        self._add_option('--wait', float, '0')

        self._add_option('--country', bool)
        self._add_option('--admin', bool)
        self._add_option('--city', bool)

        parse_result = self._parse_option()

        self.meter = parse_result['--meter'] or parse_result['-m']
        self.wait_time = parse_result['--wait'] or parse_result['-w']

        self.filter = []
        self.filter += ['country'] if parse_result['--country'] else []
        self.filter += ['admin'] if parse_result['--admin'] else []
        self.filter += ['city'] if parse_result['--city'] else []
        if not self.filter:
            self.filter = ['country', 'admin', 'city']

    def run(self):
        try:
            lat, lng = float(self.data[1]), float(self.data[2])
            box = self._gen_box_from_meter(lat, lng, self.meter)
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

            s, l = box.split(' ')
            lng_s, lat_s = s.split(',')
            lng_l, lat_l = l.split(',')

            return [float(v) for v in [lng_s, lat_s, lng_l, lat_l]]
        else:
            coord = geo.find('coordinates').get_text()
            lng, lat = (float(v) for v in coord.split(','))
            return lng, lat

    @classmethod
    def command(cls):
        return 'twitter'
