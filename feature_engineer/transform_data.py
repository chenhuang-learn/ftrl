#! /usr/bin/env python
import csv, sys, math
# sys.argv[1]->threshold
# sys.argv[2]->input
# sys.argv[3]->output

def read_frequent_feats(threshold=10):
    frequent_feats = set()
    for row in csv.DictReader(open('fc.trva.t10.txt')):
        if int(row['Total']) < threshold:
            continue
        frequent_feats.add(row['Field'] + '-' + row['Value'])
    return frequent_feats

frequent_feats = read_frequent_feats(int(sys.argv[1]))

# feat -> I1-, I1-SP1, I1-20, C1-, C1-fb935624, C1-less
def gen_feats(row):
    feats = {}
    feats['Label'] = row['Label']
    for j in range(1,14):
        field = 'I{0}'.format(j)
        value = row[field]
        if value != '':
            value = int(value)
            if value > 2:
                value = int(math.log(float(value)) ** 2)
            else:
                value = 'SP' + str(value)
        key = field + '-' + str(value)
        feats[field] = key
    for j in range(1, 27):
        field = 'C{0}'.format(j)
        value = row[field]
        key = field + '-' + value
        if key not in frequent_feats:
            key = field + '-less'
        feats[field] = key
    return feats

field_names = ['Label']
for i in range(1, 14):
    field = 'I{0}'.format(i)
    field_names.append(field)
for i in range(1, 27):
    field = 'C{0}'.format(i)
    field_names.append(field)

with open(sys.argv[3], 'w') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    if sys.argv[3][-2:] == '.0':
        writer.writeheader()
    for row in csv.DictReader(open(sys.argv[2])):
        feats = gen_feats(row)
        writer.writerow(feats)

