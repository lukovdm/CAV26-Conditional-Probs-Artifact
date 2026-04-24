#! /bin/bash

folder=$1
if [ -z "$folder" ]; then
    folder="res"
fi

mkdir -p out/plots/rq1/$folder out/plots/rq2/$folder out/plots/rq3/$folder

echo "====================="
echo "  Creating plots for RQ1..."
echo "====================="
python benchmarks/rq1/plot_results.py out/rq1/$folder/results.json --output out/plots/rq1/$folder/

echo "====================="
echo "  Creating plots for RQ2..."
echo "====================="
python benchmarks/rq2/generate_main_results_extended.py out/rq2/$folder/exact/evaluation_results.csv > out/plots/rq2/$folder/rq2-exact.tex
python benchmarks/rq2/generate_main_results_extended.py out/rq2/$folder/float/evaluation_results.csv > out/plots/rq2/$folder/rq2-float.tex

echo "====================="
echo "  Creating plots for RQ3..."
echo "====================="
python premise/premise/analysis/check.py out/rq3/$folder/ --output out/plots/rq3/$folder/

if [ "$folder" == "res" ]; then
    echo "====================="
    echo "  Done!"
    echo "====================="
    echo "You can find the plots of the paper here:"
    echo "Fig. 2:"
    echo "  - Left: out/plots/rq1/res/scatter_bounded_bisection_exact_vs_restart_exact.pdf"
    echo "  - Right: out/plots/rq1/res/scatter_bounded_bisection_float_vs_restart_float.pdf"
    echo "Fig. 3:"
    echo "  - Left: out/plots/rq1/res/scatter_quantitative_bisection-pt_exact_vs_restart_exact.pdf"
    echo "  - Right: out/plots/rq1/res/scatter_quantitative_bisection-pt_float_vs_restart_float.pdf"
    echo "Fig. 4:"
    echo "  - Left: out/plots/rq1/res/scatter_quantitative_bisection-pt_exact_vs_bisection_exact.pdf"
    echo "  - Right: out/plots/rq1/res/scatter_quantitative_bisection-pt_eps-exact_vs_bisection_eps-exact.pdf"
    echo "Table 3: out/plots/rq2/res/rq2-exact.tex"
    echo "Table 4: out/plots/rq2/res/rq2-float.tex"
else
    echo "====================="
    echo "  Done!"
    echo "====================="
    echo "You can find the plots of the smoke test here:"
    echo "RQ1: out/plots/rq1"
    echo "RQ2: out/plots/rq2"
    echo "RQ3: out/plots/rq3"
fi