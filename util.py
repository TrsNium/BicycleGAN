import numpy as np
import cv2
from PIL import Image
import numpy as np
import os
import subprocess
import random 

def load_data(data_dir, size=5000):
    if not os.path.exists(data_dir):
        subprocess.call('source download_dataset.sh')

    a_img = np.empty((0,256,256), dtype=np.float32)
    b_img = np.empty((0,256,256,3), dtype=np.float32)
    names = os.listdir(data_dir)[:size]
    
    # variables for animation
    filesize = len(names)
    interval = int(filesize * .1)
    p = 0
    size= 10
    print('load images')
    for i, name in enumerate(names):
        print('\r now process {} th image\t'.format(i)+'|'+'□'*p+'　'*(size-(p+1)) +'|', end=' ')
        img = np.asarray(Image.open(os.path.join(data_dir, name)))
        w = img.shape[1]//2
        aimg = cv2.cvtColor(img[:, :w,:], cv2.COLOR_RGB2GRAY)/255
        bimg = img[:, w:, :]/255
        a_img = np.append(a_img, np.array([aimg]), axis=0)
        b_img = np.append(b_img, np.array([bimg]), axis=0)
        
        if (i+1) % interval == 0:
            p+=1

    b_img = np.expand_dims(b_img, axis=-1)
    return a_img, b_img

def generator(batch_size, x, y):
    if not x.shape[0] != y.shape[0]:
        return 

    def gen():
        epoch = 0
        selected = []
        falg = False
        while True:
            k = batch_size
            if batch_size < x.shape[0] - len(selected):
                k = x.shape[0] - len(selected)
                flag = True
            selected_idx = random.sample(list(set(range(x.shape[0])) - set(selected)),k=k)
            x_ = x[selected_idx]
            y_ = y[selected_idx]

            if flag:
                flag = False
                selected = []
                epoch += 1

            yield epoch, x_, y_
    return gen
