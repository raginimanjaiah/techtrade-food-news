#!/bin/bash
# Run after setup_ec2.sh and after repo is cloned to /opt/techtrade-food/backend
set -e

cd /opt/techtrade-food/backend

# Virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Apply DB migration
psql $DATABASE_URL -f app/migrations/001_articles.sql

echo "=== App installed ==="