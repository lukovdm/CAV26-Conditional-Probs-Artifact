import os
from pathlib import Path
import click
import subprocess
import tqdm
import pandas as pd
import signal


def add_result_to_csv(
    csv_path,
    df,
    model,
    splitting,
    conditional_alg,
    conditional_bisection_optimization,
    family_size,
    avg_mdp_size,
    time,
    iterations,
):
    exists = (
        (df["model"] == model)
        & (df["splitting"] == splitting)
        & (df["conditional_alg"] == conditional_alg)
        & (df["bisection_optimization"] == conditional_bisection_optimization)
    ).any()
    if exists:
        print(
            f"Result for model={model}, splitting={splitting}, conditional_alg={conditional_alg}, bisection_optimization={conditional_bisection_optimization} already exists in CSV. Skipping addition."
        )
        return
    with open(csv_path, "a") as f:
        f.write(
            f"{model},{splitting},{conditional_alg},{conditional_bisection_optimization},{family_size},{avg_mdp_size},{time},{iterations}\n"
        )


@click.command()
@click.option(
    "--results-folder", type=str, required=True, help="Path to the results folder."
)
@click.option("--exact", is_flag=True, default=False, help="Run exact evaluation.")
@click.option(
    "--timeout", type=int, default=900, help="Timeout for each evaluation in seconds."
)
@click.option(
    "--smoke-test",
    is_flag=True,
    default=False,
    help="Run a quick smoke test with only one configuration to verify setup.",
)
@click.option(
    "--fast",
    is_flag=True,
    default=False,
    help="Run a faster version of the benchmarks by skipping some configurations (not implemented yet).",
)
def main(results_folder, exact, timeout, smoke_test, fast):
    # init results file
    if not os.path.exists(results_folder):
        os.makedirs(results_folder, exist_ok=True)
    main_csv_path = os.path.join(results_folder, "evaluation_results.csv")
    header = "model,splitting,conditional_alg,bisection_optimization,family_size,avg_mdp_size,time,iterations\n"
    if not os.path.exists(main_csv_path):
        with open(main_csv_path, "w") as f:
            f.write(header)
    else:
        # Check header
        with open(main_csv_path, "r") as f:
            first_line = f.readline()
        if first_line != header:
            raise RuntimeError(
                f"Header mismatch in {main_csv_path}. Expected: {header.strip()} Found: {first_line.strip()}"
            )
        print(f"Results file {main_csv_path} already exists. Appending new results.")

    # Parse the CSV data into a DataFrame
    df = pd.read_csv(main_csv_path)

    script_log_path = os.path.join(results_folder, "evaluation_log.log")

    # init eval parameters
    # models = {'ceaser-cipher-4-4' : 'models/conditional/ceaser-cipher-4-4', 'ceaser-cipher-4-10' : 'models/conditional/ceaser-cipher-4-10', 'ceaser-cipher-10-8' : 'models/conditional/ceaser-cipher-10-8', 'dpm' : 'models/conditional/dpm', 'dpm-queue' : 'models/conditional/dpm-queue', 'ladder-network' : 'models/conditional/ladder-network', 'ladder-network-input' : 'models/conditional/ladder-network-input', 'virus' : 'models/conditional/virus', 'airport-38' : 'models/conditional/airport-38', 'airport-47' : 'models/conditional/airport-47', 'airport-big' : 'models/conditional/airport-bigger'} # USED FOR GENERATING COMMAND
    models = {
        "ceaser-cipher-4-10": "models/conditional/ceaser-cipher-4-10",
        "ceaser-cipher-10-8": "models/conditional/ceaser-cipher-10-8",
        "dpm": "models/conditional/dpm",
        "dpm-queue": "models/conditional/dpm-queue",
        "ladder-network": "models/conditional/ladder-network",
        "ladder-network-input": "models/conditional/ladder-network-input",
        "virus": "models/conditional/virus",
        "airport": "models/conditional/airport-38",
        "airport-big": "models/conditional/airport-bigger",
    }  # USED FOR GENERATING COMMAND

    if smoke_test:
        models = {"ceaser-cipher-4-10": "models/conditional/ceaser-cipher-4-10"}

    splitting_methods = ["backward"]
    # first element is the conditional algorithm, second element is whether to use bisection optimization (only relevant for bisection algorithms)
    conditional_algorithm_settings = [
        ("bisection", True),
        ("bisection", False),
        ("bisection_advanced", False),
        ("bisection_pt", False),
        ("bisection_advanced_pt", False),
        ("restart", False),
    ]

    if fast:
        conditional_algorithm_settings = [
            ("bisection", True),
            ("bisection_pt", False),
            ("restart", False),
        ]
        del models["ladder-network"]
        del models["ladder-network-input"]

    exact_setting = "--exact" if exact else ""
    timeout_setting = f"--timeout {timeout}"

    # prepare what to run combinations
    eval_combinations = []
    for model in models.keys():
        for splitting in splitting_methods:
            for (
                conditional_alg,
                conditional_bisection_optimization,
            ) in conditional_algorithm_settings:

                eval_combinations.append(
                    (
                        model,
                        splitting,
                        conditional_alg,
                        conditional_bisection_optimization,
                    )
                )

    for (
        model,
        splitting,
        conditional_alg,
        conditional_bisection_optimization,
    ) in tqdm.tqdm(eval_combinations, mininterval=0):

        # Check if result already exists in df
        exists = (
            (df["model"] == model)
            & (df["splitting"] == splitting)
            & (df["conditional_alg"] == conditional_alg)
            & (df["bisection_optimization"] == conditional_bisection_optimization)
        ).any()

        if exists:
            print(
                f"Skipping existing result for model={model}, splitting={splitting}, conditional_alg={conditional_alg}, conditional_bisection_optimization={conditional_bisection_optimization}"
            )
            continue

        command = f"python3 -m paynt {models[model]} --conditional-algorithm {conditional_alg} --conditional-splitting {splitting} {'--conditional-bisection-optimization' if conditional_bisection_optimization else ''} {exact_setting} {timeout_setting}"

        timeout_full_val = timeout * 1.2
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=Path(os.path.abspath(__file__)).parent.parent.parent / "synthesis",
            preexec_fn=os.setsid,
        )
        try:
            output, _ = process.communicate(timeout=timeout_full_val)
            with open(script_log_path, "a") as f:
                f.write(output.decode())

            # Process the last line of the output
            last_line = output.decode().strip().split("\n")[-1]
            if ";" not in last_line:
                print("Error: Output does not contain ';' in the last line.")
            else:
                family_size, avg_mdp_size, time, iterations = [
                    part.strip() for part in last_line.split(";", 3)
                ]
                add_result_to_csv(
                    main_csv_path,
                    df,
                    model,
                    splitting,
                    conditional_alg,
                    conditional_bisection_optimization,
                    family_size,
                    avg_mdp_size,
                    time,
                    iterations,
                )
        except subprocess.TimeoutExpired:
            print(
                f"Timeout expired for model={model}, splitting={splitting}, conditional_alg={conditional_alg}, conditional_bisection_optimization={conditional_bisection_optimization}"
            )
            process.kill()
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            # Write timeout result: iterations=0, time=timeout, family_size and avg_mdp_size as '-'
            add_result_to_csv(
                main_csv_path,
                df,
                model,
                splitting,
                conditional_alg,
                conditional_bisection_optimization,
                "-",
                "-",
                timeout_full_val,
                0,
            )


if __name__ == "__main__":
    main()
