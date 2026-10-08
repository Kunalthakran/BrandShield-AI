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

# 2. Integration Tests via TestClients
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

# 9. Brand Profile Persistence & Singleton Tests
# Brand Creation & Refresh
brand_payload = {
    'name': 'Adidas',
    'website': 'https://adidas.com',
    'official_social': '@adidas',
    'official_app': 'Adidas App',
    'official_publisher': 'Adidas AG',
    'logo': 'https://adidas.com/logo.png'
}
save_res = client.post('/api/brand', json=brand_payload)
assert save_res.status_code == 200
saved_brand = save_res.json()
assert saved_brand['name'] == 'Adidas'
assert saved_brand['id'] is not None
brand_id = saved_brand['id']

get_res = client.get('/api/brand')
assert get_res.status_code == 200
refreshed = get_res.json()
assert refreshed['id'] == brand_id
assert refreshed['name'] == 'Adidas'
print("PASS 9: Brand profile persistence & refresh retrieval -> OK")

# Update singleton in-place
update_payload = {
    'name': 'Adidas Official',
    'website': 'https://adidas.com/global',
    'official_social': '@adidasoriginals',
    'official_app': 'Adidas Confirmed',
    'official_publisher': 'Adidas AG',
    'logo': ''
}
update_res = client.post('/api/brand', json=update_payload)
assert update_res.status_code == 200
assert update_res.json()['id'] == brand_id
assert update_res.json()['name'] == 'Adidas Official'
print("PASS 10: Brand profile update maintains singleton record -> OK")

# Rapid saves maintain singleton
for i in range(1, 6):
    rapid_res = client.post('/api/brand', json={'name': f'Brand V{i}'})
    assert rapid_res.status_code == 200
    assert rapid_res.json()['id'] == brand_id
print("PASS 11: 5 rapid consecutive saves maintain singleton row -> OK")

# Validation rejection for blank name
bad_res = client.post('/api/brand', json={'name': '   '})
assert bad_res.status_code == 422
print("PASS 12: Blank brand name rejected with 422 validation error -> OK")

print("\n[SUCCESS] ALL SMOKE & PERSISTENCE TESTS PASSED - HACKATHON MVP IS 100% OPERATIONAL!")

