#!/bin/bash

base_dir="/Users/abhayvaghasiya/Desktop/WORK/dataset_label_smoothing_UMLS"
output_dir="/Users/abhayvaghasiya/Desktop/WORK/Robust results/OUTPUT_file_UMLS_0.3-0.7"
model_list=("ComplEx" "Pykeen_MuRE" "DistMult" "Keci" "QMult")
embedding_dim=32
num_epochs=100
batch_size=1024
lr=0.1
eval_model="train_val_test"
random_seed=1

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop through each perturbation folder
for perturb_folder in "$base_dir"/*; do
    if [ -d "$perturb_folder" ]; then
        perturb_ratio=$(basename "$perturb_folder")
        
        # Loop through each model
        for model in "${model_list[@]}"; do
            output_path="${output_dir}/${model}_${perturb_ratio}_seed${random_seed}"
            
            echo "Running ${model} on dataset with perturbation ${perturb_ratio}, seed ${random_seed}"
            
            python -m dicee.scripts.run \
                --dataset_dir "$perturb_folder" \
                --model "$model" \
                --embedding_dim "$embedding_dim" \
                --random_seed "$random_seed" \
                --eval_model "$eval_model" \
                --num_epochs "$num_epochs" \
                --batch_size "$batch_size" \
                --lr "$lr" \
                --path_to_store_single_run "$output_path"
            
            echo "Finished running ${model} on dataset with perturbation ${perturb_ratio}, seed ${random_seed}"
            echo "Results stored in: $output_path"
            echo "----------------------------------------"
        done
    fi
done

echo "All runs completed."