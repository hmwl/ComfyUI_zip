import os
import zipfile
import torch 
import numpy as np
from PIL import Image
import folder_paths
import tempfile
import shutil
import matplotlib.pyplot as plt
import time
import random

class CompressImages:
    _current_id = None
    _temp_dirs = {}
    _image_counts = {}
    _zip_filename = {}  # 新增：记录每个工作流的zip文件名

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"})
            },
            "hidden": {
                "prompt": "PROMPT", 
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID",
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("temp_dir",)
    FUNCTION = "compress_images"
    OUTPUT_NODE = True
    CATEGORY = "comfyui_zip"

    def compress_images(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None, unique_id=None):
        try:
            # 确保临时目录存在
            if unique_id not in CompressImages._temp_dirs or not os.path.exists(CompressImages._temp_dirs[unique_id]):
                folder_name = f"{filename_prefix}{self.prefix_append}_{unique_id}"
                CompressImages._temp_dirs[unique_id] = os.path.join(self.output_dir, folder_name)
                CompressImages._image_counts[unique_id] = 0
                timestamp = int(time.time())
                CompressImages._zip_filename[unique_id] = f'{filename_prefix}_{timestamp}.zip'
            
            # 确保目录存在
            os.makedirs(CompressImages._temp_dirs[unique_id], exist_ok=True)

            temp_dir = CompressImages._temp_dirs[unique_id]
            zip_path = os.path.abspath(os.path.join(self.output_dir, CompressImages._zip_filename[unique_id]))

            # 追加模式打开zip文件
            zip_mode = 'a' if os.path.exists(zip_path) else 'w'
            with zipfile.ZipFile(zip_path, zip_mode) as zipf:
                for image in images:
                    if isinstance(image, torch.Tensor):
                        img_array = 255. * image.cpu().numpy()
                        img = Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))
                    elif isinstance(image, Image.Image):
                        img = image
                    else:
                        raise ValueError(f"不支持的图片格式: {type(image)}")
                
                    temp_image_path = os.path.join(temp_dir, f'temp_image_{CompressImages._image_counts[unique_id]:05d}.png')
                    img.save(temp_image_path)
                    arcname = f'image_{CompressImages._image_counts[unique_id]:05d}.png'
                    zipf.write(temp_image_path, arcname)
                    os.remove(temp_image_path)
                    CompressImages._image_counts[unique_id] += 1
                    
            folder_name = os.path.basename(CompressImages._temp_dirs[unique_id])
            
            # 正确的返回格式
            results = (folder_name,)  # 这是 RETURN_TYPES 定义的返回值
            
            return {"ui": {"file": [CompressImages._zip_filename[unique_id]]}, "result": (results,)}

        except Exception as e:
            print(f"发生错误: {str(e)}")
            self._cleanup(unique_id)
            raise e

class ZipFiles:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "images": ("IMAGE",),
            "zip_name": ("STRING", {"default": "images.zip"}),
            "save_path": ("STRING", {"default": "ComfyUI/output"}),
        },
        "hidden": {"unique_id": "UNIQUE_ID"},
    }
    
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("zip_path", "temp_dir",)
    FUNCTION = "zip_files"
    
    def zip_files(self, images, zip_name, save_path, unique_id):
        
        temp_dir = tempfile.gettempdir()
        
        return (output_path, temp_dir)

NODE_CLASS_MAPPINGS = {
    "CompressImages": CompressImages
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CompressImages": "Zip Compress"
}
