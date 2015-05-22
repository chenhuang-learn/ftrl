#! /usr/bin/env sh

echo `date`

./feature_engineer/count.py train.csv > fc.trva.t10.txt

./feature_engineer/parallel_td.py -s 15 ./feature_engineer/transform_data.py train.csv train_trans.csv

wc -l train.csv train_trans.csv

python feature_engineer/stat_field_info.py train_trans.csv feature_engineer/st_info_file > /dev/null

./feature_engineer/parallel_gs.py -s 15 -m 1 ./feature_engineer/get_samples.py train_trans.csv train_samples_m1

java -jar ftrl_train.jar train_samples_m1 1.0 1.0 0.1 1000000 > m1_result

./feature_engineer/parallel_gs.py -s 15 -m 2 ./feature_engineer/get_samples.py train_trans.csv train_samples_m2

java -jar ftrl_train.jar train_samples_m2 1.0 1.0 0.1 1086921 > m2_result

# ./feature_engineer/parallel_gs.py -s 15 -m 3 ./feature_engineer/get_samples.py train_trans.csv train_samples_m3
# java -jar ftrl_train.jar train_samples_m3 1.0 1.0 0.1 6086921 > m3_result

echo `date`

