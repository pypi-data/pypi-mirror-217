# IsoScore

This contains the Python3 implementation of IsoScore, which was originally
introduced in the 2022 paper by William Rudman, Nate Gillman, Taylor Rayne, and 
Carsten Eickhoff, published in the Findings of the ACL (https://aclanthology.org/2022.findings-acl.262/). 
IsoScore is the first tool available in the literature that accurately measures isotropy in embedding space. 
See the original paper for more information.

IsoScore 2.0.0 provides an updated version of IsoScore, called IsoScore*, that allows users to reliably measure 
isotropy of point clouds where the dimensionality of the point cloud is larger the number of samples. Additionally, 
IsoScore* is differentiable and can be used as a regularizer in embedding space. For details of IsoScore* and the impact
that using IsoScore* as a regularizer in fine-tuning pre-trained language models see: https://arxiv.org/abs/2305.19358  


### License

This project is licensed under the MIT License.

