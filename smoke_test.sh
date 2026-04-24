echo "====================="
echo "  RQ1 benchmarks..."
echo "====================="
python benchmarks/rq1/benchmark.py --models "coin-03-K=4" "asia" "crowds_3-5-0.01" --output out/rq1/smoke_test/


echo "====================="
echo "  RQ2 benchmarks..."
echo "====================="
python benchmarks/rq2/run_benchmarks.py --results-folder out/rq2/smoke_test/float/ --smoke-test
python benchmarks/rq2/run_benchmarks.py --results-folder out/rq2/smoke_test/exact/ --smoke-test --exact

echo "====================="
echo "  RQ3 benchmarks..."
echo "====================="
benchmarks/rq3/run_benchmark.sh smoke_test

echo "====================="
echo "       DONE!"
echo "====================="