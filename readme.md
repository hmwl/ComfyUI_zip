## ComfyUI 压缩包图片处理
## ComfyUI zip package image processing

### 节点介绍
### Node Introduction

#### 1. Zip Compress (压缩图片)
- 功能：将生成的图片打包成zip压缩文件
- Function: Package generated images into a zip file
- 输入参数 (Input Parameters):
  - images: 图片输入 (Image input)
  - filename_prefix: 文件名前缀，默认为"ComfyUI" (Filename prefix, default is "ComfyUI")
- 输出 (Output):
  - temp_dir: 临时目录路径 (Temporary directory path)
  - 生成的zip文件将保存在ComfyUI的输出目录中 (Generated zip file will be saved in ComfyUI's output directory)

#### 2. UnzipToInput (解压到输入)
- 功能：解压zip文件并将图片加载为可处理的格式
- Function: Extract zip file and load images into processable format
- 输入参数 (Input Parameters):
  - zip_path: zip文件路径，支持本地路径或URL (Zip file path, supports local path or URL)
- 输出 (Output):
  - images: 解压出的图片列表 (List of extracted images)
  - folder: 解压目录名称 (Extraction directory name)

> **注意**: 压缩包仅支持图片文件的zip，不支持其他类型文件和文件夹  
> **Note**: Only supports zip files containing images, other file types and folders are not supported

#### 3. 清理文件夹 (Clean Folders)
- 功能：清理临时文件夹和输出文件夹
- Function: Clean temporary and output folders
- 输入参数 (Input Parameters):
  - input_path: 需要清理的输入路径 (Input path to clean)
  - output_path: 需要清理的输出路径 (Output path to clean)
- 输出 (Output):
  - 无返回值，直接执行清理操作 (No return value, directly performs cleaning operation)

### 使用说明
### Usage Instructions

1. 压缩图片 (Compress Images):
   - 将图片节点连接到Zip Compress节点
   - 设置文件名前缀
   - 运行后将在输出目录生成zip文件

2. 解压图片 (Extract Images):
   - 在UnzipToInput节点中输入zip文件路径
   - 支持本地zip文件或在线zip文件URL
   - 解压后的图片可直接用于后续处理

3. 清理文件夹 (Clean Folders):
   - 用于清理工作流程中产生的临时文件
   - 可选择性地清理输入或输出目录
   - 建议在工作流程结束时使用

### 测试JSON文件
项目中有一个Example.json文件，可以作为使用的参考
There is an Example.json file in the project that you can refer to for usage.
