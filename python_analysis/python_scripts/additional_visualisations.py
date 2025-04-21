import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Create directories for outputs
os.makedirs('../figures', exist_ok=True)

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

# Create a summary visualisation showing significant associations by age
age_counts = summary_df.groupby('Age', observed=True)['Significant'].agg(['count', 'sum'])
age_counts['percent'] = (age_counts['sum'] / age_counts['count']) * 100

plt.figure(figsize=(14, 8))
ax1 = plt.subplot(111)
bars = ax1.bar(age_counts.index, age_counts['percent'], color='#3498db', alpha=0.7)
ax1.set_xlabel('Age (years)', fontsize=14)
ax1.set_ylabel('Percentage of Significant Associations (%)', fontsize=14)
ax1.set_title('Percentage of Significant Associations Between Childhood IQ and Cardiovascular Risk Factors by Age', 
             fontsize=16, pad=20)
ax1.set_ylim(0, 100)
ax1.grid(axis='y', alpha=0.3)

# Add count labels on top of bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
            f"{int(age_counts['sum'].iloc[i])}/{int(age_counts['count'].iloc[i])}",
            ha='center', va='bottom', fontsize=10)

# Add a trend line
z = np.polyfit(age_counts.index, age_counts['percent'], 1)
p = np.poly1d(z)
plt.plot(age_counts.index, p(age_counts.index), "r--", alpha=0.7)

# Add a secondary axis showing the number of risk factors measured
ax2 = ax1.twinx()
ax2.plot(age_counts.index, age_counts['count'], 'o-', color='#e74c3c', alpha=0.7)
ax2.set_ylabel('Number of Risk Factors Measured', fontsize=14)
ax2.set_ylim(0, 12)

# Add legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='#3498db', lw=4, alpha=0.7, label='Percentage Significant'),
    Line2D([0], [0], color='#e74c3c', lw=2, alpha=0.7, marker='o', label='Risk Factors Measured'),
    Line2D([0], [0], color='r', lw=2, linestyle='--', alpha=0.7, label='Trend Line')
]
ax1.legend(handles=legend_elements, loc='upper left')

plt.tight_layout()
plt.savefig('../figures/significant_associations_by_age.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a summary visualisation showing effect sizes by risk factor
risk_factor_summary = summary_df.groupby('Risk Factor', observed=True).agg({
    'Coefficient': ['mean', 'min', 'max', 'std'],
    'Significant': 'mean',
    'Age': 'count'
})
risk_factor_summary.columns = ['Mean_Coef', 'Min_Coef', 'Max_Coef', 'Std_Coef', 'Pct_Significant', 'Measurements']
risk_factor_summary = risk_factor_summary.sort_values('Mean_Coef')

plt.figure(figsize=(14, 10))
bars = plt.barh(risk_factor_summary.index, risk_factor_summary['Mean_Coef'], 
               color=[plt.cm.RdBu(0.2) if x < 0 else plt.cm.RdBu(0.8) for x in risk_factor_summary['Mean_Coef']])

# Add error bars
plt.errorbar(risk_factor_summary['Mean_Coef'], risk_factor_summary.index, 
             xerr=risk_factor_summary['Std_Coef'], fmt='none', ecolor='black', capsize=5)

# Add zero line
plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)

# Add labels and title
plt.xlabel('Mean Standardised Coefficient', fontsize=14)
plt.ylabel('Cardiovascular Risk Factor', fontsize=14)
plt.title('Average Association Between Childhood IQ and Cardiovascular Risk Factors Across All Ages', 
         fontsize=16, pad=20)

# Add coefficient values and significance percentage as text
for i, (idx, row) in enumerate(risk_factor_summary.iterrows()):
    # Add mean coefficient
    plt.text(row['Mean_Coef'] + (0.0005 if row['Mean_Coef'] >= 0 else -0.0005), 
             i, 
             f"{row['Mean_Coef']:.4f}", 
             va='center', 
             ha='left' if row['Mean_Coef'] >= 0 else 'right',
             fontweight='bold')
    
    # Add significance percentage on the right
    plt.text(max(risk_factor_summary['Mean_Coef']) + 0.002, 
             i, 
             f"{row['Pct_Significant']*100:.1f}% sig. ({int(row['Measurements'])} measurements)", 
             va='center', 
             ha='left')

plt.xlim(min(risk_factor_summary['Mean_Coef']) - 0.002, max(risk_factor_summary['Mean_Coef']) + 0.01)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('../figures/average_effect_by_risk_factor.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a summary visualisation showing the pattern of associations across development
# Group data into developmental periods
summary_df['Period'] = pd.cut(
    summary_df['Age'], 
    bins=[8, 12, 16, 25], 
    labels=['Childhood (9-12)', 'Adolescence (13-16)', 'Early Adulthood (17-24)']
)

period_summary = summary_df.groupby(['Risk Factor', 'Period'], observed=True).agg({
    'Coefficient': 'mean',
    'Significant': 'mean',
    'Age': 'count'
}).reset_index()

# Pivot for heatmap
period_pivot = period_summary.pivot(index='Risk Factor', columns='Period', values='Coefficient')

# Create a custom colormap (blue for negative, red for positive, white for zero)
colors = ['#1a76c4', '#ffffff', '#e74c3c']  # blue, white, red
cmap = LinearSegmentedColormap.from_list('custom_diverging', colors, N=256)

plt.figure(figsize=(14, 10))
ax = sns.heatmap(period_pivot, cmap=cmap, center=0, 
                 annot=True, fmt='.4f', linewidths=.5, 
                 cbar_kws={'label': 'Mean Standardised Coefficient'})

# Add title and labels
plt.title('Developmental Pattern of Associations Between Childhood IQ and Cardiovascular Risk Factors', 
          fontsize=16, pad=20)
plt.xlabel('Developmental Period', fontsize=14)
plt.ylabel('Cardiovascular Risk Factor', fontsize=14)

plt.tight_layout()
plt.savefig('../figures/developmental_pattern_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a summary of the most consistent and strongest associations
# For each risk factor, calculate the percentage of ages with significant associations
risk_consistency = summary_df.groupby('Risk Factor', observed=True).agg({
    'Significant': 'mean',
    'Coefficient': ['mean', 'min', 'max', lambda x: x.abs().mean()],
    'Age': 'count'
})
risk_consistency.columns = ['Pct_Significant', 'Mean_Coef', 'Min_Coef', 'Max_Coef', 'Mean_Abs_Coef', 'Measurements']
risk_consistency = risk_consistency.sort_values('Pct_Significant', ascending=False)

plt.figure(figsize=(14, 10))
ax = plt.subplot(111)

# Create scatter plot
scatter = ax.scatter(
    risk_consistency['Mean_Abs_Coef'], 
    risk_consistency['Pct_Significant'] * 100,
    s=risk_consistency['Measurements'] * 30,  # Size based on number of measurements
    c=risk_consistency['Mean_Coef'],  # Color based on direction (positive/negative)
    cmap='RdBu_r',
    alpha=0.7,
    edgecolors='black'
)

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Mean Coefficient (Direction)', fontsize=12)

# Add labels for each point
for i, (idx, row) in enumerate(risk_consistency.iterrows()):
    ax.annotate(
        idx,
        (row['Mean_Abs_Coef'], row['Pct_Significant'] * 100),
        xytext=(7, 0),
        textcoords='offset points',
        fontsize=10,
        va='center'
    )

# Add labels and title
ax.set_xlabel('Mean Absolute Coefficient (Effect Size)', fontsize=14)
ax.set_ylabel('Percentage of Ages with Significant Association (%)', fontsize=14)
ax.set_title('Consistency and Strength of Associations Between Childhood IQ and Cardiovascular Risk Factors', 
             fontsize=16, pad=20)

# Add a legend for the size of points
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=8, 
           label='4 measurements', alpha=0.7),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=12, 
           label='8 measurements', alpha=0.7)
]
ax.legend(handles=legend_elements, loc='lower right', title='Number of Ages Measured')

# Add grid
ax.grid(alpha=0.3)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig('../figures/consistency_strength_scatter.png', dpi=300, bbox_inches='tight')
plt.close()

print("Additional visualisations complete.")
