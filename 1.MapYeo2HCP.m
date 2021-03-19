%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Author: Loukas Serafeim, April 2020
%
% Yeo files found from nilearn
% Resources:
% http://surfer.nmr.mgh.harvard.edu/fswiki/CorticalParcellation_Yeo2011
% https://nilearn.github.io/modules/generated/nilearn.datasets.fetch_atlas_yeo_2011.html#nilearn.datasets.fetch_atlas_yeo_2011

% Script to bring the several Yeo atlases to my functional space, then mask
% them using the global GM-mask to make sure fine-grained study-specific
% coverage
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% 
clc;clear;

%% where to save the resliced (to functional space) Yeo atlases
save_yeo_to = [pwd , filesep , 'results/'];

%% utils (mapVolumeToVolume)
addpath([pwd , filesep , 'Utils/']);

%% define the target functional space
func_vol = spm_select('FPList', [pwd , filesep , 'data/'], ['^Cov_s5fr' '.*\.nii$']);

% path to the raw Yeo atlases
path_to_yeo_init_files = [pwd , filesep , 'Yeo_atlases/yeo_2011/Yeo_JNeurophysiol11_MNI152/'];

% build full path names
yeo_7_fine = [path_to_yeo_init_files 'Yeo2011_7Networks_MNI152_FreeSurferConformed1mm.nii'];
yeo_7_liberal = [path_to_yeo_init_files 'Yeo2011_7Networks_MNI152_FreeSurferConformed1mm_LiberalMask.nii'];

yeo_17_fine = [path_to_yeo_init_files 'Yeo2011_17Networks_MNI152_FreeSurferConformed1mm.nii'];
yeo_17_liberal = [path_to_yeo_init_files 'Yeo2011_17Networks_MNI152_FreeSurferConformed1mm_LiberalMask.nii'];


%% reslice the yeo atlases to the desired functional space (of out)
[fine_yeo_7, p1] = mapVolumeToVolume(yeo_7_fine, func_vol);
p1.fname = [save_yeo_to 'resliced_fine_grained_yeo_7.nii'];
spm_write_vol(p1, fine_yeo_7);

[liberal_yeo_7, p2] = mapVolumeToVolume(yeo_7_liberal, func_vol);
p2.fname = [save_yeo_to 'resliced_liberal_yeo_7.nii'];
spm_write_vol(p2, liberal_yeo_7);

[fine_yeo_17, p3] = mapVolumeToVolume(yeo_17_fine, func_vol);
p3.fname = [save_yeo_to 'resliced_fine_grained_yeo_17.nii'];
spm_write_vol(p3, fine_yeo_17);

[liberal_yeo_17, p4] = mapVolumeToVolume(yeo_17_liberal, func_vol);
p4.fname = [save_yeo_to 'resliced_liberal_yeo_17.nii'];
spm_write_vol(p4, liberal_yeo_17);


%% load GM mask and reslice it to the functional space
GM_global_mask = [pwd , filesep , 'data/', 'Global_GM_TMP.nii'];
[gm_mask, p5] = mapVolumeToVolume(GM_global_mask, func_vol);

%% make it binary
gm_mask_binary = logical(gm_mask) * 1;
assert(size(unique(gm_mask_binary),1) == 2);

%% mask the resliced Yeo atlases using the GM global mask that is now also resliced into the same functional space (i.e. 'func_vol' space)
fine_yeo_7_GM_masked = fine_yeo_7 .* gm_mask_binary;
p1.fname = [save_yeo_to 'masked_resliced_fine_grained_yeo_7.nii'];
spm_write_vol(p1, fine_yeo_7_GM_masked);

liberal_yeo_7_GM_masked = liberal_yeo_7 .* gm_mask_binary;
p2.fname = [save_yeo_to 'masked_resliced_liberal_yeo_7.nii'];
spm_write_vol(p2, liberal_yeo_7_GM_masked);

fine_yeo_17_GM_masked = fine_yeo_17 .* gm_mask_binary;
p3.fname = [save_yeo_to 'masked_resliced_fine_grained_yeo_17.nii'];
spm_write_vol(p3, fine_yeo_17_GM_masked);

liberal_yeo_17_GM_masked = liberal_yeo_17 .* gm_mask_binary;
p4.fname = [save_yeo_to 'masked_resliced_liberal_yeo_17.nii'];
spm_write_vol(p4, liberal_yeo_17_GM_masked);

% now use these "masked_resliced" Yeo atlases to mask the brain 3D volume
% of interest