#!/usr/bin/env python
# coding: utf-8

import twitter as tw
from math import cos
from datetime import datetime

from .command import Command


class Twitter(Command):

    def __init__(self, data):
        token = '3132998455-VhvyIApFRecDu6e7Ro6bzu02nNtKV7ClOEXeeSZ'
        token_key = 'U1EbBib9gV3yG9pAAUZ42BzlYDxklFGvLEr0wSwxxUjld'
        consumer_key = 'rN94BWPXYM2gPkQ8O5fmZ6sul'
        consumer_secret = 'CUpuN2QpLYdAWQXSwGcIBWM3qlJctud0t8fmRQagv1YJ2XEV3u'

        #super().__init__(data)

        self.auth = tw.OAuth(token, token_key, consumer_key, consumer_secret)

    def run(self):
        pass

    def _traffic(self, loc_var, timeout_sec=5):
        start_time = datetime.now()
        result = []

        itr = self._tweet_from_loc(loc_var)

        for i in itr:
            result.append(i)
            now = datetime.now()
            if (now - start_time).seconds > timeout_sec:
                end_time = now
                break

        run_time = (end_time - start_time).seconds
        return {
            "data": len(result) / run_time
        }

    def _get_stream(self):
        return tw.TwitterStream(auth=self.auth)

    def _tweet_from_loc(self, loc_var):
        st_client = self._get_stream()
        return st_client.statuses.filter(locations=loc_var)

    def _gen_sq_loc_from_meter(self, latitude: float, longitude: float, meter):
        # http://oshiete.goo.ne.jp/qa/141526.html
        var_latitude = meter / (1850 * 60)
        var_longitude = meter / (1850 * 60 * cos(longitude))

        square = [longitude - var_longitude,
                  latitude - var_latitude,
                  longitude + var_longitude,
                  latitude + var_latitude]

        result = ",".join(map(str, square))
        return result

    @classmethod
    def command(cls):
        return 'twitter'






