import sys
results = set()
for line in open(sys.argv[1]):
    line = line.strip()
    fields = line.split()
    for field in fields[1:]:
        results.add(field)
results_list = sorted(results)
print len(results_list)
print results_list


