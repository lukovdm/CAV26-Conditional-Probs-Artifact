#!/usr/bin/env python3
import argparse
import os
import re

parser = argparse.ArgumentParser(description="Generate RQ3 LaTeX table from stats.out files.")
parser.add_argument("data_dir", help="Folder containing *-unf-{variant}-{method}[-thresh=...] subfolders (e.g. out/rq3/res)")
parser.add_argument("--variant", choices=["exact", "float"], default="exact")
args = parser.parse_args()

# Number of decimals to round table values
round_decimals = 3

data_dir = args.data_dir
variant = args.variant

methods = ["bisection", "restart", "rejection"]
METHOD_DISPLAY = {
    "bisection": "treat",
    "restart": "restart",
    "rejection": "previous",
}
threshold_str = "-thresh=0.05"


def format_time(val):
    """Render a time in the paper's style: 2 decimals under 10s, 1 decimal otherwise."""
    try:
        f = float(val)
    except (TypeError, ValueError):
        return val
    return f"{f:.1f}" if f >= 10 else f"{f:.2f}"

# Table columns: thresholded and non-thresholded, each with 3 methods, each with avg_time and max_time
columns = []
for thresh in [True, False]:
    for method in methods:
        for stat in ["avg_time", "max_time"]:
            columns.append((thresh, method, stat))

# Find all folders
folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]

# Parse folder names to get model names and organize by model
model_dict = {}
folder_pattern = re.compile(r"^(?P<model>.+)-unf-(?P<variant>float|exact)-(?P<method>[^/]+)$")
for folder in folders:
    m = folder_pattern.match(folder)
    if not m:
        continue
    if m.group("variant") != variant:
        continue
    model = m.group("model")
    method_full = m.group("method")
    is_thresh = method_full.endswith(threshold_str)
    if not is_thresh:
        continue
    method = method_full.replace(threshold_str, "")
    if method not in methods:
        continue
    if model not in model_dict:
        model_dict[model] = {}
    model_dict[model][(method, is_thresh)] = folder

def parse_stats(stats_path):
    avg_time = ""
    max_time = ""
    if not os.path.exists(stats_path):
        return avg_time, max_time
    with open(stats_path) as f:
        for line in f:
            if line.startswith("avg_time="):
                avg_time = line.strip().split("=", 1)[1]
            elif line.startswith("max_time="):
                max_time = line.strip().split("=", 1)[1]
    return avg_time, max_time



# Multi-layered header construction with multirow/multicolumn
num_methods = len(methods)
num_stats = 2  # avg_time, max_time
num_groups = 1  # thresholded, (non-thresholded)

col_model = 1
col_per_group = num_methods * num_stats
total_cols = col_model + num_groups * col_per_group

print(f"\\begin{{tabular}}{{l{'r' * (total_cols - 1)}}}")
print("\\toprule")

# Top layer: Model (multirow), Thresholded/Non-thresholded (multicolumn)
# top_header = [f"\\multirow{{3}}{{*}}{{Model}}"]
# for group in ["Thresholded", "Non-thresholded"]:
#     top_header.append(f"\\multicolumn{{{col_per_group}}}{{c}}{{{group}}}")
# print(" & ".join(top_header) + " \\\\")
# cmidrule_parts = []
# for i in range(num_groups):
#     start = 2 + i * col_per_group
#     end = start + col_per_group - 1
#     cmidrule_parts.append(f"\\cmidrule(lr){{{start}-{end}}}")
# print(" " * 4 + " ".join(cmidrule_parts))

# Middle layer: Methods (multicolumn)
mid_header = [f"\\multirow{{2}}{{*}}{{Model}}",]  # Model column
for _ in range(num_groups):
    for method in methods:
        mid_header.append(
            f"\\multicolumn{{{num_stats}}}{{c}}{{{METHOD_DISPLAY[method]}}}"
        )
print(" & ".join(mid_header) + " \\\\")
cmidrule_parts = []
for i in range(num_groups):
    for j in range(num_methods):
        start = 2 + i * col_per_group + j * num_stats
        end = start + num_stats - 1
        cmidrule_parts.append(f"\\cmidrule(lr){{{start}-{end}}}")
print(" " * 4 + " ".join(cmidrule_parts))

# Bottom layer: t_avg, t_max
bottom_header = ["",]  # Model column
for _ in range(num_groups):
    for _ in range(num_methods):
        bottom_header.extend(["$t_\\text{avg}$", "$t_\\text{max}$"])
print(" & ".join(bottom_header) + " \\\\")
print("\\midrule")

# Table rows
for model in sorted(model_dict.keys()):
    row = [model]
    for thresh in [True]:
        # Collect raw values first so we can bold the minimum per stat across methods.
        row_values = []  # list of (avg_float|None, max_float|None, avg_str, max_str)
        for method in methods:
            folder = model_dict[model].get((method, thresh))
            stats_path = os.path.join(data_dir, folder, "stats.out") if folder else None
            avg_time, max_time = ("", "")
            if stats_path:
                avg_time, max_time = parse_stats(stats_path)
            try:
                avg_f = float(avg_time)
            except (TypeError, ValueError):
                avg_f = None
            try:
                max_f = float(max_time)
            except (TypeError, ValueError):
                max_f = None
            row_values.append((avg_f, max_f, format_time(avg_time), format_time(max_time)))

        avg_floats = [v[0] for v in row_values if v[0] is not None]
        max_floats = [v[1] for v in row_values if v[1] is not None]
        avg_best = min(avg_floats) if avg_floats else None
        max_best = min(max_floats) if max_floats else None

        for avg_f, max_f, avg_s, max_s in row_values:
            if avg_best is not None and avg_f == avg_best:
                avg_s = f"\\textbf{{{avg_s}}}"
            if max_best is not None and max_f == max_best:
                max_s = f"\\textbf{{{max_s}}}"
            row.append(avg_s)
            row.append(max_s)
    print(" & ".join(row) + " \\\\")
print("\\bottomrule")
print("\\end{tabular}")
