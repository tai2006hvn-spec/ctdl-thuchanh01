import sys

def bound(A, n, x, upper):
    lo = 0
    hi = n
    probes = 0
    while lo < hi:
        mid = lo + (hi - lo) // 2
        probes += 1
        if not upper:
            move_right = (A[mid] < x)
        else:
            move_right = (A[mid] <= x)
            
        if move_right:
            lo = mid + 1
        else:
            hi = mid
    return lo, probes


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    n = int(tokens[0])
    A = [int(tokens[i]) for i in range(1, n + 1)]
    x = int(tokens[n + 1])

    for i in range(1, n):
        if A[i - 1] > A[i]:
            print("ERROR: array must be sorted")
            sys.exit(1)

    lower, p1 = bound(A, n, x, upper=False)
    upper, p2 = bound(A, n, x, upper=True)

    first = -1
    if lower < n and A[lower] == x:
        first = lower
    count = upper - lower
    probes = p1 + p2

    print(f"FIRST {first}")
    print(f"COUNT {count}")
    print(f"LOWER {lower}")
    print(f"UPPER {upper}")
    print(f"PROBES {probes}")


if __name__ == "__main__":
    main()