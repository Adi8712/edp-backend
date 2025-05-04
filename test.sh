#!/bin/bash

API_URL="http://127.0.0.1:8000/api/sensor-data"

generate_vitals() {
    heart_rate=$((RANDOM % 41 + 60))
    spo2=$((RANDOM % 11 + 90))
    ecg=$((RANDOM % 1001 + 1000))
    temperature=$(awk -v min=36.5 -v max=37.5 'BEGIN{srand(); print min+rand()*(max-min)}')


    json_data=$(cat <<EOF
{
    "heart_rate": $heart_rate,
    "heart_rate_valid": 1,
    "spo2": $spo2,
    "spo2_valid": 1,
    "ecg": $ecg,
    "temperature": $temperature
}
EOF
    )

    curl -X POST "$API_URL" -H "Content-Type: application/json" -d "$json_data"
}

while true; do
    generate_vitals
    echo "Vitals posted successfully"
    sleep 2
done
