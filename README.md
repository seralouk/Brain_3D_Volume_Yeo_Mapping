# Small toolbox to extract the values of a 3D brain volume for the 7 and 17 Yeo networks

#### Code accompanying the Ph.D. disseration of Serafeim LOUKAS entitled: "Multivariate and predictive models for brain connectivity with application to neurodevelopment".
#### URL: TBA, Thèse n. 8854 (EPFL, 2021)

#### `MapYeo2HCP.m`: Script to bring the several Yeo atlases to our functional space, then mask them using the global GM-mask to ensure fine-grained study-specific coverage

#### `extract_Yeo_values.py`: Main script to extract values from a brain 3D volume for each of the 7 and 17 Yeo networks

#### Dependencies: `numpy`, `seaborn`, `os`, `nibabel` and `matplotlib`

#### Usage: Running `MapYeo2HCP.m ` is optional except if you want to bring the Yeo atlas to a space different than the MNI space. Running `extract_Yeo_values.py ` is the main script. See code for details.

