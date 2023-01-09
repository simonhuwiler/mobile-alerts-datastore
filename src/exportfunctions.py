import requests
import hashlib
import datetime
import pandas as pd
from pathlib import Path
import os

def request_measurements(deviceid, day, phoneid):

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; Android SDK built for x86 Build/MASTER)',
        'Host': 'www.data199.com',
    }

    payload_token = {
        'devicetoken':    'empty',
        'vendorid':       '6c3cdebd-bc1e-4e7a-90ea-4b50ac19a980',
        'phoneid':        str(phoneid),
        'version':        '1.54',
        'build':          '201',
        'executable':     'eu.mobile_alerts.weatherhub',
        'bundle':         'eu.mobile_alerts.weatherhub',
        'lang':           'en',
        'timezoneoffset': '0',
        'timeampm':       'true',
        'usecelsius':     'true',
        'usemm':          'true',
        'speedunit':      '0',
        'ccon':           'false',
        'timestamp':      round(datetime.datetime.now().timestamp())
    }

    token = "&".join(list(map(lambda x: '%s=%s' % (x, payload_token[x]), payload_token)))
    token = token.replace('-','').replace(',','').replace('.','')#.replace('_','')
    token = token + 'uvh2r1qmbqk8dcgv0hc31a6l8s5cnb0ii7oglpfj'
    token = token.lower()

    m = hashlib.md5()
    m.update(token.encode("utf-8"))
    hexdig = m.hexdigest()

    dt_start = datetime.datetime.strptime("%s +0000" % day, '%Y-%m-%d %z').replace(hour=0, minute=0, second=0)
    dt_end = datetime.datetime.strptime("%s +0000" % day, '%Y-%m-%d %z').replace(hour=23, minute=59, second=59)

    payload_untoken = {
        'requesttoken':   hexdig,
        'deviceid':       deviceid,
        'from':           round(dt_start.timestamp()),
        'to':             round(dt_end.timestamp())
    }

    payload = dict(payload_token, **payload_untoken)

    url = 'https://www.data199.com/api/v1/device/measurements'

    r = requests.post(url, headers=headers, data=payload)
    return r.json()

def get_device_day(device_id, day, phoneid, ignore_empty = False):
    response = request_measurements(device_id, day, phoneid)

    # Check if Folder exists
    out = Path('./measurements/%s/' % device_id)
    if out.exists() == False:
        os.mkdir(out)

    # Parse response
    try:
        df = pd.DataFrame(response['result']['measurements'])

        if len(df) == 0:
            if ignore_empty == False:
                raise Exception("Antwort ist leer, keine Daten :(")
    except Exception:
        print(response)
        raise


    # Export
    df.to_csv(out / ('%s.csv' % day), index=False)