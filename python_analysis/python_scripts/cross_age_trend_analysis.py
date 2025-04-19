import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

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

# Group data by risk factor
risk_factor_groups = summary_df.groupby('Risk Factor')

# Function to analyse trends across ages for each risk factor
def analyse_trends_by_risk_factor(risk_factor, data):
    """Analyse how the relationship between cognitive ability and a specific cardiovascular risk factor changes across ages."""
    # Sort by age
    sorted_data = data.sort_values(by='Age')
    
    # Calculate trend statistics if we have enough data points
    if len(sorted_data) >= 3:
        # Linear regression to test for trend
        x = sorted_data['Age'].values
        y = sorted_data['Coefficient'].values
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        trend_direction = "increasing" if slope > 0 else "decreasing"
        trend_significance = "significant" if p_value < 0.05 else "non-significant"
        
        # Calculate early vs late difference
        early_ages = sorted_data[sorted_data['Age'] <= 15]['Coefficient'].mean()
        late_ages = sorted_data[sorted_data['Age'] > 15]['Coefficient'].mean()
        age_difference = late_ages - early_ages
        
        # Count significant associations by age period
        early_sig = sorted_data[(sorted_data['Age'] <= 15) & (sorted_data['Significant'])].shape[0]
        early_total = sorted_data[sorted_data['Age'] <= 15].shape[0]
        early_sig_percent = (early_sig / early_total) * 100 if early_total > 0 else 0
        
        late_sig = sorted_data[(sorted_data['Age'] > 15) & (sorted_data['Significant'])].shape[0]
        late_total = sorted_data[sorted_data['Age'] > 15].shape[0]
        late_sig_percent = (late_sig / late_total) * 100 if late_total > 0 else 0
    else:
        slope = intercept = r_value = p_value = std_err = np.nan
        trend_direction = trend_significance = "insufficient data"
        early_ages = late_ages = age_difference = np.nan
        early_sig = early_total = early_sig_percent = np.nan
        late_sig = late_total = late_sig_percent = np.nan
    
    # Create summary
    summary = {
        'Risk Factor': risk_factor,
        'Num Data Points': len(sorted_data),
        'Trend Slope': slope,
        'Trend P-value': p_value,
        'Trend Direction': trend_direction,
        'Trend Significance': trend_significance,
        'R-squared': r_value**2,
        'Early Ages Mean Coef': early_ages,
        'Late Ages Mean Coef': late_ages,
        'Early-Late Difference': age_difference,
        'Early Ages Sig %': early_sig_percent,
        'Late Ages Sig %': late_sig_percent
    }
    
    return summary, sorted_data

# Analyse trends for each risk factor
trend_analyses = []
for risk_factor, data in risk_factor_groups:
    summary, sorted_data = analyse_trends_by_risk_factor(risk_factor, data)
    trend_analyses.append(summary)
    
    # Create a line plot for this risk factor across ages
    plt.figure(figsize=(12, 8))
    
    # Plot the data points
    plt.scatter(sorted_data['Age'], sorted_data['Coefficient'], 
                s=100, 
                c=['#3498db' if sig else '#d3d3d3' for sig in sorted_data['Significant']], 
                zorder=5)
    
    # Add error bars (would need to extract CI values)
    
    # Add trend line if we have enough data points
    if len(sorted_data) >= 3:
        x = sorted_data['Age'].values
        y = sorted_data['Coefficient'].values
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Plot regression line
        x_line = np.linspace(min(x), max(x), 100)
        y_line = slope * x_line + intercept
        plt.plot(x_line, y_line, 'r--', alpha=0.7, 
                 label=f'Trend: y = {slope:.6f}x + {intercept:.6f}\nR² = {r_value**2:.3f}, p = {p_value:.4f}')
    
    # Add zero line
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Add labels and title
    plt.xlabel('Age (years)', fontsize=14)
    plt.ylabel('Standardised Coefficient', fontsize=14)
    plt.title(f'Trend of Association Between Childhood IQ at Age 8 and {risk_factor} Across Ages', fontsize=16)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', label='Significant (p < 0.05)'),
        Patch(facecolor='#d3d3d3', label='Non-significant')
    ]
    if len(sorted_data) >= 3:
        plt.legend(loc='best')
    else:
        plt.legend(handles=legend_elements, loc='best')
    
    # Add coefficient values as text
    for i, row in sorted_data.iterrows():
        coef = row['Coefficient']
        p_val = row['P-value_numeric']
        age = row['Age']
        
        if p_val < 0.001:
            sig_stars = '***'
        elif p_val < 0.01:
            sig_stars = '**'
        elif p_val < 0.05:
            sig_stars = '*'
        else:
            sig_stars = ''
        
        plt.text(age, coef + (0.0005 if coef >= 0 else -0.0005), 
                 f'{coef:.4f}{sig_stars}', 
                 ha='center', va='bottom' if coef >= 0 else 'top', 
                 fontweight='bold')
    
    # Adjust layout and save
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'../figures/trend_{risk_factor.replace(" ", "_").lower()}.png', dpi=300, bbox_inches='tight')
    plt.close()

# Create a summary DataFrame for trend analyses
trend_summary_df = pd.DataFrame(trend_analyses)
trend_summary_df.to_csv('../tables/trend_summary.csv', index=False)

# Create a summary of trend findings
with open('../docs/cross_age_trend_findings.md', 'w') as f:
    f.write('# Cross-Age Trend Analysis of Childhood Cognitive Ability and Cardiovascular Risk Factors\n\n')
    
    f.write('## Overview of Trends Across Ages\n\n')
    f.write('This analysis examines how the relationship between childhood cognitive ability (IQ at age 8) and various cardiovascular risk factors evolves from childhood (age 9) through early adulthood (age 24).\n\n')
    
    # Overall patterns
    sig_trends = sum(1 for item in trend_analyses if item['Trend Significance'] == 'significant')
    total_trends = sum(1 for item in trend_analyses if item['Trend Significance'] != 'insufficient data')
    
    f.write(f'Of the {total_trends} risk factors with sufficient data points for trend analysis, ')
    f.write(f'{sig_trends} ({sig_trends/total_trends*100:.1f}%) showed a statistically significant trend across ages.\n\n')
    
    # Direction of trends
    increasing = sum(1 for item in trend_analyses if item['Trend Direction'] == 'increasing')
    decreasing = sum(1 for item in trend_analyses if item['Trend Direction'] == 'decreasing')
    
    f.write(f'- {increasing} risk factors showed an increasing trend (weakening negative association or strengthening positive association)\n')
    f.write(f'- {decreasing} risk factors showed a decreasing trend (strengthening negative association or weakening positive association)\n\n')
    
    # Early vs late differences
    f.write('## Early vs Late Age Comparisons\n\n')
    f.write('Comparing early ages (≤15 years) with later ages (>15 years):\n\n')
    
    # Calculate average percentages
    valid_early = [item for item in trend_analyses if not np.isnan(item['Early Ages Sig %'])]
    valid_late = [item for item in trend_analyses if not np.isnan(item['Late Ages Sig %'])]
    
    avg_early_sig = sum(item['Early Ages Sig %'] for item in valid_early) / len(valid_early) if valid_early else 0
    avg_late_sig = sum(item['Late Ages Sig %'] for item in valid_late) / len(valid_late) if valid_late else 0
    
    f.write(f'- Early ages (9-15): {avg_early_sig:.1f}% of associations were statistically significant\n')
    f.write(f'- Late ages (17-24): {avg_late_sig:.1f}% of associations were statistically significant\n\n')
    
    # Detailed findings by risk factor
    f.write('## Detailed Trend Analysis by Risk Factor\n\n')
    
    for analysis in sorted(trend_analyses, key=lambda x: abs(x['Trend Slope']) if not np.isnan(x['Trend Slope']) else 0, reverse=True):
        f.write(f"### {analysis['Risk Factor']}\n\n")
        
        if analysis['Num Data Points'] < 3:
            f.write("Insufficient data points for trend analysis.\n\n")
            continue
        
        f.write(f"- **Trend Direction**: {analysis['Trend Direction']}\n")
        f.write(f"- **Trend Significance**: {analysis['Trend Significance']} (p = {analysis['Trend P-value']:.4f})\n")
        f.write(f"- **Trend Slope**: {analysis['Trend Slope']:.6f}\n")
        f.write(f"- **R-squared**: {analysis['R-squared']:.3f}\n")
        f.write(f"- **Early Ages Mean Coefficient**: {analysis['Early Ages Mean Coef']:.4f}\n")
        f.write(f"- **Late Ages Mean Coefficient**: {analysis['Late Ages Mean Coef']:.4f}\n")
        f.write(f"- **Change from Early to Late Ages**: {analysis['Early-Late Difference']:.4f}\n\n")
        
        # Interpretation
        if analysis['Trend Significance'] == 'significant':
            if analysis['Trend Direction'] == 'increasing':
                if analysis['Early Ages Mean Coef'] < 0 and analysis['Late Ages Mean Coef'] < 0:
                    f.write("**Interpretation**: The negative association between childhood IQ and this risk factor weakens with age, but remains negative throughout.\n\n")
                elif analysis['Early Ages Mean Coef'] < 0 and analysis['Late Ages Mean Coef'] > 0:
                    f.write("**Interpretation**: The association between childhood IQ and this risk factor changes direction from negative in early ages to positive in later ages.\n\n")
                elif analysis['Early Ages Mean Coef'] > 0 and analysis['Late Ages Mean Coef'] > 0:
                    f.write("**Interpretation**: The positive association between childhood IQ and this risk factor strengthens with age.\n\n")
            else:  # decreasing trend
                if analysis['Early Ages Mean Coef'] < 0 and analysis['Late Ages Mean Coef'] < 0:
                    f.write("**Interpretation**: The negative association between childhood IQ and this risk factor strengthens with age.\n\n")
                elif analysis['Early Ages Mean Coef'] > 0 and analysis['Late Ages Mean Coef'] < 0:
                    f.write("**Interpretation**: The association between childhood IQ and this risk factor changes direction from positive in early ages to negative in later ages.\n\n")
                elif analysis['Early Ages Mean Coef'] > 0 and analysis['Late Ages Mean Coef'] > 0:
                    f.write("**Interpretation**: The positive association between childhood IQ and this risk factor weakens with age, but remains positive throughout.\n\n")
        else:
            f.write("**Interpretation**: No significant trend was observed in the association between childhood IQ and this risk factor across ages.\n\n")
    
    # Summary of key findings
    f.write('## Summary of Key Trend Findings\n\n')
    
    # Sort risk factors by absolute trend slope
    sorted_analyses = sorted(trend_analyses, key=lambda x: abs(x['Trend Slope']) if not np.isnan(x['Trend Slope']) else 0, reverse=True)
    
    # List significant trends
    sig_trends = [a for a in sorted_analyses if a['Trend Significance'] == 'significant']
    if sig_trends:
        f.write('### Significant Trends\n\n')
        for analysis in sig_trends:
            direction = "strengthening" if (analysis['Trend Direction'] == 'decreasing' and analysis['Early Ages Mean Coef'] < 0) or \
                                          (analysis['Trend Direction'] == 'increasing' and analysis['Early Ages Mean Coef'] > 0) else "weakening"
            f.write(f"- **{analysis['Risk Factor']}**: {direction} {'negative' if analysis['Late Ages Mean Coef'] < 0 else 'positive'} association with age (slope = {analysis['Trend Slope']:.6f}, p = {analysis['Trend P-value']:.4f})\n")
        f.write('\n')
    
    # List consistent associations (significant at most ages)
    consistent_factors = []
    for analysis in sorted_analyses:
        if analysis['Num Data Points'] >= 3:
            early_sig = analysis['Early Ages Sig %']
            late_sig = analysis['Late Ages Sig %']
            if not np.isnan(early_sig) and not np.isnan(late_sig) and (early_sig + late_sig) / 2 >= 50:
                consistent_factors.append(analysis)
    
    if consistent_factors:
        f.write('### Consistent Associations Across Ages\n\n')
        for analysis in consistent_factors:
            direction = "negative" if analysis['Late Ages Mean Coef'] < 0 else "positive"
            f.write(f"- **{analysis['Risk Factor']}**: Consistently {direction} association across most age groups\n")
        f.write('\n')
    
    # List factors with changing significance
    changing_factors = []
    for analysis in sorted_analyses:
        if analysis['Num Data Points'] >= 3:
            early_sig = analysis['Early Ages Sig %']
            late_sig = analysis['Late Ages Sig %']
            if not np.isnan(early_sig) and not np.isnan(late_sig):
                if (early_sig == 0 and late_sig > 0) or (early_sig > 0 and late_sig == 0):
                    changing_factors.append((analysis, "emerging" if early_sig == 0 else "disappearing"))
    
    if changing_factors:
        f.write('### Emerging or Disappearing Associations\n\n')
        for analysis, change_type in changing_factors:
            f.write(f"- **{analysis['Risk Factor']}**: {change_type.capitalize()} significance in later ages\n")
        f.write('\n')

print("Cross-age trend analysis complete.")
