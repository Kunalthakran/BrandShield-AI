"""
BrandShield AI - End-to-End Smoke Test Suite
Run: python smoke_test.py
"""
import os
import tempfile
import warnings
warnings.filterwarnings('ignore')

db_path = os.path.join(tempfile.gettempdir(), 'brandshield_smoke.db').replace('\\', '/')
os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'

try:
    if os.path.exists(db_path):
        os.remove(db_path)
except Exception:
    pass

from fastapi.testclient import TestClient
from main import app, Brand, Candidate, analyze

# 1. Detection Engine Unit Test
b = Brand(name='Nike', website='https://nike.com', official_social='@nike, @nikeindia', official_app='Nike', official_publisher='Nike, Inc.')
c_imposter = Candidate(brand_id=1, type='social', name='Nike Support 24/7', identifier='@nike_support247', publisher='Unknown', description='Official Nike customer support')
r1 = analyze(c_imposter, b)
assert r1['risk_score'] >= 70, f"Expected HIGH risk, got {r1['risk_score']}"
assert not r1['official_match']
print(f"PASS 1: Imposter detection -> {r1['risk_level']} {r1['risk_score']}/100")

c_official = Candidate(brand_id=1, type='social', name='Nike', identifier='@nike', publisher='Nike, Inc.', description='Official Instagram account')
r2 = analyze(c_official, b)
assert r2['risk_score'] == 0, f"Expected 0 risk score for official asset, got {r2['risk_score']}"
assert r2['official_match'] is True
assert r2['risk_level'] == 'SAFE'
print(f"PASS 2: Official asset exclusion -> {r2['risk_level']} {r2['risk_score']}/100 (100% IMMUNITY)")

# 2. Integration Tests via TestClient
client = TestClient(app)

# Health endpoint
res = client.get('/health')
assert res.status_code == 200
print("PASS 3: Health check endpoint -> OK")

# Static index.html endpoint
res = client.get('/')
assert res.status_code == 200
assert 'BrandShield AI' in res.text
assert 'Look-alike Lab (Req D)' in res.text
print("PASS 4: Static frontend UI served -> OK")

# 1-Click Demo Seed
res = client.post('/api/demo/seed')
assert res.status_code == 200
seed_data = res.json()
assert seed_data['brand']['name'] == 'Nike'
assert seed_data['candidate_count'] >= 9
print(f"PASS 5: Demo seed -> Loaded {seed_data['candidate_count']} candidate vectors")

# Threat Scan
scan_res = client.post('/api/scan', json={'brand_id': seed_data['brand']['id']})
assert scan_res.status_code == 200
results = scan_res.json()['results']
assert len(results) >= 9
print(f"PASS 6: Threat scan -> Evaluated {len(results)} assets")

# Look-alike Name Lab (Requirement D)
lab_res = client.post('/api/analyze/name', json={'official_name': 'Nike', 'candidate_name': 'Nik\u0435 Customer Care'})
assert lab_res.status_code == 200
lab_data = lab_res.json()
assert 'Unicode Homoglyph Spoofing' in lab_data['match_types']
print("PASS 7: Requirement D look-alike detection -> Homoglyphs detected accurately")

# CSV Report Export
csv_res = client.get('/api/export.csv')
assert csv_res.status_code == 200
assert 'Candidate ID,Type,Name' in csv_res.text
print("PASS 8: CSV Audit report generation -> OK")

print("\n[SUCCESS] ALL SMOKE TESTS PASSED - HACKATHON MVP IS 100% OPERATIONAL!")
