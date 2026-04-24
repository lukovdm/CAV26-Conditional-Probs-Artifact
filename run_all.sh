echo "====================="
echo "  RQ1 benchmarks..."
echo "====================="
python benchmarks/rq1/benchmark.py --output out/rq1/all

echo "====================="
echo "  RQ2 benchmarks..."
echo "====================="
python benchmarks/rq2/run_benchmarks.py --results-folder out/rq2/all/float/
python benchmarks/rq2/run_benchmarks.py --results-folder out/rq2/all/exact/ --exact

echo "====================="
echo "  RQ3 benchmarks..."
echo "====================="
(cd premise && python premise/experiments.py --results-folder ../out/rq3/all) | cat

echo "====================="
echo "       DONE!"
echo "====================="