#! /usr/bin/env sh

echo `date`

./feature_engineer/count.py train.csv > fc.trva.t10.txt

echo `date`

./feature_engineer/parallel_td.py -s 15 ./feature_engineer/transform_data.py train.csv train_trans.csv

echo `date`

python feature_engineer/stat_field_info.py train_trans.csv st_info_file > /dev/null

echo `date`

./feature_engineer/parallel_gs.py -s 15 -m 1 ./feature_engineer/get_samples.py train_trans.csv train_samples_m1

for L2 in 0.1 0.5 3.0
do
    java -jar ftrl_train.jar train_samples_m1 1.0 ${L2} 0.1 1000000 >> m1_result
done

echo `date`

./feature_engineer/parallel_gs.py -s 15 -m 2 ./feature_engineer/get_samples.py train_trans.csv train_samples_m2

for alpha in 0.01 0.05 0.5
do
    java -jar ftrl_train.jar train_samples_m2 1.0 1.0 ${alpha} 1086921 >> m2_result
done

echo `date`

# ./feature_engineer/parallel_gs.py -s 15 -m 3 ./feature_engineer/get_samples.py train_trans.csv train_samples_m3

for alpha in 0.2 0.5 1.0
do
    java -jar ftrl_train.jar train_samples_m3 1.0 0.0 ${alpha} 6086921 >> m3_result
done

echo `date`

