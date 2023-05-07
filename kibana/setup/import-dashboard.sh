#!/bin/sh

set -e

# Wait for Kibana to be ready
echo "Waiting for Kibana to be ready..."
until curl -s http://kibana:5601/api/status >/dev/null 2>&1; do
  echo "Kibana is not yet ready. Sleep for 5 seconds."
  sleep 5
done
echo "Kibana is ready!"

# Wait for Kibana's Import Obejcts API to return 200
# From experience, the API is only functional after a certain startup time
echo "Waiting for Kibana's Import Objects API to be ready. Requests might fail initially..."
while true; do
  set +e
  status_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://kibana:5601/api/saved_objects/_import -H "kbn-xsrf: true" --form file=@/assets/dashboard.ndjson)
  exit_code=$?
  set -e
  if [ $exit_code -eq 0 ] && [ $status_code -eq 200 ]; then
    echo "Received status code $status_code. The object import was successful!"
    break
  else
    echo "An error occurred when importing Kibana objects. Sleep for 5 seconds and try if the API is then functional."
    sleep 5
  fi
done

echo "The Kibana dashboard can now be used!"