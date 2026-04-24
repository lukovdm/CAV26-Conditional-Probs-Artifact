CAV 2026 Artifact
=======================================
Paper title: Fast Computation of Conditional Probabilities in MDPs and Markov Chain Families

Claimed badges: Available + Functional + Reusable

Justification for the badges:
  * **Functional**:
    - All experiments can be rerun in the docker file using three simple scripts, and this raw data can be automatically formatted as presented in the paper. We additionally provide the raw data we used to generate our submitted tables and figures. The results in figures 2-4 and tables 2-4 can be replicated by following the full review steps. Table 1 is a hand combined version of tables 3 and 4.
    - The full source code of the tools is attached with the artifact. The tools can be compiled by following the instructions availabe in their respective README files. We also provide a docker container with all tools already installed.
  * **Reusable**: 
    + Our algorithms as described in the paper are built into the existing tool Storm with its python bindings stormpy.
    + In our docker image you can use the storm tool to model check conditional properties on any MDP accepted by storm (i.e. in the .prism, .jani, .drn, and .umb formats). Additionally you can use our python bindings to do any of these operations from within python. Examples of this can be found in the notebook: [notebooks/Usage.ipynb].
    + We include a unittests as part of storm here: `storm/src/test/storm/modelchecker/prctl/mdp/ConditionalMdpPrctlModelCheckerTest.cpp`. 
    + All changes in Storm have already been merged into upstream and will be released as part of Storm 1.13. After it is released, you will be able to install storm with python bindings using the python package manager: `pip install stormpy`.
    + More documentatian on Storm and Stormpy can also be found here: https://www.stormchecker.org/.

Requirements:
  * RAM: 8GB
  * CPU cores: 8 (If you use more cores the benchmarks will go faster and consume more RAM)
  * Time (smoke test): [expected time to execute the smoke test on a standard
    laptop (including compilation, installation, etc.)]
  * Time (full review): [expected time to execute the full review (do not
    include the time of reviewers reading the paper, playing with the tool on
    their own, etc.)]

external connectivity: NO

**SMOKE TEST**
-------------------------------------------------------------------------------

Run the following to load the Docker image:

```bash
docker load < docker-tool-image.tar
```

After that, run the image using

```bash
docker run -v `pwd`/output:/tool/output --rm -it docker-tool
```

The command above starts the docker container and places you in a bash
environment, where you can inspect the source code or run the experiments. `-v`
option will mount `output` folder in your current directory to the
corresponding folder within the container where the evaluation results will be
stored. This will allow you to view the generated output even after the
container has stopped running. `--rm` is an optional flag that creates a
disposable container that will be deleted upon exit.

Start the smoke test with

```bash
./run-smoke.sh      # [ ~ runtime: 10 minutes]
```

The smoke test runs all tools on a reduced set of benchmarks and configurations.
If everything runs successfully, the script should print out intermediate progress.

To generate the plots for the smoke test you can run the following command:
```bash
./create_plots.sh smoke_test out
```

It will generate plots in the folders `out/plots/rqn/smoke_test/`. 
 - There should be [n] files in `out/plots/rq1/smoke_test/`
 - There should be [n] files in `out/plots/rq2/smoke_test/`
 - There should be 2 files in `out/plots/rq3/smoke_test/`

For completeness, we included the output files obtained by our experiments in
the folder `ref_out/`.

If the results are not as described above, please check the output of `smoke_test.sh` and `create_plots.sh`, compare to the log files in `ref_logs/smoke_test/` and include any different parts
of the log in the review.

**FULL REVIEW**
--------------------------------

Assuming the smoke test passed, run the following command to reproduce the
results. Running the full benchmark suite can take around 18 hours on a standard
laptop.

```bash
./run_all.sh    # [runtime: 18 hours]
```

The commands will print out progress as they execute the benchmarks.
The output will be in the folders `out/rqn/res/`.

For completeness, we included the output files obtained by our experiments in
folder `ref_out/`.

In the following outputs, concrete values may be differt but the overall trends should stay the same.

To generate the plots for the full experiments you can run the following command:
```bash
./create_plots.sh res out
```

The plots and tables in the paper can now be found in the following locations:
- Fig. 2:
  - Left: `out/plots/rq1/res/scatter_bounded_bisection_exact_vs_restart_exact.pdf`
  - Right: `out/plots/rq1/res/scatter_bounded_bisection_float_vs_restart_float.pdf`
- Fig. 3:
  - Left: `out/plots/rq1/res/scatter_quantitative_bisection-pt_exact_vs_restart_exact.pdf`
  - Right: `out/plots/rq1/res/scatter_quantitative_bisection-pt_float_vs_restart_float.pdf`
- Fig. 4:
  - Left: `out/plots/rq1/res/scatter_quantitative_bisection-pt_exact_vs_bisection_exact.pdf`
  - Right: `out/plots/rq1/res/scatter_quantitative_bisection-pt_eps-exact_vs_bisection_eps-exact.pdf`
- Table 2: `out/plots/rq3/res/rq3-exact.tex`
- Table 3: `out/plots/rq2/res/rq2-exact.tex`
- Table 4: `out/plots/rq2/res/rq2-float.tex`

> Note that we did find a bug in our experiments for RQ2. This changed the Tables 3 and 4 a bit. These changes did not affect our analysis or conclusions of RQ2.

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
