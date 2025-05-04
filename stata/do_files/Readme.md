# Stata Do Files Analysis and Description

This document provides a comprehensive analysis of five Stata do files used for examining the relationship between childhood IQ and cardiovascular risk factors. Each file serves a specific purpose in the overall workflow, from data preparation to statistical analysis and visualisation.

## Table of Contents
1. [js_template.do](#js_template.do)
2. [js_gen_ses.do](#js_gen_ses.do)
3. [js_all_data_regress_z_iq8_exposures_age_sex_ses.do](#js_all_data_regress_z_iq8_exposures_age_sex_ses.do)
4. [js_all_data_regress_z_iq8_exposures_plot_by_age.do](#js_all_data_regress_z_iq8_exposures_plot_by_age.do)
5. [js_all_data_regress_z_iq8_exposures_plot_by_depvars.do](#js_all_data_regress_z_iq8_exposures_plot_by_depvars.do)
6. [Overall Workflow](#overall-workflow)

## js_template.do

### Overview
`js_template.do` serves as the foundational setup file for the entire analysis workflow. It establishes the data structure, performs initial data cleaning, and creates standardised variable naming conventions for the ALSPAC (Avon Longitudinal Study of Parents and Children) dataset focused on childhood cognitive ability and cardiovascular risk factors.

### Workflow
1. **Environment Setup**: Initialises Stata environment with version settings, memory clearing, and directory configuration
2. **Data Loading**: Loads the primary dataset "B3665_Chiesa_04Oct2024.dta"
3. **Variable Organisation**: Groups variables into domains (descriptors, cognitive ability, cardiovascular risk factors, covariates)
4. **Missing Value Handling**: Replaces negative values with missing values (.) across all variables
5. **Variable Renaming**: Implements a consistent naming convention (`<abbreviation>_<description>_<age>`) for all variables
6. **Variable Labeling**: Creates descriptive labels for variables and organises them into logical groups

### Stata Functions Used
- `version`: Sets Stata version compatibility
- `clear all`: Clears memory
- `macro drop _all`: Removes all macros
- `set more off`: Disables pause in output display
- `set maxvar`: Sets maximum number of variables
- `sysdir set`: Configures directory for user-written packages
- `cd`: Changes working directory
- `use`: Loads dataset
- `replace`: Replaces values in variables
- `rename`: Renames variables
- `gen`: Creates new variables
- `egen`: Creates new variables using extended functions
- `local`: Creates local macros for variable grouping
- `foreach`: Implements looping structures for batch operations
- `label define/values`: Creates and assigns value labels

### Inputs
- Primary dataset: "B3665_Chiesa_04Oct2024.dta"

### Outputs
- Cleaned and structured dataset with:
  - Standardised variable naming
  - Organised variable groupings
  - Properly labeled variables
  - Missing values handled consistently
  - Age-specific variable collections for longitudinal analysis

### Key Variable Groups Created
1. **Descriptors**: Age, gender, ethnicity, weight
2. **Cognitive Ability**: IQ scores at ages 8, 11, and 15
3. **Cardiovascular Risk Factors**:
   - Anthropometrics: BMI, waist circumference (ages 7-24)
   - Blood pressure: Systolic and diastolic measurements
   - Lipid profiles: Cholesterol, HDL, LDL, triglycerides
   - Glucose metabolism and insulin levels
   - Behavioral factors: Physical activity, smoking
4. **Covariates**: Socioeconomic status, birth weight, gestational age

### Relationship to Other Files
This file serves as the foundation for all subsequent analysis scripts. Other do files include this template at the beginning of their execution to ensure consistent data structure and variable definitions. The template creates the variable groupings and naming conventions that are essential for the regression analyses and visualisations performed in the other scripts.

## js_gen_ses.do

### Overview
`js_gen_ses.do` is a specialised script that generates a socioeconomic status (SES) variable based on parental social class information. This SES variable is used as a covariate in the regression analyses to control for socioeconomic factors when examining the relationship between childhood IQ and cardiovascular risk factors.

### Workflow
1. **SES Variable Creation**: Generates a new SES variable by taking the minimum value (highest social class) between mother's and father's social class
2. **Missing Data Handling**: Implements logic to use one parent's social class when the other is missing
3. **Variable Labeling**: Applies detailed labels to the SES categories
4. **Distribution Check**: Tabulates the distribution of the new SES variable to verify its creation

### Stata Functions Used
- `gen`: Creates the new SES variable
- `replace`: Modifies the SES variable for cases with missing data
- `label define`: Creates value labels for the SES categories
- `label values`: Applies the defined labels to the SES variable
- `tab`: Tabulates the distribution of the SES variable

### Inputs
- Existing variables in the dataset:
  - `mother_soc`: Mother's social class
  - `father_soc`: Father's social class

### Outputs
- New variable `ses`: Socioeconomic status based on parental social class
- Labeled SES categories:
  1. "I Professional"
  2. "II Managerial/Technical"
  3. "IIINM Skilled Non-Manual"
  4. "IIIM Skilled Manual"
  5. "IV Partly Skilled"
  6. "V Unskilled"
  65. "Armed Forces"

### Relationship to Other Files
This file is included by `js_all_data_regress_z_iq8_exposures_age_sex_ses.do` to ensure the SES variable is available as a covariate in the regression analyses. The SES variable is critical for the main analysis as it allows the researchers to control for socioeconomic factors when examining the relationship between childhood IQ and cardiovascular risk factors.

## js_all_data_regress_z_iq8_exposures_age_sex_ses.do

### Overview
`js_all_data_regress_z_iq8_exposures_age_sex_ses.do` is the core analytical script that performs multiple linear regression analyses to examine the relationship between childhood IQ at age 8 and various cardiovascular risk factors across different ages, while controlling for age, sex, and socioeconomic status (SES).

### Workflow
1. **Environment Setup**: Creates output directory and configures Stata settings
2. **Data Preparation**: 
   - Includes the template file for variable definitions
   - Runs the SES generation script
   - Defines exposure variables and IQ variables
3. **Nested Loop Structure**:
   - Outer loop: Iterates through each exposure variable (BMI, waist circumference, blood pressure, etc.)
   - Inner loop: Processes IQ at age 8
   - Innermost loop: Iterates through each age point for the exposure variable
4. **Standardisation**: Converts exposure variables to z-scores for comparability
5. **Regression Analysis**: Performs linear regression with z-scored exposure as dependent variable and IQ as independent variable, controlling for age, sex, and SES
6. **Results Extraction**: Extracts regression coefficients and confidence intervals
7. **Results Storage**: Saves results to temporary files
8. **Visualisation**: Creates forest plots showing regression coefficients across ages for each exposure
9. **Output Generation**: Exports graphs and logs results to files

### Stata Functions Used
- `capture mkdir`: Creates output directory if it doesn't exist
- `set more off`: Disables pause in output display
- `tempname/tempfile`: Creates temporary storage for results
- `include/do`: Runs external Stata scripts
- `local`: Creates local macros for variable lists
- `foreach`: Implements nested looping structures
- `preserve/restore`: Preserves and restores dataset state
- `postfile/post/postclose`: Creates and manages results files
- `zscore`: Standardises variables to z-scores
- `regress`: Performs linear regression analysis
- `matrix`: Extracts and manipulates regression results
- `twoway`: Creates visualisation plots
- `graph export`: Saves graphs to files
- `log using/close`: Manages log files for results

### Inputs
- Dataset prepared by `js_template.do`
- SES variable created by `js_gen_ses.do`
- Exposure variables: BMI, waist circumference, blood pressure (systolic/diastolic), cholesterol, HDL, LDL, triglycerides, glucose metabolism, insulin
- IQ variable: total_iq_8 (IQ at age 8)
- Covariates: age, sex, SES

### Outputs
- Log files: Detailed regression results for each exposure-age combination
- PNG files: Forest plots showing regression coefficients and 95% confidence intervals across ages for each exposure variable
- Temporary results files: Structured data containing regression coefficients and confidence intervals

### Relationship to Other Files
- Includes `js_template.do` for data structure and variable definitions
- Runs `js_gen_ses.do` to create the SES covariate
- Generates results that are visualised differently in `js_all_data_regress_z_iq8_exposures_plot_by_age.do` and `js_all_data_regress_z_iq8_exposures_plot_by_depvars.do`
- Creates the core analytical results that form the basis for the visualisation scripts

## js_all_data_regress_z_iq8_exposures_plot_by_age.do

### Overview
`js_all_data_regress_z_iq8_exposures_plot_by_age.do` is a visualisation script that creates plots showing the association between IQ at age 8 and multiple cardiovascular risk factors, organised by age. This script takes regression results generated by the main analysis script and creates custom plots that display all dependent variables for each specific age point.

### Workflow
1. **Environment Setup**: Configures Stata settings and directories
2. **Data Import**: Imports the regression results CSV file generated by the main analysis
3. **Variable Cleaning**: Cleans up dependent variable names for better display in legends and labels
4. **Custom ID Assignment**: Creates a consistent ordering for dependent variables in the plots
5. **Age-Specific Filtering**: Loops through each unique age in the dataset
6. **Visualisation Creation**: For each age, creates a plot showing the association between IQ at age 8 and all cardiovascular risk factors measured at that age
7. **Output Generation**: Exports high-resolution PNG files for each age-specific plot

### Stata Functions Used
- `version`: Sets Stata version compatibility
- `clear all`: Clears memory
- `macro drop _all`: Removes all macros
- `set more off`: Disables pause in output display
- `set maxvar`: Sets maximum number of variables
- `sysdir set`: Configures directory for user-written packages
- `cd`: Changes working directory
- `import delimited`: Imports CSV data
- `label var`: Labels variables
- `gen`: Creates new variables
- `replace`: Modifies variable values
- `subinstr`: Substitutes text within strings
- `levelsof`: Extracts unique values from a variable
- `foreach`: Implements looping structure
- `preserve/restore`: Preserves and restores dataset state
- `keep if`: Filters data
- `twoway`: Creates visualisation plots with multiple elements
- `scatter`: Creates scatter plots for point estimates
- `rcap`: Creates range plots for confidence intervals
- `graph export`: Saves graphs to files

### Inputs
- CSV file: "output\js_all_data_regress_z_iq8_results.csv" containing regression results from the main analysis

### Outputs
- PNG files: Age-specific plots showing the association between IQ at age 8 and all cardiovascular risk factors measured at each specific age
  - File naming convention: "output\iq8_age[AGE]_all_depvars_custom.png"

### Relationship to Other Files
- Uses the results generated by `js_all_data_regress_z_iq8_exposures_age_sex_ses.do`
- Complements `js_all_data_regress_z_iq8_exposures_plot_by_depvars.do` by providing an alternative visualisation approach
- While `js_all_data_regress_z_iq8_exposures_plot_by_depvars.do` organises plots by dependent variable (showing age trends), this script organises plots by age (showing all dependent variables at each age)

## js_all_data_regress_z_iq8_exposures_plot_by_depvars.do

### Overview
`js_all_data_regress_z_iq8_exposures_plot_by_depvars.do` is a visualisation script that creates plots showing the association between IQ at age 8 and various cardiovascular risk factors across different ages. Unlike the plot_by_age script, this file organises the visualisation by dependent variable, allowing for the examination of age trends for each specific cardiovascular risk factor.

### Workflow
1. **Environment Setup**: Configures Stata settings and directories
2. **Data Import**: Imports the regression results CSV file generated by the main analysis
3. **Data Exploration**: Examines the structure of the imported data
4. **Variable Cleaning**: Simplifies dependent variable names for better display in plots
5. **Visualisation Creation**: Creates a panel of plots organised by dependent variable, with each panel showing the association between IQ at age 8 and a specific cardiovascular risk factor across all available ages
6. **Output Generation**: Exports a high-resolution PNG file containing all panels

### Stata Functions Used
- `version`: Sets Stata version compatibility
- `clear all`: Clears memory
- `macro drop _all`: Removes all macros
- `set more off`: Disables pause in output display
- `set maxvar`: Sets maximum number of variables
- `sysdir set`: Configures directory for user-written packages
- `cd`: Changes working directory
- `import delimited`: Imports CSV data
- `describe`: Displays variable information
- `list`: Shows data observations
- `replace`: Modifies variable values
- `subinstr`: Substitutes text within strings
- `twoway`: Creates visualisation plots
- `scatter`: Creates scatter plots for point estimates
- `rcap`: Creates range plots for confidence intervals
- `by()`: Creates panel plots by categories
- `graph export`: Saves graphs to files

### Inputs
- CSV file: "output\js_all_data_regress_z_iq8_results.csv" containing regression results from the main analysis

### Outputs
- PNG file: "output\js_all_data_regress_z_iq8_exposures_plot_by_depvars.png" showing the association between IQ at age 8 and each cardiovascular risk factor across all available ages

### Relationship to Other Files
- Uses the results generated by `js_all_data_regress_z_iq8_exposures_age_sex_ses.do`
- Complements `js_all_data_regress_z_iq8_exposures_plot_by_age.do` by providing an alternative visualisation approach
- While `js_all_data_regress_z_iq8_exposures_plot_by_age.do` organises plots by age (showing all dependent variables at each age), this script organises plots by dependent variable (showing age trends for each cardiovascular risk factor)

## Overall Workflow

The five Stata do files work together to create a comprehensive analysis of the relationship between childhood IQ at age 8 and various cardiovascular risk factors across different ages. Here's how they fit together in the overall workflow:

1. **Data Preparation and Structure** (`js_template.do`):
   - Sets up the environment and loads the raw dataset
   - Cleans and organises variables into logical groups
   - Creates standardised naming conventions
   - Prepares the dataset for analysis

2. **Covariate Creation** (`js_gen_ses.do`):
   - Generates the socioeconomic status (SES) variable
   - Handles missing data and applies appropriate labels
   - Prepares an important covariate for the regression analyses

3. **Core Statistical Analysis** (`js_all_data_regress_z_iq8_exposures_age_sex_ses.do`):
   - Includes the template and SES generation scripts
   - Performs multiple linear regression analyses
   - Controls for age, sex, and SES
   - Examines the relationship between IQ at age 8 and various cardiovascular risk factors
   - Generates forest plots and logs detailed results
   - Creates a structured results dataset for further visualisation

4. **Age-Specific Visualisation** (`js_all_data_regress_z_iq8_exposures_plot_by_age.do`):
   - Imports the regression results
   - Creates plots organised by age
   - Shows all cardiovascular risk factors for each specific age
   - Provides a cross-sectional view of associations at each age point

5. **Variable-Specific Visualisation** (`js_all_data_regress_z_iq8_exposures_plot_by_depvars.do`):
   - Imports the regression results
   - Creates plots organised by cardiovascular risk factor
   - Shows age trends for each specific risk factor
   - Provides a longitudinal view of associations across ages

This workflow demonstrates a systematic approach to analysing longitudinal data, from data preparation to statistical analysis and visualisation, with careful attention to controlling for potential confounding factors.
