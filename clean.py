import os
import shutil
import folder_paths

class CleanFolders:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "input_path": ("STRING", {"default": ""}),
            "output_path": ("STRING", {"default": ""})
        }}
    
    RETURN_TYPES = ()
    FUNCTION = "clean"
    CATEGORY = "comfyui_zip"
    OUTPUT_NODE = True

    def clean(self, input_path, output_path):
        result_msg = []
        
        # 获取基础目录
        input_base = folder_paths.get_input_directory()
        output_base = folder_paths.get_output_directory()
        
        # 确保路径是字符串类型，如果是元组则取第一个元素
        input_path = input_path[0] if isinstance(input_path, tuple) else str(input_path) if input_path else ""
        output_path = output_path[0] if isinstance(output_path, tuple) else str(output_path) if output_path else ""
        
        # 只有当提供了路径时才进行删除操作
        if input_path:
            input_full_path = os.path.join(input_base, input_path)
            if os.path.exists(input_full_path):
                try:
                    shutil.rmtree(input_full_path)
                    result_msg.append(f"已清理输入目录: {input_full_path}")
                except Exception as e:
                    result_msg.append(f"清理输入目录失败: {str(e)}")
            else:
                result_msg.append(f"输入目录不存在: {input_full_path}")
        else:
            result_msg.append("未提供输入路径，跳过清理")
            
        # 只有当提供了路径时才进行删除操作    
        if output_path:
            output_full_path = os.path.join(output_base, output_path)
            if os.path.exists(output_full_path):
                try:
                    shutil.rmtree(output_full_path)
                except Exception as e:
                    pass
                    
        return ("",)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "CleanFolders": CleanFolders
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CleanFolders": "清理文件夹"
}
