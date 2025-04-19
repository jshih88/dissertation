# Bash Script Analysis

## 1. stata_regress_zscore_by_depvar_by_age.sh

**Input:**
- Multiple Stata log files containing regression results (stored in `../../stata/log_files/`)
- Log files follow naming pattern: `js_all_data_regress_iq8_[variable]_age_sex_ses.log`
- Variables include: bmi, wc, bp_sys, bp_dia, chol, hdl, ldl, trig, glc_meta, insul

**Logic:**
1. Defines a function `parse_logs()` that:
   - Extracts key statistics from Stata regression output using grep and awk
   - Formats coefficients, confidence intervals, p-values, and R² values
   - Prints formatted results in a tabular structure
2. Processes each log file in the list using the parse_logs function
3. Organises results by dependent variable (risk factor)
4. For each risk factor, checks if data exists for each age (9, 10, 11, 12, 13, 15, 17, 24)
5. Inserts "NO_DATA" placeholders for missing age-variable combinations
6. Formats output as CSV-like text with headers

**Output:**
- Structured text output organised by risk factor (dependent variable)
- For each risk factor, displays regression results across different ages
- Each row contains: variable_age, coefficient with CI, p-value, R², sample size, missing values
- Output format is suitable for further processing by data analysis scripts

## 2. stata_regress_zscore_by_age_by_depvar.sh

**Input:**
- Identical to the first script: same Stata log files from the same directory
- Log files follow naming pattern: `js_all_data_regress_iq8_[variable]_age_sex_ses.log`
- Variables include: bmi, wc, bp_sys, bp_dia, chol, hdl, ldl, trig, glc_meta, insul

**Logic:**
1. Uses the same `parse_logs()` function as the first script to extract and format statistics
2. Processes the same set of log files
3. Key difference: Organises results by age rather than by dependent variable
4. For each age (9, 10, 11, 12, 13, 15, 17, 24), checks if data exists for each risk factor
5. Inserts "NO_DATA" placeholders for missing age-variable combinations
6. Formats output as CSV-like text with headers

**Output:**
- Structured text output organised by age
- For each age, displays regression results across different risk factors
- Each row contains: variable_age, coefficient with CI, p-value, R², sample size, missing values
- Output format is suitable for further processing by data analysis scripts

## Workflow Between Scripts

These scripts represent two different ways of organising the same underlying data:

1. **Complementary Organisation:**
   - The first script organises data by risk factor, making it easier to track how a specific risk factor's relationship with IQ changes across ages
   - The second script organises data by age, making it easier to compare how different risk factors relate to IQ at a specific age

2. **Common Data Source:**
   - Both scripts process the same Stata log files
   - Both extract identical statistical information
   - Both handle missing data in the same way

3. **Different Analytical Perspectives:**
   - Together, these scripts provide two complementary views of the same regression results
   - This dual organisation supports different types of analyses in subsequent processing steps

4. **Data Pipeline Integration:**
   - These scripts likely serve as data preparation steps for the Python analysis scripts
   - The first script's output (`by_depvar_by_age`) aligns with analyses that track risk factors across development
   - The second script's output (`by_age_by_depvar`) aligns with analyses that compare risk factors at specific ages
