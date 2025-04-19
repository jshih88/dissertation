import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Create directories for outputs
os.makedirs('../figures', exist_ok=True)
os.makedirs('../docs', exist_ok=True)

# Load the summary data
summary_df = pd.read_csv('../tables/readable_summary.csv')

# Fix the diastolic blood pressure and glucose metabolism labels
summary_df.loc[summary_df['Risk Factor'] == 'bp_di', 'Risk Factor'] = 'Diastolic Blood Pressure'
summary_df.loc[summary_df['Risk Factor'] == 'glc_met', 'Risk Factor'] = 'Glucose Metabolism'

# Remove rows with NaN coefficients
summary_df = summary_df.dropna(subset=['Coefficient (95% CI)'])

# Extract numeric coefficient from the string format
def extract_coefficient(coef_str):
    return float(coef_str.split(' ')[0])

summary_df['Coefficient'] = summary_df['Coefficient (95% CI)'].apply(extract_coefficient)

# Extract p-value as numeric
summary_df['P-value_numeric'] = summary_df['P-value'].astype(float)

# Create significance indicator
summary_df['Significant'] = summary_df['P-value_numeric'] < 0.05

# Group data by age
age_groups = summary_df.groupby('Age')

# Function to analyse data by age
def analyse_by_age(age, data):
    """Analyse the relationship between cognitive ability and cardiovascular risk factors at a specific age."""
    # Sort by absolute coefficient value to see strongest associations first
    sorted_data = data.sort_values(by='Coefficient', key=abs, ascending=False)
    
    # Count significant associations
    sig_count = sorted_data['Significant'].sum()
    total_count = len(sorted_data)
    
    # Calculate percentage of significant associations
    sig_percent = (sig_count / total_count) * 100 if total_count > 0 else 0
    
    # Identify direction of associations (negative or positive)
    neg_count = (sorted_data['Coefficient'] < 0).sum()
    pos_count = (sorted_data['Coefficient'] > 0).sum()
    
    # Calculate average effect size
    avg_effect = sorted_data['Coefficient'].abs().mean()
    
    # Identify strongest association
    strongest_idx = sorted_data['Coefficient'].abs().idxmax()
    strongest = sorted_data.loc[strongest_idx]
    
    # Create summary
    summary = {
        'Age': age,
        'Total Factors Measured': total_count,
        'Significant Associations': sig_count,
        'Percent Significant': sig_percent,
        'Negative Associations': neg_count,
        'Positive Associations': pos_count,
        'Average Effect Size': avg_effect,
        'Strongest Association': strongest['Risk Factor'],
        'Strongest Coefficient': strongest['Coefficient'],
        'Strongest P-value': strongest['P-value_numeric']
    }
    
    return summary, sorted_data

# Analyse each age group
age_analyses = []
for age, data in age_groups:
    summary, sorted_data = analyse_by_age(age, data)
    age_analyses.append(summary)
    
    # Create a bar plot for this age
    plt.figure(figsize=(12, 8))
    
    # Create color map based on significance
    colors = ['#3498db' if sig else '#d3d3d3' for sig in sorted_data['Significant']]
    
    # Create bar plot
    bars = plt.barh(sorted_data['Risk Factor'], sorted_data['Coefficient'], color=colors)
    
    # Add error bars (would need to extract CI values)
    
    # Add zero line
    plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    
    # Add labels and title
    plt.xlabel('Standardised Coefficient')
    plt.ylabel('Cardiovascular Risk Factor')
    plt.title(f'Association Between Childhood IQ at Age 8 and Cardiovascular Risk Factors at Age {int(age)}')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', label='Significant (p < 0.05)'),
        Patch(facecolor='#d3d3d3', label='Non-significant')
    ]
    plt.legend(handles=legend_elements, loc='lower right')
    
    # Add coefficient values as text
    for i, bar in enumerate(bars):
        coef = sorted_data['Coefficient'].iloc[i]
        p_val = sorted_data['P-value_numeric'].iloc[i]
        text_color = 'black'
        if p_val < 0.001:
            sig_stars = '***'
        elif p_val < 0.01:
            sig_stars = '**'
        elif p_val < 0.05:
            sig_stars = '*'
        else:
            sig_stars = ''
        
        # Position text based on bar direction
        if coef < 0:
            plt.text(coef - 0.0005, i, f'{coef:.4f}{sig_stars}', 
                     va='center', ha='right', color=text_color, fontweight='bold')
        else:
            plt.text(coef + 0.0005, i, f'{coef:.4f}{sig_stars}', 
                     va='center', ha='left', color=text_color, fontweight='bold')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(f'../figures/age_{int(age)}_associations.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create a summary DataFrame for age analyses
age_summary_df = pd.DataFrame(age_analyses)
age_summary_df.to_csv('../tables/age_summary.csv', index=False)

# Create a heatmap of all associations
pivot_data = summary_df.pivot(index='Risk Factor', columns='Age', values='Coefficient')

# Create a custom colormap (blue for negative, red for positive, white for zero)
colors = ['#1a76c4', '#ffffff', '#e74c3c']  # blue, white, red
cmap = LinearSegmentedColormap.from_list('custom_diverging', colors, N=256)

plt.figure(figsize=(14, 10))
ax = sns.heatmap(pivot_data, cmap=cmap, center=0, 
                 annot=True, fmt='.4f', linewidths=.5, 
                 cbar_kws={'label': 'Standardised Coefficient'})

# Add title and labels
plt.title('Heatmap of Associations Between Childhood IQ at Age 8 and Cardiovascular Risk Factors Across Ages', 
          fontsize=14, pad=20)
plt.xlabel('Age (years)', fontsize=12)
plt.ylabel('Cardiovascular Risk Factor', fontsize=12)

# Adjust layout and save
plt.tight_layout()
plt.savefig('../figures/all_ages_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a summary of findings by age
with open('../docs/age_specific_findings.md', 'w') as f:
    f.write('# Age-Specific Analysis of Childhood Cognitive Ability and Cardiovascular Risk Factors\n\n')
    
    for age, data in age_groups:
        summary, sorted_data = analyse_by_age(age, data)
        
        f.write(f'## Age {int(age)} Analysis\n\n')
        
        # Overview
        f.write(f"### Overview\n")
        f.write(f"At age {int(age)}, {summary['Total Factors Measured']} cardiovascular risk factors were measured. ")
        f.write(f"Of these, {summary['Significant Associations']} ({summary['Percent Significant']:.1f}%) ")
        f.write(f"showed a statistically significant association with childhood IQ measured at age 8.\n\n")
        
        # Direction of associations
        f.write(f"### Direction of Associations\n")
        f.write(f"- Negative associations (higher IQ, lower risk factor): {summary['Negative Associations']}\n")
        f.write(f"- Positive associations (higher IQ, higher risk factor): {summary['Positive Associations']}\n\n")
        
        # Strongest associations
        f.write(f"### Strongest Associations\n")
        f.write(f"The strongest association was with {summary['Strongest Association']} ")
        f.write(f"(coefficient = {summary['Strongest Coefficient']:.4f}, p = {summary['Strongest P-value']:.4f}).\n\n")
        
        # Detailed findings
        f.write(f"### Detailed Findings\n")
        f.write("| Risk Factor | Coefficient | P-value | Significant |\n")
        f.write("|-------------|-------------|---------|-------------|\n")
        
        for _, row in sorted_data.sort_values(by='Coefficient', key=abs, ascending=False).iterrows():
            sig_mark = "Yes" if row['Significant'] else "No"
            f.write(f"| {row['Risk Factor']} | {row['Coefficient']:.4f} | {row['P-value_numeric']:.4f} | {sig_mark} |\n")
        
        f.write("\n\n")

print("Age-specific analysis complete.")
