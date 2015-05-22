# an example, run ftrl on criteo dataset

## Get The Dataset

refer to: https://github.com/guestwalk/kaggle-2014-criteo/blob/master/README, 'Get The Dataset' part.

## Run main_script.sh

1. transform data
./feature_engineer/count.py train.csv > fc.trva.t10.txt
./feature_engineer/parallel_td.py -s 15 ./feature_engineer/transform_data.py train.csv train_trans.csv
features(I1-I13) greater than 2 are transformed by: int(log(v^2))->v
features(C1-C26) appear less than 10 times are transformed to a special value

2. generate samples


3. train ftrl model and progress validation
