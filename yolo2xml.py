"""
Created by Chalice on 2022-03-20.
https://github.com/dc-cheny
"""

import os
import json
from pascal_voc_writer import Writer
from PIL import Image


def parse_cls(txt_path):
    """ parse class file to cls2idx/idx2cls dict.
    """
    txt_path = str(txt_path)
    if not txt_path:
        return None
    else:
        with open(txt_path, 'r') as f:
            c = [x.strip('\n').strip() for x in f.readlines()]
    return {_c: str(idx) for idx, _c in enumerate(c)}, {str(idx): _c for idx, _c in enumerate(c)}


def yolo2xml(yolo_ann_dir, xml_dir):
    """ Suppose that images and anns are in the same folder.
    """
    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)

    all_files = os.listdir(yolo_ann_dir)
    yolo_ann_files = [x for x in all_files if x.endswith('.txt') and x != 'classes.txt']
    image_files = [x for x in all_files if x.endswith('.jpg')]
    ann_name2image_name = {im.split('.')[0]+'.txt': im for im in image_files}
    class_txt_path = os.path.join(yolo_ann_dir, 'classes.txt')
    _, idx2cls = parse_cls(class_txt_path)

    for yaf in yolo_ann_files:
        yaf_path = os.path.join(yolo_ann_dir, yaf)
        xml_filename = yaf.split('.')[0]+'.xml'
        image_path = os.path.join(yolo_ann_dir, ann_name2image_name[yaf])
        try:
            img_obj = Image.open(open(image_path, 'rb')).convert('RGB')
        except Exception as e:
            print('Load img {} error, detail={}'.format(image_path, e))
            continue
        width, height = img_obj.size

        with open(yaf_path, 'r') as f:
            yolo_ann_contents = [x.strip('\n').strip() for x in f.readlines()]
        voc_writer = Writer(xml_filename, width, height)
        for yac in yolo_ann_contents:
            yac = yac.split()
            if yac[0] in ['10', '12']:
                print(yaf)
            label, bbox = idx2cls[yac[0]], list(map(float, yac[1:]))
            x, y, w, h = bbox
            xmin = int(width*(2*x+w)/2)
            xmax = int(width*(2*x-w)/2)
            ymin = int(height*(2*y+h)/2)
            ymax = int(height*(2*y-h)/2)
            voc_writer.addObject(label, xmin, ymin, xmax, ymax)
        voc_writer.save(os.path.join(xml_dir, xml_filename))
    print('Done!')
    return


def xml2yolo(yolo_ann_dir, xml_dir):
    """ Suppose that images and anns are in the same folder.
    """
    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)

    all_files = os.listdir(yolo_ann_dir)
    yolo_ann_files = [x for x in all_files if x.endswith('.txt') and x != 'classes.txt']
    image_files = [x for x in all_files if x.endswith('.jpg')]
    ann_name2image_name = {im.split('.')[0]+'.txt': im for im in image_files}
    class_txt_path = os.path.join(yolo_ann_dir, 'classes.txt')
    _, idx2cls = parse_cls(class_txt_path)

    for yaf in yolo_ann_files:
        yaf_path = os.path.join(yolo_ann_dir, yaf)
        xml_filename = yaf.split('.')[0]+'.xml'
        image_path = os.path.join(yolo_ann_dir, ann_name2image_name[yaf])
        try:
            img_obj = Image.open(open(image_path, 'rb')).convert('RGB')
        except Exception as e:
            print('Load img {} error, detail={}'.format(image_path, e))
            continue
        width, height = img_obj.size

        with open(yaf_path, 'r') as f:
            yolo_ann_contents = [x.strip('\n').strip() for x in f.readlines()]
        voc_writer = Writer(xml_filename, width, height)
        for yac in yolo_ann_contents:
            label, [x, y, w, h] = idx2cls[yac[0]], list(map(eval, yac[1:]))
            xmin = int(width*(2*x+w)/2)
            xmax = int(width*(2*x-w)/2)
            ymin = int(height*(2*y+h)/2)
            ymax = int(height*(2*y-h)/2)
            voc_writer.addObject(label, xmin, ymin, xmax, ymax)
        voc_writer.save(os.path.join(xml_dir, xml_filename))
    print('Done!')
    return


if __name__ == '__main__':
    yolo_ann_dir = '/home/xixiang/Record-Multi-Cameras-Opencv-main/20220317/20220315_sample_with_label_batch1_new'
    xml_dir = '/home/xixiang/Record-Multi-Cameras-Opencv-main/20220317/20220315_sample_with_label_batch1_new_xml'
    yolo2xml(yolo_ann_dir, xml_dir)




