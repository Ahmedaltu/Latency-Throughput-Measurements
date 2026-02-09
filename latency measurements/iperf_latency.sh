#!/bin/bash

SERVERS=(
  "ok1.iperf.dice-student.eu"
  "sgp1.iperf.dice-student.eu"
)

LOG=~/latency_task/logs/iperf.log
TS=$(date +"%Y-%m-%d %H:%M:%S")

for S in "${SERVERS[@]}"; do
  echo "===== $TS $S ping =====" >> "$LOG"
  ping -c 5 "$S" >> "$LOG"

  echo "===== $TS $S curl =====" >> "$LOG"
  curl -o /dev/null -s -w \
  "time_namelookup=%{time_namelookup} time_connect=%{time_connect}\n" \
  http://$S/1K.bin >> "$LOG"
done
