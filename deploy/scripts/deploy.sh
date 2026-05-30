#!/bin/bash
# Manual deploy — run on EC2 after git pull
set -e

cd /opt/techtrade-food/backend
source venv/bin/activate
pip install -r requirements.txt --quiet

sudo systemctl restart techtrade-food
sudo systemctl status techtrade-food --no-pager

echo "=== Deploy complete ==="