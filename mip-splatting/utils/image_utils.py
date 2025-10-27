#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import torch
import numpy as np
from skimage.metrics import structural_similarity as SSIM

def mse(img1, img2, mask):
    if mask.dim() == 3:
        mask = mask.unsqueeze(1)
    
    mask = mask.expand_as(img1)
    
    squared_error = ((img1 - img2)) ** 2
    
    sum_masked_error = (squared_error * mask).reshape(img1.shape[0], -1).sum(1)
    num_masked_pixels = mask.reshape(img1.shape[0], -1).sum(1)
    
    num_masked_pixels = torch.clamp(num_masked_pixels, min=1e-8)
    
    mean_error = sum_masked_error / num_masked_pixels
    return mean_error.unsqueeze(1)

def psnr(img1, img2, mask):
    masked_mse = mse(img1, img2, mask)
    return 20 * torch.log10(1.0 / torch.sqrt(masked_mse + 1e-10))

def ssim_sklearn(img1, img2, mask):
    img1_np = img1.permute(0, 2, 3, 1).cpu().numpy()
    img2_np = img2.permute(0, 2, 3, 1).cpu().numpy()
    
    if mask.dim() == 4:
        mask_np = mask.squeeze(1).cpu().numpy()
    else:
        mask_np = mask.cpu().numpy()
        
    mask_np = mask_np.astype(bool)
    
    ssim_scores = []
    for i in range(img1.shape[0]):
        # data_range=1.0 assumes 0-1 float images
        ssim_map = SSIM(img1_np[i], img2_np[i],
                        data_range=1.0,
                        channel_axis=2,
                        full=True)[1]
        
        if ssim_map.ndim == 3:
            ssim_map = ssim_map.mean(axis=-1)
            
        current_mask = mask_np[i]
        masked_ssim_values = ssim_map[current_mask]
        
        if masked_ssim_values.size > 0:
            ssim_scores.append(np.mean(masked_ssim_values))
        else:
            ssim_scores.append(0.0) 
    
    return torch.tensor(ssim_scores, device=img1.device, dtype=img1.dtype).reshape(img1.shape[0], -1)

def ssim_sklearn_v2(img1, img2):
    
    ssim = SSIM(img1.permute(0, 2, 3, 1).detach().cpu().numpy()[0], img2.permute(0, 2, 3, 1).detach().cpu().numpy()[0], data_range=1.0, channel_axis=2, full=True)[1]
    return torch.tensor(ssim).reshape(img1.shape[0], -1).mean()



# def mse(img1, img2):
#     return (((img1 - img2)) ** 2).reshape(img1.shape[0], -1).mean(1, keepdim=True)

# def psnr(img1, img2):
#     mse = (((img1 - img2)) ** 2).reshape(img1.shape[0], -1).mean(1, keepdim=True)
#     return 20 * torch.log10(1.0 / torch.sqrt(mse))