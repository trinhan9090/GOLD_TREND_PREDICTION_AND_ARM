"""Crawl a NEW Yahoo snapshot without overwriting the frozen FINAL data.

Example: python src/crawl/download_snapshot.py --output-dir D:/new_snapshot
The output directory must not exist. No download happens on import.
"""
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from urllib.request import Request, urlopen
from urllib.parse import quote
import argparse
import json
import pandas as pd

TICKERS = {'gold':'GC=F', 'oil':'CL=F', 'dollar_index':'DX-Y.NYB', 'sp500':'^GSPC'}

def fetch(source, start, end, name, output):
    first = int(pd.Timestamp(start, tz='UTC').timestamp())
    last = int(pd.Timestamp(end, tz='UTC').timestamp())
    url = (f'https://query1.finance.yahoo.com/v8/finance/chart/{quote(TICKERS[source], safe="")}'
           f'?period1={first}&period2={last}&interval=1d')
    with urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=45) as response:
        payload = json.load(response)
    if payload['chart'].get('error') or not payload['chart'].get('result'):
        raise ValueError(f'{source}: Yahoo did not return a valid result')
    provenance = output/'provenance'
    (provenance/f'{name}_response.json').write_text(json.dumps(payload), encoding='utf-8')
    result = payload['chart']['result'][0]
    zone = ZoneInfo(result['meta']['exchangeTimezoneName'])
    dates = [datetime.fromtimestamp(t, zone).date().isoformat() for t in result['timestamp']]
    quotes = result['indicators']['quote'][0]
    frame = pd.DataFrame({'Date':dates, **{k.title():quotes[k] for k in ['open','high','low','close','volume']}})
    frame['Date'] = pd.to_datetime(frame.Date)
    frame = frame.loc[frame.Date.ge(start) & frame.Date.lt(end)].copy()
    frame.loc[frame.Close.isna()].to_csv(provenance/f'{name}_unavailable_quotes.csv', index=False)
    frame = frame.loc[frame.Close.notna()].sort_values('Date').reset_index(drop=True)
    if frame.empty or frame.Date.duplicated().any() or frame.isna().any().any():
        raise ValueError(f'{source}: missing or duplicate observations')
    record = {'source':source, 'url':url, 'exchange_timezone':str(zone),
              'rows':len(frame), 'start':str(frame.Date.min().date()), 'end':str(frame.Date.max().date()),
              'retrieved_utc':datetime.now(timezone.utc).isoformat()}
    return frame, record

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', required=True, help='New snapshot directory; must not exist')
    args = parser.parse_args()
    output = Path(args.output_dir).resolve()
    if output.exists():
        raise ValueError('Output already exists. Use a new folder; never overwrite the frozen snapshot.')
    for name in ['raw','support','provenance']:
        (output/name).mkdir(parents=True, exist_ok=True)
    records = []
    for source,ticker in TICKERS.items():
        history, record = fetch(source,'2004-01-01','2005-01-01',f'{source}_warmup',output)
        history.to_csv(output/f'support/{source}_warmup.csv',index=False,date_format='%Y-%m-%d')
        records.append(record)
        frame, record = fetch(source,'2005-01-01','2026-09-19',f'{source}_snapshot',output)
        frame = frame.set_index('Date')[['Close','High','Low','Open','Volume']]
        frame.columns = pd.MultiIndex.from_tuples([(c,ticker) for c in frame.columns],names=['Price','Ticker'])
        frame.to_csv(output/f'raw/{source}.csv')
        records.append(record)
    support,record = fetch('gold','2026-09-19','2026-10-18','gold_horizon_support',output)
    support.to_csv(output/'support/gold_horizon_support.csv',index=False,date_format='%Y-%m-%d')
    records.append(record)
    (output/'provenance/download_manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    print('New snapshot saved:',output)
    print('Do not mix it with old model results; a refreshed snapshot requires a new experiment.')

if __name__ == '__main__':
    main()
