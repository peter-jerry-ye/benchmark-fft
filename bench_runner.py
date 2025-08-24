
#!/usr/bin/env python3
"""
bench_runner.py
Run two programs multiple times with several inputs, parse "execution time: X ms",
and print a clean summary (min/max/median/average).

Defaults assume the following project layout (as in your screenshot):

- Rust program:
    build dir: ./fft/rs
    build: cargo build --release
    exe:   ./fft/rs/target/release/main

- MoonBit program:
    build dir: ./fft/mbt
    build: moon build --target native --release
    exe:   ./fft/mbt/target/native/release/build/main/main.exe

You can edit the PROGRAMS list below if your paths/commands differ.

Usage (from repo root):
    python3 bench_runner.py
Options:
    --no-build   Skip the build step
    --runs N     How many runs per input (default 10)
    --inputs i j k ...   Space-separated inputs (default: 18 20 22)
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

def run_cmd(cmd: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, check=False
    )

def ensure_built(program: Program) -> None:
    # Build the program; bubble up error with useful context
    proc = run_cmd(program.build_cmd, cwd=program.workdir)
    if proc.returncode != 0:
        print(f"[ERROR] Build failed for {program.name}.", file=sys.stderr)
        print("Command:", " ".join(program.build_cmd), file=sys.stderr)
        print(proc.stdout, file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        sys.exit(1)

def parse_time_ms(output: str) -> Optional[float]:
    # Take the last occurrence in case the program prints multiple lines.
    matches = TIME_RE.findall(output)
    if not matches:
        return None
    return float(matches[-1])

def run_once(program: Program, input_value: int) -> float:
    proc = run_cmd([str(program.exe_path), str(input_value)], cwd=program.workdir)
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
    # Group by (program, input)
    print()
    print("=" * 72)
    print("Benchmark Summary (execution time in ms)")
    print("=" * 72)
    header = f"{'Program':20} {'Input':>7} {'Runs':>6} {'Fastest':>12} {'Slowest':>12} {'Median':>12} {'Average':>12}"
    print(header)
    print("-" * len(header))
    for r in results:
        s = r.summary()
        if s is None:
            continue
        line = f"{r.program:20} {r.input_value:7d} {s['runs']:6d} {format_ms(s['min']):>12} {format_ms(s['max']):>12} {format_ms(s['median']):>12} {format_ms(s['average']):>12}"
        print(line)
    print("=" * 72)
    print()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-build", action="store_true", help="Skip building the programs")
    parser.add_argument("--runs", type=int, default=10, help="Number of runs per input")
    parser.add_argument("--inputs", nargs="*", type=int, default=[18, 20, 22], help="Input sizes")
    args = parser.parse_args()

    # Adjust these paths/commands if needed.
    repo_root = Path(__file__).resolve().parent

    programs = [
        Program(
            name="rust",
            workdir=repo_root / "fft" / "rs",
            build_cmd=["cargo", "build", "--release"],
            exe_path=Path("target") / "release" / "main",
        ),
        Program(
            name="moonbit",
            workdir=repo_root / "fft" / "mbt",
            build_cmd=["moon", "build", "--target", "native", "--release"],
            exe_path=Path("target") / "native" / "release" / "build" / "main" / "main.exe",
        ),
    ]

    # Build
    if not args.no_build:
        for p in programs:
            print(f"[BUILD] {p.name} ...")
            ensure_built(p)

    # Run
    results: List[BenchResult] = []
    for p in programs:
        for n in args.inputs:
            print(f"[RUN] {p.name} n={n}")
            r = BenchResult(program=p.name, input_value=n)
            for i in range(args.runs):
                t = run_once(p, n)
                r.times_ms.append(t)
            results.append(r)

    print_table(results)

if __name__ == "__main__":
    main()
