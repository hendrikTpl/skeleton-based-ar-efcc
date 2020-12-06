# skeleton-based-ar-ecc


# Edge Layer
In this part consist of Data Acquisition Module to process Video into Skeleton then subsequently send only the skeleton data into the cloud, Thus, preserving the privacy
### Data acquisition based on PoseNet https://github.com/tensorflow/tfjs-models/tree/master/posenet


# FOG Layer
only helper to cloud, and can be seen as cloud itself


# Cloud Layer
In this part consist of Skeleton-based GCN model for training and inferences
Model available
[1] STGCN
[2] STGCN-PAM
[3] 2s-AGCN

# References


