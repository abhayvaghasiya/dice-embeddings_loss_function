#!/bin/bash

# Dataset directory
dataset_dir="/Users/abhayvaghasiya/Desktop/WORK/Datasets_Perturbed_PI/UMLS/0.0/UMLS"
output_dir="/Users/abhayvaghasiya/Desktop/WORK/Without_coppel_Pi_score/UMLS_2/OUTPUT_file_UMLS_PI_score_0.1-0.9"
model_list=("ComplEx" "Pykeen_MuRE" "DistMult" "Keci" "QMult")
embedding_dim=32
num_epochs=100
batch_size=1024
lr=0.1
eval_model="train_val_test"
random_seed=1

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Get dataset name for output namings
dataset_name=$(basename "$dataset_dir")

# Loop through each model
for model in "${model_list[@]}"; do
    output_path="${output_dir}/${model}_.0_${dataset_name}_seed${random_seed}"
    
    echo "Running ${model} on dataset ${dataset_name}, seed ${random_seed}"
    
    python -m dicee.scripts.run \
        --dataset_dir "$dataset_dir" \
        --model "$model" \
        --embedding_dim "$embedding_dim" \
        --random_seed "$random_seed" \
        --eval_model "$eval_model" \
        --num_epochs "$num_epochs" \
        --batch_size "$batch_size" \
        --lr "$lr" \
        --path_to_store_single_run "$output_path"
    
    echo "Finished running ${model} on dataset ${dataset_name}, seed ${random_seed}"
    echo "Results stored in: $output_path"
    echo "----------------------------------------"
done

echo "All runs completed."