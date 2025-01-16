import os
import time
import torch
import urllib.request
from urllib.parse import urlparse
import folder_paths
import numpy as np
from PIL import Image
import shutil

class UnzipToInput:
    def __init__(self):
        self.output_dir = folder_paths.get_input_directory()
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "zip_path": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("images", "folder",)
    OUTPUT_IS_LIST = (True, False,)
    FUNCTION = "unzip_process"
    CATEGORY = "comfyui_zip"

    def download_file(self, url, save_path):
        urllib.request.urlretrieve(url, save_path)

    def is_image_file(self, filename):
        image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
        return os.path.splitext(filename.lower())[1] in image_extensions

    def unzip_process(self, zip_path):
        timestamp = str(int(time.time()))
        extract_dir = os.path.join(self.output_dir, f"unzip_{timestamp}")
        os.makedirs(extract_dir, exist_ok=True)

        # 处理URL或本地路径
        if zip_path.startswith(('http://', 'https://')):
            parsed_url = urlparse(zip_path)
            zip_filename = os.path.basename(parsed_url.path)
            temp_zip = os.path.join(extract_dir, zip_filename)
            self.download_file(zip_path, temp_zip)
            zip_path = temp_zip

        # 解压文件
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 获取所有文件列表
            name_list = zip_ref.namelist()
            
            # 过滤掉 __MACOSX 文件夹
            filtered_names = [name for name in name_list 
                            if not name.startswith('__MACOSX/') 
                            and not name.startswith('._')]
            
            # 解压文件，处理中文编码
            for name in filtered_names:
                try:
                    # 尝试使用 cp437 解码，然后用 utf-8 编码
                    unicode_name = name.encode('cp437').decode('utf-8')
                except:
                    # 如果失败，直接使用原名称
                    unicode_name = name
                
                # 获取解压后的完整路径
                extracted_path = os.path.join(extract_dir, unicode_name)
                
                # 确保目标目录存在
                os.makedirs(os.path.dirname(extracted_path), exist_ok=True)
                
                # 提取文件
                with zip_ref.open(name) as source, open(extracted_path, 'wb') as target:
                    shutil.copyfileobj(source, target)

        # 收集所有图片文件
        image_files = []
        for root, _, files in os.walk(extract_dir):
            for file in files:
                if self.is_image_file(file):
                    image_files.append(os.path.join(root, file))

        if not image_files:
            raise ValueError("No image files found in ZIP archive")

        # 读取所有图片并转换为tensor
        images_list = []
        for img_path in image_files:
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_tensor = np.array(img).astype(np.float32) / 255.0
            img_tensor = torch.from_numpy(img_tensor)
            img_tensor = img_tensor.unsqueeze(0)
            images_list.append(img_tensor)

        # 返回图片列表和文件夹名称
        folder_name = os.path.basename(extract_dir)

        return (images_list, folder_name)
