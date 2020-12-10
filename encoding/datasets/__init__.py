from .base import *
from .coco import COCOSegmentation
from .ade20k import ADE20KSegmentation
from .pascal_voc import VOCSegmentation
from .pascal_aug import VOCAugSegmentation
from .pcontext import ContextSegmentation
from .cityscapes import CitySegmentation
from .cocostuff import CocostuffSegmentation
from .pascal_person import PersonSegmentation

datasets = {
    'coco': COCOSegmentation,
    'ade20k': ADE20KSegmentation,
    'pascal_voc': VOCSegmentation,
    'pascal_aug': VOCAugSegmentation,
    'pcontext': ContextSegmentation,
    'citys': CitySegmentation,
    'cocostuff': CocostuffSegmentation,
    'pperson': PersonSegmentation,
}

def get_segmentation_dataset(name, **kwargs):
    return datasets[name.lower()](**kwargs)
