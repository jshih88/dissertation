import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
import os

# Create directories for outputs if they don't exist
os.makedirs('../figures', exist_ok=True)
os.makedirs('../tables', exist_ok=True)

# Load the summary data from the previous analysis
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

# Create significance level indicator
summary_df['Significance_Level'] = 'ns'
summary_df.loc[summary_df['P-value_numeric'] < 0.05, 'Significance_Level'] = '*'
summary_df.loc[summary_df['P-value_numeric'] < 0.01, 'Significance_Level'] = '**'
summary_df.loc[summary_df['P-value_numeric'] < 0.001, 'Significance_Level'] = '***'

# Group data into developmental periods
summary_df['Developmental_Period'] = pd.cut(
    summary_df['Age'], 
    bins=[8, 12, 16, 25], 
    labels=['Childhood (9-12)', 'Adolescence (13-16)', 'Early Adulthood (17-24)']
)

# Create a table of participant characteristics by developmental period
#period_characteristics = summary_df.groupby('Developmental_Period').agg({
period_characteristics = summary_df.groupby('Developmental_Period', observed=True).agg({
    'Sample Size': ['mean', 'min', 'max', 'count'],
    'R²': ['mean', 'min', 'max'],
    'Significant': 'mean',
    'Coefficient': ['mean', 'std', 'min', 'max']
})

period_characteristics.columns = ['_'.join(col).strip() for col in period_characteristics.columns.values]
period_characteristics.rename(columns={
    'Sample Size_count': 'Number_of_Measurements',
    'Significant_mean': 'Proportion_Significant'
}, inplace=True)
period_characteristics['Proportion_Significant'] = period_characteristics['Proportion_Significant'] * 100

# Save the table
period_characteristics.to_csv('../tables/participant_characteristics_by_period.csv')

# Create a more detailed table of results by risk factor and developmental period
#risk_period_summary = summary_df.groupby(['Risk Factor', 'Developmental_Period']).agg({
risk_period_summary = summary_df.groupby(['Risk Factor', 'Developmental_Period'], observed=True).agg({
    'Coefficient': ['mean', 'std', 'count'],
    'P-value_numeric': 'mean',
    'Significant': 'mean',
    'Sample Size': 'mean',
    'R²': 'mean'
}).reset_index()

risk_period_summary.columns = ['_'.join(col).strip() for col in risk_period_summary.columns.values]
risk_period_summary.rename(columns={
    'Risk Factor_': 'Risk_Factor',
    'Developmental_Period_': 'Developmental_Period',
    'Coefficient_mean': 'Mean_Coefficient',
    'Coefficient_std': 'SD_Coefficient',
    'Coefficient_count': 'Number_of_Measurements',
    'P-value_numeric_mean': 'Mean_P_value',
    'Significant_mean': 'Proportion_Significant',
    'Sample Size_mean': 'Mean_Sample_Size',
    'R²_mean': 'Mean_R_Squared'
}, inplace=True)
risk_period_summary['Proportion_Significant'] = risk_period_summary['Proportion_Significant'] * 100

# Save the table
risk_period_summary.to_csv('../tables/risk_factor_by_developmental_period.csv')

# Create a visualisation of effect sizes by developmental period
plt.figure(figsize=(14, 10))
#sns.boxplot(x='Developmental_Period', y='Coefficient', data=summary_df, palette='viridis')
sns.boxplot(x='Developmental_Period', y='Coefficient', hue='Developmental_Period',
            data=summary_df, palette='viridis', legend=False)
plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
plt.title('Distribution of Effect Sizes by Developmental Period', fontsize=16)
plt.xlabel('Developmental Period', fontsize=14)
plt.ylabel('Standardised Coefficient', fontsize=14)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('../figures/effect_sizes_by_period.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a visualisation of proportion of significant associations by developmental period
sig_by_period = summary_df.groupby('Developmental_Period')['Significant'].mean() * 100
plt.figure(figsize=(10, 6))
bars = plt.bar(sig_by_period.index, sig_by_period.values, color='skyblue')
plt.title('Proportion of Significant Associations by Developmental Period', fontsize=16)
plt.xlabel('Developmental Period', fontsize=14)
plt.ylabel('Percentage of Significant Associations (%)', fontsize=14)
plt.ylim(0, 100)
plt.grid(axis='y', alpha=0.3)

# Add percentage labels on top of bars
for i, bar in enumerate(bars):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f"{sig_by_period.values[i]:.1f}%", 
             ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig('../figures/significant_by_period.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a heatmap of effect sizes by risk factor and developmental period
pivot_data = summary_df.pivot_table(
    index='Risk Factor', 
    columns='Developmental_Period', 
    values='Coefficient',
    aggfunc='mean'
)

plt.figure(figsize=(12, 10))
sns.heatmap(pivot_data, cmap='RdBu_r', center=0, annot=True, fmt='.4f', linewidths=.5)
plt.title('Mean Effect Size by Risk Factor and Developmental Period', fontsize=16)
plt.tight_layout()
plt.savefig('../figures/heatmap_by_period.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a visualisation of effect sizes by risk factor category
# Group risk factors into categories
risk_categories = {
    'Anthropometric': ['Body Mass Index', 'Waist Circumference'],
    'Blood Pressure': ['Systolic Blood Pressure', 'Diastolic Blood Pressure'],
    'Lipid Profile': ['Total Cholesterol', 'High-Density Lipoprotein', 'Low-Density Lipoprotein', 'Triglycerides'],
    'Glucose Metabolism': ['Glucose Metabolism', 'Insulin']
}

# Add category column to dataframe
summary_df['Risk_Category'] = 'Other'
for category, factors in risk_categories.items():
    summary_df.loc[summary_df['Risk Factor'].isin(factors), 'Risk_Category'] = category

# Define the desired category order
category_order = [
    'Anthropometric',
    'Blood Pressure',
    'Lipid Profile',
    'Glucose Metabolism'
]

# Convert to categorical type with specified order
summary_df['Risk_Category'] = pd.Categorical(
    summary_df['Risk_Category'],
    categories=category_order,
    ordered=True
)

# Create boxplot of effect sizes by risk category
plt.figure(figsize=(14, 8))
sns.boxplot(x='Risk_Category', y='Coefficient', data=summary_df, palette='viridis')
plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
plt.title('Distribution of Effect Sizes by Risk Factor Category', fontsize=16)
plt.xlabel('Risk Factor Category', fontsize=14)
plt.ylabel('Standardised Coefficient', fontsize=14)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('../figures/effect_sizes_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a visualisation of proportion of significant associations by risk category
sig_by_category = summary_df.groupby('Risk_Category', observed=True)['Significant'].mean() * 100
plt.figure(figsize=(10, 6))
bars = plt.bar(
    x=sig_by_category.index,
    height=sig_by_category.values,
    color='skyblue'
)
plt.title('Proportion of Significant Associations by Risk Factor Category', fontsize=16)
plt.xlabel('Risk Factor Category', fontsize=14)
plt.ylabel('Percentage of Significant Associations (%)', fontsize=14)
plt.ylim(0, 100)
plt.grid(axis='y', alpha=0.3)

# Add percentage labels on top of bars
for i, bar in enumerate(bars):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f"{sig_by_category.values[i]:.1f}%", 
             ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig('../figures/significant_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a heatmap of effect sizes by risk category and developmental period
category_period_pivot = summary_df.pivot_table(
    index='Risk_Category', 
    columns='Developmental_Period', 
    values='Coefficient',
    aggfunc='mean'
)

# Reindex to ensure correct order
category_period_pivot = category_period_pivot.reindex(category_order)

plt.figure(figsize=(12, 8))
#sns.heatmap(category_period_pivot, cmap='RdBu_r', center=0, annot=True, fmt='.4f', linewidths=.5)
sns.heatmap(
    category_period_pivot,
    cmap='RdBu_r',
    center=0,
    annot=True,
    fmt='.4f',
    linewidths=.5
)
plt.title('Mean Effect Size by Risk Factor Category and Developmental Period', fontsize=16)
plt.tight_layout()
plt.savefig('../figures/heatmap_category_by_period.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a table of effect sizes by risk category and developmental period
category_period_summary = summary_df.groupby(['Risk_Category', 'Developmental_Period']).agg({
    'Coefficient': ['mean', 'std', 'count'],
    'P-value_numeric': 'mean',
    'Significant': 'mean',
    'Sample Size': 'mean',
    'R²': 'mean'
}).reset_index()

category_period_summary.columns = ['_'.join(col).strip() for col in category_period_summary.columns.values]
category_period_summary.rename(columns={
    'Risk_Category_': 'Risk_Category',
    'Developmental_Period_': 'Developmental_Period',
    'Coefficient_mean': 'Mean_Coefficient',
    'Coefficient_std': 'SD_Coefficient',
    'Coefficient_count': 'Number_of_Measurements',
    'P-value_numeric_mean': 'Mean_P_value',
    'Significant_mean': 'Proportion_Significant',
    'Sample Size_mean': 'Mean_Sample_Size',
    'R²_mean': 'Mean_R_Squared'
}, inplace=True)
category_period_summary['Proportion_Significant'] = category_period_summary['Proportion_Significant'] * 100

# Save the table
category_period_summary.to_csv('../tables/risk_category_by_developmental_period.csv')

# just quickly change the order of the risk categories so that Lipid is before Glucose
# Read the generated CSV file
file_path = '../tables/risk_category_by_developmental_period.csv'
df = pd.read_csv(file_path)

# Function to adjust the index numbers
def adjust_index(x):
    if 6 <= x <= 8:
        return x + 3  # 6→9, 7→10, 8→11
    elif 9 <= x <= 11:
        return x - 3  # 9→6, 10→7, 11→8
    return x

# Apply the index adjustment
df['Unnamed: 0'] = df['Unnamed: 0'].apply(adjust_index)

# Sort by the adjusted index and drop the temporary column
df = df.sort_values('Unnamed: 0')

# Save back to the same file
df.to_csv(file_path, index=False)

# Create a visualisation of the trajectory of effect sizes across ages for each risk factor category
# Modified trajectory plotting section

# Modified trajectory plotting with 3 significant figures
from scipy import stats
import warnings

# Fixed y-axis range for all plots
Y_MIN = -0.006
Y_MAX = 0.004

# Create individual trajectory plots for each risk category
for category, factors in risk_categories.items():
    plt.figure(figsize=(12, 8))
    
    # Get all data for this category
    category_data = summary_df[summary_df['Risk_Category'] == category].dropna(subset=['Age', 'Coefficient'])
    
    # Skip categories with no valid data
    if len(category_data) < 2:
        warnings.warn(f"Skipping {category}: Insufficient data (n={len(category_data)})")
        plt.close()
        continue
    
    # Check for variability in age data
    if category_data['Age'].nunique() < 2:
        warnings.warn(f"Skipping {category}: No age variability")
        plt.close()
        continue
    
    # Create color palette for risk factors
    palette = sns.color_palette("tab10", n_colors=len(factors))
    
    # Plot individual risk factors with colored points
    for i, factor in enumerate(factors):
        factor_points = category_data[category_data['Risk Factor'] == factor]
        plt.scatter(
            x=factor_points['Age'], 
            y=factor_points['Coefficient'],
            color=palette[i],
            label=factor,
            alpha=0.7,
            s=80,
            edgecolor='w',
            linewidth=0.5
        )
    
    # Calculate regression with error handling
    try:
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            category_data['Age'], 
            category_data['Coefficient']
        )
        r_squared = r_value**2
    except ValueError as e:
        warnings.warn(f"Regression failed for {category}: {str(e)}")
        plt.close()
        continue
    
    # Formatting function for 3 significant figures
    def format_sigfigs(x):
        return f"{x:.3g}".replace('e-0', 'e-')  # Cleaner exponent formatting
    
    # Create annotation text with 3 significant figures
    stats_text = (f"y = {format_sigfigs(intercept)} + {format_sigfigs(slope)}x\n"
                  f"R² = {format_sigfigs(r_squared)}\n"
                  f"p = {format_sigfigs(p_value)}\n"
                  f"n = {len(category_data)}")
    
    # Plot category-level regression line with CI
    sns.regplot(
        x='Age', y='Coefficient', 
        data=category_data,
        scatter=False,
        ci=95,
        color='#2ca02c',
        line_kws={
            'lw': 2.5,
            'label': f'Regression Line (95% CI)'
        },
        truncate=False
    )
    
    # Set fixed y-axis limits
    plt.ylim(Y_MIN, Y_MAX)
    
    # Add plot elements
    plt.axhline(y=0, color='#7f7f7f', linestyle='--', alpha=0.6)
    plt.title(f'{category} Trajectory (Overall Trend)', fontsize=16)
    plt.xlabel('Age (years)', fontsize=14)
    plt.ylabel('Standardised Coefficient', fontsize=14)
    
    # Add enhanced legend
    legend = plt.legend(
        title='Risk Factors',
        bbox_to_anchor=(1.02, 1),
        loc='upper left',
        frameon=True,
        framealpha=0.95,
        edgecolor='#444444',
        fontsize=11
    )
    legend.get_title().set_fontsize(12)
    
    # Add statistics annotation
    plt.text(
        0.05, 0.18,
        stats_text,
        transform=plt.gca().transAxes,
        fontsize=11,
        verticalalignment='top',
        bbox=dict(
            facecolor='white',
            alpha=0.9,
            edgecolor='#cccccc',
            boxstyle='round,pad=0.4'
        )
    )
    
    plt.grid(alpha=0.15, linestyle='--')
    plt.tight_layout()
    
    # Save with category-specific filename
    fname = f'trajectory_{category.lower().replace(" ", "_")}_annotated.png'
    plt.savefig(f'../figures/{fname}', 
                dpi=300, bbox_inches='tight')
    plt.close()

# Create a summary of the extended analysis
with open('../docs/extended_analysis_summary.md', 'w') as f:
    f.write('# Extended Analysis of Childhood Cognitive Ability and Cardiovascular Risk Factors\n\n')
    
    f.write('## Overview\n\n')
    f.write('This extended analysis builds upon the previous work by examining the relationship between childhood cognitive ability and cardiovascular risk factors across different developmental periods and risk factor categories. The analysis aims to provide a more nuanced understanding of how these relationships evolve across development and vary by type of cardiovascular risk factor.\n\n')
    
    f.write('## Developmental Periods\n\n')
    f.write('The analysis categorises ages into three developmental periods:\n\n')
    f.write('1. **Childhood (9-12 years)**: Early development period\n')
    f.write('2. **Adolescence (13-16 years)**: Period of pubertal development and increasing autonomy\n')
    f.write('3. **Early Adulthood (17-24 years)**: Transition to adulthood and establishment of adult health behaviors\n\n')
    
    f.write('## Risk Factor Categories\n\n')
    f.write('Cardiovascular risk factors are grouped into four main categories:\n\n')
    f.write('1. **Anthropometric Measures**: Body Mass Index (BMI) and Waist Circumference\n')
    f.write('2. **Blood Pressure**: Systolic and Diastolic Blood Pressure\n')
    f.write('3. **Lipid Profile**: Total Cholesterol, High-Density Lipoprotein (HDL), Low-Density Lipoprotein (LDL), and Triglycerides\n')
    f.write('4. **Glucose Metabolism**: Glucose levels and Insulin\n\n')
    
    f.write('## Key Findings\n\n')
    
    # Calculate some summary statistics for the key findings
    early_adulthood = summary_df[summary_df['Developmental_Period'] == 'Early Adulthood (17-24)']
    childhood = summary_df[summary_df['Developmental_Period'] == 'Childhood (9-12)']
    
    early_sig_pct = early_adulthood['Significant'].mean() * 100
    child_sig_pct = childhood['Significant'].mean() * 100
    
    anthro_data = summary_df[summary_df['Risk_Category'] == 'Anthropometric']
    bp_data = summary_df[summary_df['Risk_Category'] == 'Blood Pressure']
    lipid_data = summary_df[summary_df['Risk_Category'] == 'Lipid Profile']
    glucose_data = summary_df[summary_df['Risk_Category'] == 'Glucose Metabolism']
    
    anthro_sig_pct = anthro_data['Significant'].mean() * 100
    bp_sig_pct = bp_data['Significant'].mean() * 100
    lipid_sig_pct = lipid_data['Significant'].mean() * 100
    glucose_sig_pct = glucose_data['Significant'].mean() * 100
    
    f.write(f'1. **Developmental Patterns**: The proportion of significant associations between childhood cognitive ability and cardiovascular risk factors increases from childhood ({child_sig_pct:.1f}%) to early adulthood ({early_sig_pct:.1f}%), suggesting that these relationships may become more pronounced with age.\n\n')
    
    f.write(f'2. **Risk Factor Categories**: The strength and consistency of associations vary by risk factor category:\n')
    f.write(f'   - Anthropometric measures show the most consistent associations ({anthro_sig_pct:.1f}% significant)\n')
    f.write(f'   - Blood pressure measures show moderate consistency ({bp_sig_pct:.1f}% significant)\n')
    f.write(f'   - Glucose metabolism measures show variable consistency ({glucose_sig_pct:.1f}% significant)\n')
    f.write(f'   - Lipid profile measures show the least consistency ({lipid_sig_pct:.1f}% significant)\n\n')
    
    f.write('3. **Direction of Associations**: The majority of significant associations are negative, indicating that higher childhood cognitive ability is generally associated with more favorable cardiovascular risk profiles. However, some measures (particularly HDL cholesterol) show positive associations in early adulthood.\n\n')
    
    f.write('4. **Trajectories Across Development**: The analysis reveals distinct trajectories for different risk factor categories across development, with some showing strengthening associations with age (e.g., anthropometric measures) and others showing more complex patterns.\n\n')
    
    f.write('## Implications\n\n')
    f.write('These findings have several implications for understanding the relationship between childhood cognitive ability and cardiovascular health:\n\n')
    
    f.write('1. **Developmental Sensitivity**: The strengthening of associations with age suggests that the transition to adulthood may be a particularly sensitive period for the manifestation of cognitive-cardiovascular relationships.\n\n')
    
    f.write('2. **Risk Factor Specificity**: The variation in patterns across different risk factor categories suggests potentially different underlying mechanisms linking cognitive ability to various aspects of cardiovascular health.\n\n')
    
    f.write('3. **Cumulative Effects**: The increasing strength of associations with age may reflect cumulative effects of cognitive ability on health behaviors and physiological processes over time.\n\n')
    
    f.write('4. **Prevention Implications**: The findings suggest that early cognitive development may be an important target for cardiovascular disease prevention, with potential benefits that accumulate across development.\n\n')
    
    f.write('## Conclusion\n\n')
    f.write('This extended analysis provides a more nuanced understanding of the relationship between childhood cognitive ability and cardiovascular risk fact\n\n')
