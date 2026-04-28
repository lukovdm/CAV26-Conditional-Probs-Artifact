CAV 2026 Artifact
=======================================
Paper title: Fast Computation of Conditional Probabilities in MDPs and Markov Chain Families

Claimed badges: Available + Functional + Reusable

Justification for the badges:
  * **Functional**:
    - We provide (1) the benchmarks, (2) scripts to rerun the experiments, (3) the raw data that we obtained from running the experiments, and (4) scripts to summarize the data as in the paper. All is available in a single docker container.  
      Specifically: All experiments can be rerun in the docker file using three simple scripts and this raw data can be automatically formatted as presented in the paper.  The results in figures 2-4 and tables 2-4 can be replicated by following the full review steps outlined below. Table 1 is a hand combined version of tables 3 and 4. The main results can be obtained with a reduced benchmark suite.
    - The full source code of the tools is attached with the artifact. The tools can be compiled by following the instructions available in their respective README files. We also provide a docker container with all tools already installed.
  * **Reusable**: 
    + Our algorithms as described in the paper are built into the existing tool Storm with its python bindings stormpy.
    + In our docker image you can use the storm tool to model check conditional properties on any MDP accepted by storm (i.e., in the `.prism`, `.jani`, `.drn`, and `.umb` formats). Additionally, you can use our python bindings to do any of these operations from within python. Examples of this can be found in the section Example Usage.
    + We include unit tests as part of storm here: `storm/src/test/storm/modelchecker/prctl/mdp/ConditionalMdpPrctlModelCheckerTest.cpp`. 
    + All changes in Storm have already been merged into upstream and will be released as part of Storm 1.13. After it is released, you will be able to install storm with python bindings using the python package manager: `pip install stormpy`.
    + More documentation on Storm and Stormpy can also be found here: https://www.stormchecker.org/.

Requirements:
  * RAM: 8GB
  * CPU cores: 8 (If you use more cores the benchmarks will go faster and consume more RAM)
  * Time (smoke test): 10 minutes
  * Time (full review): 5 hours when using the fast experiment set, 21 hours when using the full experiment set

External connectivity: NO

### Contents
- Smoke Test
- Full Review
- Example Usage
- Replicating the Figures from the Original Experiment Data

**Smoke Test**
-------------------------------------------------------------------------------

Run the following to load the Docker image:

```bash
docker load < docker-image.tar
```

After that, run the image using

```bash
docker run -v `pwd`/out:/opt/benchmarks/out -p 8888:8888 --rm -it lukovdm/cav26-cond:latest
```

The command above starts the docker container and places you in a bash environment, where you can inspect the source code or run the experiments. A Jupyter Lab environment is started at the same time and can be accessed at [http://127.0.0.1:8888/lab?token=cav26]() to view any files in the docker container.

Start the smoke test with

```bash
./smoke_test.sh      # [ ~ runtime: 3 minutes]
```

The smoke test runs all tools on a reduced set of benchmarks and configurations.
If everything runs successfully, the script prints out intermediate progress for each RQ separately. Example output should look as follows:
```log
=====================
  RQ1 benchmarks...
=====================
Benchmarking 2 models with methods: ['bisection', 'bisection-pt', 'restart']
Testing both exact, exact-tolerance and float


Computers / CPU threads / Max jobs to run
1:local / 24 / 8

Computer:jobs running/jobs completed/%of started jobs/Average seconds to complete
ETA: 0s Left: 16 AVG: 0.04s  local:7/23/100%/0.0s /opt/storm/build/bin/storm -drn benchmarks/rq1/models/concrete-mdps/coin-03-K=4.drn --prop 'Pmax=? [true];Pmax>=0.5 [F "finished" & "all_coins_equal_0"  || F "all_coins_equal_1"]' --timeout 300 --dot-maxwidth 30 --exact --conditional:algorithm restart
...

=====================
  RQ2 benchmarks...
=====================
 83%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████▏                     | 5/6 [00:01<00:00,  3.76it/s]              # <It waits here for a bit>
 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6/6 [00:02<00:00,  2.24it/s]

 =====================
  RQ3 benchmarks...
=====================
Running in smoke test mode with only one benchmark and one configuration.
  0%|                                            | 0/1 [00:00<?, ?it/s]
100%|████████████████████████████████████████████| 10/10 [00:01<00:00,  9.59it/s]
100%|████████████████████████████████████████████| 1/1 [00:11<00:00, 11.24s/it]
All experiments completed.
=====================
       DONE!
=====================
```

If RQ1 is not successful, look into the folder logs. If any of its subfolders has a non-empty `stderr` file please include its contents in the review.
If RQ2 is not successful, look into the folder out/rq2/smoke_test/exact/evaluation_log.log. Please include its contents in the review.

To generate the plots for the smoke test you can run the following command:
```bash
./create_plots.sh smoke_test out
```

It will generate plots in the folders `out/plots/rq*/smoke_test/`. 
 - There should be 45 files in `out/plots/rq1/smoke_test/`
 - There should be 2 files in `out/plots/rq2/smoke_test/`
 - There should be 2 files in `out/plots/rq3/smoke_test/`

For completeness, we included the output files obtained by our experiments in
the folder `ref_out/`.

If the results are not as described above, please check the output of `smoke_test.sh` and `create_plots.sh`, compare to the log files in `ref_logs/smoke_test/` and include any different parts
of the log in the review.

**Full Review**
--------------------------------

Assuming the smoke test passed, run the following command in the docker image to reproduce the
results. Running the full benchmark suite can take around 20 hours on a standard
laptop.

```bash
./run_all.sh    # [runtime: 18 hours]
```

We also provide a reduced experiment set. This experiment set supports our main results while skipping many experiments only used for auxiliary results. This set takes around [n hours]. The reduced experiment set takes a seeded random subset of all models and only runs methods directly contributing to the figures in the paper, not in the appendix. Concretely it tests:
- RQ1: on a seeded random half of models and only on methods `treat`, `bis-std`, `pt-bis-std`, and `restart`.
- RQ2: only on methods `treat`, `pt-bis-std`, and `restart`.
- RQ3: only with exact arithmetic and qualitative queries.

```bash
./run_fast.sh   # [runtime: 4 hours]
```

The commands will print out progress similarly as the smoke test as they execute the benchmarks.

The output will be in the folders `out/rq*/full/` if you ran the full set and `out/rq*/fast/` if you ran the fast experiment set.

For completeness, we included the output files obtained by our experiments in
folder `ref_out/`.

In the following outputs, concrete values may be different, but the overall trends should stay the same.

To generate the plots for the full experiments you can run the following command:
```bash
./create_plots.sh full out
```
To generate the plots for the fast experiments you can run:
```bash
./create_plots.sh fast out
```

The plots and tables in the paper can now be found in the following locations:
- Fig. 2:
  - Left: `out/plots/rq1/full/scatter_bounded_bisection_exact_vs_restart_exact.pdf`
  - Right: `out/plots/rq1/full/scatter_bounded_bisection_float_vs_restart_float.pdf`
- Fig. 3:
  - Left: `out/plots/rq1/full/scatter_quantitative_bisection-pt_exact_vs_restart_exact.pdf`
  - Right: `out/plots/rq1/full/scatter_quantitative_bisection-pt_float_vs_restart_float.pdf`
- Fig. 4:
  - Left: `out/plots/rq1/full/scatter_quantitative_bisection-pt_exact_vs_bisection_exact.pdf`
  - Right: `out/plots/rq1/full/scatter_quantitative_bisection-pt_eps-exact_vs_bisection_eps-exact.pdf`
- Table 2: `out/plots/rq3/full/rq3-exact.tex`
- Table 3: `out/plots/rq2/full/rq2-exact.tex`
- Table 4: `out/plots/rq2/full/rq2-float.tex`
Or for the fast experiment set:
- Fig. 2:
  - Left: `out/plots/rq1/fast/scatter_bounded_bisection_exact_vs_restart_exact.pdf`
  - Right: `out/plots/rq1/fast/scatter_bounded_bisection_float_vs_restart_float.pdf`
- Fig. 3:
  - Left: `out/plots/rq1/fast/scatter_quantitative_bisection-pt_exact_vs_restart_exact.pdf`
  - Right: `out/plots/rq1/fast/scatter_quantitative_bisection-pt_float_vs_restart_float.pdf`
- Fig. 4:
  - Left: `out/plots/rq1/fast/scatter_quantitative_bisection-pt_exact_vs_bisection_exact.pdf`
  - Right: `out/plots/rq1/fast/scatter_quantitative_bisection-pt_eps-exact_vs_bisection_eps-exact.pdf`
- Table 2: `out/plots/rq3/fast/rq3-exact.tex`
- Table 3: `out/plots/rq2/fast/rq2-exact.tex`
- Table 4: `out/plots/rq2/fast/rq2-float.tex`

> Note that we did find a bug in our experiments for RQ2. This did not affect the treat and restart methods, and thus did our main conclusions of RQ 2, that the restart method was not able to solve many of the instances that treat solved. The bug did impact how the bisection methods performed, they perform worse in general after fixing the bug. However, treat already outperformed these methods in most models anyway and thus did not influence the conclusions here either.

**Example Usage**
----------------------------------------

Storm can be called from the command line or using python bindings. We give examples of both. To calculate a conditional probability on the wlan example model you can run the following:

```bash
/opt/storm/build/bin/storm -drn ../benchmarks/rq1/models/concrete-mdps/wlan-BOFF=4.drn \
    --prop 'Pmax=? [F "collision8" || F "collision2"]' \
    --conditional:algorithm bisection
```

You can select different algorithms by changing the `--conditional:algorithm` flag. To use exact arithmetic add the `--exact` flag, and to use epsilon-exact arithmetic also add `--conditional:precision 1e-6`.

We provide a notebook showing example usages of the python bindings our tool. When starting the docker image a Jupyter Lab server is started alongside it. You can access this Jupyter notebook server using the following URL: [http://127.0.0.1:8888/lab?token=cav26](). In the folder notebooks you can open the file `Usage.ipynb`.

Furthermore, you can also view all files in the artifact and all output generated in the `out/` folder in this interface.

**Replicating the Figures from the Original Experiment Data**
-----------------------------------------------------------------

The original experiment data can be found in the folder `paper_out`. By running the following command the figures and tables found in the paper can be replicated.

```bash
./create_plots.sh res paper_out
```

The plots and tables in the paper can now be found in the following locations:
- Fig. 2:
  - Left: `paper_out/plots/rq1/res/scatter_bounded_bisection_exact_vs_restart_exact.pdf`
  - Right: `paper_out/plots/rq1/res/scatter_bounded_bisection_float_vs_restart_float.pdf`
- Fig. 3:
  - Left: `paper_out/plots/rq1/res/scatter_quantitative_bisection-pt_exact_vs_restart_exact.pdf`
  - Right: `paper_out/plots/rq1/res/scatter_quantitative_bisection-pt_float_vs_restart_float.pdf`
- Fig. 4:
  - Left: `paper_out/plots/rq1/res/scatter_quantitative_bisection-pt_exact_vs_bisection_exact.pdf`
  - Right: `paper_out/plots/rq1/res/scatter_quantitative_bisection-pt_eps-exact_vs_bisection_eps-exact.pdf`
- Table 2: `paper_out/plots/rq3/res/rq3-exact.tex`
- Table 3: `paper_out/plots/rq2/res/rq2-exact.tex`
- Table 4: `paper_out/plots/rq2/res/rq2-float.tex`
