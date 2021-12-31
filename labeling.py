import sys
import math
import random

# Usage: python program.py infile partition_degree logfunc-const1 logfunc-exp1 powfunc-const1 powfunc-exp1 num_label> outfile

# return y = const * ln( degree ) + exponent


def logfunction(constant, exponent, degree):
    return constant * math.log(degree) + exponent

# return y = const * (degree^exponent)


def powerfunction(constant, exponent, degree):
    return constant * pow(degree, exponent)

# return random number on distribution y = const * (x^exponent)


def random_powerfunction(constant, exponent, num_label):
    prob = {}
    for i in range(num_label+1):
        if i == 0:
            prob[i] = 0
            continue
        prob[i] = prob[i-1] + constant * pow(i, exponent)
#               print(str(i) +' '+ str(exponent)+' ' + str(constant) + ' ' +str(pow(i,exponent)) + ' ' + str(constant*pow(i,exponent)))

    r = random.random() * prob[num_label]

    index = -1
    for i in range(1, num_label+1):
        if r <= prob[i]:
            index = i
            break

    return index


def assign_vertex_label():
    # 2. For each vertex whoes degree <= partition_degree, we set label following the predefined label distribution given vertex degree.
    # : apply logfunc1 and powfunc1 for degrees <= partition_degree.

    for vertex in degree:
        # assign label using log and power function
        if degree[vertex] <= partition_degree:
            exponent = logfunction(
                logfunc_const1, logfunc_exp1, degree[vertex])
            constant = powerfunction(
                powfunc_const1, powfunc_exp1, degree[vertex])
            # print(exponent)
            exponent = -exponent
            # modify exponent by scale. Note that if scale=1, exponent does not change.
            exponent = exponent * \
                math.log(constant) / (math.log(constant) +
                                      exponent * math.log(scale))
            exponent = -exponent
            #print('changed: ' + str(exponent))
            #print('constant: ' + str(constant) + '\t\texponent: ' + str(exponent))
            label = random_powerfunction(constant, exponent, num_label)
            vertex_label[vertex] = label

    # 2.5. In order to graph contain predefined number of labels,
    # Replace the label of vertex having most frequent label to one of the unpresent label.
    # current label statistics
    label_stat = {}
    for vertex in degree:
        if degree[vertex] <= partition_degree:
            label = vertex_label[vertex]
            if label not in label_stat:
                label_stat[label] = 0
            label_stat[label] += 1

    # find out missing label
    is_exist = []
    for i in range(0, num_label+1):
        is_exist.append(False)
    for l in label_stat:
        is_exist[l] = True
    not_exist = []
    for i in range(1, num_label+1):
        if is_exist[i] == False:
            not_exist.append(i)

    # find out most frequent label
    most_frequent_label = -1
    most_frequent = 0
    for l in label_stat:
        if label_stat[l] > most_frequent:
            most_frequent = label_stat[l]
            most_frequent_label = l

    # adjusting by replace
    for vertex in degree:
        if len(not_exist) == 0:
            break

        if degree[vertex] <= partition_degree:
            if vertex_label[vertex] == most_frequent_label:
                vertex_label[vertex] = not_exist[0]
                del not_exist[0]

    # check error
    if len(not_exist) != 0:
        print('ERROR')

    # 3. For each vertex whoes degree > partition_degree, we set label following the neighbor's power law distribution
    # (neighbor should be the random sample of a power law distribution)
    # increasing order of degree
    for vertex, d in sorted(degree.iteritems(), key=lambda (k, v): (v, k)):
        #print(str(vertex) +'\t' +  str(d))
        # assign label using neighbor power law distribution
        if degree[vertex] > partition_degree:

            # labeled_neighbor
            neighbor_label = []
            for neighbor in edge[vertex]:
                if neighbor in vertex_label:
                    neighbor_label.append(vertex_label[neighbor])

            if len(neighbor_label) != 0:
                # randomly select one labeled neighbor
                r = random.randrange(0, len(neighbor_label))
                vertex_label[vertex] = neighbor_label[r]

            if len(neighbor_label) == 0:
                # print('exception')
                exponent = logfunction(
                    logfunc_const1, logfunc_exp1, degree[vertex])
                constant = powerfunction(
                    powfunc_const1, powfunc_exp1, degree[vertex])
                exponent = -exponent
                # modify exponent by scale. Note that if scale=1, exponent does not change.
                exponent = exponent * \
                    math.log(constant) / (math.log(constant) +
                                          exponent * math.log(scale))
                exponent = -exponent
                label = random_powerfunction(constant, exponent, num_label)
                vertex_label[vertex] = label

# return true if #labels is correct


def check_num_label():
    label_dic = {}
    for v in vertex_label:
        if vertex_label[v] not in label_dic:
            label_dic[vertex_label[v]] = 1
    #print('check_num_label(): ' + str(len(label_dic)))
    if len(label_dic) != num_label:
        return False
    return True

# main


if len(sys.argv) != 9:
    print('Usage: python program.py infile partition_degree logfunc-const1 logfunc-exp1 powfunc-const1 powfunc-exp1 num_label scale > outfile')
    sys.exit()

filename = str(sys.argv[1])

partition_degree = int(sys.argv[2])
logfunc_const1 = float(sys.argv[3])
logfunc_exp1 = float(sys.argv[4])
powfunc_const1 = float(sys.argv[5])
powfunc_exp1 = float(sys.argv[6])
num_label = int(sys.argv[7])
scale = float(sys.argv[8])

infile = open(filename, 'r')
# 1. read input graph and store degree for each vertex
# rename vertex id in increasing order from 0
degree = {}
vertex_name = {}
name_index = 0
edge = {}
while True:
    line = infile.readline()
    if not line:
        break

    args = line.split()

    left = int(args[0])
    right = int(args[1])

    if left not in vertex_name:
        vertex_name[left] = name_index
        name_index += 1
    if right not in vertex_name:
        vertex_name[right] = name_index
        name_index += 1

    # degree
    if vertex_name[left] not in degree:
        degree[vertex_name[left]] = 0
    if vertex_name[right] not in degree:
        degree[vertex_name[right]] = 0

    degree[vertex_name[left]] += 1
    degree[vertex_name[right]] += 1

    # edge
    if vertex_name[left] not in edge:
        edge[vertex_name[left]] = []
    if vertex_name[right] not in edge:
        edge[vertex_name[right]] = []

    edge[vertex_name[left]].append(vertex_name[right])
    edge[vertex_name[right]].append(vertex_name[left])

infile.close()


vertex_label = {}
assign_vertex_label()
is_correct = check_num_label()
while is_correct == False:
    assign_vertex_label()
    is_correct = check_num_label()


# 4. After we set label, print vertex with label in increasing order of vertex id
# e.g., v 0 1
# print edge with default label 0
# e.g., e 0 1 0
# Note that we have to print t 1 #vertices first before printing vertices.

print('t 1 ' + str(len(degree)))

# vertex
for vertex in sorted(degree.keys()):
    print('v ' + str(vertex) + ' ' + str(vertex_label[vertex]))

# edge
for left in sorted(edge.keys()):
    for right in sorted(edge[left]):
        if left < right:
            print('e ' + str(left) + ' ' + str(right) + ' 0')
