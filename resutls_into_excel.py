import os
import json
import pandas as pd

# Path to the main directory containing all the folders
main_dir = '/Users/abhayvaghasiya/Desktop/WORK/Robust results/OUTPUT_file_UMLS_0.3-0.7'

# Define the order of models and perturbation ratios
model_order = ['ComplEx', 'Pykeen_MuRE', 'DistMult', 'Keci', 'QMult']
perturbation_order = ['0.0', '0.01', '0.02', '0.04', '0.08', '0.16', '0.32', '0.64']

# Prepare an empty list to hold all results
all_results = []

# Iterate over each directory in the main directory
for folder_name in os.listdir(main_dir):
    folder_path = os.path.join(main_dir, folder_name)
    
    # Check if the path is indeed a directory
    if os.path.isdir(folder_path):
        # Define the specific JSON file path
        json_file_path = os.path.join(folder_path, 'eval_report.json')
        
        # Check if the specific JSON file exists
        if os.path.exists(json_file_path):
            # Load JSON data
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            
            # Extract model name and perturbation ratio from folder name
            parts = folder_name.split('_')
            model = parts[0]
            perturbation = parts[1]
            
            # Extract data and format it
            results = {
                "Model": f"{model}_{perturbation}",
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

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(all_results)

# Create a custom sorting key
def custom_sort(row):
    model = row['Model'].split('_')[0]
    perturbation = row['Model'].split('_')[1]
    
    # Find the index of the model, use len(model_order) if not found
    model_index = next((i for i, m in enumerate(model_order) if m.lower() == model.lower()), len(model_order))
    
    # Find the index of the perturbation, use len(perturbation_order) if not found
    perturb_index = next((i for i, p in enumerate(perturbation_order) if p == perturbation), len(perturbation_order))
    
    return (model_index, perturb_index)

# Sort the DataFrame using the custom sorting function
df['sort_key'] = df.apply(custom_sort, axis=1)
df_sorted = df.sort_values('sort_key').drop('sort_key', axis=1)

# Specify the path for the output Excel file
output_excel_path = '/Users/abhayvaghasiya/Desktop/WORK/Robust results/UMLS_compiled_results_with_scalling_0.3-0.7.xlsx'

# Save DataFrame to Excel
df_sorted.to_excel(output_excel_path, index=False)

print("All data has been compiled and sorted into:", output_excel_path)