from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt


# FINISHED
def load_and_center_dataset(filename):
    x = np.load(filename)
    x = x - np.mean(x, 0)
    return x


# FINISHED
def get_covariance(dataset):
    return (1 / (len(dataset) - 1)) * (np.dot(np.transpose(dataset), dataset))


# Finished
def get_eig(S, m):
    w, v = eigh(S, eigvals=(len(S) - m, len(S) - 1))
    w = np.flip(w)
    w = np.diag(w)
    for i in range(len(v)):
        v[i] = np.flip(v[i])
    return w, v


def get_eig_perc(S, perc):
    w, v = eigh(S)
    sum = 0
    for x in w:
        sum += x
    count = 0
    for x in w:
        if x/sum > perc:
            count += 1
    n, m = get_eig(S, count)
    return n, m


def project_image(img, U):
    # projection = np.empty(len(U))
    projection = np.zeros(len(U))
    # for i in range(len(projection)):
    #    projection[i] = 0
    U = np.transpose(U)
    for j in range(len(U)):
        # projection = np.add(projection, np.dot(U[j], img)*U[j])
        projection += np.dot(U[j], img)*U[j]
    return projection


def display_image(orig, proj):
    orig = np.reshape(orig, (32, 32))
    orig = np.transpose(orig)
    proj = np.reshape(proj, (32, 32))
    proj = np.transpose(proj)
    figure, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_title('Original')
    ax2.set_title('Projection')
    c1 = ax1.imshow(orig, aspect='equal')
    figure.colorbar(c1, ax=ax1)
    c2 = ax2.imshow(proj, aspect='equal')
    figure.colorbar(c2, ax=ax2)
    plt.show()
