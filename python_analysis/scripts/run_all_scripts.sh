#!/bin/bash

# run all the scripts in this directory

./stata_regress_zscore_by_age_by_depvar.sh > ../tables/stata_regress_zscore_by_age_by_depvar.csv
./stata_regress_zscore_by_depvar_by_age.sh > ../tables/stata_regress_zscore_by_depvar_by_age.csv
