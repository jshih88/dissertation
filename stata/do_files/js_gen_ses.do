di "=== Generating ses ==="

// Generate SES as the highest social class (lowest numerical value) between mother and father
gen ses = min(mother_soc, father_soc)

// If one parent's value is missing, use the other parent's value
replace ses = mother_soc if missing(father_soc) & !missing(mother_soc)
replace ses = father_soc if missing(mother_soc) & !missing(father_soc)

// Label the SES variable
label define ses_label 1 "I Professional" 2 "II Managerial/Technical" 3 "IIINM Skilled Non-Manual" ///
    4 "IIIM Skilled Manual" 5 "IV Partly Skilled" 6 "V Unskilled" 65 "Armed Forces", replace
label values ses ses_label

//di "--- Count Before dropping missing ses ---"
//count
// Optionally, drop observations with missing SES
//drop if missing(ses)
//count

// Check the distribution of the new SES variable
tab ses, missing

