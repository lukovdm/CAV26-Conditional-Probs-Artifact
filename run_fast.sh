#!/bin/bash
echo "====================="
echo "   RQ1 benchmarks    "
echo "====================="
# time (python benchmarks/rq1/benchmark.py --output out/rq1/fast --methods bisection bisection-pt restart --random-subset-models 0.5)

echo "====================="
echo "   RQ2 benchmarks    "
echo "====================="
time (python benchmarks/rq2/run_benchmarks.py --results-folder out/rq2/fast/float/ --fast --timeout 300)
time (python benchmarks/rq2/run_benchmarks.py --results-folder out/rq2/fast/exact/ --fast --timeout 300 --exact)

echo "====================="
echo "   RQ3 benchmarks    "
echo "====================="
# time (cd premise && python premise/experiments.py --results-folder ../out/rq3/fast --fast) | cat

echo "====================="
echo "       DONE!"
echo "====================="