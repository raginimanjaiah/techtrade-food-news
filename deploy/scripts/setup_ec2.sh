#!/bin/bash
# Run once on a fresh Ubuntu 24 EC2 instance
# Usage: bash setup_ec2.sh

set -e
echo "=== TechTrade.Food EC2 Setup ==="

# System packages
apt-get update -y
apt-get install -y python3-pip python3-venv postgresql postgresql-contrib redis-server nginx certbot python3-certbot-nginx git curl

# PostgreSQL
systemctl enable postgresql && systemctl start postgresql
sudo -u postgres psql -c "CREATE USER techtrade WITH PASSWORD 'changeme123';" || true
sudo -u postgres psql -c "CREATE DATABASE techtrade_food OWNER techtrade;" || true

# Redis
systemctl enable redis-server && systemctl start redis-server

# App directory
mkdir -p /opt/techtrade-food
cd /opt/techtrade-food

# Clone repo (update URL before running)
# git clone https://github.com/YOUR_ORG/techtrade-food-backend.git .

echo "=== System setup complete ==="
echo "Next: copy .env, run install_app.sh"