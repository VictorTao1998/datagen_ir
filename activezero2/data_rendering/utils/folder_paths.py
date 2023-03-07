import os.path as osp

TEXTURE_FOLDER = "/messytable-slow/mini-imagenet-tools/mini_imagenet/"
TEXTURE_LIST = "/messytable-slow/mini-imagenet-tools/mini_imagenet_list.txt"
OBJECT_DIR = "/rayc-fast/ICCV2021_Diagnosis/ocrtoc_materials/models/"
OBJECT_CSV_PATH = "/rayc-fast/ICCV2021_Diagnosis/ocrtoc_materials/objects.csv"
SCENE_DIR = "/rayc-fast/ICCV2021_Diagnosis/ocrtoc_materials/scenes"
TEXTURE_SQ_FOLDER = "/messytable-slow/mini-imagenet-tools/mini_imagenet_square/"
TEXTURE_SQ_LIST = "/messytable-slow/mini-imagenet-tools/mini_imagenet_square/list.txt"
ENV_MAP_FOLDER = "/messytable-slow/mini-imagenet-tools/rand_env/"
ENV_MAP_LIST = "/messytable-slow/mini-imagenet-tools/rand_env/list.txt"

if not osp.exists(TEXTURE_FOLDER):
    TEXTURE_FOLDER = "/media/jianyu/dataset/messy-table-dataset/mini-imagenet-tools/mini_imagenet/"
    TEXTURE_LIST = "/media/jianyu/dataset/messy-table-dataset/mini-imagenet-tools/mini_imagenet_list.txt"
    OBJECT_DIR = "/media/jianyu/dataset/ICCV2021_Diagnosis/ocrtoc_materials/models/"
    OBJECT_CSV_PATH = "/media/jianyu/dataset/ICCV2021_Diagnosis/ocrtoc_materials/objects.csv"
    SCENE_DIR = "/media/jianyu/dataset/ICCV2021_Diagnosis/ocrtoc_materials/scenes"
    TEXTURE_SQ_FOLDER = "/media/jianyu/dataset/messy-table-dataset/mini-imagenet-tools/mini_imagenet_square/"
    TEXTURE_SQ_LIST = "/media/jianyu/dataset/messy-table-dataset/mini-imagenet-tools/mini_imagenet_square/list.txt"
    ENV_MAP_FOLDER = "/media/jianyu/dataset/messy-table-dataset/mini-imagenet-tools/rand_env/"
    ENV_MAP_LIST = "/media/jianyu/dataset/messy-table-dataset/mini-imagenet-tools/rand_env/list.txt"