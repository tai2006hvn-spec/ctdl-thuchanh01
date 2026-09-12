import sys

def merge_sort_records(A, lo, hi, buffer):
    if lo >= hi:
        return
    mid = (lo + hi) // 2
    merge_sort_records(A, lo, mid, buffer)
    merge_sort_records(A, mid + 1, hi, buffer)

    i = lo
    j = mid + 1
    out = lo

    while i <= mid and j <= hi:
        key_i = (A[i][0], A[i][1])
        key_j = (A[j][0], A[j][1])
        if key_i <= key_j:
            buffer[out] = A[i]
            i += 1
        else:
            buffer[out] = A[j]
            j += 1
        out += 1

    while i <= mid:
        buffer[out] = A[i]
        i += 1
        out += 1
    while j <= hi:
        buffer[out] = A[j]
        j += 1
        out += 1

    for k in range(lo, hi + 1):
        A[k] = buffer[k]


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    if len(tokens) < 2:
        print("ERROR: invalid data")
        sys.exit(1)

    try:
        n = int(tokens[0])
        k = int(tokens[1])
    except ValueError:
        print("ERROR: invalid data")
        sys.exit(1)

    if not (1 <= n <= 2000 and 1 <= k <= n):
        print("ERROR: invalid data")
        sys.exit(1)

    if len(tokens) != 2 + 4 * n + 2:
        print("ERROR: invalid data")
        sys.exit(1)

    try:
        qx = int(tokens[-2])
        qy = int(tokens[-1])
    except ValueError:
        print("ERROR: invalid data")
        sys.exit(1)

    if not (0 <= qx <= 10 and 0 <= qy <= 10):
        print("ERROR: invalid data")
        sys.exit(1)

    seen_ids = set()
    records = []
    idx = 2

    for _ in range(n):
        try:
            sample_id = int(tokens[idx])
            x = int(tokens[idx + 1])
            y = int(tokens[idx + 2])
            label = tokens[idx + 3]
        except ValueError:
            print("ERROR: invalid data")
            sys.exit(1)

        if not (1 <= sample_id <= 1000000) or (sample_id in seen_ids):
            print("ERROR: invalid data")
            sys.exit(1)
        seen_ids.add(sample_id)

        if not (0 <= x <= 10 and 0 <= y <= 10):
            print("ERROR: invalid data")
            sys.exit(1)
        if label not in ("A", "B"):
            print("ERROR: invalid data")
            sys.exit(1)

        d2 = (x - qx) * (x - qx) + (y - qy) * (y - qy)
        records.append([d2, sample_id, label])
        idx += 4

    buffer = [None] * n
    merge_sort_records(records, 0, n - 1, buffer)

    print(f"NEIGHBORS {k}")
    votes_a = 0
    votes_b = 0

    for i in range(k):
        d2, sample_id, label = records[i]
        print(f"{sample_id} {label} {d2}")
        if label == "A":
            votes_a += 1
        else:
            votes_b += 1

    print(f"VOTES A {votes_a} B {votes_b}")
    prediction = "A" if votes_a >= votes_b else "B"
    print(f"PREDICT {prediction}")


if __name__ == "__main__":
    main()