#!/bin/bash

SERVERS=(
  "ok1.iperf.dice-student.eu"
  "sgp1.iperf.dice-student.eu"
)

LOG=~/latency_task/throughput_logs/iperf_throughput.log
TS=$(date +"%Y-%m-%d %H:%M:%S")

for S in "${SERVERS[@]}"; do
  echo "===== $TS $S TCP =====" >> "$LOG"
  iperf3 -c "$S" -t 10 >> "$LOG"
done
