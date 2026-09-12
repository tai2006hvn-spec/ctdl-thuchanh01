import sys

def bound(A, n, x, upper):
    """
    Tìm kiếm nhị phân trên khoảng nửa mở [lo, hi):
    - upper = False: tìm lower_bound (vị trí đầu tiên >= x)
    - upper = True:  tìm upper_bound (vị trí đầu tiên > x)
    """
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


def count_range(A, n, L, R):
    """
    Đếm số phần tử trong đoạn [L, R].
    Quy ước: Nếu L > R thì trả về 0.
    """
    if L > R:
        return 0, 0, 0, 0

    lower, p1 = bound(A, n, L, upper=False)
    upper, p2 = bound(A, n, R, upper=True)
    count = upper - lower
    total_probes = p1 + p2
    return count, lower, upper, total_probes


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    n = int(tokens[0])
    A = [int(tokens[i]) for i in range(1, n + 1)]
    L = int(tokens[n + 1])
    R = int(tokens[n + 2])

    # Kiểm tra tính chất không giảm của dãy
    for i in range(1, n):
        if A[i - 1] > A[i]:
            print("ERROR: array must be sorted")
            sys.exit(1)

    # Đếm số phần tử trong đoạn [L, R]
    count, lower, upper, probes = count_range(A, n, L, R)

    # In kết quả chuẩn
    print(f"QUERY_RANGE [{L}, {R}]")
    print(f"LOWER_L {lower}")
    print(f"UPPER_R {upper}")
    print(f"COUNT {count}")
    print(f"PROBES {probes}")


if __name__ == "__main__":
    main()