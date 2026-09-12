import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    n = int(tokens[0])
    A = [int(tokens[i]) for i in range(1, n + 1)]
    x = int(tokens[n + 1])

    total = 0
    low = None
    high = None
    scan_visits = 0
    for val in A:
        scan_visits += 1
        total += val
        if low is None or val < low: low = val
        if high is None or val > high: high = val

    first_idx = -1
    search_cmps = 0
    for i, val in enumerate(A):
        search_cmps += 1
        if val == x:
            first_idx = i
            break

    pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            pairs += 1

    # 4. Vòng nhân đôi
    doubles = 0
    size = 1
    while size <= n:
        doubles += 1
        size *= 2

    print(f"SUM {total}")
    print(f"MIN {low if low is not None else 'NA'}")
    print(f"MAX {high if high is not None else 'NA'}")
    print(f"FIRST {first_idx}")
    print(f"SEARCH_CMPS {search_cmps}")
    print(f"PAIRS {pairs}")
    print(f"DOUBLINGS {doubles}")
    print(f"SCAN_VISITS {scan_visits}")

if __name__ == "__main__":
    main()