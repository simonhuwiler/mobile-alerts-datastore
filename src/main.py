import json
import exportfunctions
from pathlib import Path
import datetime

# Load Device-ID-List
config = json.load(open(Path('./config.json'), 'r'))

# Get Yesterday
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
day = yesterday.strftime('%Y-%m-%d')

for device_id in config['devices']:
  print("Export %s %s" % (device_id, day))
  exportfunctions.get_device_day(device_id, day, config['phoneid'])

print("🙌 Done")