# 🌿 Wellness Tracker

Personal tracker for Month 1 of a health program.

## Requirements

- Python 3.9+
- pip
- (optional) Docker, if running containerized
- (optional) Helm + a running Kubernetes cluster (minikube), if deploying to K8s

## Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run
python app.py
```

## Usage

Open your browser at: **http://localhost:5000**

Data is stored locally in the `wellness.db` file (SQLite).

## Tracked goals

- Water in the morning before coffee
- Food before coffee
- Max 2 coffees
- Stretching / posture, 10 min
- Exercise without stress
- Sleep at a consistent time
- Supplements (Mg, C, D3)
- Massage / physiotherapy

## Tracked symptoms (1–5 ★)

- Chest pain
- Shortness of breath
- Tachycardia
- Energy
- Sleep quality