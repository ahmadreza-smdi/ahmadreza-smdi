"""Read the FHFA all-transactions metro CSV using official specification row 20.

No HUD joining, return/yield estimation or uncertainty propagation occurs here.
"""
from pathlib import Path
from decimal import Decimal, InvalidOperation
import csv, hashlib, json, re, zipfile, xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parent
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def xlsx_rows(path):
    with zipfile.ZipFile(path) as z:
        strings = [''.join(s.itertext()) for s in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS)] if 'xl/sharedStrings.xml' in z.namelist() else []
        for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:row', NS):
            result = {}
            for c in row.findall('m:c', NS):
                value = c.find('m:v', NS)
                text = value.text if value is not None else ''
                if c.get('t') == 's': text = strings[int(text)]
                elif c.get('t') == 'inlineStr': text = ''.join(c.find('m:is', NS).itertext())
                result[re.sub(r'\d+', '', c.get('r'))] = text
            yield result

def decimal_or_missing(text, positive=False):
    if text.strip() in ('', '-'): return None
    # FHFA wraps the standard-error field in parentheses; this is not a negative amount.
    if not positive and re.fullmatch(r'\(\s*\d+(?:\.\d+)?\s*\)', text.strip()): text=text.strip()[1:-1].strip()
    try: value = Decimal(text)
    except InvalidOperation as exc: raise ValueError('Invalid number') from exc
    if not value.is_finite() or value < 0 or (positive and value == 0): raise ValueError('Invalid index or standard error')
    return value

def read_hpi(stream):
    records = []; seen = set(); names = {}
    for line, row in enumerate(csv.reader(stream), 1):
        if len(row) != 6: raise ValueError(f'Expected six fields at row {line}')
        name, code, year, quarter, index, error = row
        if not name.strip() or not re.fullmatch(r'\d{5}', code): raise ValueError(f'Invalid identity at row {line}')
        if not re.fullmatch(r'\d{4}', year) or quarter not in ('1','2','3','4'): raise ValueError(f'Invalid period at row {line}')
        key = (code, int(year), int(quarter))
        if key in seen: raise ValueError(f'Duplicate geography/quarter at row {line}')
        if code in names and names[code] != name: raise ValueError(f'Inconsistent geography label for {code}')
        seen.add(key); names[code] = name
        records.append({'source_row': line, 'name': name, 'code': code, 'year': int(year), 'quarter': int(quarter), 'index': decimal_or_missing(index, positive=True), 'index_standard_error': decimal_or_missing(error), 'raw_standard_error': error})
    return records

def read_geographies(path):
    rows = list(xlsx_rows(path))
    assert rows[2]['A'] == 'CBSA Code' and rows[2]['B'] == 'Metropolitan Division Code'
    geos = {}
    def add(code, name, kind, parent, county):
        if code not in geos: geos[code] = {'name': name, 'kind': kind, 'parent_cbsa': parent, 'counties': set()}
        g = geos[code]
        if (g['name'],g['kind'],g['parent_cbsa']) != (name,kind,parent): raise ValueError('Inconsistent geography definition')
        g['counties'].add(county)
    for row in rows[3:]:
        code = row.get('A','')
        if not re.fullmatch(r'\d{5}', code): continue
        county = row['J'].zfill(2) + row['K'].zfill(3)
        add(code,row['D'],'metro' if row['E']=='Metropolitan Statistical Area' else 'micro',code,county)
        if row.get('B'): add(row['B'],row['F'],'division',code,county)
    return geos

