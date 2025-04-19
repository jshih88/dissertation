# Python Data Analysis Workflow

## Overview

This document describes a comprehensive data analysis workflow implemented through five interconnected Python scripts. The workflow processes Stata regression results to analyse the relationship between childhood cognitive ability (IQ at age 8) and various cardiovascular risk factors across different ages and developmental periods.

## Workflow Diagram

```
┌─────────────────┐
│ Stata           │
│ Regression      │
│ Results         │
└────────┬────────┘
         │
         ▼
┌───────────────────┐
│ extracted_data.py │
│                   │
│ Data extraction   │
│ & organisation    │
└────────┬──────────┘
         │
         ▼
┌──────────────────────┐
│ readable_summary.csv │
└───┬──────────────┬───┘
    │              │
    │              │
    ▼              ▼
┌────────────┐ ┌───────────────┐
│age_specific│ │cross_age_trend│
│analysis.py │ │analysis.py    │
│            │ │               │
│Age-based   │ │Trend          │
│analysis    │ │analysis       │
└────┬───────┘ └────┬──────────┘
     │              │
     │              │
     ▼              ▼
┌──────────────────────┐
│ extended_analysis.py │
│                      │
│ Developmental period │
│ & risk category      │
│ analysis             │
└───────────┬──────────┘
            │
            ▼
┌────────────────────────────┐
│additional_visualisations.py│
│                            │
│ Supplementary              │
│ visualisations             │
└────────────────────────────┘
```

## Detailed Workflow Description

### Step 1: Data Extraction and Organisation (`extracted_data.py`)

**Input:** 
- Raw Stata regression results file (`../tables/stata_regress_zscore_by_depvar_by_age.csv`)

**Process:**
1. Reads the Stata regression output file containing results for multiple cardiovascular risk factors across different ages
2. Parses the data to extract coefficients, confidence intervals, p-values, R² values, and sample sizes
3. Organises the data into structured DataFrames for each risk factor
4. Creates summary tables with standardised formatting for further analysis

**Output:**
- Individual CSV files for each risk factor (`../tables/{factor}_results.csv`)
- Comprehensive summary CSV with all results (`../tables/all_results_summary.csv`)
- Human-readable summary table (`../tables/readable_summary.csv`) that serves as the primary input for subsequent analyses

### Step 2A: Age-Specific Analysis (`age_specific_analysis.py`)

**Input:**
- Processed summary data (`../tables/readable_summary.csv`)

**Process:**
1. Analyses the relationship between childhood IQ and cardiovascular risk factors at each specific age
2. Calculates statistics for each age group:
   - Count and percentage of significant associations
   - Direction of associations (negative or positive)
   - Average effect sizes
   - Strongest associations
3. Creates visualisations showing associations for each age
4. Generates a heatmap of all associations across ages

**Output:**
- Age-specific bar plots showing associations (`../figures/age_{age}_associations.png`)
- Comprehensive heatmap visualisation (`../figures/all_ages_heatmap.png`)
- Age summary statistics table (`../tables/age_summary.csv`)
- Detailed markdown report with findings (`../docs/age_specific_findings.md`)

### Step 2B: Cross-Age Trend Analysis (`cross_age_trend_analysis.py`)

**Input:**
- Processed summary data (`../tables/readable_summary.csv`)

**Process:**
1. Analyses how the relationship between childhood IQ and each cardiovascular risk factor changes across ages
2. Performs linear regression to test for trends in each risk factor
3. Compares early vs. late age periods
4. Calculates trend statistics (slope, p-value, R²)
5. Creates line plots showing trends for each risk factor

**Output:**
- Trend line plots for each risk factor (`../figures/trend_{risk_factor}.png`)
- Trend summary statistics table (`../tables/trend_summary.csv`)
- Detailed markdown report with findings (`../docs/cross_age_trend_findings.md`)

### Step 3: Extended Analysis (`extended_analysis.py`)

**Input:**
- Processed summary data (`../tables/readable_summary.csv`)

**Process:**
1. Groups data into developmental periods:
   - Childhood (9-12 years)
   - Adolescence (13-16 years)
   - Early Adulthood (17-24 years)
2. Categorises risk factors into groups:
   - Anthropometric (BMI, Waist Circumference)
   - Blood Pressure (Systolic, Diastolic)
   - Lipid Profile (Cholesterol, HDL, LDL, Triglycerides)
   - Glucose Metabolism (Glucose, Insulin)
3. Analyses patterns within developmental periods and risk categories
4. Creates visualisations of effect sizes and significant associations
5. Generates trajectory plots for each risk category

**Output:**
- Period characteristics table (`../tables/participant_characteristics_by_period.csv`)
- Risk factor by period table (`../tables/risk_factor_by_developmental_period.csv`)
- Risk category by period table (`../tables/risk_category_by_developmental_period.csv`)
- Various visualisations:
  - Effect sizes by period boxplot
  - Significant associations by period bar chart
  - Heatmaps of effect sises
  - Trajectory plots for each risk category
- Markdown summary report (`../docs/extended_analysis_summary.md`)

### Step 4: Additional Visualisations (`additional_visualisations.py`)

**Input:**
- Processed summary data (`../tables/readable_summary.csv`)

**Process:**
1. Creates supplementary visualisations to highlight key patterns
2. Analyses significant associations by age with trend line
3. Summarises effect sizes by risk factor with error bars
4. Visualises developmental patterns in a heatmap
5. Evaluates consistency and strength of associations in a scatter plot

**Output:**
- Significant associations by age chart (`../figures/significant_associations_by_age.png`)
- Average effect by risk factor chart (`../figures/average_effect_by_risk_factor.png`)
- Developmental pattern heatmap (`../figures/developmental_pattern_heatmap.png`)
- Consistency and strength scatter plot (`../figures/consistency_strength_scatter.png`)

## Data Flow

The workflow follows a logical progression from data extraction to increasingly sophisticated analyses:

1. **Initial Data Processing**: `extracted_data.py` transforms raw Stata output into structured data
2. **Parallel Initial Analyses**: 
   - `age_specific_analysis.py` examines each age individually
   - `cross_age_trend_analysis.py` looks at trends across ages
3. **Integrated Analysis**: `extended_analysis.py` combines insights by grouping into developmental periods and risk categories
4. **Final Visualisation**: `additional_visualisations.py` creates supplementary visualisations to highlight key findings

Each script builds upon the outputs of previous scripts, creating a comprehensive analysis pipeline that examines the data from multiple perspectives.
