#!/bin/bash

# function to read in parse the stata output log files
parse_logs ()
{
  infile=$1
  summary_list=$(egrep "^z_|Number of obs|Adj R-squared|^             z_total_iq_8" ${infile} | egrep -v "^z_total_iq_8|^z_IQ" | sed -e 's/^.*Number/Number/g' -e 's/^.*Adj/Adj/g' -e 's/\|//g' | dos2unix | paste -d' ' - - - -)

  echo " DepVar        Coefficient(95% CI)        P-value      R2        Num-of-obs  Missed-Values"
  echo "---------  ---------------------------    -------    ------      ----------  ------------"
  echo "${summary_list}" | while read i
  do
#    echo "***[$i]***"
#   z_bmi_24,created,with,11672,missing,values,Number,of,obs,=,2893,Adj,R-squared,=,0.0195,z_total_iq_8,-.0852171,.0194055,-4.39,0.000,-.1232672,-.0471671
    z_var_age=$(echo $i | awk '{print $1}')
    var=$(echo $i | awk '{print $1}' | awk -F'_' '{print $2}')
    age=$(echo $i | awk '{print $1}' | awk -F'_' '{print $3}')
    coef=$(echo ${i} | awk '{print $17}')
    lci=$(echo ${i} | awk '{print $21}')
    uci=$(echo ${i} | awk '{print $22}')
    pval=$(echo ${i} | awk '{print $20}')
    adj_r2=$(echo ${i} | awk '{print $15}')
    obs=$(echo ${i} | awk '{print $11}')
    miss=$(echo ${i} | awk '{print $4}')

    form_coef=$(printf '%.4f' "$coef")
    form_lci=$(printf '%.4f' "$lci")
    form_uci=$(printf '%.4f' "$uci")
    form_pval=$(printf '%.4f' "$pval")
    form_adj_r2=$(printf '%.4f' "$adj_r2")
    form_miss=$(printf "%'3d" $miss)

    form_ci=$(printf "%s(%s to %s)" $form_coef $form_lci $form_uci)
    printf "%-10s %-30s %-10s %-10s %8s %12s\n" "$z_var_age" "$form_ci" "$form_pval" "$form_adj_r2" "$obs" "$form_miss"
  done
}

# list of all the log files that will be parsed
#log_list="js_all_data_regress_z_iq8_bmi_age_sex_ses.log"
log_list="js_all_data_regress_z_iq8_bmi_age_sex_ses.log js_all_data_regress_z_iq8_wc_age_sex_ses.log js_all_data_regress_z_iq8_bp_sys_age_sex_ses.log js_all_data_regress_z_iq8_bp_dia_age_sex_ses.log js_all_data_regress_z_iq8_chol_age_sex_ses.log js_all_data_regress_z_iq8_hdl_age_sex_ses.log js_all_data_regress_z_iq8_ldl_age_sex_ses.log js_all_data_regress_z_iq8_trig_age_sex_ses.log js_all_data_regress_z_iq8_glc_meta_age_sex_ses.log js_all_data_regress_z_iq8_insul_age_sex_ses.log"
log_dir="../../stata/log_files"

parse_logs_tmp="parse_logs.tmp"
rm -f ${parse_logs_tmp}

for i in ${log_list}
do
  #echo "[log file = [$i]"
  parse_logs "${log_dir}/$i"  >> ${parse_logs_tmp}
done

# now, fill in the gap that does NOT have any data
for i in 9 10 11 12 13 15 17 24
do
  echo "age: [$i]"
  echo "DepVar,Coefficient(95% CI),P-value,R2,Num-of-obs,Missing-Values"
  for j in bmi wc bp_sys bp_dia chol hdl ldl trig glc_meta insul
  do
    check=$(grep z_${j}_${i} ${parse_logs_tmp})
    if [ "x${check}" = "x" ]
    then
      echo "z_${j}_${i},NO_DATA,NO_DATA,NO_DATA,NO_DATA,NO_DATA"
    else
      echo ${check} | sed -e 's/ to /_to_/g' -e 's/\,//g' -e 's/ /,/g' -e 's/_to_/ to /g'
    fi
  done
  echo
done

#rm -f ${parse_logs_tmp}
