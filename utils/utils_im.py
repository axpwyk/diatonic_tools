# -*- coding: utf-8 -*-
# //////////////////// HEADER //////////////////// #
import numpy as np
import skimage.util as su
import skimage.transform as st
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
from skimage.io import imread, imsave
import os
DPI = 150
FONTSIZE = DPI // 8
# assign a style
plt.style.use('seaborn-pastel')
# assign a math font
plt.rc('mathtext', **{'fontset': 'cm'})
plt.rc('text', **{'usetex': False})
# assign a chinese font
plt.rc('font', **{'sans-serif': 'Consolas-with-Yahei'})
plt.rc('axes', **{'unicode_minus': False})
# //////////////////// HEADER //////////////////// #


''' ndimage manipulating functions '''


def focus(img, window=(-0.5, 0.5, -0.5, 0.5), if_save=False, file_name='untitled'):
    """ draw a window on `img` and show its contents """
    # img: (h, w, c) image
    # (x_min, x_max, y_min, y_max), normalized coords
    h, w = img.shape[:2]
    w_min = int((window[0]+1)/2*w)
    w_max = int((window[1]+1)/2*w)
    h_min = int((window[2]+1)/2*h)
    h_max = int((window[3]+1)/2*h)

    patch = img[h_min:h_max, w_min:w_max]

    fig, ax = _add_figure_2d(img.shape[1] / DPI, img.shape[0] / DPI, figtype='image')
    # imshow `img` with extent: left top = (0, 0); right bottom = (w, h)
    ax.imshow(img, extent=[0, w, h, 0], zorder=0, cmap='gray')
    # instantiate a rectangle for the window
    rect = plt.Rectangle((w_min, h_min), w_max-w_min, h_max-h_min, fill=False, linewidth=2, color='r', zorder=1)
    # add the rectangle window on `img`
    ax.add_patch(rect)
    if if_save:
        fig.savefig(f'{file_name}_original.svg', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.show()
    plt.close()

    _add_figure_2d(patch.shape[1] / DPI, patch.shape[0] / DPI)
    # imshow `patch`
    plt.imshow(patch, cmap='gray')
    if if_save:
        plt.savefig(f'{file_name}_fig_patch.svg', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.show()
    plt.close()


def paste(img, canvas, i, j, method='replace', export_dtype='float'):
    """ paste `img` on `canvas` with its left-top corner at (i, j) """
    # check dtypes
    img = su.img_as_float(img)
    canvas = su.img_as_float(canvas)
    # check shapes
    if len(img.shape) != 2 or len(img.shape) != 3:
        if len(canvas.shape) != 2 or len(canvas.shape) != 3:
            assert AttributeError('dimensions of input images not all equal to 2 or 3!')
    # check channels
    # all grayscale image
    if len(img.shape) == 2 and len(canvas.shape) == 2:
        pass
    # `img` color image, possible with alpha channel; `canvas` grayscale image
    elif len(img.shape) == 3 and len(canvas.shape) == 2:
        c = img.shape[-1]
        if c == 3:
            canvas = np.stack([canvas]*c, axis=-1)
        if c == 4:
            canvas = np.stack([canvas]*(c-1)+[np.ones((canvas.shape[0], canvas.shape[1]))], axis=-1)
    # `canvas` color image, possible with alpha channel; `img` grayscale image
    elif len(img.shape) == 2 and len(canvas.shape) == 3:
        c = canvas.shape[-1]
        if c == 3:
            img = np.stack([img]*c, axis=-1)
        if c == 4:
            img = np.stack([img]*(c-1)+[np.ones((img.shape[0], img.shape[1]))], axis=-1)
    # all color image
    elif len(img.shape) == 3 and len(canvas.shape) == 3:
        if img.shape[-1] == 3 and canvas.shape[-1] == 4:
            img = np.concatenate([img, np.ones((img.shape[0], img.shape[1], 1))], -1)
        elif img.shape[-1] == 4 and canvas.shape[-1] == 3:
            canvas = np.concatenate([canvas, np.ones((canvas.shape[0], canvas.shape[1], 1))], -1)
        elif img.shape[-1] == canvas.shape[-1]:
            pass
        else:
            assert ValueError('channel number should equal to 3 or 4!')
    # get shapes
    h_i, w_i = img.shape[:2]
    h_c, w_c = canvas.shape[:2]
    # find extent of `img` on `canvas`
    i_min = np.max([0, i])
    i_max = np.min([h_c, i+h_i])
    j_min = np.max([0, j])
    j_max = np.min([w_c, j+w_i])
    # paste `img` on `canvas`
    if method == 'replace':
        canvas[i_min:i_max, j_min:j_max] = img[i_min-i:i_max-i, j_min-j:j_max-j]
    elif method == 'add':
        canvas[i_min:i_max, j_min:j_max] += img[i_min-i:i_max-i, j_min-j:j_max-j]
    else:
        raise ValueError('no such method!')
    # return `canvas`
    if export_dtype == 'float':
        return canvas
    elif export_dtype == 'ubyte':
        return su.img_as_ubyte(canvas)
    else:
        raise ValueError('no such data type for exporting!')


def combine(imgs, num_w=10, padding=5, m_h=5, m_w=5, bg_level_1=1.0, bg_level_2=1.0, export_dtype='float'):
    """ paste contents of `imgs` on a single image with m_h (vertical margin) and m_w (horizontal margin) """
    # dtypes check
    imgs = [su.img_as_float(img) for img in imgs]
    # shapes check
    shapes = [img.shape for img in imgs]
    if not all([len(s) == 2 or len(s) == 3 for s in shapes]):
        assert AttributeError('dimensions of imgs not all 2 or 3!')
    n = len(imgs)
    # find the shape of canvas
    num_h = (n - 1) // num_w + 1
    hs = [imgs[k].shape[0] for k in range(n) if k % num_w == 0]
    ws = [imgs[k].shape[1] for k in range(num_w)]
    h = sum(hs) + m_h*(num_h-1)
    w = sum(ws) + m_w*(num_w-1)
    # canvas initialization
    if all([len(s)==2 for s in shapes]):
        canvas = np.zeros((h, w), np.float) + bg_level_1
        fig = np.zeros((h+2*padding, w+2*padding), np.float) + bg_level_2
    else:
        c = max([s[-1] for s in shapes if len(s)==3])
        canvas = np.zeros((h, w, c), np.float) + bg_level_1
        fig = np.zeros((h+2*padding, w+2*padding, c), np.float) + bg_level_2
    # paste `imgs` on `canvas`
    lt_poses = [(sum(hs[:i])+i*m_h, sum(ws[:j])+j*m_w) for i in range(num_h) for j in range(num_w) if i*num_w+j<n]
    for i, lt_pos in enumerate(lt_poses):
        canvas = paste(imgs[i], canvas, lt_pos[0], lt_pos[1])
    # add padding, i.e. paste `canvas` on `fig`
    fig = paste(canvas, fig, padding, padding)
    # return
    if export_dtype == 'float':
        return fig
    elif export_dtype == 'ubyte':
        return su.img_as_ubyte(fig)
    else:
        raise ValueError('no such data type for exporting!')


def combine_v2(imgs, num_w=10, strides=(10, 10), padding=5, bg_level_1=1.0, bg_level_2=1.0, export_dtype='float'):
    """ paste contents of `imgs` on a single image with `strides` """
    # dtypes check
    imgs = [su.img_as_float(img) for img in imgs]
    # shapes check
    shapes = [img.shape for img in imgs]
    if not all([len(s) == 2 or len(s) == 3 for s in shapes]):
        assert AttributeError('dimensions of imgs not all 2 or 3!')
    # find the shape of canvas
    n = len(imgs)
    num_h = (n - 1) // num_w + 1
    h = strides[0]*(num_h-1) + shapes[-1][0]
    w = strides[1]*(num_w-1) + shapes[-1][1]
    # canvas initialization
    if all([len(s)==2 for s in shapes]):
        canvas = np.zeros((h, w), np.float) + bg_level_1
        fig = np.zeros((h+2*padding, w+2*padding), np.float) + bg_level_2
    else:
        c = max([s[-1] for s in shapes if len(s)==3])
        canvas = np.zeros((h, w, c), np.float) + bg_level_1
        fig = np.zeros((h+2*padding, w+2*padding, c), np.float) + bg_level_2
    # paste `imgs` on `canvas`
    lt_poses = [(strides[0]*i, strides[1]*j) for i in range(num_h) for j in range(num_w) if i*num_w+j<n]
    for i, lt_pos in enumerate(lt_poses):
        canvas = paste(imgs[i], canvas, lt_pos[0], lt_pos[1])
    # add padding, i.e. paste `canvas` on `fig`
    fig = paste(canvas, fig, padding, padding)
    # return
    if export_dtype == 'float':
        return fig
    elif export_dtype == 'ubyte':
        return su.img_as_ubyte(fig)
    else:
        raise ValueError('no such data type for exporting!')


def combine_v2_avg(imgs, num_w=10, strides=(10, 10), padding=5, bg_level_1=1.0, bg_level_2=1.0, export_dtype='float'):
    """ paste contents of `imgs` on a single image with `strides` """
    # dtypes check
    imgs = [su.img_as_float(img) for img in imgs]
    # shapes check
    shapes = [img.shape for img in imgs]
    if not all([len(s) == 2 or len(s) == 3 for s in shapes]):
        assert AttributeError('dimensions of imgs not all 2 or 3!')
    # find the shape of canvas
    n = len(imgs)
    num_h = (n - 1) // num_w + 1
    h = strides[0]*(num_h-1) + shapes[-1][0]
    w = strides[1]*(num_w-1) + shapes[-1][1]
    lt_poses = [(strides[0]*i, strides[1]*j) for i in range(num_h) for j in range(num_w) if i*num_w+j<n]
    # canvas initialization
    if all([len(s)==2 for s in shapes]):
        canvas = np.zeros((h, w), np.float)
        fig = np.zeros((h+2*padding, w+2*padding), np.float) + bg_level_2
    else:
        c = max([s[-1] for s in shapes if len(s)==3])
        canvas = np.zeros((h, w, c), np.float)
        fig = np.zeros((h+2*padding, w+2*padding, c), np.float) + bg_level_2
    # paste `imgs` on `canvas`, average overlapping areas (using ones matrix `counter` to record overlapping times)
    counter = np.zeros((h, w))
    for i, lt_pos in enumerate(lt_poses):
        canvas = paste(imgs[i], canvas, lt_pos[0], lt_pos[1], 'add')
        counter = paste(np.ones((imgs[i].shape[0], imgs[i].shape[1])), counter, lt_pos[0], lt_pos[1], 'add')
    canvas[counter<0.5] = bg_level_1
    counter[counter<0.5] = 1.0
    if len(canvas.shape) == 2:
        canvas = canvas / counter
    else:
        canvas = canvas / np.expand_dims(counter, -1)
    # add padding, i.e. paste `canvas` on `fig`
    fig = paste(canvas, fig, padding, padding)
    # return
    if export_dtype == 'float':
        return fig
    elif export_dtype == 'ubyte':
        return su.img_as_ubyte(fig)
    else:
        raise ValueError('no such data type for exporting!')


def zoom(img, scale):
    # keep the last axis unscaled
    dims = len(img.shape)
    return st.rescale(img, [scale]*(dims-1) + [1], multichannel=False)


def fenc(img):
    fft = np.fft.fft2(img)
    fft_shift = np.fft.fftshift(fft)
    return fft_shift


def fdec(fft_shift):
    ifft = np.fft.ifftshift(fft_shift)
    img = np.fft.ifft2(ifft)
    return img


def standardize(img):
    mu = np.mean(img)
    std = np.std(img)
    return (img - mu) / std


def standardize_0(img):
    img_max = np.max(img)
    img_min = np.min(img)
    A = np.max([abs(img_max), abs(img_min)])
    return img / A


def normalize(img):
    img_max = np.max(img)
    img_min = np.min(img)
    return (img - img_min) / (img_max - img_min)


def std2norm(img):
    return (img + 1) / 2


''' matplotlib figure and axis settings '''


def available_fonts():
    fonts = [font.name for font in fontManager.ttflist if
             os.path.exists(font.fname) and os.stat(font.fname).st_size > 1e6]
    return fonts


def _axes_settings_2d(ax, figtype, title=None):
    if figtype == 'image':
        ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_frame_on(False)
    elif figtype == 'figure':
        # ax.spines['right'].set_color('none')
        # ax.spines['top'].set_color('none')
        # ax.xaxis.set_ticks_position('bottom')
        # ax.spines['bottom'].set_position(('data', 0))
        # ax.yaxis.set_ticks_position('left')
        # ax.spines['left'].set_position(('data', 0))
        pass
    else:
        pass
    ax.margins(x=0.0, y=0.0)
    ax.set_title(title, fontdict={'fontsize': FONTSIZE})
    return ax


def _axes_settings_3d(ax, figtype, title=None):
    if figtype == 'image':
        # ax.set_aspect('equal')
        ax.set_axis_off()
        ax.set_frame_on(False)
        ax.margins(x=0.0, y=0.0, z=0.0)
        ax.view_init(45, 30)
        ax.grid(False)
    elif figtype == 'figure':
        ax.view_init(45, 30)
        ax.grid(False)
    else:
        pass
    ax.margins(x=0.0, y=0.0, z=0.0)
    ax.set_title(title, fontdict={'fontsize': FONTSIZE})
    return ax


def _add_figure_2d(w, h, figtype, title=None):
    # figure settings
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.1, hspace=0.1)
    # axes settings
    ax = _axes_settings_2d(fig.gca(), figtype, title)
    return fig, ax


def _add_figure_3d(w, h, figtype, title=None):
    # figure settings
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.1, hspace=0.1)
    # axes settings
    from mpl_toolkits.mplot3d import Axes3D
    # only when `Axes3D` imported can we use '3d' projection
    # ax = fig.gca(projection='3d')
    ax = _axes_settings_3d(Axes3D(fig), figtype, title)
    return fig, ax


def add_figure_2d(w, h, figtype='image', title=None):
    return _add_figure_2d(w, h, figtype, title)


def add_figure_3d(w, h, figtype='image', title=None):
    return _add_figure_3d(w, h, figtype, title)


def savefig(file_name, transparent=False):
    # pad_inches: Amount of padding around the figure when bbox_inches is 'tight'. If None, use savefig.pad_inches
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.1, transparent=transparent)


''' matplotlib plotting functions '''


def add_hist_rgb(img, bins, figsize=None, title=None, show=False):
    if not len(plt.get_fignums()):
        if figsize:  # figsize (w, h) in pixels
            fig, ax = _add_figure_2d(figsize[0] / DPI, figsize[1] / DPI, figtype='figure', title=title)
        else:
            fig, ax = _add_figure_2d(img.shape[1] / DPI, img.shape[0] / DPI, figtype='figure', title=title)
    else:
        fig, ax = plt.gcf(), plt.gca()
        ax.set_title(title, fontdict={'fontsize': FONTSIZE})

    c = img.shape[-1]
    img = np.reshape(img, [-1, c])

    ax.hist(img[:, 0], bins, rwidth=0.2, color='r')
    ax.hist(img[:, 1], bins, rwidth=0.2, color='g')
    ax.hist(img[:, 2], bins, rwidth=0.2, color='b')

    if show:
        fig.show()
    else:
        return fig, ax


def add_image_2d(img, coords=None, figsize=None, title=None, colormap='gray', show=False):
    if not len(plt.get_fignums()):
        if figsize:  # figure size (w, h) in pixels
            fig, ax = _add_figure_2d(figsize[0] / DPI, figsize[1] / DPI, figtype='image', title=title)
        else:
            fig, ax = _add_figure_2d(img.shape[1] / DPI, img.shape[0] / DPI, figtype='image', title=title)
    else:
        fig, ax = plt.gcf(), plt.gca()
        if title:
            ax.set_title(title, fontdict={'fontsize': FONTSIZE})

    if coords is not None:
        # extent: [left, right, bottom, top]
        # if bottom > top then it will automatically make yaxis_inverted() = True (by default it is False)
        # setting extent may affect aspect
        if coords == 'xy':
            extent = [-1, 1, 1, -1]
        elif coords == 'ij':
            extent = [0, img.shape[1], img.shape[0], 0]
        else:
            extent = coords
        ax.imshow(img, cmap=colormap, zorder=-1, aspect='auto', extent=extent)
    else:
        ax.imshow(img, cmap=colormap, zorder=-1, aspect='auto')

    if show:
        fig.show()
    else:
        return fig, ax


def add_image_3d(img, offset=0, figsize=None, title=None, show=False):
    if not len(plt.get_fignums()):
        if figsize:  # figure size (w, h) in pixels
            fig, ax = _add_figure_3d(figsize[0] / DPI, figsize[1] / DPI, figtype='image', title=title)
        else:
            fig, ax = _add_figure_3d(1024 / DPI, 1024 / DPI, figtype='image', title=title)
    else:
        fig, ax = plt.gcf(), plt.gca()
        ax.set_title(title, fontdict={'fontsize': FONTSIZE})

    h, w = img.shape[0], img.shape[1]
    u, v = np.linspace(-1, 1, h), np.linspace(-1, 1, w)
    u, v = np.meshgrid(u, v)
    X = np.zeros_like(u) + offset; Y = u; Z = -v

    # not good, too slow
    ax.plot_surface(X, Y, Z, facecolors=img, rstride=2, cstride=2)

    if show:
        fig.show()
    else:
        return fig, ax


def add_images_2d(imgs, num_w, wspace=0.1, hspace=0.1, coords=None, figsize=None, titles=None, show=False):
    n = len(imgs)
    num_h = (n - 1) // num_w + 1
    h = sum([imgs[i].shape[0] for i in range(n) if i % num_w == 0])
    w = sum([imgs[j].shape[1] for j in range(num_w)])

    if figsize:
        fig, ax = _add_figure_2d(figsize[0] / DPI, figsize[1] / DPI, figtype='image')
    else:
        fig, ax = _add_figure_2d(w / DPI, h / DPI, figtype='image')
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=wspace, hspace=hspace)
    ax.remove()

    axs = []
    for i in range(n):
        ax = _axes_settings_2d(fig.add_subplot(num_h, num_w, i + 1), 'image')
        axs.append(ax)

        if titles:
            ax.set_title(titles[i], fontdict={'fontsize': FONTSIZE})

        if coords is not None:
            if coords == 'ij':
                extent = [0, imgs[i].shape[1], imgs[i].shape[0], 0]
            elif coords == 'xy':
                extent = [-1, 1, 1, -1]
            else:
                extent = coords
            ax.imshow(imgs[i], cmap='gray', zorder=-1, extent=extent)
        else:
            ax.imshow(imgs[i], cmap='gray', zorder=-1)

    if show:
        fig.show()
    else:
        return fig, axs


def add_images_3d(imgs, offsets=None, title=None, show=False):
    if not offsets:
        offsets = np.arange(len(imgs))

    for i, img in enumerate(imgs):
        add_image_3d(img, offsets[i], title=None, show=False)
    plt.gca().set_title(title)

    if show:
        plt.gcf().show()
    else:
        return plt.gcf(), plt.gca()


def add_displacement_grid_2d(grid, indexing='xy', figsize=None, title=None, show=False):
    ''' add displacement grid plot

    inputs:
        grid        image grid used to show deform field, identity grid + displacement vector field
                    numpy ndarray, shape: (h, w, 2), value range: (-1, 1) in 'xy' indexing

    comments:
        * important: extent of the image must satisfy bottom > top, e.g. [-1, 1, 1, -1]
        * important: if no imshow, y axis will automatically invert
        * important: 2D image: x-y coords; 3D image: z-x-y coords
        * author: Timmymm
        * source: CSDN
        * url: https://blog.csdn.net/weixin_41699811/article/details/84259755
    '''
    if not len(plt.get_fignums()):
        if figsize:
            fig, ax = _add_figure_2d(figsize[0] / DPI, figsize[1] / DPI, figtype='image', title=title)
        else:
            fig, ax = _add_figure_2d(grid.shape[1] / DPI, grid.shape[0] / DPI, figtype='image', title=title)
    else:
        fig, ax = plt.gcf(), plt.gca()
        if title:
            ax.set_title(title, fontdict={'fontsize': FONTSIZE})

    if not ax.yaxis_inverted():
        ax.invert_yaxis()

    smooth_level = 1
    step_length = 32

    h, w = grid.shape[0], grid.shape[1]

    if indexing == 'xy':
        pixel_size = 2 / grid.shape[0], 2 / grid.shape[1]
        x = np.linspace(-1+pixel_size[1]/2, 1-pixel_size[1]/2, w*smooth_level)
        y = np.linspace(-1+pixel_size[0]/2, 1-pixel_size[1]/2, h*smooth_level)
        X, Y = np.meshgrid(x, y, indexing='xy')
        # here determines whether input grid is of format 'xy' or 'ij', here it's 'xy'
        Zx = st.rescale(grid[:, :, 0] + abs(grid.min()), [smooth_level, smooth_level], multichannel=False, order=3, mode='wrap')
        Zy = st.rescale(grid[:, :, 1] + abs(grid.min()), [smooth_level, smooth_level], multichannel=False, order=3, mode='wrap')
        max_Zx, min_Zx = np.max(Zx), np.min(Zx)
        max_Zy, min_Zy = np.max(Zy), np.min(Zy)
        x_steps = np.linspace(min_Zx, max_Zx, step_length)
        x_steps[0] = x_steps[0] + 1e-5
        x_steps[-1] = x_steps[-1] - 1e-5
        y_steps = np.linspace(min_Zy, max_Zy, step_length * (h // w))
        y_steps[0] = y_steps[0] + 1e-5
        y_steps[-1] = y_steps[-1] - 1e-5
        # plot grid
        ax.contour(X, Y, Zx, x_steps, colors=[[1.0, 1.0, 0.0]], linewidths=0.5, zorder=1)
        ax.contour(X, Y, Zy, y_steps, colors=[[1.0, 1.0, 0.0]], linewidths=0.5, zorder=1)

    elif indexing == 'ij':
        pixel_size = 1, 1
        i = np.linspace(pixel_size[0]/2, h-pixel_size[0]/2, h*smooth_level)
        j = np.linspace(pixel_size[1]/2, w-pixel_size[1]/2, w*smooth_level)
        I, J = np.meshgrid(i, j, indexing='ij')
        # here determines whether input grid is of format 'xy' or 'ij', here it's 'ij'
        Zi = st.rescale(grid[:, :, 0] + abs(grid.min()), [smooth_level, smooth_level], multichannel=False, order=3, mode='wrap')
        Zj = st.rescale(grid[:, :, 1] + abs(grid.min()), [smooth_level, smooth_level], multichannel=False, order=3, mode='wrap')
        max_Zi, min_Zi = np.max(Zi), np.min(Zi)
        max_Zj, min_Zj = np.max(Zj), np.min(Zj)
        i_steps = np.linspace(min_Zi, max_Zi, step_length)
        i_steps[0] = i_steps[0] + 1e-5
        i_steps[-1] = i_steps[-1] - 1e-5
        j_steps = np.linspace(min_Zj, max_Zj, step_length * (h // w))
        j_steps[0] = j_steps[0] + 1e-5
        j_steps[-1] = j_steps[-1] - 1e-5
        # plot grid
        ax.contour(J, I, Zj, j_steps, colors=[[1.0, 1.0, 0.0]], linewidths=0.5, zorder=1)
        ax.contour(J, I, Zi, i_steps, colors=[[1.0, 1.0, 0.0]], linewidths=0.5, zorder=1)

    else: raise ValueError("Argument `indexing` must be 'xy' or 'ij'!")

    if show:
        fig.show()
    else:
        return fig, ax


def add_displacement_grid_3d(grid, figsize=None, title=None, show=False):
    # TODO: add_displacement_grid_3d
    pass


def add_displacement_vector_field_2d(field, indexing='xy', figsize=None, title=None, show=False):
    ''' x-y coordinate '''
    if not len(plt.get_fignums()):
        if figsize:
            fig, ax = _add_figure_2d(figsize[0] / DPI, figsize[1] / DPI, figtype='image', title=title)
        else:
            fig, ax = _add_figure_2d(field.shape[1] / DPI, field.shape[0] / DPI, figtype='image', title=title)
    else:
        fig, ax = plt.gcf(), plt.gca()
        if title:
            ax.set_title(title, fontdict={'fontsize': FONTSIZE})

    if not ax.yaxis_inverted():
        ax.invert_yaxis()

    h, w = field.shape[0], field.shape[1]

    if indexing == 'xy':
        pixel_size = 2 / h, 2 / w
        x = np.linspace(-1+pixel_size[1]/2, 1-pixel_size[1]/2, w)
        y = np.linspace(-1+pixel_size[0]/2, 1-pixel_size[0]/2, h)
        X, Y = np.meshgrid(x, y, indexing='xy')
        # from documents:
        #
        # 'uv': The arrow axis aspect ratio is 1 so that if U == V the orientation of the arrow
        #       on the plot is 45 degrees counter-clockwise from the horizontal axis (positive to the right).
        #       Use this if the arrows symbolize a quantity that is not based on X, Y data coordinates.
        #
        # 'xy': Arrows point from (x,y) to (x+u, y+v). Use this for plotting a gradient field, for example.
        #
        # Note: inverting a data axis will correspondingly invert the arrows *only with* angles='xy'.
        colors = np.concatenate([field, np.ones_like(field)], axis=-1)
        colors = np.hypot(field[:, :, 0], field[:, :, 1])
        ax.quiver(X, Y, field[:, :, 0], field[:, :, 1], colors, angles='xy', width=0.002, zorder=1)

    elif indexing == 'ij':
        pixel_size = 1, 1
        i = np.linspace(pixel_size[0] / 2, h - pixel_size[0] / 2, h)
        j = np.linspace(pixel_size[1] / 2, w - pixel_size[1] / 2, w)
        I, J = np.meshgrid(i, j, indexing='ij')
        # ax.quiver only supports 'xy' coordinates, so J, I, ~[1], ~[0]
        colors = np.concatenate([normalize(np.roll(field, 1, -1)), np.ones_like(field)], axis=-1)
        colors = np.hypot(field[:, :, 1], field[:, :, 0])
        ax.quiver(J, I, field[:, :, 1], field[:, :, 0], colors, angles='xy', width=0.002, zorder=1)

    if show:
        fig.show()
    else:
        return fig, ax


def add_displacement_vector_field_3d(field, figsize=None, title=None, show=False):
    if not len(plt.get_fignums()):
        if figsize:
            fig, ax = _add_figure_3d(figsize[0] / DPI, figsize[1] / DPI, figtype='image', title=title)
        else:
            fig, ax = _add_figure_3d(4, 4, figtype='image', title=title)
    else:
        fig, ax = plt.gcf(), plt.gca()
        if title:
            ax.set_title(title, fontdict={'fontsize': FONTSIZE})

    z = np.linspace(-1, 1, field.shape[0])
    y = np.linspace(-1, 1, field.shape[1])
    x = np.linspace(-1, 1, field.shape[2])

    X, Y, Z = np.meshgrid(x, y, z)

    ax.quiver(X, Y, Z, field[:, :, :, 0], field[:, :, :, 1], field[:, :, :, 2], color='r', length=0.1)

    if show:
        fig.show()
    else:
        return fig, ax


def add_displacement_vector_image_2d(field, alpha=0.5, figsize=None, title=None, show=False):
    if not len(plt.get_fignums()):
        if figsize:
            fig, ax = _add_figure_2d(figsize[0] / DPI, figsize[1] / DPI, figtype='image', title=title)
        else:
            fig, ax = _add_figure_2d(field.shape[1] / DPI, field.shape[0] / DPI, figtype='image', title=title)
    else:
        fig, ax = plt.gcf(), plt.gca()
        if title:
            ax.set_title(title, fontdict={'fontsize': FONTSIZE})

    h, w, d = field.shape
    field = (field + 1) / 2
    # x: red direction | y: green direction | z: blue direction
    field = np.stack([field[:, :, 0], field[:, :, 1], np.zeros((h, w))], -1)

    ax.imshow(field, zorder=2, alpha=alpha, extent=[-1, 1, 1, -1])

    if show:
        fig.show()
    else:
        return fig, ax


def add_displacement_vector_image_3d(field, alpha=0.5, figsize=None, title=None, show=False):
    if not len(plt.get_fignums()):
        if figsize:
            fig, ax = _add_figure_2d(figsize[0] / DPI, figsize[1] / DPI, figtype='image', title=title)
        else:
            fig, ax = _add_figure_2d(field.shape[1] / DPI, field.shape[0] / DPI, figtype='image', title=title)
    else:
        fig, ax = plt.gcf(), plt.gca()
    if title:
        ax.set_title(title, fontdict={'fontsize': FONTSIZE})

    h, w, d = field.shape
    field = (field + 1) / 2
    # x: red direction | y: green direction | z: blue direction
    field = np.stack([field[:, :, 0], field[:, :, 1], field[:, :, 2]], -1)

    ax.imshow(field, zorder=2, alpha=alpha, extent=[-1, 1, 1, -1])

    if show:
        fig.show()
    else:
        return fig, ax


def add_text_matrix(s='276951438', num_h=3, padding=0.2, fontsize=FONTSIZE, show=False):
    fig, ax = _add_figure_2d(10, 10, 'image')
    num_w = (len(s) - 1) // num_h + 1
    xs = np.linspace(padding, 1-padding, num_w)[::-1]
    ys = np.linspace(padding, 1-padding, num_h)[::-1]
    xys = np.meshgrid(xs, ys)
    xys = np.transpose(xys, [1, 2, 0])
    xys = np.reshape(xys, [-1, 2])

    plt.rc('font', **{'sans-serif': 'UD Digi Kyokasho N-R'})

    for i in range(len(s)):
        ax.annotate(s[i], xys[i][::-1], fontsize=fontsize, ha='center', va='center', bbox={'linewidth': 1, 'edgecolor': 'r'})
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    if show:
        plt.show()


def latex_array(mat, rlabels=None, clabels=None, precision=3):
    # np.set_printoptions(formatter={'float_kind': lambda x: '%.3f' % x})
    f = lambda x: np.format_float_positional(x, precision=precision)
    h, w = mat.shape
    # header of array
    s = ''
    if rlabels:
        s += '\\begin{array}{r|rr}\n'
    else:
        s += '\\begin{array}{r}\n'
    s += "\t\\hline\n"
    if clabels:
        if len(clabels) != w:
            raise ValueError('Wrong clabels length!')
        s += '\t'
        s += '~ & '
        for clabel in clabels[:-1]:
            clabel = r'\title{' + clabel + r'}'
            s += f'{clabel} & '
        clabel = r'\title{' + clabels[-1] + r'}'
        s += f'{clabel} \\\\\n'
        s += '\t\\hline\n'
    # contents of array
    for i in range(h):
        s_temp = '\t'
        if rlabels:
            if len(rlabels) != h:
                raise ValueError('Wrong rlabels length!')
            rlabel = rlabels[i]
            rlabel = r'\title{' + rlabel + r'}'
            s_temp += f'{rlabel} & '
        for j in range(w-1):
            s_temp += f'{f(mat[i, j])} & '
        s_temp += f'{f(mat[i, w-1])} \\\\\n'
        s += s_temp
    s += '\t\\hline\n'
    s += '\\end{array}'
    return s
