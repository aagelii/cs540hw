import numpy as np

import pca
x = pca.load_and_center_dataset("YaleB_32x32.npy")
S = pca.get_covariance(x)
Lambda, U = pca.get_eig(S, 2)
projection = pca.project_image(x[0], U)
pca.display_image(x[0], projection)
# Lambda, U = pca.get_eig_perc(S, 0.04)
# Lambda, U = pca.get_eig_perc(S, 0.07)
# projection = pca.project_image(x[0], U)
# projection = pca.project_image(x[1], U)
