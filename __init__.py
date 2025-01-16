from .unzip import UnzipToInput
from .compress import CompressImages
from .clean import CleanFolders

NODE_CLASS_MAPPINGS = {
    "UnzipToInput": UnzipToInput,
    "CompressImages": CompressImages,
    "CleanFolders": CleanFolders
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UnzipToInput": "Unzip To Input",
    "CompressImages": "Zip Compress",
    "CleanFolders": "Clean Folders"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']