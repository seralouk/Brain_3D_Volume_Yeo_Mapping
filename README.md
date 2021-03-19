{\rtf1\ansi\ansicpg1252\cocoartf2513
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;\csgray\c0\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww25540\viewh12780\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs28 \cf0 # Small toolbox to extract the values of a 3D brain volume for the 7 and 17 Yeo networks\
\
#### Code accompanying the Ph.D. disseration of Serafeim LOUKAS entitled: "Multivariate and predictive models for brain connectivity with application to neurodevelopment".\
#### URL: TBA, Th\'e8se n. 8854 (EPFL, 2021)\
\
----\
\
#### `\cf2 \cb3 MapYeo2HCP.m\cf0 \cb1 `: \cf2 \cb3 Script to bring the several Yeo atlases to our functional space, then mask them using the global GM-mask to ensure fine-grained study-specific coverage\
\
\cf0 \cb1 #### `\cf2 \cb3 extract_Yeo_values.py\cf0 \cb1 `: \cf2 \cb3 Main script to extract values from a brain 3D volume for each of the 7 and 17 Yeo networks\cf0 \cb1 \
\
#### Dependencies: `numpy`, `seaborn`, `os`, `nibabel` and `matplotlib`\
----\
\
#### Usage: Running `\cf2 \cb3 MapYeo2HCP.m \cf0 \cb1 ` is optional except if you want to bring the Yeo atlas to a space different than the MNI space.\
			Running `\cf2 \cb3 extract_Yeo_values.py \cf0 \cb1 ` is the main script. See code for details.}