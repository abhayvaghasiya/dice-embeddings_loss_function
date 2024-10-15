import os
import json
import pandas as pd

# Path to the main directory containing all the folders
main_dir = '/Users/abhayvaghasiya/Desktop/WORK/label_smoothing/WN18RR/OUTPUT_file_WN18RR_with_label_smoothing_0.3'

# Define the order of models and perturbation ratios
model_order = ['ComplEx', 'DistMult', 'Keci', 'QMult', 'Pykeen_MuRE']
perturbation_order = ['0.0', '0.01', '0.02', '0.04', '0.08', '0.16', '0.32', '0.64']

# Prepare an empty list to hold all results
all_results = []

# Iterate over each model
for model in model_order:
    # Iterate over each perturbation ratio
    for perturbation in perturbation_order:
        # Construct the expected folder name
        if model == "Pykeen_MuRE":
            folder_name = f"{model}_{perturbation}_seed1"
        else:
            folder_name = f"{model}_{perturbation}_seed1"
        folder_path = os.path.join(main_dir, folder_name)
        
        # Check if the folder exists
        if os.path.isdir(folder_path):
            # Define the specific JSON file path
            json_file_path = os.path.join(folder_path, 'eval_report.json')
            
            # Check if the specific JSON file exists
            if os.path.exists(json_file_path):
                try:
                    # Load JSON data
                    with open(json_file_path, 'r') as file:
                        data = json.load(file)
                    
                    # Construct the model name for the results
                    model_name = f"{model}_{perturbation}"
                    
                    # Extract data and format it
                    results = {
                        "Model": model_name,
                        "Train H@1": data["Train"]["H@1"],
                        "Train H@3": data["Train"]["H@3"],
                        "Train H@10": data["Train"]["H@10"],
                        "Train MRR": data["Train"]["MRR"],
                        "Val H@1": data["Val"]["H@1"],
                        "Val H@3": data["Val"]["H@3"],
                        "Val H@10": data["Val"]["H@10"],
                        "Val MRR": data["Val"]["MRR"],
                        "Test H@1": data["Test"]["H@1"],
                        "Test H@3": data["Test"]["H@3"],
                        "Test H@10": data["Test"]["H@10"],
                        "Test MRR": data["Test"]["MRR"]
                    }
                    
                    all_results.append(results)
                    print(f"Processed: {model_name}")
                except Exception as e:
                    print(f"Error processing {json_file_path}: {str(e)}")
            else:
                print(f"JSON file not found: {json_file_path}")
        else:
            print(f"Folder not found: {folder_path}")

# Check if we have any results
if not all_results:
    print("No data was processed. Check the main directory path and folder structure.")
else:
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(all_results)

    # Sort the DataFrame based on the order of models and perturbations
    df['model'] = df['Model'].apply(lambda x: x.split('_')[0])
    df['perturbation'] = df['Model'].apply(lambda x: x.split('_')[1])
    df['model_order'] = df['model'].map({m: i for i, m in enumerate(model_order)})
    df['perturbation_order'] = df['perturbation'].map({p: i for i, p in enumerate(perturbation_order)})
    df_sorted = df.sort_values(['model_order', 'perturbation_order']).drop(['model', 'perturbation', 'model_order', 'perturbation_order'], axis=1)

    # Specify the path for the output Excel file
    output_excel_path = '/Users/abhayvaghasiya/Desktop/WORK/label_smoothing/WN18RR/WN18RR_compiled_results_with_label_smoothing_0.3.xlsx'

    # Save DataFrame to Excel
    df_sorted.to_excel(output_excel_path, index=False)

    print(f"All data has been compiled and sorted into: {output_excel_path}")
    print(f"Total number of processed results: {len(all_results)}")