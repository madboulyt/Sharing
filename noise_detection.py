import numpy as np
from cv2 import imread
from skimage import img_as_float

def noise_estimate(im, pch_size=8):
    if im.ndim == 3:
        im = im.transpose((2, 0, 1))
    else:
        im = np.expand_dims(im, axis=0)

    C, H, W = im.shape
    stride = 3

    # Inline patch extraction (no function call overhead)
    num_H = (H - pch_size) // stride + 1
    num_W = (W - pch_size) // stride + 1
    num_pch = num_H * num_W
    pch = np.zeros((C, pch_size * pch_size, num_pch), dtype=im.dtype)
    kk = 0
    for ii in range(pch_size):
        for jj in range(pch_size):
            temp = im[:, ii:H-pch_size+ii+1:stride, jj:W-pch_size+jj+1:stride]
            pch[:, kk, :] = temp.reshape((C, num_pch))
            kk += 1

    pch = pch.reshape((-1, num_pch))
    d = pch.shape[0]
    X = pch - pch.mean(axis=1, keepdims=True)
    sig_value = np.linalg.eigvalsh(X @ X.T / num_pch)  # eigvalsh returns sorted, skip .sort()

    for ii in range(-1, -d-1, -1):
        tau = np.mean(sig_value[:ii])
        if np.sum(sig_value[:ii] > tau) == np.sum(sig_value[:ii] < tau):
            return np.sqrt(tau)

NOISE_THRESHOLD = 8 / 255  # tune this value (8 out of 255)

def is_noisy(image_path):
    im = img_as_float(imread(image_path))
    score = noise_estimate(im)
    return score > NOISE_THRESHOLD , score


if __name__ == '__main__':
    print(is_noisy('image.png'))