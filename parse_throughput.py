import re
import math
from statistics import mean, median

def percentile(data, p):
    if not data:
        return math.inf
    data = sorted(data)
    k = (len(data) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return data[int(k)]
    return data[f] + (data[c] - data[f]) * (k - f)

def mean_absolute_deviation(values):
    if not values:
        return math.inf
    m = mean(values)
    return mean([abs(x - m) for x in values])

def summarize(values):
    if not values:
        return {
            "runs": 0,
            "min": math.inf,
            "max": math.inf,
            "median": math.inf,
            "mean": math.inf,
            "mad": math.inf,
            "spread": math.inf
        }

    return {
        "runs": len(values),
        "min": min(values),
        "max": max(values),
        "median": median(values),
        "mean": mean(values),
        "mad": mean_absolute_deviation(values),
        "spread": percentile(values, 75) - percentile(values, 25)
    }

def fmt(x):
    if x == math.inf:
        return "inf"
    return f"{x:.3f}"

def main():
    log_file = "/home/altuwai/latency_task/throughput_logs/iperf_throughput.log"

    server_rates = {}
    current_server = None

    with open(log_file, "r", errors="ignore") as f:
        for line in f:
            # Header
            m = re.match(r"^===== .*? ([a-zA-Z0-9\.\-]+) TCP =====$", line.strip())
            if m:
                current_server = m.group(1)
                continue

            # Final sender bitrate line
            if current_server and "sender" in line:
                m = re.search(r"([\d\.]+)\s+Mbits/sec", line)
                if m:
                    rate = float(m.group(1))
                    server_rates.setdefault(current_server, []).append(rate)

    print("\nIPERF3 THROUGHPUT RESULTS (TCP sender bitrate)")
    print("---------------------------------------------------------------")
    print(f"{'Server':35} {'Runs':>4} {'Min':>8} {'Max':>8} {'Median':>8} {'Mean':>8} {'MAD':>8} {'Spread':>10}")

    for server in sorted(server_rates.keys()):
        stats = summarize(server_rates[server])
        print(
            f"{server:35} "
            f"{stats['runs']:4d} "
            f"{fmt(stats['min']):>8} "
            f"{fmt(stats['max']):>8} "
            f"{fmt(stats['median']):>8} "
            f"{fmt(stats['mean']):>8} "
            f"{fmt(stats['mad']):>8} "
            f"{fmt(stats['spread']):>10}"
        )

if __name__ == "__main__":
    main()
