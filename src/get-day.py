import argparse
import json
import exportfunctions
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('date', type=str, help='Datum (Format: 2021-01-31)')
args = parser.parse_args()

print("========================================")
print("Bestimmten Tag exportieren")
print("Datum: %s" % args.date)
print("========================================")

# Load Device-ID-List
config = json.load(open(Path('./config.json'), 'r'))

for device_id in config['devices']:
  print("Export %s %s" % (device_id, args.date))
  exportfunctions.get_device_day(device_id, args.date, config['phoneid'], True)

print("🙌 Done")