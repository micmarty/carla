import os
import glob
from pathlib import Path
import numpy as np
import shutil

ROOT_DIR = 'E:/mycarla/PythonAPI/dataset'
COMMANDS = ['left', 'get_left_lane', 'keep_lane', 'straight', 'get_right_lane', 'right']

def is_complete_seq(seq_id, root_dir) -> bool:
    seq_imgs = list(glob.glob(f"{root_dir}/{seq_id}_*.png"))
    seq_jsons = list(glob.glob(f"{root_dir}/spline/{seq_id}_*.json"))
    is_complete = len(seq_imgs) == len(seq_jsons) == 10
    print(f'{seq_id} valid? {is_complete}')
    return is_complete

def extract_seq_id(path: str) -> str: 
    return Path(path).stem.split('_')[0]

def find_bad_sequences(root_dir):
    all_img_paths = glob.glob(f"{root_dir}/*.png")
    print(f'{len(all_img_paths)} images found')

    seq_ids = {extract_seq_id(path) for path in all_img_paths}
    bad_seq_ids = [seq_id for seq_id in seq_ids if not is_complete_seq(seq_id, root_dir)]

    # Result
    print(f'{len(bad_seq_ids)} incomplete sequences found')
    print(bad_seq_ids)
    return bad_seq_ids

def ask_for_removing_approval(bad_seq_ids, root_dir):
    for seq_id in bad_seq_ids:
        pattern = f'{root_dir}/**/{seq_id}_*'
        removal_candidates = glob.glob(pattern, recursive=True)
        print(f'Sequence {seq_id} - candidates for removal:')
        print(*removal_candidates, sep='\n')
        print()
        if input(f'Remove {len(removal_candidates)} files? [Y/n]') in ['', 'y', 'Y']:
            [os.remove(path) for path in removal_candidates]
            print('Removed.')

def group_sequences_into_folders(root_dir):
    all_img_paths = glob.glob(f"{root_dir}/*.png")
    seq_ids = {extract_seq_id(path) for path in all_img_paths}
    for seq_id in seq_ids:
        os.makedirs(f'{root_dir}/{seq_id}', exist_ok=True)
        seq_imgs = list(glob.glob(f'{root_dir}/{seq_id}_*.png'))
        seq_jsons = list(glob.glob(f'{root_dir}/spline/{seq_id}_*.json'))

        for img_path in seq_imgs:
            _, idx_in_seq = Path(img_path).stem.split('_')
            src, dst = img_path, f'{root_dir}/{seq_id}/{idx_in_seq}.png'
            shutil.move(src, dst)
            print(f'Moving {src} to {dst}')

        for json_path in seq_jsons:
            _, idx_in_seq = Path(json_path).stem.split('_')
            src, dst = json_path, f'{root_dir}/{seq_id}/{idx_in_seq}.json'
            shutil.move(src, dst)
            print(f'Moving {src} to {dst}')
    os.rmdir(f'{root_dir}/spline')
    print('Removed spline/ folder')


if __name__ == '__main__':
    data_dirs = [
        'test_town02_dataset',
        'test_town06_dataset',
        'test_town07_dataset',
        'train_town01_dataset',
        'train_town03_dataset',
        'train_town04_dataset',
        'train_town05_dataset',
    ]
    for data_dir in data_dirs:
        full_dir = ROOT_DIR + '/' + data_dir
        # ids = find_bad_sequences(full_dir)
        # ask_for_removing_approval(ids, full_dir)
        group_sequences_into_folders(full_dir)
