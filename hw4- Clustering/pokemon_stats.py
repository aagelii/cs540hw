import csv
import numpy as np
import matplotlib.pyplot as plt
import math


def load_data(filepath):
    pokemons = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            del row['Legendary']
            del row['Generation']
            row['#'] = int(row['#'])
            row['HP'] = int(row['HP'])
            row['Total'] = int(row['Total'])
            row['Attack'] = int(row['Attack'])
            row['Defense'] = int(row['Defense'])
            row['Sp. Atk'] = int(row['Sp. Atk'])
            row['Sp. Def'] = int(row['Sp. Def'])
            row['Speed'] = int(row['Speed'])
            if count >= 20:
                break
            count += 1
            pokemons.append(row)
    return pokemons


def calculate_x_y(stats):
    return stats["Attack"] + stats["Sp. Atk"] + stats["Speed"], stats['HP'] + stats["Sp. Def"] + stats["Defense"]


def hac(dataset):
    newDataset = []
    count = 0
    for i in dataset:
        if np.isnan(i[0]) or np.isnan(i[1]) or np.isinf(i[0]) or np.isinf(i[1]):
            continue
        else:
            newDataset.append([i[0], i[1], count])
            count += 1
    Z = []
    x = 0
    y = 0
    nextIndex = len(newDataset)
    for i in range(len(newDataset) - 1):
        minDist = math.inf
        for j in range(len(newDataset)):
            for k in range(j, len(newDataset)):
                if newDataset[j][2] == newDataset[k][2]:
                    continue
                else:
                    distance = math.sqrt(
                        ((newDataset[j][0] - newDataset[k][0]) ** 2) + ((newDataset[j][1] - newDataset[k][1]) ** 2))
                    if minDist > distance:
                        minDist = distance
                        x = j
                        y = k
        a = newDataset[x][2]
        b = newDataset[y][2]
        c = 0
        for m in range(len(newDataset)):
            if newDataset[m][2] == a or newDataset[m][2] == b:
                newDataset[m][2] = nextIndex
                c += 1
        if a < b:
            Z.append([a, b, minDist, c])
        else:
            Z.append([b, a, minDist, c])
        nextIndex += 1
    Z = np.matrix(Z)
    return Z


def random_x_y(m):
    dataset = []
    for i in range(m):
        dataset.append([np.random.randint(1, 360), np.random.randint(1, 360)])
    return dataset


def imshow_hac(dataset):
    figure = plt.figure()
    for i in range(len(dataset)):
        plt.scatter(dataset[i][0], dataset[i][1])
        plt.plot()
    newDataset = []
    count = 0
    for i in dataset:
        if np.isnan(i[0]) or np.isnan(i[1]) or np.isinf(i[0]) or np.isinf(i[1]):
            continue
        else:
            newDataset.append([i[0], i[1], count])
            count += 1
    Z = []
    x = 0
    y = 0
    nextIndex = len(newDataset)
    for i in range(len(newDataset) - 1):
        minDist = math.inf
        for j in range(len(newDataset)):
            for k in range(j + 1, len(newDataset)):
                if newDataset[j][2] == newDataset[k][2]:
                    continue
                else:
                    distance = math.sqrt(
                        ((newDataset[j][0] - newDataset[k][0]) ** 2) + ((newDataset[j][1] - newDataset[k][1]) ** 2))
                    if minDist > distance:
                        minDist = distance
                        x = j
                        y = k
        a = newDataset[x][2]
        b = newDataset[y][2]
        c = 0
        for m in range(len(newDataset)):
            if newDataset[m][2] == a or newDataset[m][2] == b:
                newDataset[m][2] = nextIndex
                c += 1
        if a < b:
            Z.append([a, b, minDist, c])
            plt.plot([newDataset[x][0], newDataset[y][0]], [newDataset[x][1], newDataset[y][1]])
        else:
            Z.append([b, a, minDist, c])
            plt.plot([newDataset[y][0], newDataset[x][0]], [newDataset[y][1], newDataset[x][1]])
        nextIndex += 1
        plt.pause(.1)
    plt.show()

