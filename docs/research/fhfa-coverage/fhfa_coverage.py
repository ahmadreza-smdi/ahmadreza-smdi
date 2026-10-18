"""Reproduce frozen FHFA endpoint-coverage counts, not price/rent comparisons."""
from pathlib import Path
from collections import defaultdict
import argparse
import csv
import hashlib
import io
import json
import sys

from _fhfa_source import read_hpi, read_geographies, xlsx_rows
from _whole_metros import read_supplement, merge_whole

ROOT = Path(__file__).resolve().parent
STATES = ('observed', 'missing_index', 'absent_row')
FILES = (
    'raw/fhfa-all-transactions-metro.csv',
    'raw/fhfa-hpi-specifications.xlsx',
    'raw/fhfa-whole-metros-with-divisions.xlsx',
    'raw/census-2023-cbsa-delineation.xlsx',
)
FIELDS = ['start', 'end', 'both_observed', 'not_both_observed', 'total_metros'] + [
    a+'__'+b for a in STATES for b in STATES]


def paired_rows(observations, years=5):
    if type(years) is not int or not 1 <= years <= 100:
        raise ValueError('Duration must be 1 through 100 calendar years')
    groups = defaultdict(dict)
    periods = []
    for row in observations:
        period = row['year']*4+row['quarter']-1
        if period in groups[row['code']]:
            raise ValueError('Duplicate metro-quarter')
        groups[row['code']][period] = row['index']
        periods.append(period)
    if not periods:
        raise ValueError('Empty source')
    def status(values, period):
        if period not in values:
            return 'absent_row'
        return 'missing_index' if values[period] is None else 'observed'
    def label(period):
        return f'{period//4}Q{period%4+1}'
    result = []
    for end in range(min(periods)+years*4, max(periods)+1):
        start = end-years*4
        counts = {a+'__'+b: 0 for a in STATES for b in STATES}
        for values in groups.values():
            counts[status(values, start)+'__'+status(values, end)] += 1
        both = counts['observed__observed']
        result.append({'start': label(start), 'end': label(end),
                       'both_observed': both, 'not_both_observed': len(groups)-both,
                       'total_metros': len(groups), **counts})
    return result


def rebuild_csv(root=ROOT):
    root = Path(root)
    manifest = json.loads((root/'SOURCES.json').read_text(encoding='utf-8'))
    entries = manifest.get('files') if isinstance(manifest, dict) else None
    if (not isinstance(entries, list) or len(entries) != len(FILES)
            or any(not isinstance(entry, dict)
                   or not isinstance(entry.get('file'), str)
                   or not isinstance(entry.get('sha256'), str)
                   or len(entry['sha256']) != 64
                   or any(c not in '0123456789abcdef' for c in entry['sha256'])
                   for entry in entries)
            or {entry['file'] for entry in entries} != set(FILES)):
        raise ValueError('Unexpected source manifest')
    # Read once, hash those bytes, then parse only private captured copies.
    raw = {name: (root/name).read_bytes() for name in FILES}
    for entry in entries:
        if hashlib.sha256(raw[entry['file']]).hexdigest() != entry['sha256']:
            raise ValueError('Source snapshot changed: '+entry['file'])
    # XLSX readers take paths; use a temporary mirror of the captured inputs.
    import tempfile
    with tempfile.TemporaryDirectory(prefix='fhfa-coverage-') as directory:
        private = Path(directory)
        for name, data in raw.items():
            target = private/name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        spec = list(xlsx_rows(private/FILES[1]))
        fields = [r for r in spec if r.get('J') == 'Index Standard Error'
                  and 'Metropolitan Statistical' in r.get('A', '')]
        if len(fields) != 1 or '1995Q1=100' not in fields[0].get('I', ''):
            raise ValueError('Unexpected FHFA field specification')
        main = read_hpi(io.StringIO(raw[FILES[0]].decode('utf-8'), newline=''))
        supplement = read_supplement(list(xlsx_rows(private/FILES[2])))
        geographies = read_geographies(private/FILES[3])
        whole = merge_whole(main, supplement, geographies)
    if len({r['code'] for r in whole}) != 386 or len(whole) != 79516:
        raise ValueError('Unexpected frozen whole-metro inventory')
    rows = paired_rows(whole)
    if len(rows) != 186:
        raise ValueError('Unexpected frozen pair count')
    output = io.StringIO(newline='')
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator='\r\n')
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, default=ROOT,
                        help='Directory containing SOURCES.json and the four raw snapshots')
    args = parser.parse_args()
    try:
        result = rebuild_csv(args.source_dir)
    except (ValueError, OSError) as exc:
        parser.exit(2, str(exc)+'\n')
    sys.stdout.buffer.write(result)


if __name__ == '__main__':
    main()
