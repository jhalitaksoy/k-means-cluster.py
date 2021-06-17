import random
import math
import sys

import matplotlib.pyplot as plt
import numpy as np

import os, shutil


class Point :
    x = 0
    y = 0
    cluster = -1
    def __init__(self, x, y, cluster = -1):
        self.x = x
        self.y = y
        self.cluster = cluster
    
    def __repr__(self):
          return "X:%.2f, Y:%.2f, Cluster:%d" % (self.x, self.y, self.cluster)
    
    def __str__(self):
         return "X:%.2f, Y:%.2f, Cluster:%d" % (self.x, self.y, self.cluster)

def sumPoint(point1, point2) : 
    x1 = point1.x
    y1 = point1.y

    x2 = point2.x
    y2 = point2.y

    return Point(x1 + x2, y1 + y2)

def distance(point1, point2):
    x1 = point1.x
    y1 = point1.y

    x2 = point2.x
    y2 = point2.y

    return math.sqrt(pow((x1 - x2),2) + pow((y1 - y2),2))

def safeDivision(value, divison):
    if value == 0 :
        return 0
    else : 
        return value / divison
    
logs = ""

def log(msg):
    global logs
    print(msg)
    logs += str(msg) + "\n" 

def clearOutputs() : 
    folder = 'output' 
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            log('Failed to delete %s. Reason: %s' % (file_path, e))    

def saveState(iterasyon, points, centers, colors, showPointCluster = True) : 
    ypoints = np.array([3, 8, 1, 10])

    padding = 0.2

    for point in points: 
        plt.plot(point.x, point.y, marker='o', markersize=5, color=colors[point.cluster])
        #if showPointCluster : plt.text(point.x + padding, point.y + padding, str(point.cluster))

    for i, point in enumerate(centers): 
        plt.plot(point.x, point.y, marker='h', markersize=5, color=colors[i])
        plt.text(point.x + padding, point.y + padding , str(i))
    
    plt.title(str(iterasyon) + ". Iteration")
    plt.savefig('output/' + str(iterasyon) + '.png')
    plt.clf()

def randomColor():
    r = random.random()
    b = random.random()
    g = random.random()

    color = (r, g, b)
    return color

def calculate(dataset, k, max_iteration = 10):
    global logs
    logs = ""

    points = [Point(x, y, -1) for (x, y) in dataset]
    centers = random.sample(points, k)

    colors = [randomColor() for i in range(k)]

    #iteration count
    i = 0
    item_moved = True

    clearOutputs()

    log("Starting...")
    log("Cluster size = " + str(k))
    log("Max Iteration = " + str(max_iteration))
    log("########################################################")
    log("Iteration " + str(i) + " (Initial State)")
    log("Points : ")
    log(points)
    log("Random Centers : ")
    log(centers)
    saveState(i, points, centers, colors, showPointCluster=False)

    i += 1

    while i < max_iteration and item_moved :
        item_moved = False
        log("########################################################")
        log("Iteration " + str(i))

        # calculate distance from center points for each element 
        # and select cluster
        for point in points :
            clusterIndex = -1
            j = 0
            prevDistance = sys.maxsize
            prevCluster = point.cluster
            for centerPoint in centers :
                current_distance = distance(centerPoint, point)
                if current_distance < prevDistance :
                    prevDistance = current_distance
                    point.cluster = j
                j += 1
            if not item_moved : 
                item_moved = point.cluster != prevCluster
                #if item_moved : log("İtem Moved")
        # update center points
        for cluster in range(k):
            size = 0
            sum_of_x = 0
            sum_of_y = 0
            for point in points :
                if point.cluster == cluster : 
                    size = size + 1 
                    sum_of_x = sum_of_x + point.x
                    sum_of_y = sum_of_y + point.y
            centers[cluster] = Point(safeDivision(sum_of_x, size), safeDivision(sum_of_y, size))

        log("Points : ")
        log(points)
        log("New Centers : ")
        log(centers)
        saveState(i, points, centers, colors)
        i += 1
    f = open("output/logs.txt", "w")
    f.write(logs)
    f.close()
