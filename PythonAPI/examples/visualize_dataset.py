#import imageio
import matplotlib.image as mpimg
import glob
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from pathlib import Path
import numpy as np
import json
import os
import random
command = None
def load_spline(path: Path) -> np.ndarray:
    """Spline is reshaped from (7,2) -> (14, 1).
    Returns: 1D np.array (first 7 distance values, then 7 angle values)
    """
    with path.open() as f:
        data = json.load(f)
    
    relative_distance = lambda waypoint: waypoint[0]
    relative_angle = lambda waypoint: waypoint[1]

    # FIXME Normalize!
    waypoints = data['spline']
    global command
    command = data['command']
    #assert command in ['left', 'right'] #['get_left_lane', 'get_right_lane']
    distances = [relative_distance(wp) for wp in waypoints]
    angles = [relative_angle(wp) for wp in waypoints]
    return np.array(distances + angles)

if __name__ == '__main__':
    fig = plt.figure()
    plots = []

    horizontal_offset, vertical_offset = 224 / 2, 200
    scale = 5

    all_img_paths = glob.glob("E:\\mycarla\\PythonAPI\\examples\\_out\\*.png")
    idx = 0
    start_idx = 0
    end_idx = 6000
    for img_path in sorted(all_img_paths, key=os.path.getctime): # [start_idx:end_idx]
        print('Loading: ', idx, '/', end_idx - start_idx)
        try:
            filename = Path(img_path).with_suffix('.json').name
            json_path = Path(img_path).parent / 'spline' / filename
            spline = load_spline(json_path)

            img = mpimg.imread(img_path)
            img_plot = plt.imshow(img, animated=True)

            rel_angles = spline[7:14] * scale + horizontal_offset
            distances = vertical_offset - spline[:7] * scale
            spline_plot, = plt.plot(rel_angles, distances, '.-r', animated=True)
            command_title = plt.text(224/3, 200, command, fontsize=16)
            file_title = plt.text(224/3, 30, filename, fontsize=10, color='w')

            plots.append([img_plot, spline_plot, file_title, command_title])
            idx += 1
        except Exception as e:
            print(type(e), e)
            # Corrupted png file
            pass
        

    ani = animation.ArtistAnimation(fig, plots, interval=100, blit=True)
    # conda install -c conda-forge ffmpeg
    print('Exporting clip...')
    ani.save(f'clip_sync_{random.randint(0,999)}.mp4')
    print('Done exporting clip...')
    print('Rendering plot...')
    plt.show()
