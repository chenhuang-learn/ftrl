import sys, pickle
from csv import DictReader

path = sys.argv[1]
st_info_path = sys.argv[2]

# set statistical_fields and label_field
statistical_fields = ['I1', 'I2', 'I3', 'I4', 'I5', 'I6',
        'I7', 'I8', 'I9', 'I10', 'I11', 'I12', 'I13',
        'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
        'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15',
        'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22',
        'C23', 'C24', 'C25', 'C26']
label_field = 'Label'

# statistic something to statistical_info
statistical_info = {}
for s_field in statistical_fields:
    statistical_info[s_field] = {}

for t, row in enumerate(DictReader(open(path))):
    for s_field in statistical_fields:

        s_value = row[s_field]
        if s_value not in statistical_info[s_field]:
            statistical_info[s_field][s_value] = {'1':0, '0':0}

        y = 0
        if label_field in row:
            if row[label_field] == '1' or row[label_field] == '+1':
                y = 1

        if y == 1:
            statistical_info[s_field][s_value]['1'] += 1
        else:
            statistical_info[s_field][s_value]['0'] += 1

st_info_file = open(st_info_path, 'wb')
pickle.dump(statistical_info, st_info_file)
st_info_file.close()

# print statistical_info
statistical_info_list = sorted(statistical_info.iteritems(), key=lambda x:x[0])
for s_field, s_values in statistical_info_list:
    print "field name: %s, values num: %d" % (
            s_field, len(s_values))
    s_values_list = sorted(s_values.iteritems(), key=lambda x:x[0])
    for s_value, info in s_values_list:
        pos = info['1']
        neg = info['0']
        print "\t%s, total: %d, pos: %d, neg: %d, ratio: %.3f" % (
                s_value, pos+neg, pos, neg, float(pos)/(pos+neg))

