def save_average_line_chart(results, filename="bench_avg.png"):
    """
    Line chart of AVERAGE times only, one line per program.
    Rust and Go are styled with standout markers/linestyles.
    """
    import matplotlib.pyplot as plt

    # Collect averages per program
    data = {}
    all_inputs = set()
    for r in results:
        summ = r.summary()
        if not summ:
            continue
        data.setdefault(r.program, {})[r.input_value] = float(summ["average"])
        all_inputs.add(r.input_value)

    all_inputs = sorted(all_inputs)
    programs = sorted(data.keys())

    # Assign standout styles
    style_map = {
        "rust":   {"marker": "X", "linestyle": ":",  "linewidth": 1.5, "markersize": 3},
        "go":     {"marker": "v", "linestyle": "--", "linewidth": 1.0, "markersize": 3},
    }
    # Fallback styles for others
    markers = ["^", "D", "v", "P", "X"]
    linestyles = ["-.", ":"]
    fig, ax = plt.subplots()

    for idx, program in enumerate(programs):
        xs = sorted(data[program].keys())
        ys = [data[program][x] for x in xs]

        if program in style_map:
            kwargs = style_map[program]
        else:
            kwargs = {
                "marker": markers[idx % len(markers)],
                "linestyle": linestyles[idx % len(linestyles)],
                "linewidth": 1,
                "markersize": 3,
            }

        ax.plot(xs, ys, label=program, **kwargs)

    # Axes, ticks, grid
    ax.set_xlabel("log2(input_size)")
    ax.set_ylabel("Average time (ms)")
    ax.set_title("FFT Benchmark: Average Time by Input Size")
    ax.set_xticks(all_inputs)
    ax.set_xticklabels([str(x) for x in all_inputs])
    ax.grid(True, which="both", linestyle="--", alpha=0.3)

    ax.legend()
    fig.tight_layout()
    fig.savefig(filename, dpi=200)
    print(f"[INFO] Saved average line chart to {filename}")
