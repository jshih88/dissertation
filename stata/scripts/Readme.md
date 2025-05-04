# Bash Script Analysis: js_all_data_regress_z_iq8_results.sh

## Overview

This bash script extracts and formats regression results from multiple Stata log files, creating a simplified CSV output with key regression parameters.

## Input

- Multiple Stata log files containing regression results (stored in `../log_files/`)
- Log files follow naming pattern: `js_all_data_regress_z_iq8_[variable]_age_sex_ses.log`
- Variables include: bmi, wc, bp_sys, bp_dia, chol, hdl, ldl, trig, glc_meta, insul

## Logic

1. Prints a CSV header line with column names: `iq,depvar,age,beta,lci,uci`
2. Defines a list of log files to process
3. For each log file in the list:
   - Uses `grep` to find lines containing "Regression results summary"
   - Uses `awk` to extract specific fields from these lines
   - Formats the extracted data as comma-separated values
   - Converts any Windows line endings to Unix format using `dos2unix`

## Output

- A clean CSV-formatted output with the following columns:
  - `iq`: IQ measure used in the regression (typically total_iq_8)
  - `depvar`: Dependent variable (cardiovascular risk factor)
  - `age`: Age at which the risk factor was measured
  - `beta`: Regression coefficient (effect size)
  - `lci`: Lower confidence interval bound
  - `uci`: Upper confidence interval bound
- Each row represents one regression analysis result
- Output is printed to standard output (can be redirected to a file)

## Workflow Context

This script serves as a data extraction and formatting tool in a larger analysis pipeline:

1. **Data Source**: Stata regression analyses examining the relationship between childhood IQ and cardiovascular risk factors
2. **Processing**: Extracts only the essential summary statistics from verbose log files
3. **Output Format**: Creates a clean, standardised CSV format suitable for further analysis
4. **Next Steps**: The CSV output can be easily imported into statistical software or data analysis scripts (e.g., Python, R) for visualisation and further analysis

The script provides a more concise alternative to the other scripts (`stata_regress_zscore_by_depvar_by_age.sh` and `stata_regress_zscore_by_age_by_depvar.sh`), focusing only on the core regression parameters without additional statistics like p-values, R², and sample sizes.
