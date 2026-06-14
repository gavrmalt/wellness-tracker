from flask import Flask, render_template, request, jsonify
import sqlite3, os
from datetime import datetime, date, timedelta

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), 'wellness.db')

# ── Database ──────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS days (
                date TEXT PRIMARY KEY,
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS checks (
                date TEXT,
                goal_id TEXT,
                done INTEGER DEFAULT 0,
                PRIMARY KEY (date, goal_id)
            );
            CREATE TABLE IF NOT EXISTS symptoms (
                date TEXT,
                symptom_id TEXT,
                rating INTEGER DEFAULT 0,
                PRIMARY KEY (date, symptom_id)
            );
        ''')

# ── Routes ────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/day/<day_date>', methods=['GET'])
def get_day(day_date):
    with get_db() as db:
        day = db.execute('SELECT * FROM days WHERE date=?', (day_date,)).fetchone()
        checks = db.execute('SELECT goal_id, done FROM checks WHERE date=?', (day_date,)).fetchall()
        syms = db.execute('SELECT symptom_id, rating FROM symptoms WHERE date=?', (day_date,)).fetchall()
    return jsonify({
        'date': day_date,
        'notes': day['notes'] if day else '',
        'checks': {r['goal_id']: bool(r['done']) for r in checks},
        'symptoms': {r['symptom_id']: r['rating'] for r in syms}
    })

@app.route('/api/day/<day_date>', methods=['POST'])
def save_day(day_date):
    data = request.json
    with get_db() as db:
        db.execute('INSERT OR REPLACE INTO days (date, notes) VALUES (?,?)',
                   (day_date, data.get('notes', '')))
        for goal_id, done in data.get('checks', {}).items():
            db.execute('INSERT OR REPLACE INTO checks (date, goal_id, done) VALUES (?,?,?)',
                       (day_date, goal_id, 1 if done else 0))
        for sym_id, rating in data.get('symptoms', {}).items():
            db.execute('INSERT OR REPLACE INTO symptoms (date, symptom_id, rating) VALUES (?,?,?)',
                       (day_date, sym_id, rating))
    return jsonify({'ok': True})

@app.route('/api/week/<start_date>', methods=['GET'])
def get_week(start_date):
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    days_data = []
    with get_db() as db:
        for i in range(7):
            d = str(start + timedelta(days=i))
            day = db.execute('SELECT * FROM days WHERE date=?', (d,)).fetchone()
            checks = db.execute('SELECT goal_id, done FROM checks WHERE date=?', (d,)).fetchall()
            syms = db.execute('SELECT symptom_id, rating FROM symptoms WHERE date=?', (d,)).fetchall()
            days_data.append({
                'date': d,
                'notes': day['notes'] if day else '',
                'checks': {r['goal_id']: bool(r['done']) for r in checks},
                'symptoms': {r['symptom_id']: r['rating'] for r in syms}
            })
    return jsonify(days_data)

if __name__ == '__main__':
    init_db()
    print('\n🌿 Wellness Tracker')
    print('➜  http://localhost:5000\n')
    app.run(debug=True, host="0.0.0.0", port=5000)