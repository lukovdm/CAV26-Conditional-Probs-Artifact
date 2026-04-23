echo "====================="
echo "  RQ1 benchmarks..."
echo "====================="
python benchmarks/rq1/benchmark.py --output out/rq1/res

echo "====================="
echo "  RQ2 benchmarks..."
echo "====================="
# python benchmarks/rq2/run_benchmarks.py --results-folder out/rq2/res/float/
python benchmarks/rq2/run_benchmarks.py --results-folder out/rq2/res/exact/ --exact

echo "====================="
echo "  RQ3 benchmarks..."
echo "====================="
benchmarks/rq3/run_benchmark.sh res

echo "====================="
echo "       DONE!"
echo "====================="