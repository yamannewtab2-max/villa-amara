#!/usr/bin/env python3
"""Build index.html for the Villa Amara demo.

One source of truth for every image URL: PICK maps slot -> index in urls.json
(the Flickr CDN URL chosen after visual curation). Re-run to regenerate.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
URLS = json.load(open('/tmp/urls.json'))

def U(i):
    u = URLS[str(i)]
    if not u:
        raise SystemExit(f'no url for index {i}')
    return u

PICK = {
    'hero':      [23, 38, 13, 2, 0],
    'band':      [51, 46, 63],
    'villa':     11,
    'suites':   [16, 1, 30],
    'gallery':  [7, 9, 12, 21, 124, 133, 151, 181],
}

SUITES = [
    dict(slot=0, name='Garden Suite', meta='64 m² · Private plunge pool · Valley side',
         txt='A single pavilion set into the terraces, with an outdoor bath and a daybed built for two.',
         price='$320'),
    dict(slot=1, name='Pool Pavilion', meta='96 m² · 12 m infinity edge · Rice-terrace view',
         txt='The largest of the pavilions, open on three sides, with a pool that runs to the edge of the valley.',
         price='$560'),
    dict(slot=2, name='Valley Residence', meta='180 m² · Two bedrooms · Butler &amp; car',
         txt='Two bedrooms, a private dining pavilion and a car with driver for the length of your stay.',
         price='$840'),
]

GALLERY = [
    (0, 'Pavilion pool, mid-morning'),
    (1, 'Rock pool &amp; water garden'),
    (2, 'The upper pool, treeline'),
    (3, 'Infinity edge at dusk'),
    (4, 'The beach, ten minutes down'),
    (5, 'Lights on the water, night'),
    (6, 'The house, evening'),
    (7, 'Stone bath, marble house'),
]

TICKER = ['Infinity pool', '24 h butler', 'Spa &amp; hammam', 'Private chef',
          'Rice-terrace walks', 'Airport transfer', 'Nine pavilions', 'Ayung valley']

BG = '<div class="bg"></div><div class="bg"></div>'

data = {
    'hero':  [U(i) for i in PICK['hero']],
    'band':  [U(i) for i in PICK['band']],
    'slots': {'villa': U(PICK['villa'])},
    'suites': [dict(img=U(PICK['suites'][s['slot']]), alt=s['name'], name=s['name'],
                    meta=s['meta'], txt=s['txt'], price=s['price']) for s in SUITES],
    'gallery': [dict(img=U(PICK['gallery'][slot]), cap=cap) for slot, cap in GALLERY],
    'ticker': TICKER,
}

html = (ROOT / 'index.tpl.html').read_text()
html = html.replace('%%BG%%', BG).replace('%%BG2%%', BG)
html = html.replace('%%DATA%%', json.dumps(data, ensure_ascii=False))
(ROOT / 'index.html').write_text(html)

print('index.html', len(html), 'bytes')
print('hero  ', len(data['hero']))
for s in data['suites']:
    print('suite ', s['name'], '->', s['img'].split('/')[-1])
print('gallery', len(data['gallery']))
assert all(data['hero']) and all(data['band'])
assert len(set(x['img'] for x in data['suites']) | set(g['img'] for g in data['gallery'])
           | set(data['hero']) | set(data['band']) | {data['slots']['villa']})
print('unique photos used:', len(set(data['hero']) | set(data['band']) | {data['slots']['villa']}
      | set(x['img'] for x in data['suites']) | set(g['img'] for g in data['gallery'])))
