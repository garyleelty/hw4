import csv
import statistics
import sys
import numpy as np
import math
import random
import pandas as pd


def main():
    data = []
    val = input("input")
    x = val.split()
    k = int(x[0])
    r = int(x[1])
    flag = int(x[2])
    if flag == 1:
        verbose = True
    else:
        verbose = False
    with open(sys.argv[1], mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            temp = [float(row[1]), float(row[2])]
            data.append(temp)
    kMeansWithRandomRestart(k, data, verbose, r)


def kMeansWithRandomRestart(k, data, verbose, r):
    best = 9999
    iteration = 0
    starvation = 0
    clu = []
    cen = []
    for i in range(r):
        clusters, centers, iter, distance = kMeans(k, data, verbose)
        # clustering,numerations
        iteration += iter
        if best > distance:
            clu = clusters
            cen = centers
            best = distance
        if len(clusters) < k:
            starvation += 1
    print('Best clustering found')
    print('KMeans terminates with final clustering')

    for i in range(len(clu)):
        temp = []
        x = clu[i]
        for a in x:
            temp.append(chr(a + 97))
        print('Cluster ', i, ' : ', temp, ' .Center=', cen[i])
    print('Cost=', best)
    print('Average number of iterations: ', iteration/r)
    print('Starvation occurred ', starvation, ' times.')


def random_start(k, n):
    clu = np.arange(n)
    random.shuffle(clu)
    clusters = []
    size = n // k
    for i in range(k):
        if i != k - 1:
            clusters.append(clu[i * size:(i + 1) * size].tolist())
        else:
            clusters.append(clu[i * size:].tolist())
    for a in clusters:
        a.sort()
    return clusters


def kMeans(k, data, verbose):
    n = len(data)
    centers = []
    distance = 0
    clusters = random_start(k, n)
    print(clusters)
    m_data = []
    for i in clusters:
        for point in i:
            m_data.append(data[point])
            # print(m_data)
        centers.append(get_mean(m_data))
    iterations = 0
    # Main loop of kMeans
    repeat = True
    while repeat:
        iterations += 1
        c = []
        for i in range(k):
            c.append([])
        new_center = []
        for i in clusters:
            m_data = []
            for point in i:
                m_data.append(data[point])
            new_center.append(get_mean(m_data))
        distance = get_distance(clusters, new_center, data)
        if verbose:
            verboseReport(clusters, new_center, distance, iterations)
        for j in range(n):
            c[closest_center(new_center, data[j])].append(j)
        emp_new_c = []
        emp_new_cen = []
        #delete the empty clusters
        # print(c)
        for i in range(len(c)):
            if len(c[i]) != 0:
                emp_new_c.append(c[i])
                emp_new_cen.append(new_center[i])
            else:
                pass
        c = emp_new_c
        new_center = emp_new_cen
        if c != clusters:
            pass
        else:
            repeat = False

        clusters = c
        centers = new_center

    return clusters, centers, iterations, distance


def closest_center(center, point):
    center_log = -1
    m_dis = 999
    for a in range(len(center)):
        dis = 0
        for b in range(len(center[a])):
            temp = center[a][b] - point[b]
            dis += temp ** 2
        if m_dis > dis:
            m_dis = dis
            center_log = a
    return center_log

#print the verboseReport
def verboseReport(clusters, centers, distance, iterations):
    for i in range(len(centers)):
        temp = []
        x = clusters[i]
        for a in x:
            temp.append(chr(a + 97))
        print('Cluster ', i, ' : ', temp, ' . Center=', centers[i])
    print('Cost=', distance)
    print(iterations, ' iteration\n')

# get mean of value and return center
def get_mean(data):
    if not data:
        return []
    n = len(data[0])
    center = []
    for a in range(n):
        sum_n = 0
        for b in data:
            sum_n += b[a]
        center.append(sum_n / len(data))
    return center

# use Euclidean distances squared
def get_distance(clusters, center, data):
    distance = 0
    for i in range(len(center)):
        dist = 0
        for a in range(len(clusters[i])):
            for b in range(len(center[i])):
                dist += (center[i][b] - data[clusters[i][a]][b]) ** 2
        distance += dist
    return distance


if __name__ == "__main__":
    main()
