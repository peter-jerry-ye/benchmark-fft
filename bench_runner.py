#!/usr/bin/env python3
"""
bench_runner.py  (with verification + --verbose)

Features
- Builds Rust + MoonBit (or skip with --no-build)
- Optional verification per input: MoonBit writes golden file, Rust reads & compares
- Benchmarks inputs (default 18 20 22), N runs each (default 10)
- Parses "execution time: XXX ms" and prints min/max/median/average
- --verbose prints every command executed (build + runs + verification)

Usage (from repo root):
    python3 bench_runner.py
Options:
    --no-build              Skip building the programs
    --runs N                Number of runs per input (default 10)
    --inputs i j k ...      Input sizes (default: 18 20 22)
    --no-verify             Disable MBT->file then Rust->verify step
    --verify-per-run        Verify on every Rust timing run (slower)
    --verify-dir PATH       Directory for verification files (default: ./.verify_out)
    --verbose               Log every executed command
"""

import argparse
import re
import statistics as stats
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

TIME_RE = re.compile(r"execution time:\s*([0-9]+(?:\.[0-9]+)?)\s*ms", re.IGNORECASE)

@dataclass
class Program:
    name: str
    workdir: Path
    build_cmd: List[str]
    exe_path: Path

@dataclass
class BenchResult:
    program: str
    input_value: int
    times_ms: List[float] = field(default_factory=list)

    def summary(self):
        if not self.times_ms:
            return None
        return {
            "runs": len(self.times_ms),
            "min": min(self.times_ms),
            "max": max(self.times_ms),
            "median": stats.median(self.times_ms),
            "average": stats.mean(self.times_ms),
        }

def run_cmd(cmd: List[str], cwd: Optional[Path] = None, verbose: bool = False) -> subprocess.CompletedProcess:
    workdir = str(cwd) if cwd else None
    if verbose:
        prefix = f"[CMD in {workdir}] " if workdir else "[CMD] "
        print(prefix + " ".join(map(str, cmd)), file=sys.stderr)
    return subprocess.run(
        cmd, cwd=workdir, capture_output=True, text=True, check=False
    )

def ensure_built(program: Program, verbose: bool) -> None:
    proc = run_cmd(program.build_cmd, cwd=program.workdir, verbose=verbose)
    if proc.returncode != 0:
        print(f"[ERROR] Build failed for {program.name}.", file=sys.stderr)
        print("Command:", " ".join(program.build_cmd), file=sys.stderr)
        print(proc.stdout, file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        sys.exit(1)

def parse_time_ms(output: str) -> Optional[float]:
    matches = TIME_RE.findall(output)
    if not matches:
        return None
    return float(matches[-1])

def run_once(program: Program, input_value: int, verbose: bool, extra_arg: Optional[str] = None) -> float:
    cmd = [str(program.exe_path), str(input_value)]
    if extra_arg is not None:
        cmd.append(extra_arg)
    proc = run_cmd(cmd, cwd=program.workdir, verbose=verbose)
    if proc.returncode != 0:
        print(f"[ERROR] Run failed for {program.name} input={input_value}", file=sys.stderr)
        print(proc.stdout, file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        sys.exit(2)
    t = parse_time_ms(proc.stdout + "\n" + proc.stderr)
    if t is None:
        print(f"[ERROR] Could not parse execution time from output for {program.name} input={input_value}", file=sys.stderr)
        print("Output:")
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        sys.exit(3)
    return t

def format_ms(x: float) -> str:
    return f"{x:8.3f} ms"

def print_table(results: List[BenchResult]) -> None:
    print()
    print("=" * 80)
    print("Benchmark Summary (execution time in ms)")
    print("=" * 80)
    header = f"{'Program':20} {'Input':>7} {'Runs':>6} {'Fastest':>12} {'Slowest':>12} {'Median':>12} {'Average':>12}"
    print(header)
    print("-" * len(header))
    for r in results:
        s = r.summary()
        if s is None:
            continue
        line = f"{r.program:20} {r.input_value:7d} {s['runs']:6d} {format_ms(s['min']):>12} {format_ms(s['max']):>12} {format_ms(s['median']):>12} {format_ms(s['average']):>12}"
        print(line)
    print("=" * 80)
    print()

def verify_pair(mbt: Program, rust: Program, input_value: int, out_dir: Path, verbose: bool, per_run: bool = False):
    """
    If per_run is False: generate one golden file with MBT and check once with Rust.
    If per_run is True:  return a callable that, given a run index, will perform
                         MBT->file then Rust->verify for each run (slower, but strongest).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    golden = out_dir / f"mbt_{input_value}.txt"

    def verify_once(tag: str = ""):
        # MoonBit writes golden file
        proc1 = run_cmd([str(mbt.exe_path), str(input_value), str(golden)], cwd=mbt.workdir, verbose=verbose)
        if proc1.returncode != 0:
            print(f"[ERROR] Verification: MBT failed for input={input_value}", file=sys.stderr)
            print(proc1.stdout, file=sys.stderr)
            print(proc1.stderr, file=sys.stderr)
            sys.exit(10)
        # Rust reads & compares
        proc2 = run_cmd([str(rust.exe_path), str(input_value), str(golden)], cwd=rust.workdir, verbose=verbose)
        if proc2.returncode != 0:
            print(f"[ERROR] Verification: Rust failed (mismatch?) input={input_value} {tag}", file=sys.stderr)
            print("Rust output:\n", proc2.stdout, file=sys.stderr)
            print(proc2.stderr, file=sys.stderr)
            sys.exit(11)

    if per_run:
        return lambda idx: verify_once(tag=f"(run #{idx+1})")
    else:
        verify_once()
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-build", action="store_true", help="Skip building the programs")
    parser.add_argument("--runs", type=int, default=10, help="Number of runs per input")
    parser.add_argument("--inputs", nargs="*", type=int, default=[18, 20], help="Input sizes")
    parser.add_argument("--no-verify", action="store_true", help="Disable MBT->file then Rust->verify step")
    parser.add_argument("--verify-per-run", action="store_true", help="Verify on every Rust timing run")
    parser.add_argument("--verify-dir", type=str, default=".verify_out", help="Directory for verification files")
    parser.add_argument("--verbose", action="store_true", help="Log every executed command")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent

    rust = Program(
        name="rust",
        workdir=repo_root / "fft" / "rs",
        build_cmd=["cargo", "build", "--release"],
        exe_path=Path("target") / "release" / "main",
    )
    mbt = Program(
        name="moonbit",
        workdir=repo_root / "fft" / "mbt",
        build_cmd=["moon", "build", "--target", "native", "--release"],
        exe_path=Path("target") / "native" / "release" / "build" / "main" / "main.exe",
    )
    programs = [rust, mbt]  # build & run order

    # Build
    if not args.no_build:
        for p in programs:
            print(f"[BUILD] {p.name} ...")
            ensure_built(p, verbose=args.verbose)

    results: List[BenchResult] = []

    for n in args.inputs:
        if not args.no_verify:
            print(f"[VERIFY] input={n}")
            verifier = verify_pair(mbt, rust, n, repo_root / args.verify_dir, verbose=args.verbose, per_run=args.verify_per_run)
        else:
            verifier = None

        # Benchmark both programs
        for p in programs:
            print(f"[RUN] {p.name} n={n}")
            r = BenchResult(program=p.name, input_value=n)
            for i in range(args.runs):
                if verifier is not None and args.verify_per_run and p.name == "rust":
                    verifier(i)
                t = run_once(p, n, verbose=args.verbose)  # timing runs don't pass the file
                r.times_ms.append(t)
            results.append(r)

    print_table(results)

if __name__ == "__main__":
    main()
