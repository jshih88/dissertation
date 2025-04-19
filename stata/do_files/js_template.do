***************************************************************************************************
********ALSPAC Childhood Cognitive Ability and the Emergence of Cardiovascular Risk Factors********
************************************Author: Jocelyn Shih*******************************************
****************************************Date:2025**************************************************
***************************************************************************************************

**Standard settings**

** Standard settings **
* Set the Stata version to ensure compatibility with version 18.5
version 18.5
* Clear all data from memory to start with a clean workspace
clear all
* Drop all macros to remove any previously defined macros and avoid conflicts
macro drop _all
* Turn off the "more" prompt, which pauses output when the screen is full
set more off
* Increase the maximum number of variables allowed in a dataset to 10,000
set maxvar 10000
* Set the path for the PLUS directory to a specific location for user-written Stata packages
sysdir set PLUS "S:\ICS_Student_Projects\2024-25\Jocelyn"

**Set Directory**
* Change the current working directory to the specified path
cd "S:\ICS_Student_Projects\2024-25\Jocelyn"

**Create Analysis Log**
* Load the dataset "B3665_Chiesa_04Oct2024.dta" into memory
use "B3665_Chiesa_04Oct2024", clear


***************************************************************************************
********************Data Preparation and Set-Up****************************
** Domain                        Variables
** ------                        ---------
** Cognitive Ability:            IQ scores at ages 8, 11, and 15
** Cardiovascular Risk Factors:
**   Anthropometrics:            BMI, waist circumference (ages 7–24).
**   Biomarkers:                 Blood pressure, lipid profiles etc
**   Behavioral:                 Physical activity, diet quality, smoking initiation.
** Covariates:
**   Mediators:                  Parental SES, educational attainment, adult income.
**   Confounders:                Birth weight, maternal smoking, gestational age.
***************************************************************************************

** Grouping of different variable types
local vardomains descriptor cognitive_ability cardio_risk_factors covariates

** Grouping of special variables into relevant types
local descriptor_vartypes age gender ethnicity weight
local cognitive_ability_vartypes iq
local cardio_risk_factors_vartypes blood_pressure bmi waist lipid glucose insulin physical_actvity smoking
local covariates_vartypes socio_economic birth_weight gestational_age

** Defining list of variables related to each special variable
local age_vars_raw f7003c f9003c fd003c fe003c ff0011a fg0011a fh0011a fh6276 FJ003a FKAR0010
local gender_vars_raw kz021 ccm900
local ethnicity_vars_raw c800 c804
local weight_vars_raw f7ms026 f9ms026 fdms026 fems026 fh3010 FJMR022 FKMS1030
local iq_vars_raw f8ws110 f8ws111 f8ws112 f8ws115 fh6280
local blood_pressure_vars_raw f7sa021 f7sa022 f9sa021 f9sa022 fdar117 fdar118 fesa021 fesa022 ff2620 ff2625 ff2621 ff2626 fg6120 fg6125 fg6121 fg6126 fh2030 fh2035 fh2031 fh2036 FJAR015a FJAR016a FJAR017a FJAR018a FJAR015b FJAR016b FJAR017b FJAR018b FJEL091 FJEL105 FKBP1030 FKBP1031
local bmi_vars_raw f7ms026a f9ms026a fdms026a fems026a ff2039 fg3139 fh3019 FKMS1040 FJMR022a
local waist_vars_raw f7ms018 f9ms018 fdms018 fems018 ff2020 fg3120 fh4020 FKMS1052
local lipid_vars_raw CHOL_F7 CHOL_F9 chol_TF3 CHOL_TF4 Chol_F24 HDL_F7 HDL_f9 hdl_TF3 HDL_TF4 HDL_F24 LDL_F7 LDL_f9 ldl_TF3 LDL_TF4 LDL_F24 TRIG_F7 trig_f9 trig_TF3 TRIG_TF4 Trig_F24
local glucose_vars_raw Glc_F7 Glc_TF3 Glc_TF4 glucose_TF3 glucose_TF4 Glc_F24 Glucose_F24
local insulin_vars_raw insulin_F9 insulin_TF3 insulin_TF4 Insulin_F24
local physical_actvity_vars_raw feag103 feag104 feag105 fg1211 fg1212 fg1213 fh5013 fh5014 fh5015 fh5022 fh5023 fh5024 FKAC0001 FKAC1080 fg4827
local smoking_vars_raw fg4822 fh8430 fh8432 FJSM050 FJSM150 FKSM1010 FKSM1020 FKSM1060
local socio_economic_vars_raw c645a c666a c755 c765
local birth_weight_vars_raw kz030b kz030c kz030d
local gestational_age_vars_raw bestgest


***************************************************************************
** The code is designed to clean multiple variables organized into groups and types.
** It uses nested loops to iterate through variable groups, types, and individual variables.
**For each variable, it checks if the value is negative and replaces it with missing (.).
* for each var domain
foreach vard of local vardomains {
    * for each of the var type
    foreach vart of local `vard'_vartypes {
        * for each of the var
        foreach var of local `vart'_vars_raw {
            * Replace the value of the current variable with missing (.) if the value is less than 0
			di "======================================================="
			di "Replacing missing values for [`vard'] [`vart'] [`var']:"
            replace `var' = . if `var' < 0
			di "======================================================="
        }
    }
}

***************************************************************************
** renaming convention: <abbreviation>_<descriptions>_<age>
***************************************************************************

** Desriptors

* Desriptors/Age
*----- ------                   //
rename f7003c   age_7           // Age (months) at Focus @ 7 visit
rename f9003c   age_9           // Age (months) at F9 visit
rename fd003c	age_10			// Age (months) at F10 visit
rename fe003c	age_11			// Age (months) at F11+ visit
rename ff0011a  age_12          // DV: Age of study child at attendance (months)
rename fg0011a  age_13          // DV: Age of study child at attendance (months): TF2
rename fh0011a  age_15          // DV: Age of study child at attendance (months): TF3
rename fh6276   age_bottom_15   // YP: Chronological Age (bottom of each group) - Wasi Score : TF3
rename FJ003a   age_17          // Age in months at clinic visit: TF4
rename FKAR0010 age_24          // Age at clinic visit (in months): F@24

local age_vars age_9 age_10 age_11 age_12 age_13 age_15 age_bottom_15 age_17 age_24
local age_age_vars 9 10 11 12 13 15 17 24

* Desriptors/Gender
*----- ------                   //
rename kz021    sex             // Participant assigned sex at birth
rename ccm900   cgender         // D1: Child's gender
local gender_vars sex cgender

* Desriptors/Ethnicity
*----- ------                   //
rename c800     ethnic          // Ethnic group
rename c804     ethnic_bg       // Child ethnic background
local ethnicity_vars ethnic ethnic_bg

* Desriptors/Weight
*----- ------                   //
rename f7ms026  wt_7            // Weight (kg): F7
rename f9ms026  wt_9            // Weight (kg): F9
rename fdms026  wt_10           // Weight (kg): F10
rename fems026  wt_11           // Weight (kg): F11
rename fh3010   wt_15           // Weight (Kgs): TF3
rename FJMR022  wt_17           // Weight (kgs): TF4
rename FKMS1030 wt_24           // Weight (kg): F@24

local wt_vars wt_9 wt_10 wt_11 wt_15 wt_17 wt_24
local wt_age_vars 9 10 11 15 17 24
gen wt_label = "Weight"

** Main Exposure Of Interest

* Main Exposure Of Interest/Cognitive Ability/IQ
*----- ------                   //
rename f8ws110  verbal_iq_8     // WISC - Verbal IQ: F8
rename f8ws111  perf_iq_8       // WISC - Performance IQ: F8
rename f8ws112  total_iq_8      // WISC - Total IQ: F8
rename f8ws115  cat_iq_8        // WISC - Categorical Total IQ: F8
rename fh6280   total_iq_15     // Total IQ score : TF3

local iq_vars verbal_iq_8 perf_iq_8 total_iq_8 cat_iq_8 total_iq_15

** Main outcome of interest

* Main outcome of interest/Cardiovascular Risk Factors/Blood Pressure
*----- ------                   //
rename f7sa021  bp_sys_7        // Mean BP systolic: samples: F7
rename f7sa022  bp_dia_7        // Mean BP diastolic: samples: F7
rename f9sa021  bp_sys_9        // Mean BP systolic: samples: F9
rename f9sa022  bp_dia_9        // Mean BP diastolic: samples: F9
rename fdar117  bp_sys_10       // Systolic blood pressure: F10
rename fdar118  bp_dia_10       // Diastolic blood pressure: F10
rename fesa021  bp_sys_11       // Mean BP systolic: samples F11+
rename fesa022  bp_dia_11       // Mean BP diastolic: samples F11+
rename ff2620   bp_sys_r1_12    // BP result 1 - systolic: activity: TF1
rename ff2625   bp_sys_r2_12    // BP result 2 - systolic: activity: TF1
rename ff2621   bp_dia_r1_12    // BP result 1 - diastolic: activity: TF1
rename ff2626   bp_dia_r2_12    // BP result 2 - diastolic: activity: TF1
rename fg6120   bp_sys_r1_13    // BP result 1 - systolic: TF2
rename fg6125   bp_sys_r2_13    // BP result 2 - systolic: TF2
rename fg6121   bp_dia_r1_13    // BP result 1 - diastolic: TF2
rename fg6126   bp_dia_r2_13    // BP result 2 - diastolic: TF2
rename fh2030   bp_sys_r1_15    // BP result 1 - systolic: TF3
rename fh2035   bp_sys_r2_15    // BP result 2 - systolic: TF3
rename fh2031   bp_dia_r1_15    // BP result 1 - diastolic: TF3
rename fh2036   bp_dia_r2_15    // BP result 2 - diastolic: TF3
rename FJAR015a bp_sys_ra_r1_17 // Right arm BP 1: systolic: TF4
rename FJAR016a bp_sys_ra_r2_17 // Right arm BP 2: systolic: TF4
rename FJAR017a bp_sys_la_r1_17 // Left arm BP 1: systolic: TF4
rename FJAR018a bp_sys_la_r2_17 // Left arm BP 2: systolic: TF4
rename FJAR015b bp_dia_ra_r1_17 // Right arm BP 1: diastolic: TF4
rename FJAR016b bp_dia_ra_r2_17 // Right arm BP 2: diastolic: TF4
rename FJAR017b bp_dia_la_r1_17 // Left arm BP 1: diastolic: TF4
rename FJAR018b bp_dia_la_r2_17 // Left arm BP 2: diastolic: TF4
rename FJEL091  bp_dia_cen_17   // Central Diastolic Pressure: ELBA: TF4 FJEL091
rename FJEL105  bp_sys_cen_17   // Central Systolic Pressure: ELBA: TF4
rename FKBP1030 bp_sys_24       // Average seated systolic blood pressure (mmHg): F@24
rename FKBP1031 bp_dia_24       // Average seated diastolic blood pressure (mmHg): F@24

* generate mean values
egen bp_sys_12 = rowmean(bp_sys_r1_12 bp_sys_r2_12)
egen bp_dia_12 = rowmean(bp_dia_r1_12 bp_dia_r2_12)
egen bp_sys_13 = rowmean(bp_sys_r1_13 bp_sys_r2_13)
egen bp_dia_13 = rowmean(bp_dia_r1_13 bp_dia_r2_13)
egen bp_sys_15 = rowmean(bp_sys_r1_15 bp_sys_r2_15)
egen bp_dia_15 = rowmean(bp_dia_r1_15 bp_dia_r2_15)
egen bp_sys_17 = rowmean(bp_sys_ra_r1_17 bp_sys_ra_r2_17)
egen bp_dia_17 = rowmean(bp_dia_ra_r1_17 bp_dia_ra_r2_17)

local bp_sys_vars bp_sys_9 bp_sys_10 bp_sys_11 bp_sys_12 bp_sys_13 bp_sys_15 bp_sys_17 bp_sys_24
local bp_sys_age_vars 9 10 11 12 13 15 17 24
gen bp_sys_label = "Systolic_blood_pressure"

local bp_dia_vars bp_dia_9 bp_dia_10 bp_dia_11 bp_dia_12 bp_dia_13 bp_dia_15 bp_dia_17 bp_dia_24
local bp_dia_age_vars 9 10 11 12 13 15 17 24
gen bp_dia_label = "Diastolic_blood_pressure"

* Main outcome of interest/Cardiovascular Risk Factors/BMI
*----- ------                   //
rename f7ms026a bmi_7           // BMI: F7
rename f9ms026a bmi_9           // BMI: F9
rename fdms026a bmi_10          // BMI: F10
rename fems026a bmi_11          // BMI: F11
rename ff2039   bmi_12          // DV: Body mass index (BMI): measuring: TF1
rename fg3139   bmi_13          // DV: Body mass index (BMI): measures: TF2
rename fh3019   bmi_15          // DV: Body mass index (BMI): measures: TF3
rename FJMR022a bmi_17          // DV: BMI: TF4
rename FKMS1040 bmi_24          // DV: Body mass index (BMI): F@24

local bmi_vars bmi_9 bmi_10 bmi_11 bmi_12 bmi_13 bmi_15 bmi_17 bmi_24
local bmi_age_vars 9 10 11 12 13 15 17 24
gen bmi_label = "BMI"

* Main outcome of interest/Cardiovascular Risk Factors/Waist Circumference
*----- ------                   //
rename f7ms018  wc_7            // Waist circumference (cm): F7
rename f9ms018  wc_9            // Waist circumference (cm): F9
rename fdms018  wc_10           // Waist circumference (cm): F10
rename fems018  wc_11           // Waist circumference (cm): F11
rename ff2020   wc_12           // M11: Waist circumference (cms): measuring: TF1
rename fg3120   wc_13           // M11: Waist circumference (cms): TF2
rename fh4020   wc_15           // M11: Waist circumference (cms): TF3
rename FKMS1052 wc_24_mm        // DV: Average waist circumference (mm): F@24

gen wc_24 = wc_24_mm / 10

local wc_vars wc_9 wc_10 wc_11 wc_12 wc_13 wc_15 wc_24
local wc_age_vars 9 10 11 12 13 15 24
gen wc_label = "Waist_circumference"

* Main outcome of interest/Cardiovascular Risk Factors/Lipid Profile
*----- ------                   //
rename CHOL_F7  chol_7          // Cholesterol mmol/l, Focus@7
rename CHOL_F9  chol_9          // Cholesterol mmol/l, Focus @9
rename chol_TF3 chol_15         // Cholesterol mmol/l, TF3
rename CHOL_TF4 chol_17         // Cholesterol mmol/l, TF4
rename Chol_F24 chol_24         // Cholesterol mmol/L, Focus@24
rename HDL_F7   hdl_7           // HDL mmol/l, Focus@7
rename HDL_f9   hdl_9           // HDL mmol/l, Focus@9
rename hdl_TF3  hdl_15          // HDL mmol/l, TF3
rename HDL_TF4  hdl_17          // HDL mmol/l, TF4
rename HDL_F24  hdl_24          // High-density lipoprotein (HLD) mmol/L, Focus@24
rename LDL_F7   ldl_7           // LDL mmol/l, Focus@7
rename LDL_f9   ldl_9           // LDL mmol/l, Focus@9
rename ldl_TF3  ldl_15          // LDL mmol/l, TF3
rename LDL_TF4  ldl_17          // LDL mmol/l, TF4
rename LDL_F24  ldl_24          // Low-density lipoprotein (LDL) mmol/L, Focus@24
rename TRIG_F7  trig_7          // Triglycerides mmol/l, Focus@7
rename trig_f9  trig_9          // Triglycerides mmol/l, Focus@9
rename trig_TF3 trig_15         // Triglycerides mmol/l, TF3
rename TRIG_TF4 trig_17         // Triglycerides mmol/l, TF4
rename Trig_F24 trig_24         // Triglycerides mmol/L, Focus@24

local chol_vars chol_9 chol_15 chol_17 chol_24
local chol_age_vars 9 15 17 24
gen chol_label = "Cholesterol"

local hdl_vars hdl_9 hdl_15 hdl_17 hdl_24
local hdl_age_vars 9 15 17 24
gen hdl_label = "High-density_lipoprotein_(HLD)"

local ldl_vars ldl_9 ldl_15 ldl_17 ldl_24
local ldl_age_vars 9 15 17 24
gen ldl_label = "Low-density_lipoprotein_(LDL)"

local trig_vars trig_9 trig_15 trig_17 trig_24
local trig_age_vars 9 15 17 24
gen trig_label = "Triglycerides"

* Main outcome of interest/Cardiovascular Risk Factors/Glucose Levels
*----- ------                       //
rename Glc_F7       glc_meta_7       // Glucose (mmol/l): F7
rename Glc_TF3      glc_meta_15      // Glucose (mmol/l): TF3
rename Glc_TF4      glc_meta_17      // Glucose (mmol/l): TF4
rename Glc_F24      glc_meta_24      // Glucose (mmol/l): F24
rename glucose_TF3	glc_bio_15       // Glucose mmol/l, TF3
rename glucose_TF4	glc_bio_17       // Glucose mmol/l, TF4
rename Glucose_F24	glc_bio_24       // Glucose mmol/L, Focus@24

// use age 7 for age 9
gen glc_meta_9 = glc_meta_7

local glc_meta_vars glc_meta_9 glc_meta_15 glc_meta_17 glc_meta_24
local glc_meta_age_vars 9 15 17 24
gen glc_meta_label = "Glucose_metabolism"

local glc_bio_vars glc_bio_15 glc_bio_17 glc_bio_24
local glc_bio_age_vars 15 17 24
gen glc_bio_label = "Glucose_bioavailability"

* Main outcome of interest/Cardiovascular Risk Factors/Insulin Levels
*----- ------                   //
rename insulin_F9  insul_9      // Insulin mU/L, Focus@9
rename insulin_TF3 insul_15     // Insulin mu/l, TF3
rename insulin_TF4 insul_17     // Insulin mu/l, TF4
rename Insulin_F24 insul_24     // Insulin uU/mL, Focus@24

local insul_vars insul_9 insul_15 insul_17 insul_24
local insul_age_vars 9 15 17 24
gen insul_label = "Insulin"

* Main outcome of interest/Cardiovascular Risk Factors/Physical Actvity Levels
*----- ------                   //
rename feag103  pa_count_11     // DV: MVPA>=3600 total count for whole week (valid days): activity: F11
rename feag104  pa_min_11       // DV: MVPA>=3600 total minutes for whole week (valid days): activity: F11
rename feag105  pa_cpm_11       // DV: MVPA>=3600 mean cpm for whole week (valid days): activity: F11
rename fg1211   pa_count_13     // DV: MVPA >=3600 total count for whole week (valid days): activity: TF2
rename fg1212   pa_min_13       // DV: MVPA >=3600 total minutes for whole week (valid days): activity: TF2
rename fg1213   pa_cpm_13       // DV: MVPA >=3600 mean cpm for whole week (valid days): activity: TF2
rename fh5013   pa_count_15     // DV: MVPA>= 3600 total count for whole week (valid days): actigraph: TF3
rename fh5014   pa_min_15       // DV: MVPA>= 3600 total minutes for whole week (valid days): actigraph: TF3
rename fh5015   pa_cpm_15       // DV: MVPA>= 3600 mean cpm for whole week (valid days): actigraph: TF3
rename fh5022   pa_cpm_7t12_15  // DV: MVPA>= 3600 daily mean cpm 7am-12pm: whole week (valid days): actigraph: TF3
rename fh5023   pa_cpm_12t5_15  // DV: MVPA>= 3600 daily mean cpm 12pm-5pm: whole week (valid days): actigraph: TF3
rename fh5024   pa_cpm_5t10_15  // DV: MVPA>= 3600 daily mean cpm 5pm-10pm: whole week (valid days): actigraph: TF3
rename FKAC0001 pa_attn_24      // YP attended physical activity session: F@24
rename FKAC1080 pa_min_24       // Total number of valid light activity minutes overall: F@24
rename fg4827   pa_minpd_24     // Average number of valid light activity minutes per day: F@24 FKAC1090

local physical_actvity_vars pa_count_11 pa_min_11 pa_cpm_11 pa_count_13 pa_min_13 pa_cpm_13 pa_count_15 pa_min_15 pa_cpm_15 pa_cpm_7t12_15 pa_cpm_12t5_15 pa_cpm_5t10_15 pa_attn_24 pa_min_24 pa_minpd_24

* Main outcome of interest/Cardiovascular Risk Factors/Smoking
*----- ------                   //
rename fg4822   sm_13           // S2: Teenager has smoked cigarettes: TF2
rename fh8430   sm_whole_15     // SM1030: YP has ever smoked a whole cigarette: TF3
rename fh8432   sm_total_15     // SM1050: Total number of cigarettes YP has smoked in their lifetime: TF3
rename FJSM050  sm_whole_17     // SM344: YP has ever smoked a whole cigarette (including roll-ups): TF4
rename FJSM150  sm_total_17     // SM346: Total number of cigarettes YP has smoked in their lifetime: TF4
rename FKSM1010 sm_whole_24     // B1: YP has ever smoked a whole cigarette: F@24
rename FKSM1020 sm_total_24     // B2: Total number of cigarettes smoked in lifetime: F@24
rename FKSM1060 sm_pday_24      // B6: YP smokes every day: F@24
local smoking_vars sm_13 sm_whole_15 sm_total_15 sm_whole_17 sm_total_17 sm_whole_24 sm_total_24 sm_pday_24

** Confounders

* Confounders/Socioeconomic status
*----- ------                   //
rename c645a    mother_ed       // Mums highest ed qualification
rename c666a    father_ed       // Partners highest ed qualification
rename c755     mother_soc      // Social Class - Maternal
rename c765     father_soc      // Social Class - Paternal
local socio_economic_vars mother_ed father_ed mother_soc father_soc

* Confounders/Birth weight
*----- ------                   //
rename kz030b   bw_odata        // Birthweight from obstetrics data (grams)
rename kz030c   bw_alspac       // Birthweight from ALSPAC measurers (grams)
rename kz030d   bw_0            // Birthweight from notifications or clinical records (grams)
local birth_weight_vars bw_odata bw_alspac bw_0

* Confounders/Gestational age
*----- ------                   //
rename bestgest gest            // The best gestation we can get - Length of pregnancy (weeks)
local gestational_age_vars gest

///////////////////////////////////////////////////////////////////////////

// List IDs of Complete Cases
// Original Observation ID
gen orig_obs_id = _n

label define sex_label 1 "Male" 2 "Female", replace
label values sex sex_label


