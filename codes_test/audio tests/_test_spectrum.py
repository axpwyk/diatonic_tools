from scipy.io.wavfile import read
from audio import draw_spectrum_mono
from utils.utils_im import *
import skimage.transform as tf
from skimage.io import imsave
import pathlib


'''非线性函数'''
def nl1(x):
    y = 1/2*np.sin(np.pi*(x-1/2))+1/2
    return y


def nl2(x):
    return np.sin(np.pi/2*x)


def nl3(x, a, delta_a):
    A = (1/2+delta_a-a)/(a**2-a)
    B = 1-A
    return A*x**2+B*x


'''读取数据'''
path = pathlib.Path(r'../../audio/korekuraide.mp3')
sampling_frequency, wav = read(path)
wav = wav / 32768
wav = wav[:, 0]

# sampling_frequency = 44100
# wav = sum([np.sin(2*np.pi*440*np.power(2, -9/12)*t*np.linspace(0, 4, 4*sampling_frequency)) for t in range(1, 10)])/9

'''确定参数'''
window_samples = 4096
freq_step = sampling_frequency / window_samples
time_range = [0, 120]

'''获取初始频谱（对数变换+标准化）'''
spectrum_L = draw_spectrum_mono(wav[sampling_frequency*time_range[0]:sampling_frequency*time_range[1]], sampling_frequency, window_samples)
spectrum_L = np.log(spectrum_L+1)
spectrum_L = (spectrum_L-spectrum_L.min())/(spectrum_L.max()-spectrum_L.min())

'''半对数重采样'''
logarithmic = True
if logarithmic:
    num_h, num_w = spectrum_L.shape
    W, H = np.meshgrid(np.arange(num_w), np.linspace(-48, 67, num_h))
    H = 440*np.power(2, H/12)
    H = H*(window_samples/sampling_frequency)
    grid = np.array([H, W])
    print(f'grid.shape: {grid.shape}')
    spectrum_L = tf.warp(spectrum_L, grid)

    '''绘制钢琴卷帘'''
    # lo = 440*np.power(2, -48/12)*window_samples/sampling_frequency
    # hi = 440*np.power(2, 67/12)*window_samples/sampling_frequency
    lo = 0
    hi = window_samples//2
    keys_center = np.linspace(lo, hi, 67+48+1, endpoint=True)
    keys_width = (hi-lo)/(67+48)
    keys_length = 96
    keys = np.ones((window_samples//2, keys_length))
    for idx, cur_key_center in enumerate(keys_center):
        if (idx+7)%12 in [0, 2, 4, 6, 7, 9, 11]:
            if idx not in [0, 67+48]:
                keys[int(cur_key_center-keys_width/2), :] = 0.0
                keys[int(cur_key_center+keys_width/2), :] = 0.0
        else:
            keys[int(cur_key_center-keys_width/2):int(cur_key_center+keys_width/2), :] = 0.0
    keys[:, :2] = 0.0
    spectrum_L = np.concatenate([np.flipud(keys), spectrum_L], axis=1)

'''图像后处理'''
for _ in range(2):
    spectrum_L = nl1(spectrum_L)
    spectrum_L = nl3(spectrum_L, 0.85, 0.3)
spectrum_L = np.flipud(spectrum_L)

'''绘制图像'''
# plt_add_image_2d(spectrum_L, show=True)
# plt.xticks(np.linspace(0, (time_range[1]-time_range[0])*sampling_frequency, 50), np.linspace(time_range[0], time_range[1], 50))
# plt.yticks(np.linspace(0, window_samples/2, 10), np.linspace(0, sampling_frequency/2, 10))
# plt.imshow(spectrum_L)

'''存储图像'''
imsave(pathlib.Path(f'../output/sd_{time_range[0]}s-{time_range[1]}s_spectrum-L_pp01.png'), spectrum_L)
