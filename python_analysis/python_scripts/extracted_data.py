import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create directories for outputs
os.makedirs('../tables', exist_ok=True)
os.makedirs('../figures', exist_ok=True)

# Define the cardiovascular risk factors
risk_factors = {
    'bmi': 'Body Mass Index',
    'wc': 'Waist Circumference',
    'bp_sys': 'Systolic Blood Pressure',
    'bp_dia': 'Diastolic Blood Pressure',
    'chol': 'Total Cholesterol',
    'hdl': 'High-Density Lipoprotein',
    'ldl': 'Low-Density Lipoprotein',
    'trig': 'Triglycerides',
    'glc_meta': 'Glucose Metabolism',
    'insul': 'Insulin'
}

# Function to extract data from the results file
def extract_data(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split by risk factor sections
    sections = {}
    current_section = None
    
    for line in content.split('\n'):
        if line.startswith('DepVar: ['):
            current_section = line.strip('DepVar: []')
            sections[current_section] = []
        elif current_section and line and not line.startswith('DepVar,'):
            sections[current_section].append(line)
    
    # Process each section into a DataFrame
    dataframes = {}
    
    for factor, lines in sections.items():
        if not lines:
            continue
            
        data = []
        for line in lines:
            if 'NO_DATA' in line:
                parts = line.split(',')
                age = int(parts[0].split('_')[-1])
                data.append({
                    'Age': age,
                    'Coefficient': None,
                    'CI_Lower': None,
                    'CI_Upper': None,
                    'P_value': None,
                    'R2': None,
                    'N': None,
                    'Missing': None
                })
            else:
                parts = line.split(',')
                age = int(parts[0].split('_')[-1])
                
                # Extract coefficient and CI
                coef_ci = parts[1]
                coef = float(coef_ci.split('(')[0])
                ci_parts = coef_ci.split('(')[1].split(' to ')
                ci_lower = float(ci_parts[0])
                ci_upper = float(ci_parts[1].strip(')'))
                
                # Extract other values
                p_value = float(parts[2])
                r2 = float(parts[3])
                n = int(parts[4])
                missing = int(parts[5])
                
                data.append({
                    'Age': age,
                    'Coefficient': coef,
                    'CI_Lower': ci_lower,
                    'CI_Upper': ci_upper,
                    'P_value': p_value,
                    'R2': r2,
                    'N': n,
                    'Missing': missing
                })
        
        df = pd.DataFrame(data)
        df = df.sort_values('Age')
        dataframes[factor] = df
    
    return dataframes

# Extract data from the results file
data_frames = extract_data('../tables/stata_regress_zscore_by_depvar_by_age.csv')

# Save each DataFrame to a CSV file
for factor, df in data_frames.items():
    df.to_csv(f'../tables/{factor}_results.csv', index=False)

# Create a summary DataFrame with key information
summary_data = []

for factor, df in data_frames.items():
    for _, row in df.iterrows():
        if row['Coefficient'] is not None:
            significance = "***" if row['P_value'] < 0.001 else "**" if row['P_value'] < 0.01 else "*" if row['P_value'] < 0.05 else ""
            summary_data.append({
                'Risk Factor': risk_factors.get(factor, factor),
                'Age': row['Age'],
                'Coefficient': row['Coefficient'],
                'CI_Lower': row['CI_Lower'],
                'CI_Upper': row['CI_Upper'],
                'P_value': row['P_value'],
                'Significance': significance,
                'R2': row['R2'],
                'N': row['N']
            })

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('../tables/all_results_summary.csv', index=False)

# Create a more readable summary table
readable_summary = []

for factor, df in data_frames.items():
    for _, row in df.iterrows():
        if row['Coefficient'] is not None:
            significance = "***" if row['P_value'] < 0.001 else "**" if row['P_value'] < 0.01 else "*" if row['P_value'] < 0.05 else ""
            coef_with_ci = f"{row['Coefficient']:.4f} ({row['CI_Lower']:.4f} to {row['CI_Upper']:.4f}){significance}"
            readable_summary.append({
                'Risk Factor': risk_factors.get(factor, factor),
                'Age': row['Age'],
                'Coefficient (95% CI)': coef_with_ci,
                'P-value': f"{row['P_value']:.4f}",
                'R²': f"{row['R2']:.4f}",
                'Sample Size': row['N']
            })

readable_df = pd.DataFrame(readable_summary)
readable_df = readable_df.sort_values(['Risk Factor', 'Age'])
readable_df.to_csv('../tables/readable_summary.csv', index=False)

print("Data extraction and organization complete.")
