#! /usr/bin/env python
import sys, csv, hashlib, pickle
# sys[1]: mode(1, 2, 3)
# sys[2]: input
# sys[3]: output

mode = sys.argv[1]

# return an integer in [1, nr_bins]
def hashstr(str, nr_bins):
    return int(hashlib.md5(str.encode('utf8')).hexdigest(),
            16) % nr_bins + 1

# return an integer in [start, nr_bins+start-1]
def hashstr2(str, nr_bins, start):
    return int(hashlib.md5(str.encode('utf8')).hexdigest(),
            16) % nr_bins + start

def get_statistical_info(file_name):
    file = open(file_name)
    st_info = pickle.load(file)
    file.close()
    return st_info

def get_st_fields():
    st_fields = []
    for i in range(1,14):
        st_fields.append("I"+str(i))
    for i in range(1,27):
        st_fields.append("C"+str(i))
    return st_fields

# map feature to [1, |features|]
def get_feature_map(st_info):
    feature_map = {}
    index = 1
    for s_field in get_st_fields():
        for s_value in st_info[s_field].iterkeys():
            feature_map[s_value] = index
            index += 1
    return feature_map

def simple_field_pair(st_info):
    s_fields = get_st_fields()
    simple_pairs = []
    for i in range(len(s_fields)):
        for j in range(i+1, len(s_fields)):
            len_i = len(st_info[s_fields[i]])
            len_j = len(st_info[s_fields[j]])
            if len_i * len_j < int(5e6):
                simple_pairs.append((s_fields[i], s_fields[j]))
    return simple_pairs

st_info = get_statistical_info("st_info_file")
st_fields = get_st_fields()
if mode == '2' or mode == '3':
    feature_map = get_feature_map(st_info)
    features_num = len(feature_map)
if mode == '3':
    simple_pairs = simple_field_pair(st_info)

with open(sys.argv[3], 'w') as f:
    for row in csv.DictReader(open(sys.argv[2])):
        feats = []
        if mode == '1':
            # features hash to [1, 1e6]
            for st_field in st_fields:
                feats.append(str(hashstr(row[st_field], int(1e6))))
        elif mode == '2':
            # features map to [1, |features_num|(1086921)]
            for st_field in st_fields:
                feats.append(str(feature_map[row[st_field]]))
        elif mode == '3':
            for st_field in st_fields:
                feats.append(str(feature_map[row[st_field]]))
            for pair in simple_pairs:
                feats.append(str(hashstr2(row[pair[0]] + row[pair[1]], int(5e6), features_num+1)))
        else:
            raise ValueError('wrong mode input')
        f.write(row['Label'] + ' ' + ' '.join(feats) + '\n')

