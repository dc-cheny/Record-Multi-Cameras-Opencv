import os
import shutil
import random


def sample_images(root_dir, sample_num, to_dir):
    cam0 = [os.path.join(root_dir, 'camera_0', x) for x in os.listdir(os.path.join(root_dir, 'camera_0'))]
    cam2 = [os.path.join(root_dir, 'camera_2', x) for x in os.listdir(os.path.join(root_dir, 'camera_2'))]

    each_sample_num = sample_num // 2
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)

    cam0_sample = random.choices(cam0, k=each_sample_num)
    cam2_sample = random.choices(cam2, k=each_sample_num)
    for cs in [cam0_sample, cam2_sample]:
        for _c in cs:
            shutil.copy(_c, os.path.join(to_dir, os.path.basename(_c)))

def split_dataset(data_dir, to_dir, split_ratio=0.8):
    all_files = os.listdir(data_dir)
    all_images = [x for x in all_files if x.endswith('.jpg')]

    # build yolo dataset structure
    file_type = ['images', 'labels']
    train_val = ['train', 'val']
    for ft in file_type:
        for tv in train_val:
            if not os.path.exists(os.path.join(to_dir, ft, tv)):
                os.makedirs(os.path.join(to_dir, ft, tv))

    random.shuffle(all_images)  # shuffle images for splitting
    train_images = all_images[:int(len(all_images)*split_ratio)]
    val_images = all_images[int(len(all_images)*split_ratio):]
    for idx, images in enumerate([train_images, val_images]):
        train_flag = 'train' if not idx else 'val'
        for img in images:
            ori_img_path = os.path.join(data_dir, img)
            ori_ann_path = os.path.join(data_dir, img.split('.')[0]+'.txt')
            to_img_path = os.path.join(to_dir, 'images', train_flag, img)
            to_ann_path = os.path.join(to_dir, 'labels', train_flag, img.split('.')[0]+'.txt')
            shutil.copy(ori_img_path, to_img_path)
            shutil.copy(ori_ann_path, to_ann_path)
    print('Splitting Done!')
    return


def catch_data():
    cam0_dir = 'detrice_data_0313/camera_0'
    cam2_dir = 'detrice_data_0313/camera_2'
    label_dir = 'detrice_data_0313/labels'
    cam0_imgs = os.listdir(cam0_dir)
    cam2_imgs = os.listdir(cam2_dir)
    labels = os.listdir(label_dir)
    labels = [x.split('.')[0] for x in labels]

    for ci in cam0_imgs:
        prefix = ci.split('.')[0]
        if prefix in labels:
            ori_path = os.path.join(cam0_dir, ci)
            to_path = os.path.join('detrice_data_0313/images', ci)
            shutil.copy(ori_path, to_path)
    for ci in cam2_imgs:
        prefix = ci.split('.')[0]
        if prefix in labels:
            ori_path = os.path.join(cam2_dir, ci)
            to_path = os.path.join('detrice_data_0313/images', ci)
            shutil.copy(ori_path, to_path)


if __name__ == '__main__':
    # catch_data()
    # sample_images('20220315', 200, '20220315/20220315_sample')

    split_dataset('20220317/20220315_sample_with_label_batch1_new', '20220317/dataset_0318_0.7', 0.7)