import os

import numpy as np
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import axes3d

from optimization.mintracker import ExactMinTracker, ApproximateMinTracker


# import data from csv as np.array
def get_data_from_csv():
    """
    Retrieves the input data from the csv files.
    """
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'inputData3D.csv')
    df = pd.read_csv(file_name)
    return df.values


def create_random_points(num: int):
    """
    Generates num random datapoints between 0 and 1
    """
    datavalues = np.random.rand(num, 3)
    return datavalues


def make_plots(discarded_set: np.ndarray, non_minimal_candidates: np.ndarray,
               minimal_set: np.ndarray, step: int, version: str):
    """
    Generates the 3D plots for three sets:
    """
    # set up plot figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Elimination by Objective')
    # Setting the axes properties
    ax.set_xlim3d([0.0, 1.0])
    ax.set_xlabel('X')
    ax.set_ylim3d([0.0, 1.0])
    ax.set_ylabel('Y')
    ax.set_zlim3d([0.0, 1.0])
    ax.set_zlabel('Z')
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Optimal Elements',
                              markerfacecolor='r', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='Candidate Elements',
                              markerfacecolor='b', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='Discarded Elements',
                              markerfacecolor='grey', markersize=10)]

    # generate scatter plots of the data
    if discarded_set is not None:
        ax.scatter(discarded_set[:, 0], discarded_set[:, 1], discarded_set[:, 2],
                   marker=".", color='grey', zorder=1, label='Discarded Elements')

    if non_minimal_candidates.size != 0:
        ax.scatter(non_minimal_candidates[:, 0], non_minimal_candidates[:, 1], non_minimal_candidates[:, 2],
                   marker=".", color='b', zorder=2, label='Candidate Elements')

    ax.scatter(minimal_set[:, 0], minimal_set[:, 1], minimal_set[:, 2],
               marker=".", color='r', zorder=3, label='Minimal Elements')

    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, ncol=3)

    outdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plots', '3Dplots', version)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    file_name = 'figure' + str(step).zfill(4) + '.png'
    file_path = os.path.join(outdir, file_name)

    plt.tight_layout(pad=2)
    plt.savefig(file_path)
    # plt.show()
    plt.close()

    im = Image.open(file_path)

    return im


def main():
    # set up data and slack vector
    dataset = create_random_points(1000)
    # dataset = get_data_from_csv()
    slack = [0.2, 0.2, 0.2]  # slack variable to set by decision maker
    epsilon = [0.01, 0.01, 0.01]

    mintracker_exact = ExactMinTracker(slack)
    mintracker_approximate = ApproximateMinTracker(slack, epsilon)

    images_e = []
    images_a = []

    for i in np.arange(len(dataset)):
        x = np.reshape(dataset[i, :], (1, 3))
        mintracker_exact.update_mintracker_exact(x)
        mintracker_approximate.update_mintracker_approx(x)
        minimals, non_minimal_candidates = mintracker_exact.get_minimals()
        minimals_a, non_minimal_candidates_a = mintracker_approximate.get_minimals()

        im_e = make_plots(mintracker_exact.discarded, non_minimal_candidates, minimals, i, 'exact')
        im_a = make_plots(mintracker_approximate.discarded, non_minimal_candidates_a, minimals_a, i, 'approximate')

        images_a.append(im_a)
        images_e.append(im_e)

    dir_path_e = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plots', '3Dplots', 'exact')
    dir_path_a = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plots', '3Dplots', 'approximate')
    file_name = 'animation.gif'

    images_e[0].save(os.path.join(dir_path_e, file_name),
                     save_all=True,
                     append_images=images_e[1:],
                     duration=400,
                     loop=0)

    images_a[0].save(os.path.join(dir_path_a, file_name),
                     save_all=True,
                     append_images=images_a[1:],
                     duration=400,
                     loop=0)

    print('Exact Solutions:')
    print(mintracker_exact.get_minimals())
    print('Approximate Solutions:')
    print(mintracker_approximate.get_minimals())


if __name__ == "__main__":
    main()
