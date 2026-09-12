import sys

def insertion_sort(A, n):
    cmps = 0
    shifts = 0
    for i in range(1, n):
        key = A[i]
        j = i - 1
        while j >= 0:
            cmps += 1
            if A[j] <= key:
                break
            A[j + 1] = A[j]
            shifts += 1
            j -= 1
        A[j + 1] = key
    return cmps, shifts


def merge_sort_helper(A, lo, hi, buffer):
    if lo >= hi:
        return 0

    mid = (lo + hi) // 2
    cmps = 0
    cmps += merge_sort_helper(A, lo, mid, buffer)
    cmps += merge_sort_helper(A, mid + 1, hi, buffer)

    i = lo
    j = mid + 1
    out = lo

    while i <= mid and j <= hi:
        cmps += 1
        if A[i] <= A[j]:
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

    return cmps


def merge_sort(A, n):
    if n <= 1:
        return 0
    buffer = [0] * n
    return merge_sort_helper(A, 0, n - 1, buffer)


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    n = int(tokens[0])
    raw_A = [int(tokens[i]) for i in range(1, n + 1)]

    A_insert = raw_A.copy()
    A_merge = raw_A.copy()

    ins_cmps, ins_shifts = insertion_sort(A_insert, n)
    mrg_cmps = merge_sort(A_merge, n)

    print("INSERT", *A_insert)
    print(f"INSERT_CMPS {ins_cmps}")
    print(f"INSERT_SHIFTS {ins_shifts}")
    print("MERGE", *A_merge)
    print(f"MERGE_CMPS {mrg_cmps}")


if __name__ == "__main__":
    main()