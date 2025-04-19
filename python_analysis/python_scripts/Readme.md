# Python Data Analysis Workflow with Modules and Functions

## Overview

This document describes a comprehensive data analysis workflow implemented through five interconnected Python scripts. The workflow processes Stata regression results to analyse the relationship between childhood cognitive ability (IQ at age 8) and various cardiovascular risk factors across different ages and developmental periods.

## Workflow Diagram

```
┌─────────────────────┐
│  extracted_data.py  │
│                     │
│  pandas, os         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     readable_summary.csv                        │
└─────────┬─────────────────────────────┬───────────────┬─────────┘
          │                             │               │
          ▼                             ▼               ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│age_specific_analysis│    │cross_age_trend_     │    │extended_analysis.py │
│.py                  │    │analysis.py          │    │                     │
│                     │    │                     │    │                     │
│pandas, matplotlib,  │    │pandas, matplotlib,  │    │pandas, matplotlib,  │
│seaborn, numpy, os   │    │numpy, scipy, os     │    │seaborn, scipy, os   │
└──────────┬──────────┘    └──────────┬──────────┘    └──────────┬──────────┘
           │                          │                          │
           └──────────────┬───────────┴──────────────┬───────────┘
                          │                          │
                          ▼                          ▼
           ┌─────────────────────────┐    ┌─────────────────────┐
           │  Analysis Results &     │    │additional_          │
           │  Visualisations         │    │visualisations.py    │
           │                         │    │                     │
           └─────────────────────────┘    │pandas, matplotlib,  │
                                          │seaborn, numpy, os   │
                                          └──────────┬──────────┘
                                                     │
                                                     ▼
                                          ┌─────────────────────┐
                                          │  Supplementary      │
                                          │  Visualisations     │
                                          └─────────────────────┘
```

## Script Descriptions with Modules and Functions

### 1. extracted_data.py

**Input:** Stata regression results file (`../tables/stata_regress_zscore_by_depvar_by_age.csv`)

**Key Modules and Functions:**
- **pandas (pd)**: Data manipulation and analysis
  - `pd.DataFrame()`: Creates structured data tables
  - `df.sort_values()`: Sorts data by specified columns
  - `df.to_csv()`: Exports data to CSV files
- **os**: Operating system interface
  - `os.makedirs()`: Creates directories with `exist_ok=True` parameter
- **Custom Functions**:
  - `extract_data()`: Parses Stata output into structured DataFrames

**Logic:**
- Extracts data from Stata regression results for various cardiovascular risk factors
- Parses coefficient values, confidence intervals, p-values, R² values, and sample sizes
- Organises data into structured DataFrames for each risk factor
- Creates summary tables with standardised formatting

**Output:**
- Individual CSV files for each risk factor (`../tables/{factor}_results.csv`)
- Summary CSV with all results (`../tables/all_results_summary.csv`)
- Human-readable summary table (`../tables/readable_summary.csv`)

### 2. age_specific_analysis.py

**Input:** Processed summary data (`../tables/readable_summary.csv`)

**Key Modules and Functions:**
- **pandas (pd)**: Data manipulation and analysis
  - `pd.read_csv()`: Reads CSV files into DataFrames
  - `df.groupby()`: Groups data for aggregation
  - `df.pivot()`: Reshapes data for visualisation
- **matplotlib.pyplot (plt)**: Plotting library
  - `plt.figure()`, `plt.barh()`, `plt.axvline()`, `plt.savefig()`
- **seaborn (sns)**: Statistical data visualisation
  - `sns.heatmap()`: Creates heatmap visualisation
- **matplotlib.colors**: Color handling
  - `LinearSegmentedColormap.from_list()`: Creates custom color maps
- **Custom Functions**:
  - `analyse_by_age()`: Analyses relationships at specific ages

**Logic:**
- Analyses relationships between childhood IQ and cardiovascular risk factors at specific ages
- Calculates statistics for each age group (significant associations, direction, effect sizes)
- Creates bar plots showing associations for each age
- Generates a heatmap of all associations across ages

**Output:**
- Age-specific bar plots (`../figures/age_{age}_associations.png`)
- Heatmap visualisation (`../figures/all_ages_heatmap.png`)
- Age summary statistics (`../tables/age_summary.csv`)
- Detailed markdown report (`../docs/age_specific_findings.md`)

### 3. cross_age_trend_analysis.py

**Input:** Processed summary data (`../tables/readable_summary.csv`)

**Key Modules and Functions:**
- **pandas (pd)**: Data manipulation and analysis
  - `pd.read_csv()`, `df.groupby()`, `df.to_csv()`
- **matplotlib.pyplot (plt)**: Plotting library
  - `plt.figure()`, `plt.scatter()`, `plt.plot()`, `plt.savefig()`
- **numpy (np)**: Numerical computing
  - `np.linspace()`: Creates evenly spaced values
- **scipy.stats**: Statistical functions
  - `stats.linregress()`: Performs linear regression analysis
- **Custom Functions**:
  - `analyse_trends_by_risk_factor()`: Analyses trends across ages for each risk factor

**Logic:**
- Analyses how relationships between childhood IQ and cardiovascular risk factors change across ages
- Performs linear regression to test for trends in each risk factor
- Compares early vs. late age periods
- Creates line plots showing trends for each risk factor

**Output:**
- Trend line plots for each risk factor (`../figures/trend_{risk_factor}.png`)
- Trend summary statistics (`../tables/trend_summary.csv`)
- Detailed markdown report (`../docs/cross_age_trend_findings.md`)

### 4. extended_analysis.py

**Input:** Processed summary data (`../tables/readable_summary.csv`)

**Key Modules and Functions:**
- **pandas (pd)**: Data manipulation and analysis
  - `pd.read_csv()`, `pd.cut()`: Bins continuous data into categories
  - `pd.Categorical()`: Creates categorical data with specified order
  - `df.pivot_table()`: Creates pivot tables for analysis
- **matplotlib.pyplot (plt)**: Plotting library
  - `plt.figure()`, `plt.bar()`, `plt.savefig()`
- **seaborn (sns)**: Statistical data visualisation
  - `sns.boxplot()`, `sns.heatmap()`, `sns.regplot()`
- **scipy.stats**: Statistical functions
  - `stats.linregress()`: Performs linear regression analysis

**Logic:**
- Groups data into developmental periods (Childhood, Adolescence, Early Adulthood)
- Categorises risk factors into groups (Anthropometric, Blood Pressure, Lipid Profile, Glucose Metabolism)
- Analyses patterns within developmental periods and risk categories
- Creates visualisations of effect sizes and significant associations
- Generates trajectory plots for each risk category

**Output:**
- Period characteristics table (`../tables/participant_characteristics_by_period.csv`)
- Risk factor by period table (`../tables/risk_factor_by_developmental_period.csv`)
- Risk category by period table (`../tables/risk_category_by_developmental_period.csv`)
- Various visualisations (boxplots, heatmaps, bar charts)
- Trajectory plots for each risk category
- Markdown summary report (`../docs/extended_analysis_summary.md`)

### 5. additional_visualisations.py

**Input:** Processed summary data (`../tables/readable_summary.csv`)

**Key Modules and Functions:**
- **pandas (pd)**: Data manipulation and analysis
  - `pd.read_csv()`, `df.groupby()`, `df.pivot()`
- **matplotlib.pyplot (plt)**: Plotting library
  - `plt.figure()`, `plt.subplot()`, `plt.bar()`, `plt.barh()`, `plt.errorbar()`
- **numpy (np)**: Numerical computing
  - `np.polyfit()`, `np.poly1d()`: Fits polynomial to data
- **seaborn (sns)**: Statistical data visualisation
  - `sns.heatmap()`: Creates heatmap visualisation
- **matplotlib.lines**: Line creation
  - `Line2D()`: Creates line objects for legends

**Logic:**
- Creates supplementary visualisations to highlight key patterns
- Analyses significant associations by age with trend line
- Summarises effect sizes by risk factor with error bars
- Visualises developmental patterns in a heatmap
- Evaluates consistency and strength of associations in a scatter plot

**Output:**
- Significant associations by age chart (`../figures/significant_associations_by_age.png`)
- Average effect by risk factor chart (`../figures/average_effect_by_risk_factor.png`)
- Developmental pattern heatmap (`../figures/developmental_pattern_heatmap.png`)
- Consistency and strength scatter plot (`../figures/consistency_strength_scatter.png`)

## Workflow Integration

The five scripts form a sequential and parallel analysis pipeline:

1. **Data Preparation:**
   - `extracted_data.py` processes raw Stata regression output into a structured format using **pandas** for data manipulation
   - The script creates the foundation dataset (`readable_summary.csv`) that serves as input for all subsequent analyses

2. **Parallel Initial Analyses:**
   - Two scripts perform complementary analyses on the prepared data:
     - `age_specific_analysis.py` examines associations at each individual age using **pandas** for data grouping and **matplotlib/seaborn** for visualisation
     - `cross_age_trend_analysis.py` analyses trends across the age spectrum using **scipy.stats** for linear regression and **matplotlib** for trend visualisation

3. **Integrated Analysis:**
   - `extended_analysis.py` builds on previous findings by grouping data into developmental periods and risk categories using **pandas.cut()** for categorisation
   - Uses **seaborn** for advanced visualisations and **scipy.stats** for statistical testing

4. **Supplementary Visualisation:**
   - `additional_visualisations.py` creates targeted visualisations to highlight key findings using **matplotlib** for custom plots
   - Employs **numpy** for trend line fitting and **seaborn** for heatmap generation

Each script builds upon the outputs of previous scripts, creating a comprehensive analysis pipeline that examines the data from multiple perspectives. The workflow progresses from basic data extraction to increasingly sophisticated analyses, culminating in integrated visualisations that synthesise the findings.

## Key Python Libraries Used Throughout the Workflow

1. **pandas**: Core data manipulation library used in all scripts for:
   - Reading/writing CSV files
   - Data filtering and transformation
   - Grouping and aggregation
   - Pivoting data for visualisation

2. **matplotlib**: Primary visualisation library used for:
   - Creating bar charts, scatter plots, and line plots
   - Adding annotations and reference lines
   - Customising plot appearance
   - Saving visualisations to files

3. **seaborn**: Advanced statistical visualisation library for:
   - Creating heatmaps to show patterns across multiple variables
   - Generating box plots to show distributions
   - Creating regression plots with confidence intervals

4. **numpy**: Numerical computing library used for:
   - Mathematical operations on data
   - Trend line fitting
   - Creating evenly spaced sequences

5. **scipy.stats**: Statistical functions library for:
   - Linear regression analysis
   - Statistical testing
   - Trend analysis

6. **os**: Operating system interface used for:
   - Creating directories for outputs
   - Managing file paths

These libraries work together to provide a comprehensive toolkit for data analysis, from initial data processing to statistical analysis and visualisation, enabling a thorough examination of the relationship between childhood cognitive ability and cardiovascular risk factors across development.
