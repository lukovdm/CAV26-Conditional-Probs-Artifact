#! /bin/bash
# Usage: create_plots.sh [folder] [base]
#   folder: sub-run name, e.g. "res" (default) or "smoke_test"
#   base:   input/output base directory, e.g. "out" (default), "paper_out", "ref_out"

folder=$1
base=$2
if [ -z "$folder" ]; then
    folder="res"
fi
if [ -z "$base" ]; then
    base="out"
fi

mkdir -p $base/plots/rq1/$folder $base/plots/rq2/$folder $base/plots/rq3/$folder

echo "====================="
echo "  Creating plots for RQ1..."
echo "====================="
python benchmarks/rq1/plot_results.py $base/rq1/$folder/results.json --output $base/plots/rq1/$folder/ --format pdf

echo "====================="
echo "  Creating plots for RQ2..."
echo "====================="
python benchmarks/rq2/generate_main_results_extended.py $base/rq2/$folder/exact/evaluation_results.csv > $base/plots/rq2/$folder/rq2-exact.tex
python benchmarks/rq2/generate_main_results_extended.py $base/rq2/$folder/float/evaluation_results.csv > $base/plots/rq2/$folder/rq2-float.tex

echo "====================="
echo "  Creating plots for RQ3..."
echo "====================="
python benchmarks/rq3/latex_table_2.py $base/rq3/$folder/ --variant exact > $base/plots/rq3/$folder/rq3-exact.tex
python benchmarks/rq3/latex_table_2.py $base/rq3/$folder/ --variant float > $base/plots/rq3/$folder/rq3-float.tex

echo "====================="
echo "  Done!"
echo "====================="
echo ""
echo "You can find the plots of the paper here:"
echo "Fig. 2:"
echo "  - Left: $base/plots/rq1/$folder/scatter_bounded_bisection_exact_vs_restart_exact.pdf"
echo "  - Right: $base/plots/rq1/$folder/scatter_bounded_bisection_float_vs_restart_float.pdf"
echo "Fig. 3:"
echo "  - Left: $base/plots/rq1/$folder/scatter_quantitative_bisection-pt_exact_vs_restart_exact.pdf"
echo "  - Right: $base/plots/rq1/$folder/scatter_quantitative_bisection-pt_float_vs_restart_float.pdf"
echo "Fig. 4:"
echo "  - Left: $base/plots/rq1/$folder/scatter_quantitative_bisection-pt_exact_vs_bisection_exact.pdf"
echo "  - Right: $base/plots/rq1/$folder/scatter_quantitative_bisection-pt_eps-exact_vs_bisection_eps-exact.pdf"
echo "Table 2: $base/plots/rq3/$folder/rq3-exact.tex"
echo "Table 3: $base/plots/rq2/$folder/rq2-exact.tex"
echo "Table 4: $base/plots/rq2/$folder/rq2-float.tex"