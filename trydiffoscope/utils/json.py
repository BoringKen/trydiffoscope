from __future__ import absolute_import

import json
import datetime

class JSONEncoder(json.JSONEncoder):
    def default(self, instance):
        if isinstance(instance, datetime.datetime):
            return instance.isoformat()

        return json.JSONEncoder.default(self, instance)
