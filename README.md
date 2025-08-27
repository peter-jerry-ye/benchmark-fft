# FFT Benchmark Project

A multi-language FFT (Fast Fourier Transform) performance benchmark comparing Rust, MoonBit, Swift, and Go implementations.

## Features

- **Multi-language support**: Rust, MoonBit, Swift, and Go implementations
- **Automated building**: Auto-builds all language programs
- **Performance benchmarking**: Runs multiple tests with statistical analysis
- **Result visualization**: Generates performance comparison charts
- **Optional verification**: MoonBit ↔ Rust result verification
- **Verbose logging**: Optional detailed command execution logs

## Requirements

This project has been tested on the following environments:
- Python 3.13.7
- Rust 1.89.0
- MoonBit v0.6.25
- Swift 6.0
- go 1.22

## Quick Start

```bash
# Basic benchmark (build + test)
python3 bench_runner.py

# Skip building (if already built)
python3 bench_runner.py --no-build

# Custom parameters
python3 bench_runner.py --runs 20 --inputs 16 18 20 24

# Enable verification
python3 bench_runner.py --verify --verbose
```

## Examples

```bash
# Quick test (skip build, 5 runs)
python3 bench_runner.py --no-build --runs 5

# Detailed test (build all, 20 runs, enable verification)
python3 bench_runner.py --runs 20 --verify --verbose

# Custom input sizes
python3 bench_runner.py --inputs 16 18 20 22 24 --runs 15
```

## Output

- **Build progress**: Shows building status for each language
- **Test results**: Statistical summary table with min/max/median/average times
- **Chart**: Generates `bench_avg.png` performance comparison chart
- **Verification**: Optional MoonBit ↔ Rust result verification

## Default Settings

- Input sizes: 18, 20, 22 (2^18, 2^20, 2^22 complex points)
- Runs per input: 10
- Verification: disabled by default
- Chart output: `bench_avg.png`
- Verification files: `./.verify_out/`

## Troubleshooting

- Use `--verbose` for detailed error information
- Ensure all language environments are properly installed
- Check write permissions for verification directory
