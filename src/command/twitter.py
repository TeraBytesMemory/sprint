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
        token = ''
        token_key = ''
        consumer_key = ''
        consumer_secret = ''

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

        self._add_option('-h', bool)
        self._add_option('--help', bool)

        parse_result = self._parse_option()

        self.meter = parse_result['--meter'] or parse_result['-m']
        self.expand = parse_result['--expand'] or parse_result['-e']
        self.wait_time = parse_result['--wait'] or parse_result['-w']
        self.help = parse_result['--help'] or parse_result['-h']

        self.filter = []
        self.filter += ['country'] if parse_result['--country'] else []
        self.filter += ['admin'] if parse_result['--admin'] else []
        self.filter += ['city'] if parse_result['--city'] else []
        if not self.filter:
            self.filter = ['country', 'admin', 'city']

    def run(self):
        if self.help:
            yield from self._help()
            return

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

    def _help(self):
        doc = '''
usage: bot twitter [-e] [-h] [-m] [-w] [--admin] [--city] [--country] location ...

Twitter APIとGoogle Maps Geocoding APIを用いて、指定した箇所のツイートを収集する。
収集する際は、基本的には指定した制限時間内でのツイートを取得して返す。

必要な引数：
        location: 経度,緯度の順番の二つの少数の場合、入力した経度,緯度の位置を中心とした100mの正方形からツイートを探す。
                  また、地名を入力することも可能。入力した地名をGoogle Maps Geocodingで取得した場所のツイートを探す。

                  ex.) bot twitter 139.7528, 35.685175, bot twitter los angles
オプション;
        -e, --expand: 地名を入力した場合はその地域を含むような長方形内のツイートを探す。その長方形のサイズを周囲指定分メートルだけ広く収集できるようになる。（未指定の場合は拡張しない）
        ex.) bot twitter 渋谷 -e 100
        -h, --help: ヘルプコマンド。ツイートの収集は行わない。あとわかりにくくてごめんなさい。
        -m, --meter: 経度,緯度を入力した場合の正方形の大きさ。例えば、-m=100の場合は100mの正方形からツイートを探す。
                     (未指定の場合は100になる) ex.) bot twitter -m 200 139.7528, 35.685175
        -w, --wait: このオプションで指定した時間以内でツイートを取得する。未指定の場合は5秒以内でツイートを探す。指定時間よりもかかる場合もある。
                    ex.) bot twitter los angles -w 30
        --admin, --city, --country: 収集するツイートの属性を制限する。それぞれのオプションを指定した場合、それぞれ admin（県、地方）、city（市）、country（国）の属性を持つツイートのみを返す。ここでいう属性は、TwitterAPIのツイートで指定された場所の種類のことをいう。複数指定可能。
'''

        yield {
            'data': doc
        }

    @classmethod
    def command(cls):
        return 'twitter'
