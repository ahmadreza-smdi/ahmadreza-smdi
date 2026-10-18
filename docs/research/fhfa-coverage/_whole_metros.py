"""Combine official whole-metro series; never aggregate division indexes."""
from collections import defaultdict, Counter
from decimal import Decimal
import csv, hashlib, json, re
from _fhfa_source import ROOT, xlsx_rows, decimal_or_missing, read_hpi, read_geographies

def read_supplement(rows):
    if not rows or 'All-Transactions' not in rows[0].get('A',''): raise ValueError('Unexpected index family')
    if not any('1995:Q1=100' in r.get('A','') and 'NSA' in r.get('A','') for r in rows[:4]): raise ValueError('Expected same index base and adjustment')
    header={'A':'cbsa_code','B':'metro_name','C':'yr','D':'qtr','E':'index_nsa'}
    positions=[i for i,r in enumerate(rows) if all(r.get(k)==v for k,v in header.items())]
    if len(positions)!=1: raise ValueError('Expected unique labeled header')
    result=[];seen=set();names={}
    for i,r in enumerate(rows[positions[0]+1:],positions[0]+2):
        if not any(r.values()):continue
        code=r.get('A','');name=r.get('B','');year=r.get('C','');quarter=r.get('D','')
        if not re.fullmatch(r'\d{5}',code) or not name or not re.fullmatch(r'\d{4}',year) or quarter not in ('1','2','3','4'):raise ValueError(f'Invalid supplemental row {i}')
        key=(code,int(year),int(quarter))
        if key in seen:raise ValueError('Duplicate supplemental geography/quarter')
        if code in names and names[code]!=name:raise ValueError('Supplemental identity changed')
        names[code]=name;seen.add(key)
        result.append({'source_row':i,'source_file':'raw/fhfa-whole-metros-with-divisions.xlsx','name':name,'code':code,'year':int(year),'quarter':int(quarter),'index':decimal_or_missing(r.get('E',''),positive=True),'index_standard_error':None,'standard_error_status':'not_supplied_in_supplement'})
    return result

def merge_whole(main,supplement,geos):
    direct={r['code'] for r in main if geos.get(r['code'],{}).get('kind')=='metro'}
    supplements={r['code'] for r in supplement}
    if direct & supplements:raise ValueError('Overlapping whole-metro sources; reconcile rather than overwrite')
    if any(geos.get(code,{}).get('kind')!='metro' for code in supplements):raise ValueError('Supplement code is not verified whole metro')
    out=[]
    for r in main:
        if r['code'] in direct:
            out.append({**r,'source_file':'raw/fhfa-all-transactions-metro.csv','standard_error_status':'missing' if r['index_standard_error'] is None else 'supplied'})
    out.extend(supplement)
    keys=[(r['code'],r['year'],r['quarter']) for r in out]
    if len(set(keys))!=len(keys):raise ValueError('Duplicate whole-metro observations')
    return sorted(out,key=lambda r:(r['code'],r['year'],r['quarter']))

