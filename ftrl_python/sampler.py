#! /usr/bin/env python
import sys
import time

def libsvm_line2feature(line):
    feature_indexes = []
    feature_values = []
    line = line.strip()
    fields = line.split()
    if float(fields[0]) > 0:
        label = 1.0
    else:
        label = -1.0
    for field in fields[1:]:
        subFields = field.split(':')
        feature_indexes.append(int(subFields[0]))
        feature_values.append(float(subFields[1]))
    return (zip(feature_indexes, feature_values), label)

class FileSampler(object):
    def __init__(self, file_name):
        self._file_name = file_name

    def generate_samples(self, num_samples = -1):
        samples = 0
        for line in open(self._file_name):
            samples += 1
            if samples % 1000000 == 0:
                print samples, time.localtime()
                sys.stdout.flush()
            if num_samples != -1 and samples > num_samples:
                break
            yield libsvm_line2feature(line)

if __name__ == "__main__":
    sampler = FileSampler(sys.argv[1])
    for sample in sampler.generate_samples(2):
        print sample

