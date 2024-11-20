#!/bin/bash

# Set random seed
export PYTHONHASHSEED=1
export CUDA_LAUNCH_BLOCKING=1

# Dataset and output directories
dataset_dir="/Users/abhayvaghasiya/Desktop/WORK/Datasets/Datasets_Perturbed/UMLS/0.01"
output_dir="/Users/abhayvaghasiya/Desktop/WORK/UMLS_updated_Label_smoothing"

# Model parameters
model_list=("ComplEx" "Pykeen_MuRE" "DistMult" "Keci" "QMult")
embedding_dim=32
num_epochs=100
batch_size=1024
lr=0.1
eval_model="train_val_test"
scaler=0.3
random_seed=1  # Set the random seed here for consistent usage below
label_smoothing_rate=0.1  # Added label smoothing rate

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Get dataset name for output namings
dataset="UMLS"

# Loop through each model and k value
for model in "${model_list[@]}"; do
    for k in 0.01 ; do
        output_path="${output_dir}/${dataset}-${model}-${k}"
        
        echo "Running ${model} on dataset ${dataset}, k=${k}, seed ${random_seed}"
        
        python -m dicee.scripts.run \
            --trainer torchCPUTrainer \
            --path_to_store_single_run "$output_path" \
            --model "$model" \
            --embedding_dim "$embedding_dim" \
            --num_epochs "$num_epochs" \
            --batch_size "$batch_size" \
            --random_seed "$random_seed" \
            --label_smoothing_rate "$label_smoothing_rate" \
            --eval_model "$eval_model" \
            --lr "$lr" \
            --dataset_dir "$dataset_dir"
        
        echo "Finished running ${model} on dataset ${dataset}, k=${k}, seed ${random_seed}"
        echo "Results stored in: $output_path"
        echo "----------------------------------------"
    done
done

echo "All runs completed."