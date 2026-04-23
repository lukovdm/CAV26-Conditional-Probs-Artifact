CAV 2026 Artifact
=======================================
Paper title: Fast Computation of Conditional Probabilities in MDPs and Markov Chain Families

Claimed badges: Available + Functional + Reusable

Justification for the badges:

  * Functional: [give reasons why you believe that the Functional badge should
    be awarded (if applied for Functional or Reusable); example:  The artifact
    replicates most of the results in the paper (see below for details).  It
    compiles Tool and executes the benchmarks on it and the other tools.  We
    validate the correctness of the outputs of Tool by cross-comparison with
    the results of the other tools.  The source code of Tool is included in the
    artifact.]

    - replicated: [which claims/results of the paper are replicated by the
      artifact and how (you can, e.g., refer to a concrete point in FULL REVIEW
      below), e.g.,
       * Table 1: point (1)
       * Figure 1: point (2)
       * Figures 2 and 3: point (3)
       * Figure 4: point (4) [requires external connectivity]
       * Proof of Thm. 5: point (5)
      ]

    - not-replicated: [which claims/results cannot be replicated and why, e.g.,
       * Table 2: to reproduce the results, one needs to have access to the
                  computer Holly 6000, which is not available outside our
                  research lab
       * Table 3: this table is a result of a survey among undergraduate students
                  at the Institute of Happiness; the survey cannot be
                  reproduced as a part of the artifact, but the raw filled in
                  questionnaires are available in the directory survey/
       * Fig. 6: to obtain the results, one needs to have a working installation
                 of AcmeVerifier of Acme Inc.; if the reviewers have it,
                 they can reproduce the results by point (6) below.
      ]

  * Reusable: Our algorithms as described in the paper are built into the existing tools Storm and PAYNT. 
    + We include a unittests as part of storm here: `storm/src/test/storm/modelchecker/prctl/mdp/ConditionalMdpPrctlModelCheckerTest.cpp`. Furthermore, all changes in Storm have already been merged into upstream and will be released within short notice. After it is released, you will be able to install storm with python bindings using the python package manager: `pip install stormpy`. Until such time nightly builds of storm and stormpy docker containers are availabe where one can use the _treat_ algorithm and its bisection variants. The docker container used for this artifact is based on these containers.
    Lastly, we have included a Jupyter notebook detailing how the python bindings of storm can be used to model check conditional properties on MDPs. More documentatian on Storm and Stormpy can also be found here: https://www.stormchecker.org/.
    + _Expectations on adding the conditional algs to PAYNT._


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
./run_all.sh    # [to run the full version ~ runtime: n hours]
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
