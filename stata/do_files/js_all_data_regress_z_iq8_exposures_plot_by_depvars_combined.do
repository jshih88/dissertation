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

import delimited using "output\js_all_data_regress_z_iq8_results.csv", clear
describe
list in 1/5  // Check the first 5 observations

replace depvar = subinstr(depvar, "BMI_(bmi)", "BMI", .)
replace depvar = subinstr(depvar, "Cholesterol_(chol)", "Cholesterol", .)
replace depvar = subinstr(depvar, "Diastolic_blood_pressure_(bp_dia)", "Diastolic_blood_pressure", .)
replace depvar = subinstr(depvar, "Glucose_metabolism_(glc_meta)", "Glucose_metabolism", .)
replace depvar = subinstr(depvar, "High-density_lipoprotein_(HLD)_(hdl)", "High-density_lipoprotein", .)
replace depvar = subinstr(depvar, "Low-density_lipoprotein_(LDL)_(ldl)", "Low-density lipoprotein", .)
replace depvar = subinstr(depvar, "Insulin_(insul)", "Insulin", .)
replace depvar = subinstr(depvar, "Systolic_blood_pressure_(bp_sys)", "Systolic_blood_pressure", .)
replace depvar = subinstr(depvar, "Triglycerides_(trig)", "Triglycerides", .)
replace depvar = subinstr(depvar, "Waist_circumference_(wc)", "Waist_circumference", .)

twoway ///
    (scatter beta age, mcolor(blue) msize(small)) ///
    (rcap uci lci age, lcolor(red) lwidth(thin)), ///
    by(depvar) ///
    title("Effect of IQ on Dependent Variables by Age", size(vsmall)) ///
    xtitle("Age", size(small)) ///
    ytitle("Beta Coefficient", size(small)) ///
    xlabel(9(5)24) ///
    ylabel(, labsize(small)) ///
    yline(0, lcolor(gs12)) ///
    legend(off) ///
    graphregion(color(white))

graph export "output\js_all_data_regress_z_iq8_exposures_plot_by_depvars_combined.png", width(2000) height(1200) replace

