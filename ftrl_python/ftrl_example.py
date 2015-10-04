from ftrl import ftrl_proximal
from sampler import FileSampler
from sklearn.metrics import roc_auc_score
from collections import namedtuple

Config = namedtuple('Config', ['alpha', 'beta', 'L1', 'L2',
    'num_dim', 'train_files', 'test_files'])

def libsvm_file_process(config):
    ftrl = ftrl_proximal(config.alpha, config.beta, config.L1, config.L2, config.num_dim)
    train_pred, train_label = [], []
    for cycle in range(2):
        for train_file in config.train_files:
            for features, label in FileSampler(train_file).generate_samples():
                prob = ftrl.predict(features)
                ftrl.update(features, prob, label)
                train_pred.append(prob)
                train_label.append(1 if label > 0 else 0)
    test_pred, test_label = [], []
    for test_file in config.test_files:
        for features, label in FileSampler(test_file).generate_samples():
            prob = ftrl.predict(features)
            test_pred.append(prob)
            test_label.append(1 if label > 0 else 0)
    return train_pred, train_label, test_pred, test_label, config

alphas = [0.03, 0.1, 0.3]
beta = 1.
L1s = [0.0, 0.1, 0.3]
L2s = [0.0, 0.1, 0.3, 1.0]
num_dim = 123
train_files = ["a9a_train.pls"]
test_files = ["a9a_test.pls"]

configs = []
for alpha in alphas:
    for L1 in L1s:
        for L2 in L2s:
            config = Config(alpha, beta, L1, L2, num_dim, train_files, test_files)
            configs.append(config)

results = []
for config in configs:
    results.append(libsvm_file_process(config))

for result in results:
     print str(result[4].alpha) + "_" + str(result[4].L1) + "_" + str(result[4].L2) + " " + \
             str(roc_auc_score(result[1], result[0])) + " " + str(roc_auc_score(result[3], result[2]))

