#! /usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt

line_indexes = []
average_loss_1 = []
average_loss_2 = []

line_index = 0
for line in open("m1_result"):
    line = line.strip()
    fields = line.split(',')
    if len(fields) == 2:
        line_indexes.append(line_index)
        average_loss_1.append(float(fields[1]))
        line_index += 1
for line in open("m2_result"):
    line = line.strip()
    fields = line.split(',')
    if len(fields) == 2:
        average_loss_2.append(float(fields[1]))

line_indexes = np.array(line_indexes)
average_loss_1 = np.array(average_loss_1)
average_loss_2 = np.array(average_loss_2)
print len(line_indexes)
print len(average_loss_1)
print len(average_loss_2)

plt.plot(line_indexes, average_loss_1, color='green')
plt.plot(line_indexes, average_loss_2, color='red')
plt.show()

