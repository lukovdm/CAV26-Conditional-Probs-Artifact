#!/usr/bin/env python3


import sys
import pandas as pd
import numpy as np

def sci_notation(val):
	if val < 1e4:
		return str(val)
	exp = int(np.floor(np.log10(val)))
	base = val / 10**exp
	base = round(base, 1)
	if abs(base - int(base)) < 1e-8:
		base = int(base)
	return f"{base}e{exp}"

def main():
	if len(sys.argv) != 2:
		print(f"Usage: {sys.argv[0]} <csv_file>")
		sys.exit(1)
	csv_file = sys.argv[1]
	df = pd.read_csv(csv_file)

	model_rename_map = {
		'ceaser-cipher-4-10': 'ceas-4-10',
		'ceaser-cipher-10-8': 'ceas-10-8',
		'dpm': 'dpm',
		'dpm-queue': 'dpm-q',
		'ladder-network': 'ladder',
		'ladder-network-input': 'ladder-in',
		'virus': 'virus',
		'airport': 'airport',
		'airport-big': 'airport-b',
	}

	model_order = [
		'ceaser-cipher-4-10',
		'ceaser-cipher-10-8',
		'ladder-network',
		'ladder-network-input',
		'dpm',
		'dpm-queue',
		'virus',
		'airport',
		'airport-big',
	]
	df['model'] = pd.Categorical(df['model'], categories=model_order, ordered=True)
	df = df.sort_values('model')

	considered_algs = [
		('bisection', True),
		('bisection', False),
		# ('bisection_advanced', True),
		('bisection_advanced', False),
		# ('bisection_pt', True),
		('bisection_pt', False),
		# ('bisection_advanced_pt', True),
		('bisection_advanced_pt', False),
		('restart', False)
	]

	# Define bisection and restart algorithms for labeling
	bisection_algs = [
		(('bisection', True), 'treat'),
		(('bisection', False), 'bis-std'),
		(('bisection_advanced', False), 'bis-adv'),
		(('bisection_pt', False), 'pt-bis-std'),
		(('bisection_advanced_pt', False), 'pt-bis-adv'),
	]
	restart_alg = (('restart', False), 'Restart')
	# Only keep rows that match any (alg, opt) in considered_algs
	alg_opt_set = set(considered_algs)
	def row_match(row):
		if row['conditional_alg'] == restart_alg[0]:
			return (row['conditional_alg'], False) in alg_opt_set or (row['conditional_alg'], True) in alg_opt_set
		else:
			return (row['conditional_alg'], bool(row['bisection_optimization'])) in alg_opt_set
	df = df[df.apply(row_match, axis=1)]

	# Build algorithm label map for considered_algs
	alg_label_map = {a: l for a, l in bisection_algs}
	alg_label_map[restart_alg[0]] = restart_alg[1]

	# Build column format string dynamically
	n_algs = len(considered_algs)
	print(r"\begin{tabular}{lrr@{\hskip 12pt}" + ("r@{\\hskip 4pt}l@{\\hskip 12pt}" * n_algs) + "}")
	print(r"\toprule")
	# First header row: model, fam size, mdp size, then each algorithm (with multicolumn)
	col_headers = ["Model", "$|\\mathcal{F}|$", "$|M|$"]
	for alg, alg_opt in considered_algs:
		col_headers.append(rf"\multicolumn{{2}}{{c@{{\hskip 12pt}}}}{{{alg_label_map.get((alg, alg_opt), alg)}}}")
	print(" & ".join(col_headers) + r" \\")
	# Second header row: subcolumns for time and ips
	# sub_headers = ["", "", ""]
	# for _ in considered_algs:
	# 	sub_headers += ["Time", "$it/s$"]
	# print(" & ".join(sub_headers) + r" \\")
	print(r"\midrule")

	for model in df['model'].unique():
		row = df[df['model'] == model]
		if row.empty:
			continue
		fam_size = 0
		avg_mdp_size = 0
		fam_idx = None
		for idx in range(len(row)):
			if row.iloc[idx]['family_size'] != '-':
				fam_idx = idx
				break
		if fam_idx is not None:
			fam_size = row.iloc[fam_idx]['family_size']
			fam_size_str = sci_notation(float(fam_size))
			avg_mdp_size = row.iloc[fam_idx]['avg_mdp_size']
		else:
			fam_size_str = '-'
			avg_mdp_size = '-'

		cells = []
		min_time = None
		min_idx = None
		for idx, (alg, opt) in enumerate(considered_algs):
			if alg == restart_alg[0]:
				r = row[row['conditional_alg'] == alg]
			else:
				r = row[(row['conditional_alg'] == alg) & (row['bisection_optimization'] == opt)]
			if r.empty:
				cells.extend(["-", "-"])
				continue
			time = r.iloc[0]['time']
			iters = r.iloc[0]['iterations']
			ips = iters / time if time > 0 else 0
			# Prepare cell values
			if time is None:
				tcell = "-"
				ipscell = "-"
			elif time > 880:
				tcell = "TO"
				ipscell = f"{ips:.0f}"
			else:
				tcell = f"{time:.0f}s"
				ipscell = f"{ips:.0f}"
			cells.extend([tcell, ipscell])
			# Track minimum time for bolding (now includes restart alg)
			if time is not None and time <= 880:
				if min_time is None or time < min_time:
					min_time = time
					min_idx = idx * 2  # time column index

		# Bold the minimum time cell
		if min_idx is not None and cells[min_idx] not in ("-", "TO"):
			cells[min_idx] = f"\\textbf{{{cells[min_idx]}}}"

		print(f"{model_rename_map.get(model, model)} & {fam_size_str} & {int(avg_mdp_size)} & " + " & ".join(cells) + r" \\")
	print(r"\bottomrule")
	print(r"\end{tabular}")

if __name__ == "__main__":
	main()
