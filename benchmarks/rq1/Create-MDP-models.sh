#!/bin/bash
set -x

skip=$1
if [ -z "$skip" ]; then
    skip=0
fi


vt=exact

# Load common DTMC benchmarks
if [ "$skip" -le 0 ]; then
    prism_folder="models/common-dtmc"
    out_folder="models/transformed-mdp"

    brp_constants_list=("N=16,MAX=8,PCHAN=0.1" "N=32,MAX=8,PCHAN=0.1" "N=64,MAX=8,PCHAN=0.1"  "N=128,MAX=8,PCHAN=0.1"
                        "N=16,MAX=8,PCHAN=0.2" "N=32,MAX=8,PCHAN=0.2" "N=64,MAX=8,PCHAN=0.2"  "N=128,MAX=8,PCHAN=0.2")
    uncertainty_list=("0.05" "0.15")
    brp_filename="brp.pm"
    for uncertainty in "${uncertainty_list[@]}"; do
      for constants in "${brp_constants_list[@]}"; do
          new_filename="brp-${constants//,/-}-${uncertainty}.drn"
          echo "Processing $brp_filename with constants $constants"
          if [ -f "$out_folder/$new_filename" ]; then
              echo "Output file already exists, skipping..."
              continue
          fi
          python add_uncertainty.py "$prism_folder/$brp_filename" "$out_folder/$new_filename" --type mdp --uncertainty ${uncertainty} --$vt --constants "$constants" --copy-labels
      done
    done

    egl_constants_list=("N=4,L=12" "N=5,L=16")
    uncertainty_list=("0.05" "0.15")
    egl_filename="egl.pm"
    for uncertainty in "${uncertainty_list[@]}"; do
      for constants in "${egl_constants_list[@]}"; do
          new_filename="egl-${constants//,/-}-${uncertainty}.drn"
          echo "Processing $egl_filename with constants $constants"
          if [ -f "$out_folder/$new_filename" ]; then
              echo "Output file already exists, skipping..."
              continue
          fi
          python add_uncertainty.py "$prism_folder/$egl_filename" "$out_folder/$new_filename" --type mdp --uncertainty ${uncertainty} --$vt --constants "$constants" --copy-labels
      done
    done

    too_big=("crowds_20-5")
    uncertainty_list=("0.01" "0.05" "0.15")
    for uncertainty in "${uncertainty_list[@]}"; do
      for file in $(ls -lS "$prism_folder"/crowds_*.pm | awk '{print $9}' | tac); do
          filename=$(basename "$file" .pm)
          if [[ " ${too_big[@]} " =~ " ${filename} " ]]; then
              echo "Skipping too big model $filename"
              continue
          fi
          echo "Processing $filename.pm"
          if [ -f "$out_folder/$filename-${uncertainty}.drn" ]; then
              echo "Output file already exists, skipping..."
              continue
          fi
          python add_uncertainty.py "$prism_folder/$filename.pm" "$out_folder/$filename-${uncertainty}.drn" --type mdp --uncertainty ${uncertainty} --$vt --copy-labels
      done
    done
fi
#
## Load wlan benchmarks
if [ "$skip" -le 1 ]; then
    coins_constants_list=("K=4" "K=8" "K=12")
    coins_files=("03" "04" "05")

    for coins in "${coins_files[@]}"; do
        coin_filename="coin.${coins}.prism"

        for constants in "${coins_constants_list[@]}"; do
            new_filename="coin-${coins}-${constants}.drn"
            echo "Processing $wlan_filename with constants $constants"
            if [ -f "./models/concrete-mdps/$new_filename" ]; then
                echo "Output file already exists, skipping..."
                continue
            fi
            ../../storm/build/bin/storm --prism ./models/baier-mdps/${coin_filename} --constants "$constants" --exportbuild ./models/concrete-mdps/${new_filename} --build-all-labels
        done
    done

    wlan_constants_list=("BOFF=4" "BOFF=6" "BOFF=10")
    for constants in "${wlan_constants_list[@]}"; do
        new_filename="wlan-${constants}.drn"
        echo "Processing $wlan_filename with constants $constants"
        if [ -f "./models/concrete-mdps/$new_filename" ]; then
            echo "Output file already exists, skipping..."
            continue
        fi
        ../../storm/build/bin/storm --prism ./models/baier-mdps/wlan.nm --constants "$constants" --exportbuild ./models/concrete-mdps/${new_filename} --build-all-labels
    done
fi

## Load BN benchmarks
if [ "$skip" -le 3 ]; then
    jani_folder="models/BN-benchmarks-dtmc"
    out_folder="models/BN-benchmarks-mdp"
    bad_models=("sachs" "insurance" "andes" "pathfinder" "barley") # Models are not probabilistic

    for file in $(ls -lS "$jani_folder"/*.jani | awk '{print $9}' | tac); do
        filename=$(basename "$file" .jani)
        if [[ " ${bad_models[@]} " =~ " ${filename} " ]]; then
            echo "Skipping bad model $filename"
            continue
        fi
        echo "Processing $filename.jani"
        if [ -f "$out_folder/$filename.drn" ]; then
            echo "Output file already exists, skipping..."
            continue
        fi
        python add_uncertainty.py "$file" "$out_folder/$filename.drn" --type mdp --uncertainty $uncertainty --$vt
    done
fi