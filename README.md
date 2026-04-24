CAV 2026 Artifact
=======================================
Paper title: Fast Computation of Conditional Probabilities in MDPs and Markov Chain Families

Claimed badges: Available + Functional + Reusable

Justification for the badges:
  * **Functional**:
    - All experiments can be rerun in the docker file using three simple scripts, and this raw data can be automatically formatted as presented in the paper. We additionally provide the raw data we used to generate our submitted tables and figures. The results in figures 2-4 and tables 2-4 can be replicated by following the full review steps. Table 1 is a hand combined version of tables 3 and 4.
    - The full source code of the tools is attached with the artifact. The tools can be compiled by following the instructions available in their respective README files. We also provide a docker container with all tools already installed.
  * **Reusable**: 
    + Our algorithms as described in the paper are built into the existing tool Storm with its python bindings stormpy.
    + In our docker image you can use the storm tool to model check conditional properties on any MDP accepted by storm (i.e., in the `.prism`, `.jani`, `.drn`, and `.umb` formats). Additionally, you can use our python bindings to do any of these operations from within python. Examples of this can be found in the notebook: [notebooks/Usage.ipynb].
    + We include a unittests as part of storm here: `storm/src/test/storm/modelchecker/prctl/mdp/ConditionalMdpPrctlModelCheckerTest.cpp`. 
    + All changes in Storm have already been merged into upstream and will be released as part of Storm 1.13. After it is released, you will be able to install storm with python bindings using the python package manager: `pip install stormpy`.
    + More documentation on Storm and Stormpy can also be found here: https://www.stormchecker.org/.

Requirements:
  * RAM: 8GB
  * CPU cores: 8 (If you use more cores the benchmarks will go faster and consume more RAM)
  * Time (smoke test): [expected time to execute the smoke test on a standard
    laptop (including compilation, installation, etc.)]
  * Time (full review): [expected time to execute the full review (do not
    include the time of reviewers reading the paper, playing with the tool on
    their own, etc.)]

external connectivity: NO

### Contents
- Smoke Test
- Full Review
- Example Usage Notebook
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

The command above starts the docker container and places you in a bash environment, where you can inspect the source code or run the experiments. A Jupyter Lab environment is started at the same time and can be accessed at [http://127.0.0.1:8888/...]() to view any files in the docker container.

Start the smoke test with

```bash
./run-smoke.sh      # [ ~ runtime: 3 minutes]
```

The smoke test runs all tools on a reduced set of benchmarks and configurations.
If everything runs successfully, the script should print out intermediate progress.

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
results. Running the full benchmark suite can take around 18 hours on a standard
laptop.

```bash
./run_all.sh    # [runtime: 18 hours]
```

We also provide a reduced experiment set. This experiment set supports our main results while skipping many experiments only used for auxiliary results. This set takes around [n hours]. The reduced experiment set takes a seeded random subset of all models and only runs methods directly contributing to the figures in the paper.

```bash
./run_fast.sh
```

The commands will print out progress as they execute the benchmarks.

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

> Note that we did find a bug in our experiments for RQ2. This changed the tables 3 and 4 a bit. These changes did not affect our analysis or conclusions of RQ2.

**Example Usage Notebook**
----------------------------------------

We provide a notebook showing example usages of our tool. When starting the docker image a Jupyter Lab server is started alongside it. You can access this Jupyter notebook server using the following URL: [http://127.0.0.1:8888/]. In the folder notebooks you can open the file `Usage.ipynb`.

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
