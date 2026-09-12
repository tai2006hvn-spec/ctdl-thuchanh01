#!/usr/bin/env python3
"""Independent, deterministic tests for the four lab programs; stdlib only.

Run from any directory: python tests/verify.py
Optional: --cpp C:/path/to/g++.exe --julia C:/path/to/julia.exe
The verifier never installs dependencies. Missing runtimes are reported as skipped.
"""
from __future__ import annotations

import argparse
import bisect
import datetime as dt
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
SEED = 13060102


def case(name, text, expected, code=0):
    return {"name": name, "input": text, "expected": expected, "code": code}


def oracle01(a, target):
    first = a.index(target) if target in a else -1
    return "\n".join([
        f"SUM {sum(a)}",
        f"MIN {min(a) if a else 'NA'}",
        f"MAX {max(a) if a else 'NA'}",
        f"FIRST {first}",
        f"SEARCH_CMPS {first + 1 if first >= 0 else len(a)}",
        f"PAIRS {len(a) * (len(a) - 1) // 2}",
        f"DOUBLINGS {len(a).bit_length()}",
        f"SCAN_VISITS {len(a)}",
    ]) + "\n"


def merge_comparisons(a):
    """Count via sorted subranges, independent of students' merge output.

    Inclusive midpoint means the left side has ceil(n/2) items.
    """
    if len(a) <= 1:
        return 0
    split = (len(a) + 1) // 2
    left, right = sorted(a[:split]), sorted(a[split:])
    i = j = count = 0
    while i < len(left) and j < len(right):
        count += 1
        if left[i] <= right[j]:
            i += 1
        else:
            j += 1
    return (count + merge_comparisons(a[:split])
            + merge_comparisons(a[split:]))


def oracle02(a):
    # Every inversion causes precisely one insertion shift.
    shifts = sum(a[i] > a[j] for j in range(len(a)) for i in range(j))
    # Each step compares its greater predecessors and, if one exists,
    # the rightmost predecessor <= key (the final failed comparison).
    failed = sum(any(v <= a[j] for v in a[:j]) for j in range(1, len(a)))
    suffix = (" " + " ".join(map(str, sorted(a)))) if a else ""
    return (f"INSERT{suffix}\nINSERT_CMPS {shifts + failed}\n"
            f"INSERT_SHIFTS {shifts}\nMERGE{suffix}\n"
            f"MERGE_CMPS {merge_comparisons(a)}\n")


def boundary_probes(n, boundary):
    # Derive path from the already known insertion position, not key comparisons.
    lo, hi, probes = 0, n, 0
    while lo < hi:
        mid = (lo + hi) // 2
        probes += 1
        if mid < boundary:
            lo = mid + 1
        else:
            hi = mid
    return probes


def oracle03(a, target):
    lower, upper = bisect.bisect_left(a, target), bisect.bisect_right(a, target)
    first = lower if lower < upper else -1
    probes = boundary_probes(len(a), lower) + boundary_probes(len(a), upper)
    return (f"FIRST {first}\nCOUNT {upper - lower}\nLOWER {lower}\n"
            f"UPPER {upper}\nPROBES {probes}\n")


def oracle04(rows, query, k):
    qx, qy = query
    neighbors = sorted(
        (((x - qx) ** 2 + (y - qy) ** 2, ident, label)
         for ident, x, y, label in rows),
        key=lambda item: (item[0], item[1]),
    )[:k]
    votes_a = sum(label == "A" for _, _, label in neighbors)
    votes_b = k - votes_a
    lines = [f"NEIGHBORS {k}"]
    lines += [f"{ident} {label} {distance}"
              for distance, ident, label in neighbors]
    lines += [f"VOTES A {votes_a} B {votes_b}",
              f"PREDICT {'A' if votes_a >= votes_b else 'B'}"]
    return "\n".join(lines) + "\n"


def array_input(a, target=None):
    text = f"{len(a)}\n" + " ".join(map(str, a)) + "\n"
    return text + (f"{target}\n" if target is not None else "")


def knn_input(rows, query, k):
    return (f"{len(rows)} {k}\n"
            + "".join(" ".join(map(str, row)) + "\n" for row in rows)
            + f"{query[0]} {query[1]}\n")


def build_cases(random_count):
    rng = random.Random(SEED)
    all_cases = {f"bai{i:02d}": [] for i in range(1, 5)}
    a_cases = [
        ("empty", [], 4), ("singleton_found", [3], 3),
        ("singleton_absent", [3], -1),
        ("all_equal", [4] * 8, 4),
        ("negative_duplicates", [-8, -1, -8, 0, 7], -8),
        ("ascending", list(range(-8, 9)), 8),
        ("descending", list(range(8, -9, -1)), -9),
        ("sample", [7, 2, 5, 2, 9, 1], 2),
        ("limits", [-1000000, 1000000, 0, -1000000], 1000000),
    ]
    for i in range(random_count):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 35))]
        target = rng.choice(a) if a and i % 2 else rng.randint(-25, 25)
        a_cases.append((f"random_{i:02d}", a, target))
    for name, a, target in a_cases:
        all_cases["bai01"].append(case(name, array_input(a, target), oracle01(a, target)))
        all_cases["bai02"].append(case(name, array_input(a), oracle02(a)))
        ordered = sorted(a)
        all_cases["bai03"].append(case(name, array_input(ordered, target),
                                             oracle03(ordered, target)))
    for name, a, target in [
        ("target_below", [-4, 0, 0, 5], -5),
        ("target_above", [-4, 0, 0, 5], 6),
        ("target_gap", [-4, 0, 0, 5], 3),
        ("duplicate_block_at_end", [-4, 0, 5, 5, 5], 5),
    ]:
        all_cases["bai03"].append(case(name, array_input(a, target), oracle03(a, target)))
    all_cases["bai03"].append(case(
        "reject_unsorted", array_input([1, 4, 3, 9], 3),
        "ERROR: array must be sorted\n", 1))
    rows = [(1, 1, 1, "A"), (2, 2, 1, "A"), (3, 2, 3, "A"),
            (4, 6, 5, "B"), (5, 7, 7, "B"), (6, 8, 6, "B")]
    knn_cases = [
        ("sample", rows, (4, 4), 3),
        ("k_one", rows, (4, 4), 1),
        ("k_n_vote_tie", rows, (4, 4), 6),
        ("k_two_vote_tie", rows, (4, 4), 2),
        ("singleton", [(9, 10, 10, "B")], (0, 0), 1),
        ("distance_tie_reordered_ids", [(9, 4, 5, "B"), (2, 6, 5, "A"),
                                        (7, 5, 4, "B"), (1, 5, 6, "A")], (5, 5), 3),
        ("exact_match_tie", [(12, 4, 4, "B"), (2, 4, 4, "A")], (4, 4), 1),
        ("coordinate_extremes", [(1, 0, 0, "A"), (2, 10, 10, "B")], (10, 10), 1),
    ]
    for i in range(random_count):
        n = rng.randint(1, 35)
        ids = rng.sample(range(1, 100001), n)
        sample = [(ident, rng.randint(0, 10), rng.randint(0, 10),
                   rng.choice(["A", "B"])) for ident in ids]
        knn_cases.append((f"random_{i:02d}", sample,
                          (rng.randint(0, 10), rng.randint(0, 10)), rng.randint(1, n)))
    for name, sample, query, k in knn_cases:
        all_cases["bai04"].append(case(name, knn_input(sample, query, k),
                                             oracle04(sample, query, k)))
    invalid = [
        ("invalid_k_zero", rows, (4, 4), 0),
        ("invalid_k_negative", rows, (4, 4), -1),
        ("invalid_k_too_large", rows, (4, 4), 7),
        ("duplicate_id", [(1, 1, 1, "A"), (1, 2, 2, "B")], (4, 4), 1),
        ("unsupported_label", [(1, 1, 1, "C")], (4, 4), 1),
        ("coordinate_below", [(1, -1, 1, "A")], (4, 4), 1),
        ("coordinate_above", [(1, 1, 11, "A")], (4, 4), 1),
        ("query_coordinate_below", [(1, 1, 1, "A")], (-1, 4), 1),
        ("query_coordinate_above", [(1, 1, 1, "A")], (4, 11), 1),
    ]
    for name, sample, query, k in invalid:
        all_cases["bai04"].append(case(name, knn_input(sample, query, k),
                                             "ERROR: invalid data\n", 1))
    return all_cases


def find_executable(requested, candidates):
    if requested:
        path = Path(requested)
        return str(path.resolve()) if path.is_file() else shutil.which(requested)
    return next((found for name in candidates if (found := shutil.which(name))), None)


def execute(command, text, timeout):
    start = time.perf_counter()
    try:
        completed = subprocess.run(command, input=text, capture_output=True,
                                   text=True, encoding="utf-8", timeout=timeout,
                                   cwd=PACKAGE)
        return {"returncode": completed.returncode, "stdout": completed.stdout,
                "stderr": completed.stderr, "seconds": round(time.perf_counter() - start, 4)}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"returncode": None, "stdout": "", "stderr": str(exc),
                "seconds": round(time.perf_counter() - start, 4)}


def record_result(test, result):
    passed = result["returncode"] == test["code"] and result["stdout"] == test["expected"]
    entry = {"case": test["name"], "status": "passed" if passed else "failed",
             "returncode": result["returncode"], "seconds": result["seconds"]}
    if not passed:
        entry.update({"expected_returncode": test["code"], "input": test["input"],
                      "expected": test["expected"], "actual": result["stdout"],
                      "stderr": result["stderr"]})
    return entry


def run_julia_batch(runtime, source, cases, timeout):
    """Reuse each program's main() for valid cases, avoiding repeated Julia startup.

    Original source is loaded unchanged. Its initial main() consumes case 0;
    subsequent calls use invokelatest after redirecting streams to case files.
    Invalid-input tests run separately because they intentionally call exit(1).
    """
    valid = [test for test in cases if test["code"] == 0]
    invalid = [test for test in cases if test["code"] != 0]
    work = HERE / "build" / (source.stem + "_julia_batch")
    work.mkdir(parents=True, exist_ok=True)
    for i, test in enumerate(valid):
        (work / f"{i}.in").write_text(test["input"], encoding="utf-8")
        # Remove only the previous run's own result markers, never recursively.
        for suffix in ["out", "done"]:
            (work / f"{i}.{suffix}").unlink(missing_ok=True)
    helper = HERE / "julia_batch.jl"
    command = [runtime, "--startup-file=no", str(helper), str(source), str(work), str(len(valid))]
    batch = execute(command, "", max(timeout, 20 + 3 * len(valid)))
    entries = []
    for i, test in enumerate(valid):
        output_path, done_path = work / f"{i}.out", work / f"{i}.done"
        result = {"returncode": 0 if done_path.exists() else batch["returncode"],
                  "stdout": output_path.read_text(encoding="utf-8") if output_path.exists() else "",
                  "stderr": batch["stderr"], "seconds": 0.0}
        entries.append(record_result(test, result))
    for test in invalid:
        result = execute([runtime, "--startup-file=no", str(source)], test["input"], timeout)
        entries.append(record_result(test, result))
    return entries, batch["seconds"]


def write_reports(report):
    (HERE / "verification.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Kết quả kiểm thử thực tế", "",
             f"Thời điểm: {report['timestamp_utc']}. Seed cố định: {SEED}.", "",
             "Oracle dùng Python stdlib: `sorted`, `bisect`, công thức đếm cặp; "
             "số dịch chèn bằng số nghịch thế. Không lấy đáp án từ mã lời giải.", "",
             "| Ngôn ngữ | Bài | Đạt | Lỗi | Trạng thái |",
             "|---|---|---:|---:|---|"]
    for language, info in report["languages"].items():
        if info["status"] == "skipped":
            lines.append(f"| {language} | cả 4 | 0 | 0 | Bỏ qua: {info['reason']} |")
            continue
        for exercise, result in info["exercises"].items():
            lines.append(f"| {language} | {exercise} | {result['passed']} | "
                         f"{result['failed']} | {result['status']} |")
    lines += ["", f"Tổng: **{report['passed']} ca đạt; {report['failed']} ca lỗi**. "
              f"Số ngôn ngữ bỏ qua: {report['skipped_languages']}.", "",
              "Các ca gồm mẫu, rỗng, một phần tử, trùng, âm, tăng/giảm, "
              "biên tìm kiếm, dữ liệu chưa sắp xếp, k=1/k=n/k=2, hòa phiếu, "
              "hòa khoảng cách khác thứ tự ID và đầu vào kNN không hợp lệ. "
              f"Có thêm {report['random_cases_per_exercise']} ca ngẫu nhiên "
              "cố định cho mỗi bài và mỗi ngôn ngữ được chạy.", "",
              "Thời gian trong JSON là thời gian kiểm thử, không phải benchmark thuật toán. "
              "Khi chạy Julia theo lô, thời gian từng ca hợp lệ ghi 0 và thời gian cả lô "
              "được lưu riêng. Ngôn ngữ bỏ qua chưa được kiểm chứng lúc chạy."]
    for language, info in report["languages"].items():
        if info["status"] != "skipped":
            lines += ["", f"Runtime {language}: `{info['runtime']}`.",
                      f"Phiên bản: `{info.get('version', 'không đọc được')}`."]
            for exercise, result in info["exercises"].items():
                if result.get("compile_error"):
                    lines += ["", f"Lỗi biên dịch {language}/{exercise}:",
                              "```text", result["compile_error"], "```"]
    (HERE / "verification.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cpp", help="C++17 compiler, defaults to g++/clang++ on PATH")
    parser.add_argument("--julia", help="Julia runtime, defaults to julia on PATH")
    parser.add_argument("--python", default=sys.executable, help="Python runtime")
    parser.add_argument("--random-cases", type=int, default=30)
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()
    if args.random_cases < 0:
        parser.error("--random-cases must be nonnegative")
    cases = build_cases(args.random_cases)
    runtimes = {"Python": find_executable(args.python, ["python3", "python"]),
                "C++17": find_executable(args.cpp, ["g++", "clang++"]),
                "Julia": find_executable(args.julia, ["julia"])}
    layouts = {"Python": ("python", ".py"), "C++17": ("cpp", ".cpp"),
               "Julia": ("julia", ".jl")}
    report = {"timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "seed": SEED, "random_cases_per_exercise": args.random_cases,
              "languages": {}, "passed": 0, "failed": 0, "skipped_languages": 0}
    build_dir = HERE / "build"
    build_dir.mkdir(exist_ok=True)
    for language, runtime in runtimes.items():
        if not runtime:
            report["languages"][language] = {
                "status": "skipped", "reason": "không tìm thấy runtime/compiler"}
            report["skipped_languages"] += 1
            print(f"SKIP {language}: runtime/compiler unavailable", flush=True)
            continue
        version = execute([runtime, "--version"], "", args.timeout)
        info = {"status": "passed", "runtime": runtime,
                "version": (version["stdout"] or version["stderr"]).strip().splitlines()[0],
                "exercises": {}}
        report["languages"][language] = info
        folder, suffix = layouts[language]
        for exercise, tests in cases.items():
            source = PACKAGE / "code" / folder / (exercise + suffix)
            compile_error = None
            if not source.is_file():
                compile_error = f"Source missing: {source}"
            if language == "C++17" and not compile_error:
                executable = build_dir / (exercise + (".exe" if os.name == "nt" else ""))
                compilation = execute([runtime, "-std=c++17", "-O2", "-Wall", "-Wextra",
                                       str(source), "-o", str(executable)], "", args.timeout)
                if compilation["returncode"] != 0:
                    compile_error = compilation["stderr"] or compilation["stdout"]
                command = [str(executable)]
            else:
                command = [runtime, str(source)]
            if compile_error:
                result = {"status": "failed", "passed": 0, "failed": len(tests),
                          "compile_error": compile_error, "cases": []}
            else:
                started = time.perf_counter()
                if language == "Julia":
                    entries, batch_seconds = run_julia_batch(runtime, source, tests, args.timeout)
                else:
                    entries = [record_result(test, execute(command, test["input"], args.timeout))
                               for test in tests]
                    batch_seconds = None
                passed = sum(entry["status"] == "passed" for entry in entries)
                result = {"status": "passed" if passed == len(entries) else "failed",
                          "passed": passed, "failed": len(entries) - passed,
                          "seconds": round(time.perf_counter() - started, 4), "cases": entries}
                if batch_seconds is not None:
                    result["valid_batch_seconds"] = batch_seconds
            info["exercises"][exercise] = result
            report["passed"] += result["passed"]
            report["failed"] += result["failed"]
            if result["failed"]:
                info["status"] = "failed"
            print(f"{language} {exercise}: {result['passed']} passed, "
                  f"{result['failed']} failed", flush=True)
    write_reports(report)
    print(f"Reports: {HERE / 'verification.json'}", flush=True)
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
