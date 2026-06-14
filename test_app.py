# test_app.py
import pytest
import json
from app import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        init_db()
        yield client

def test_index(client):
    res = client.get('/')
    assert res.status_code == 200

def test_save_and_get_day(client):
    data = {
        'checks': {'water': True, 'coffee': False},
        'symptoms': {'pain': 3, 'energy': 4},
        'notes': 'Test note'
    }
    res = client.post('/api/day/2024-01-01',
                      data=json.dumps(data),
                      content_type='application/json')
    assert res.status_code == 200
    assert res.json['ok'] == True

def test_get_day(client):
    res = client.get('/api/day/2024-01-01')
    assert res.status_code == 200
    assert 'checks' in res.json

def test_get_week(client):
    res = client.get('/api/week/2024-01-01')
    assert res.status_code == 200
    assert len(res.json) == 7