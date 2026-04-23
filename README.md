CAV 2026 Artifact
=======================================
Paper title: Fast Computation of Conditional Probabilities in MDPs and Markov Chain Families

Claimed badges: Available + Functional + Reusable

Justification for the badges:

  * Functional: 
    - The full source code of the tools is attached with the artifact. The tools can be compiled by following the instructions availabe in their respective README files. We also provide a docker container with all tools already installed.
    - All results presented in the paper can be reproduced using this artifact. The results in Figures 2-4 and Tables 2-4 can be replicated by following the full review steps. Table 1 is a hand combined version of Tables 3 and 4.

  * Reusable: Our algorithms as described in the paper are built into the existing tool Storm with its python bindings stormpy. 
    + We include a unittests as part of storm here: `storm/src/test/storm/modelchecker/prctl/mdp/ConditionalMdpPrctlModelCheckerTest.cpp`. Furthermore, all changes in Storm have already been merged into upstream and will be released within short notice. After it is released, you will be able to install storm with python bindings using the python package manager: `pip install stormpy`. Until such time nightly builds of storm and stormpy docker containers are availabe where one can use the _treat_ algorithm and its bisection variants. The docker container used for this artifact is based on these containers.
    + Lastly, we have included a Jupyter notebook detailing how the python bindings of storm can be used to model check conditional properties on MDPs. More documentatian on Storm and Stormpy can also be found here: https://www.stormchecker.org/.


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
If everything runs successfully, the script should print out intermediate progress, similar to the following:

```
[fill in]
```

To generate the plots for the smoke test you can run the following command:
```bash
./create_plots.sh smoke_test
```

It will generate plots in the folders `out/plots/rqn/smoke_test/`. 
 - There should be [n] files in `out/plots/rq1/smoke_test/`
 - There should be [n] files in `out/plots/rq2/smoke_test/`
 - There should be [n] files in `out/plots/rq3/smoke_test/`

For completeness, we included the output files obtained by our experiments in
the folder `ref_out/`.

If the results are not as described above, please check the output of `smoke_test.sh` and `create_plots.sh`, compare to the log files in `ref_logs/smoke_test/` and include any different parts
of the log in the review.

**FULL REVIEW**
--------------------------------

Assuming the smoke test passed, run the following command to reproduce the
results. Running the full benchmark suite can take around [n hours] on a standard
laptop.

```bash
./run_all.sh    # [runtime: n hours]
```

The commands will print out progress as their execute the benchmarks.
The output will be in the folders `out/rqn/res/`.

For completeness, we included the output files obtained by our experiments in
folder `ref_out/`.

In the following outputs, concrete values may be differt but the overall trends should stay the same.

To generate the plots for the full experiments you can run the following command:
```bash
./create_plots.sh res
```

The plots and tables in the paper can now be found in the following locations:
- Fig. 2:
  - Left: out/plots/rq1/res/scatter_bounded_bisection_exact_vs_restart_exact.pdf"
  - Right: out/plots/rq1/res/scatter_bounded_bisection_float_vs_restart_float.pdf"
- Fig. 3:
  - Left: out/plots/rq1/res/scatter_quantitative_bisection-pt_exact_vs_restart_exact.pdf"
  - Right: out/plots/rq1/res/scatter_quantitative_bisection-pt_float_vs_restart_float.pdf"
- Fig. 4:
  - Left: out/plots/rq1/res/scatter_quantitative_bisection-pt_exact_vs_bisection_exact.pdf"
  - Right: out/plots/rq1/res/scatter_quantitative_bisection-pt_eps-exact_vs_bisection_eps-exact.pdf"
- Table 3: out/plots/rq2/res/rq2-exact.tex"
- Table 4: out/plots/rq2/res/rq2-float.tex"