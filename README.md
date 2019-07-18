# rl-opt

Generates 2D and 3D plots and animations of the survivor set for a given lexicographic semiorder.

## Lexicographic Semiorder

A lexicographic semiorder compares elements of a Cartesian Product of several sets lexicographically. A element x is said to be smaller than
another element y if there exists an index where x_i is better than y_i by a threshold sigma.

## Survivor Set
The survivor set is sequential generated by eliminating all elements which are not within the threshold of the minimum value of the current projection step. 
Since the data is often streamed sequentially it is necessary to retain data points which are in fact not minimal but can be in the future.

## Plots

The plots and animations display for a given input set which is streamed to the algorithm the current minimal set,
the points which have to be retained and the discarded points.


<table>
<tr>
<td>

![animation](https://user-images.githubusercontent.com/44157083/61469058-d40b6200-a97e-11e9-8e5b-d353fab65fc6.gif)

2D Survivor Set

<td>

![animation](https://user-images.githubusercontent.com/44157083/61469173-04eb9700-a97f-11e9-8db0-36e11d2c8704.gif)

3D Survivor Set

</tr>
</table>

<table>
<tr>
<td>

[heatmapbest.pdf](https://github.com/idsc-frazzoli/rl-opt/files/3407188/heatmapbest.pdf)

Heat best case

<td>

[Master_Thesis_Andre.pdf](https://github.com/idsc-frazzoli/rl-opt/files/3407176/Master_Thesis_Andre.pdf)

3D Survivor Set

<td>

[heatmapworst.pdf](https://github.com/idsc-frazzoli/rl-opt/files/3407194/heatmapworst.pdf)

3D Survivor Set

</tr>
</table>

### Creating the gifs

Once the scripts have be run, the figures will be stored in a separate folder (2Dplots or 3Dplots). Using ImageMagick a gif can be created
from the figure*.png.
Go to the folder location and run (bash not python):
```
$ convert -delay 10 -loop 0 *.png anim.gif
```
