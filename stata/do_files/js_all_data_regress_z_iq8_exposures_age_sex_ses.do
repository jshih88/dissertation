// 1. Set Up Environment
capture mkdir output
set more off
tempname memhold
tempfile results

// 2. Load Data & Preprocess Once
include "S:\ICS_Student_Projects\2024-25\Jocelyn\Do Files\js_template.do"
//do "S:\ICS_Student_Projects\2024-25\Jocelyn\Do Files\js_no_missing_data_iq8.do"
//do "S:\ICS_Student_Projects\2024-25\Jocelyn\Do Files\js_no_missing_data_bmi.do"
do "S:\ICS_Student_Projects\2024-25\Jocelyn\Do Files\js_gen_ses.do"

local exposure_vars bmi wc bp_sys bp_dia chol hdl ldl trig glc_meta insul
//local exposure_vars bmi

// looking at iq at 8
local iq_vars 8

foreach vexpo of local exposure_vars {
	local label_text = `vexpo'_label[1]

	foreach viq of local iq_vars {
		preserve
		tempfile results     // Define temporary file for results
		tempname memhold     // Define temporary postfile handle

		// Initialize postfile with the temporary file
		postfile `memhold' age beta lci uci using "`results'", replace

		// Start log (ensure directory exists)
		capture mkdir "output"
		capture log close
		log using "output/js_all_data_regress_z_iq8_`vexpo'_age_sex_ses.log", replace

		// *** Standardize the exposure (IQ) ***
        zscore total_iq_`viq'

		foreach vage of local `vexpo'_age_vars {
			// Checks if the specified variable exists in the dataset.
			capture confirm variable `vexpo'_`vage'
			zscore `vexpo'_`vage'

			//list orig_obs_id `vexpo'_`vage' z_`vexpo'_`vage' age_`vage' i.sex i.ses
			di "==============================================================================="
			di "Regression on: [regress z_`vexpo'_`vage' z_total_iq_`viq' age_`vage' i.sex i.ses]"
			di "==============================================================================="
			regress z_`vexpo'_`vage' z_total_iq_`viq' age_`vage' i.sex i.ses
			matrix results = r(table)

			// content of matrix
			// Row	Statistic	Example Label
			// 1	Coefficient (beta)	b
			// 2	Standard error	se
			// 3	t-statistic	t
			// 4	p-value	p
			// 5	Lower bound of 95% confidence interval	ll (CI lower)
			// 6	Upper bound of 95% confidence interval	ul (CI upper)

			//matrix list results
			di "==========================="
			di "Regression results:"
			di "z_IQ at: " `viq'
			di "Exposure: " "`label_text' (`vexpo')"
			di "Age: " `vage'
			di "IQ Coefficient: " results[1,1]
			di "IQ 95% CI Lower: " results[5,1]
			di "IQ 95% CI Upper: " results[6,1]
			di "Regression results summary:", "z_IQ_at: " `viq', ", Exposure: " "`label_text'_(`vexpo')", ", Age: " `vage', ", IQ_Coefficient: " results[1,1], ", IQ_95%_CI_Lower: " results[5,1], ", IQ_95%_CI_Upper: " results[6,1]
			di "==========================="
			post `memhold' (`vage') (results[1,1]) (results[5,1]) (results[6,1])
		}

		postclose `memhold'
		use "`results'", clear  // Load the temporary file

		gen id = _n

		local i 1
		foreach vage of local `vexpo'_age_vars {
			label define age_label_`vexpo' `i' "`vage'", add
			local ++i
		}
		label values id age_label_`vexpo'

		twoway ///
			(scatter id beta, msymbol(D) mcolor(navy)) ///
			(rcap lci uci id, horizontal lcolor(maroon)), ///
			ylabel(1(1)`=`i'-1', valuelabel angle(0) labsize(small)) ///
			ytitle("Age") ///
			xtitle("Regression Coefficient (95% CI)") ///
			title("Combined Association: [Childhood z_IQ at `viq'] and [`label_text'] Across Ages with ALL data", size(medium) span) ///
			subtitle("Adjusted for Age, Sex and SES", size(small)) ///
			legend(off) ///
			xline(0, lpattern(dash) lcolor(black)) ///
			xscale(range(-0.02 0.01)) ///
			xlabel(-0.02(0.005)0.01, format(%4.3f)) ///
			plotregion(color(white)) graphregion(color(white))

		graph export "output/js_all_data_regress_z_iq8_`vexpo'_age_sex_ses.png", width(2000) height(1200) replace

		log close
		restore
	}
}
