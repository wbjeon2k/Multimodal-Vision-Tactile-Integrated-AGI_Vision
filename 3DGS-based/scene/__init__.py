
import os
import random
import json
from utils.system_utils import searchForMaxIteration
from scene.dataset_readers import sceneLoadTypeCallbacks
from scene.gaussian_model import GaussianModel
from arguments import ModelParams
from utils.camera_utils import cameraList_from_camInfos, camera_to_JSON
import torch 

def save_tactile_colored_ply(gaussian_model, path):
    print(f"[Tactile Save] Saving colored PLY to: {path}")
    SH_C0 = 0.28209479177387814
    with torch.no_grad():
        backup_dc = gaussian_model._features_dc.clone()
        backup_rest = gaussian_model._features_rest.clone()
        
        original_rgb = (backup_dc.squeeze(1) * SH_C0) + 0.5
        original_rgb = torch.clamp(original_rgb, 0.0, 1.0)

        if hasattr(gaussian_model, "tactile_features"):
            feat_val = gaussian_model.tactile_features[:, 0:1]
            feat_val = torch.clamp(feat_val, 0.0, 1.0)
            
            # color_sky = torch.tensor([0.53, 0.81, 0.92], device="cuda")
            # color_warm_red = torch.tensor([1.0, 0.39, 0.28], device="cuda")
            
            # is_rough = (feat_val < 0.5).float()
            # tactile_rgb = is_rough * color_warm_red + (1.0 - is_rough) * color_sky
            color_flat_green = torch.tensor([0.36, 0.78, 0.39], device="cuda")
            is_flat = (feat_val > 0.5).float()
            tactile_rgb = is_flat * color_flat_green + (1.0 - is_flat) * original_rgb
            
        else:
            print("[Warning] No tactile_features found. Saving as black.")
            tactile_rgb = torch.zeros_like(gaussian_model._features_dc[:, 0, :])

        tactile_sh_dc = (tactile_rgb - 0.5) / 0.28209479177387814
        
        gaussian_model._features_dc.data = tactile_sh_dc.unsqueeze(1)
        gaussian_model._features_rest.data.fill_(0.0)

        gaussian_model.save_ply(path)

        gaussian_model._features_dc.data = backup_dc
        gaussian_model._features_rest.data = backup_rest

    print("[Tactile Save] Done.")
    
    
class Scene:

    gaussians : GaussianModel

    def __init__(self, args : ModelParams, gaussians : GaussianModel, load_iteration=None, shuffle=True, resolution_scales=[1.0]):
        """b
        :param path: Path to colmap scene main folder.
        """
        self.model_path = args.model_path
        self.loaded_iter = None
        self.gaussians = gaussians

        if load_iteration:
            if load_iteration == -1:
                self.loaded_iter = searchForMaxIteration(os.path.join(self.model_path, "point_cloud"))
            else:
                self.loaded_iter = load_iteration
            print("Loading trained model at iteration {}".format(self.loaded_iter))

        self.train_cameras = {}
        self.test_cameras = {}

        if os.path.exists(os.path.join(args.source_path, "sparse")):
            scene_info = sceneLoadTypeCallbacks["Colmap"](args.source_path, args.images, args.eval)
        elif os.path.exists(os.path.join(args.source_path, "transforms_train.json")):
            print("Found transforms_train.json file, assuming Blender data set!")
            scene_info = sceneLoadTypeCallbacks["Blender"](args.source_path, args.white_background, args.eval)
        elif os.path.exists(os.path.join(args.source_path, "metadata.json")):
            print("Found metadata.json file, assuming multi scale Blender data set!")
            scene_info = sceneLoadTypeCallbacks["Multi-scale"](args.source_path, args.white_background, args.eval, args.load_allres)
        else:
            assert False, "Could not recognize scene type!"

        if not self.loaded_iter:
            with open(scene_info.ply_path, 'rb') as src_file, open(os.path.join(self.model_path, "input.ply") , 'wb') as dest_file:
                dest_file.write(src_file.read())
            json_cams = []
            camlist = []
            if scene_info.test_cameras:
                camlist.extend(scene_info.test_cameras)
            if scene_info.train_cameras:
                camlist.extend(scene_info.train_cameras)
            for id, cam in enumerate(camlist):
                json_cams.append(camera_to_JSON(id, cam))
            with open(os.path.join(self.model_path, "cameras.json"), 'w') as file:
                json.dump(json_cams, file)

        if shuffle:
            random.shuffle(scene_info.train_cameras)  # Multi-res consistent random shuffling
            # random.shuffle(scene_info.test_cameras)  # Multi-res consistent random shuffling

        self.cameras_extent = scene_info.nerf_normalization["radius"]

        for resolution_scale in resolution_scales:
            print("Loading Training Cameras")
            self.train_cameras[resolution_scale] = cameraList_from_camInfos(scene_info.train_cameras, resolution_scale, args)
            print("Loading Test Cameras")
            self.test_cameras[resolution_scale] = cameraList_from_camInfos(scene_info.test_cameras, resolution_scale, args)

        if self.loaded_iter:
            self.gaussians.load_ply(os.path.join(self.model_path,
                                                           "point_cloud",
                                                           "iteration_" + str(self.loaded_iter),
                                                           "point_cloud.ply"))
        else:
            self.gaussians.create_from_pcd(scene_info.point_cloud, self.cameras_extent)

    def save(self, iteration):
        point_cloud_path = os.path.join(self.model_path, "point_cloud/iteration_{}".format(iteration))
        os.makedirs(point_cloud_path, exist_ok=True) # 폴더가 없으면 생성

        self.gaussians.save_ply(os.path.join(point_cloud_path, "point_cloud.ply"))
        tactile_ply_path = os.path.join(point_cloud_path, "tactile_color.ply")
        save_tactile_colored_ply(self.gaussians, tactile_ply_path)

    def getTrainCameras(self, scale=1.0):
        return self.train_cameras[scale]

    def getTestCameras(self, scale=1.0):
        return self.test_cameras[scale]