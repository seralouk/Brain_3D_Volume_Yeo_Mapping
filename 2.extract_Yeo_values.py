# -------------------------------------------------------
#
#    Main script to extract values from a brain 3D volume
#    for each of the 7 and 17 Yeo networks
#
#    Created by:         Serafeim Loukas 
#    Last checked:       11.03.2020
#
#    Some resources:
# 		http://ftp.nmr.mgh.harvard.edu/pub/dist/freesurfer/tutorial_packages/OSX/freesurfer/average/Yeo_JNeurophysiol11_MNI152/
# 		https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal
# ------------------------------------------------------

import nibabel as nib, matplotlib.pyplot as plt
import numpy as np, os, seaborn as sns
from matplotlib.colors import ListedColormap


#* where to save figs
save_fig_to = './results/'

#* Global variables
show_outliers = False

# Path to the 3D brain volume
eigenmode_map = './Data/stat_map.nii'

#* Load the brain signal at the voxel level
eigenmode_map_ = nib.load(eigenmode_map)
eigenmode_map_data = np.array(eigenmode_map_.get_fdata())

#* Ordered Yeo names from: 
# https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal
names_7_nets = ['Visual', 'Somatomotor', 'Dorsal Attention', 
				'Ventral Attention', 'Limbic', 'Frontoparietal',
				'Default']

#* Ordered Yeo names from: 
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4364170/ (Fig. 1)
names_17_nets = ['Visual A', 'Visual B', 'Somatomotor A', 'Somatomotor B', 
				 'Dorsal Attention A','Dorsal Attention B',   
				 'VenAttn', 'Salience', 'Limbic A (temp)', 'Limbic B (OFC)',
				 'Control C', 'Control A', 'Control B', 'Default D (Aud)', 'Default C',
				 'Default A', 'Default B']


#* Load the Yeo atlas (masked and resliced to the same functional space as the 'cosine_dist_map')
path_to_final_yeo = './results/'

#* Choose liberal OR fine Yeo parcellation
yeo_files = [f for f in os.listdir(path_to_final_yeo) if f.startswith("masked_resliced_libe")]
yeo_files = sorted(yeo_files)
print(yeo_files)

#* load the 17 net file
yeo_17_nets = nib.load(path_to_final_yeo + [f for f in yeo_files if f.endswith("_yeo_17.nii")][0])
print(yeo_17_nets.get_filename())
yeo_17_nets_data = np.array(yeo_17_nets.get_fdata())
yeo_17_nets_data[yeo_17_nets_data<0] = 0

#* load the 7 net file
yeo_7_nets = nib.load(path_to_final_yeo + [f for f in yeo_files if f.endswith("_yeo_7.nii")][0])
print(yeo_7_nets.get_filename())
yeo_7_nets_data = np.array(yeo_7_nets.get_fdata())
yeo_7_nets_data[yeo_7_nets_data<0] = 0

#* flatten and extract average per network values
flat_dims = np.prod(eigenmode_map_data.shape)
eigenmode_map_data_flat = np.reshape(eigenmode_map_data, [1,flat_dims])

yeo_17_nets_data_flat = np.reshape(yeo_17_nets_data, [1,flat_dims])
assert(np.unique(yeo_17_nets_data_flat).shape[0]==18)

yeo_7_nets_data_flat = np.reshape(yeo_7_nets_data, [1,flat_dims])
assert(np.unique(yeo_7_nets_data_flat).shape[0]==8)

#* extract average per network values for the case of 7 networks
n_nets = np.unique(yeo_7_nets_data_flat).shape[0]
#average_vals = np.zeros((n_nets-1))

results_7_nets = list()
for net in range(1,n_nets): # 0 is not a net
	results_7_nets.append(eigenmode_map_data_flat[yeo_7_nets_data_flat==net])
	#average_vals[net-1] = eigenmode_map_data_flat[yeo_7_nets_data_flat==net].mean()


# Order networks based on the mean value of the underlying values of the brain map file
idx_sorting = np.array([i.mean() for i in results_7_nets]).argsort() # this is only the sorting index

# Sort networks and names for nice plotting
results_7_nets_ordered = [results_7_nets[i] for i in idx_sorting]
names_7_nets_ordered = [names_7_nets[i] for i in idx_sorting]

# Make custome colormap to match Yeo's colors as in the publication
cols7 = ((255,255,255),
         (120,  18, 134),
         (70 ,130, 180),
         ( 0 ,118 , 14),
         (196 , 58 ,250),
         (220 ,248 ,164),
         (230, 148,  34),
         (205 , 62,  78 ))
cols = np.asarray(cols7, dtype=float)/255.
yeoCols = ListedColormap(cols,name='colormapYeo')

# sort correctly the colors
colors_list = []
for i in range(0,len(idx_sorting)):
    colors_list.append(cols[idx_sorting[i] + 1])

# use this palette
sns.set_palette(colors_list)

# The boxplots
fig, axes = plt.subplots(1,1,figsize=(12,10))
ax = sns.boxplot(data=results_7_nets_ordered, linewidth=3,showmeans=True, orient='h',
				meanprops={"marker":"*","markerfacecolor":"white", "markeredgecolor":"blue"}, width=0.6, showfliers = show_outliers)
# Select which box you want to change    
#mybox = ax.artists[-1]
#mybox.set_facecolor('royalblue')
#*set edge color = black
for b in range(len(ax.artists)):
	ax.artists[b].set_edgecolor('black')
#axes.set_ylim([-2,2])
axes.set_yticklabels(names_7_nets_ordered)
axes.set_xlabel("3D brain map values", size= 16)
axes.set_ylabel("Yeo functional networks", labelpad=15, size= 16)
plt.title("Volume values for the Yeo 7 functional networks", size= 18)
plt.xticks(fontsize= 10) 
plt.yticks(fontsize= 10) 
plt.grid(alpha=0.4)
plt.savefig(save_fig_to + 'Yeo_7_nets.png', bbox_inches='tight', pan_inches=0.5, dpi=300)
#plt.show()


# #* Build table
# stats_df = pd.DataFrame(columns=['Network ID', 'Network name','Mean','Median'])
# for net_ in range(len(results_7_nets)):
# 	naming = names_7_nets[net_]
# 	tmp_mean = np.mean(results_7_nets[net_])
# 	tmp_median = np.median(results_7_nets[net_])
# 	stats_df.loc[net_,:] = [net_+1, naming, tmp_mean, tmp_median]

# stats_df.to_csv(save_fig_to + "Global_map_7_net_stats_{}.csv".format(case), index=0)


##################################################################################
##################################################################################
######################         17 networks            ############################
##################################################################################
##################################################################################

#* extract average per network values for the case of 17 networks
n_nets = np.unique(yeo_17_nets_data_flat).shape[0]
#average_vals = np.zeros((n_nets-1))

results_17_nets = list()
for net in range(1,n_nets): # 0 is not a net
	results_17_nets.append(eigenmode_map_data_flat[yeo_17_nets_data_flat==net])

# plots
idx_sorting_17 = np.array([i.mean() for i in results_17_nets]).argsort()
results_17_nets_ordered = [results_17_nets[i] for i in idx_sorting_17]
names_17_nets_ordered = [names_17_nets[i] for i in idx_sorting_17]

# Make custome colormap to match Yeo's colors as in the publication
cols17 =((255,255,255),
        (120,  18, 134 ),
        (255,   0,   0 ),
        (70 ,130, 180  ),
        (42, 204, 164  ),
        (74 ,155 , 60  ),
        (0 ,118,  14  ),
        (196 , 58, 250 ),
        (255 ,152, 213 ),
        (220 ,248, 164 ),
        (122, 135 , 50 ),
        (119 ,140 ,176 ),
        (230 ,148,  34 ),
        (135,  50 , 74 ),
        (12  ,48, 255  ),
        (0 ,  0, 130  ),
        (255, 255,   0 ),
        (205 , 62 , 78 ))
cols = np.asarray(cols17, dtype=np.float)/255.
yeoCols = ListedColormap(cols,name='colormapYeo17')

# sort correctly the colors
colors_list = []
for i in range(0,len(idx_sorting_17)):
    colors_list.append(cols[idx_sorting_17[i] + 1])

# use this palette
sns.set_palette(colors_list)

# The boxplots
fig, axes = plt.subplots(1,1,figsize=(16,10))
ax = sns.boxplot(data=results_17_nets_ordered, linewidth=3, showmeans=True, orient='h',
				meanprops={"marker":"*","markerfacecolor":"white", "markeredgecolor":"blue"}, width=0.6, showfliers = show_outliers)
# Select which box you want to change    
#mybox = ax.artists[-1]
# Change the appearance of that box
#mybox.set_facecolor('royalblue')
#*set edge color = black
for b in range(len(ax.artists)):
	ax.artists[b].set_edgecolor('black')
axes.set_yticklabels(names_17_nets_ordered, rotation=30)
axes.set_xlabel("3D brain map values", size= 16)
axes.set_ylabel("Yeo functional networks", labelpad=15, size= 16)
plt.xticks(fontsize= 10) 
plt.yticks(fontsize= 10) 
plt.title("Volume values for the Yeo 17 functional networks", size= 18)
plt.grid(alpha=0.4)
plt.savefig(save_fig_to + 'Yeo_17_nets.png', bbox_inches='tight', pan_inches=0.5, dpi=300)
#plt.show()

# #* Build table
# stats_df = pd.DataFrame(columns=['Network ID', 'Network name','Mean','Median'])
# for net_ in range(len(results_17_nets)):
# 	naming = names_17_nets[net_]
# 	tmp_mean = np.mean(results_17_nets[net_])
# 	tmp_median = np.median(results_17_nets[net_])
# 	#tmp_std = np.std(results_17_nets[net_])
# 	stats_df.loc[net_,:] = [net_+1, naming, tmp_mean, tmp_median]

# stats_df.to_csv(save_fig_to + "Global_map_17_net_stats_{}.csv".format(case), index=0)





