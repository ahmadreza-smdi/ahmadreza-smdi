from pathlib import Path
from decimal import Decimal
import csv
import io
import json
import tempfile
import unittest

from fhfa_coverage import ROOT, FILES, paired_rows, rebuild_csv


class CoverageChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actual = rebuild_csv()

    def test_frozen_raw_rebuild_matches_all_previously_reviewed_rows(self):
        self.assertEqual(self.actual, (ROOT/'expected-coverage.csv').read_bytes())
        rows = list(csv.DictReader(io.StringIO(self.actual.decode('utf-8'))))
        self.assertEqual(len(rows), 186)
        self.assertEqual((rows[0]['start'], rows[-1]['end']), ('1975Q1', '2026Q2'))
        for row in rows:
            self.assertEqual(int(row['total_metros']), 386)
            self.assertEqual(sum(int(v) for k, v in row.items() if '__' in k), 386)

    def test_three_independently_reviewed_counterexamples(self):
        rows = {r['start']: r for r in csv.DictReader(io.StringIO(self.actual.decode('utf-8')))}
        for start, a, b, both in [('1976Q4',40,140,39), ('1979Q3',136,201,135),
                                  ('1990Q1',339,382,338)]:
            row = rows[start]
            self.assertEqual(sum(int(v) for k,v in row.items() if k.startswith('observed__')), a)
            self.assertEqual(sum(int(v) for k,v in row.items() if k.endswith('__observed')), b)
            self.assertEqual(int(row['both_observed']), both)
            self.assertGreater(min(a,b), both)

    def test_absent_and_blank_are_different(self):
        def row(code, year, index):
            return dict(code=code,year=year,quarter=1,index=index)
        rows = paired_rows([row('00001',2000,Decimal('100')),row('00001',2005,None),
                            row('00002',2000,Decimal('100')),row('00003',2005,Decimal('120'))])
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['observed__missing_index'],1)
        self.assertEqual(rows[0]['observed__absent_row'],1)
        self.assertEqual(rows[0]['absent_row__observed'],1)
        self.assertEqual(rows[0]['both_observed'],0)

    def test_changed_raw_snapshot_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'SOURCES.json').write_bytes((ROOT/'SOURCES.json').read_bytes())
            for name in FILES:
                target = root/name
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((ROOT/name).read_bytes())
            p = root/FILES[0]
            p.write_bytes(p.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError,'Source snapshot changed'):
                rebuild_csv(root)

    def test_unexpected_manifest_is_refused_before_reading_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'SOURCES.json').write_text(json.dumps({'files':[{'file':'../unexpected'}]*4}))
            with self.assertRaisesRegex(ValueError,'Unexpected source manifest'):
                rebuild_csv(root)


if __name__ == '__main__':
    unittest.main()
