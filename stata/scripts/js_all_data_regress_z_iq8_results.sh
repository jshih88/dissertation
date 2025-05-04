#!/bin/bash

echo "iq,depvar,age,beta,lci,uci"

log_list="js_all_data_regress_z_iq8_bmi_age_sex_ses.log js_all_data_regress_z_iq8_wc_age_sex_ses.log js_all_data_regress_z_iq8_bp_sys_age_sex_ses.log js_all_data_regress_z_iq8_bp_dia_age_sex_ses.log js_all_data_regress_z_iq8_chol_age_sex_ses.log js_all_data_regress_z_iq8_hdl_age_sex_ses.log js_all_data_regress_z_iq8_ldl_age_sex_ses.log js_all_data_regress_z_iq8_trig_age_sex_ses.log js_all_data_regress_z_iq8_glc_meta_age_sex_ses.log js_all_data_regress_z_iq8_insul_age_sex_ses.log"
log_dir="../log_files"

for i in ${log_list}
do
  grep "Regression results summary" "${log_dir}/$i" | awk '{print $5","$8","$11","$14","$17","$20}' | dos2unix
done
