# AutoJRC
Automatic Joint Roughness Coefficient Framework

AutoJRC is an automatic framework for estimating the Joint Roughness Coefficient (JRC) of rock surfaces from images using computer vision techniques. It integrates modules for 3D reconstruction, model scaling and alignment, semantic segmentation, point cloud post-processing, and adaptive JRC estimation. The full pipeline takes approximately 10 minutes per scene, significantly improving the efficiency of field investigations.

## Model Download

We provide a pretrained semantic segmentation model `JRCNet.pth` (943 MB), available on the [Releases page](https://github.com/RockVisual/AutoJRC/releases). This model is used to extract semantic regions from reconstructed rock surface images.

### Model Description

The segmentation model `JRCNet.pth` was trained to accurately identify the following semantic classes in rock face imagery:

- RockFace: Rock joint surfaces of interest
- POB: Portable orientation board used for georeferencing
- Other: Unrelated rock surfaces
- Background: All non-relevant areas

To use this model in the pipeline, place it in the segmentation module directory and load it in `04_segmentation(yuyifenge).py`.

## Pipeline Structure

00_SfM-based shooting parameter selection algorithm  
01_3D_reconstruction(python3.7).py  
02_automatic_scaling_alignment(python3.7).py  
03_Cloudpoint_to_Image(python3.7).py  
04_segmentation(yuyifenge).py  
05_RockFace_extract(python3.7).py  
06_post_processing(python3.7).py  
07_JRC_estimation(python3.7).py  
