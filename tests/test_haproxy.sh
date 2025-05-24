#!/bin/bash

LB_IP="34.220.9.184"
USER="ubuntu"
PORTS=(80 60000 60050 60200 60405 65000)
WEB_SERVERS=("35.92.62.198" "35.90.39.126")
LOG_PATH="/var/log/nginx/access.log"


echo -e "==== Testing HAProxy Load Balancer ====\n"

echo "==== Basic Content and Port Routing Test ===="
for port in "${PORTS[@]}"; do
  echo -e "\n --> Testing port $port\n"
  curl -s http://$LB_IP:$port | tee >(sed 's/^/    /')
  echo ""
  sleep 1
done

echo -e "\n\n==== Sticky Session Test (5 requests from same client) ====\n"
for i in {1..5}; do
  echo "Request $i:"
  curl -s http://$LB_IP | grep -oE '\- [AB]' || echo "No content"
  sleep 1
done

echo -e "\n\n==== Check for Client IP ===="

# Get my local public IP
MY_IP=$(curl -s ifconfig.me)
echo "Public IP: $MY_IP"

# Check the Servers for Client IP
TARGET_SERVER=""
for SERVER in "${WEB_SERVERS[@]}"; do
  echo -e "\nChecking server: $SERVER"

  LOG_MATCH=$(ssh -o StrictHostKeyChecking=no ${USER}@${SERVER} "sudo tail -n 10 $LOG_PATH" | grep "$MY_IP")

  if [[ -n "$LOG_MATCH" ]]; then
    TARGET_SERVER=$SERVER
    echo "Match found: $LOG_MATCH"
  else
    echo "No match found on $SERVER"
  fi
done

echo -e "\n\n====  Failover Test ===="

# Stop/Start Nginx on the target webserver
for action in stop start; do
  echo -e "\nRunning: \'sudo systemctl $action nginx\' on $TARGET_SERVER"
  ssh -o StrictHostKeyChecking=no ${USER}@${TARGET_SERVER} "sudo systemctl $action nginx"
  sleep 5

  # Observe HAProxy routing traffic to the remaining webserver and not failing back
  echo "Sending requests after $action:"
  for i in {1..5}; do
    echo "Request: $action-$i"
    curl -s http://$LB_IP | grep -oE '\- [AB]' || echo "No content"
    sleep 1
  done
done

echo -e "\n==== Done ===="