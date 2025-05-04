# Dissertation Project Repository

This repository contains all materials used for the dissertation project, organised into a structured framework for both Python and Stata analyses.

## Repository Structure

The repository is organised into two main analysis directories, each with a similar structure to maintain consistency across different analytical approaches:

```
dissertation/
├── python_analysis/
│   ├── docs/            # Documentation files
│   ├── figures/         # Generated figures and visualisations
│   ├── python_scripts/  # Python analysis scripts
│   ├── scripts/         # Utility and helper scripts
│   └── tables/          # Generated tables and results
│
├── stata/
│   ├── do_files/        # Stata do files for analysis
│   ├── figures/         # Generated figures from Stata
│   ├── log_files/       # Stata log files
│   ├── scripts/         # Utility and helper scripts for Stata
│   └── tables/          # Generated tables and results from Stata
│
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Analysis Components

### Python Analysis

The `python_analysis` directory contains all Python-based analyses, including:

- **docs/**: Documentation related to the Python analysis methodology and results
- **figures/**: Visualisations and plots generated from Python analysis
- **python_scripts/**: Main Python scripts for data processing, analysis, and modeling
- **scripts/**: Helper scripts and utilities for the Python workflow
- **tables/**: Data tables and results exported from Python analysis

### Stata Analysis

The `stata` directory contains all Stata-based analyses, including:

- **do_files/**: Stata do files that perform data cleaning, analysis, and visualisation
- **figures/**: Visualisations and plots generated from Stata analysis
- **log_files/**: Log files generated during Stata analysis execution
- **scripts/**: Helper scripts and utilities for the Stata workflow
- **tables/**: Data tables and results exported from Stata analysis

## Languages Used

This project uses multiple programming languages:
- **Python (60.6%)**: Primary language for data analysis, visualisation, and modeling
- **Stata (32.3%)**: Statistical analysis and econometric modeling
- **Shell (7.1%)**: Utility scripts for automation and environment setup

## Getting Started

To use this repository:

1. Clone the repository:
   ```
   git clone https://github.com/jshih88/dissertation.git
   ```

2. Navigate to either the Python or Stata directories depending on your analysis needs.

3. Follow the specific instructions in the documentation files within each directory.

## Workflow Sequences

### Stata Analysis

**Base Directory** = "stata/"

1. Run "do_files/js_all_data_regress_z_iq8_exposures_age_sex_ses.do" in Stata to create the log files in directory "log_files/*.log". This do-file also includes do-files "js_template.do" and "js_gen_ses.do"

2. Run "scripts/js_all_data_regress_z_iq8_results.sh" that uses "log_files/*.log" to create the consolidated table "tables/js_all_data_regress_z_iq8_results.csv"

3. Run "scripts/js_all_data_regress_z_iq8_exposures_plot_by_age.do" that uses "tables/js_all_data_regress_z_iq8_results.csv" to create plots in "figures/iq8_<age>_all_depvars_sorted.png"

4. Run "scripts/js_all_data_regress_z_iq8_exposures_plot_by_depvars.do" that uses "tables/js_all_data_regress_z_iq8_results.csv" to create plots in "figures/js_all_data_regress_z_iq8_<depvar>_age_sex_ses.png"

### Python Data Science Ecosystem Analysis

**Base Directory** = "python_analysis/"

5. Run "scripts/stata_regress_zscore_by_age_by_depvar.sh" that uses "../stata/log_files/*.log" to create the consolidated table "tables/stata_regress_zscore_by_age_by_depvar.csv"

6. Run "scripts/stata_regress_zscore_by_depvar_by_age.sh" that uses "../stata/log_files/*.log" to create the consolidated table "tables/stata_regress_zscore_by_depvar_by_age.csv"

7. Run "python_scripts/extracted_data.py" to extract data from "tables/stata_regress_zscore_by_depvar_by_age.csv" and customize them to "tables/all_results_summary.csv" and "tables/readable_summary.csv"

8. Run "python_scripts/age_specific_analysis.py" that uses "tables/readable_summary.csv"

9. Run "python_scripts/cross_age_trend_analysis.py" that uses "tables/readable_summary.csv"

10. Run "extended_analysis.py" that uses "tables/readable_summary.csv"

11. Run "additional_visualisations.py" that uses "tables/readable_summary.csv"
