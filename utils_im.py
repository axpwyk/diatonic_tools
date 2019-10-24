# -*- coding: utf-8 -*-
# //////////////////// HEADER //////////////////// #
import numpy as np
import skimage.util as su
from scipy.ndimage import zoom
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager
import os
DPI = 150
# //////////////////// HEADER //////////////////// #


def _figure_settings(w, h, dpi=DPI, text=None):
    # assign a math font
    mpl.rcParams['mathtext.fontset'] = 'cm'
    # assign a chinese font
    mpl.rcParams['font.sans-serif'] = ['STKaiti']
    mpl.rcParams['axes.unicode_minus'] = False
    # figure settings
    fig = plt.figure(figsize=(w, h), dpi=dpi)
    ax = fig.gca(aspect='equal')
    ax.set_frame_on(False)
    ax.axis('off')
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    # ax.spines['left'].set_color('none')
    # ax.spines['bottom'].set_color('none')
    plt.xticks(()), plt.yticks(())
    plt.subplots_adjust(right=0.97, left=0.03, bottom=0.03, top=0.97, wspace=0.1, hspace=0.1)
    plt.title(text, fontdict={'fontsize': 32})
    return fig, ax


def _figure_settings_for_axes3d(text=None):
    mpl.rcParams['mathtext.fontset'] = 'cm'
    fig = plt.figure(figsize=(10, 10), dpi=DPI)
    from mpl_toolkits.mplot3d import Axes3D
    # only when `Axes3D` imported can we use '3d' projection
    # ax = fig.gca(projection='3d')
    ax = Axes3D(fig)
    ax.set_frame_on(False)
    ax.axis('off')
    ax.view_init(45, 30)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    plt.subplots_adjust(right=0.97, left=0.03, bottom=0.03, top=0.97, wspace=0.1, hspace=0.1)
    plt.title(text)
    return fig, ax


def focus(img, window=(-0.5, 0.5, -0.5, 0.5), if_save=False, save_path='', file_name='fig'):
    """ draw a window on `img` and show its contents """
    # (x_min, x_max, y_min, y_max), normalized coords
    h, w = img.shape[:2]
    w_min = int((window[0]+1)/2*w)
    w_max = int((window[1]+1)/2*w)
    h_min = int((window[2]+1)/2*h)
    h_max = int((window[3]+1)/2*h)

    patch = img[h_min:h_max, w_min:w_max]

    _figure_settings(img.shape[1]/DPI, img.shape[0]/DPI)
    # imshow `img` with extent: left top = (0, 0); right bottom = (w, h)
    plt.imshow(img, extent=[0, w, h, 0], zorder=0, cmap='gray')
    # instantiate a rectangle for the window
    rect = plt.Rectangle((w_min, h_min), w_max-w_min, h_max-h_min, fill=False, linewidth=2, color='r', zorder=1)
    # add the rectangle window on `img`
    plt.gca().add_patch(rect)
    if if_save:
        plt.savefig(os.path.join(save_path, f'{file_name}_original.svg'))
    plt.show()
    plt.close()

    _figure_settings(patch.shape[1]/DPI, patch.shape[0]/DPI)
    # imshow `patch`
    plt.imshow(patch, cmap='gray')
    if if_save:
        plt.savefig(os.path.join(save_path, f'{file_name}_fig_patch.svg'))
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


def zoom_rgb(img, scale):
    # keep the last axis unscaled
    dims = len(img.shape)
    return zoom(img, [scale]*(dims-1) + [1])


def available_fonts():
    fonts = [font.name for font in fontManager.ttflist if
             os.path.exists(font.fname) and os.stat(font.fname).st_size > 1e6]
    return fonts


def figure_settings(w, h, dpi=DPI, text=None):
    return _figure_settings(h, w, dpi, text)


def plt_add_hist_rgb(img, bins, text=None, show=True):
    """ draw rgb histogram """
    c = img.shape[-1]
    img = np.reshape(img, [-1, c])

    plt.hist(img[:, 0], bins, rwidth=0.2, color='r')
    plt.hist(img[:, 1], bins, rwidth=0.2, color='g')
    plt.hist(img[:, 2], bins, rwidth=0.2, color='b')

    if text:
        plt.title(text)

    if show:
        plt.show()


def plt_add_image_2d(img, text=None, show=True, coords=False):
    if not plt.fignum_exists(1):
       fig, ax = _figure_settings(img.shape[1]/DPI, img.shape[0]/DPI, text=text)
    else:
        ax = plt.gca()
        ax.set_title(text)

    if coords:
        # extent: [left, right, bottom, top]
        # if bottom > top then it will automatically make yaxis_inverted() = True (by default it is False)
        ax.imshow(img, cmap='gray', zorder=-1, extent=[-1, 1, 1, -1])
    else:
        ax.imshow(img, cmap='gray', zorder=-1)

    if show:
        plt.show()


def plt_add_image_3d(img, z=0, text=None, show=True):
    if not plt.fignum_exists(1):
        fig, ax = _figure_settings_for_axes3d(text=text)
    else:
        ax = plt.gca()
        ax.set_title(text)
    if not ax.yaxis_inverted():
        ax.invert_yaxis()

    h, w = img.shape[0], img.shape[1]
    u, v = np.linspace(-1, 1, w), np.linspace(-1, 1, h)
    u, v = np.meshgrid(u, v)
    X = np.zeros_like(u) + z; Y = u; Z = v

    ax.plot_surface(X, Y, Z, facecolors=img, linewidth=0, rcount=64, ccount=64)

    if show:
        plt.show()


def plt_add_images_2d(imgs, num_w, titles=None, h_space=0.025, w_space=0.025, text=None, show=True, coords=False):
    n = len(imgs)
    num_h = (n - 1) // num_w + 1
    hs = [imgs[i].shape[0] for i in range(n) if i % num_w == 0]
    ws = [imgs[j].shape[1] for j in range(num_w)]
    h = sum(hs)
    w = sum(ws)

    fig, ax = _figure_settings(w/DPI, h/DPI, text=text)

    plt.subplots_adjust(wspace=w_space, hspace=h_space)
    for i in range(n):
        ax = fig.add_subplot(num_h, num_w, i+1)
        # ax.set_aspect('equal')
        ax.set_xticks([]), ax.set_yticks([])
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['left'].set_color('none')
        ax.spines['bottom'].set_color('none')
        if titles:
            ax.set_title(titles[i], fontdict={'fontsize': 32})
        if coords:
            ax.imshow(imgs[i], cmap='gray', zorder=-1, extent=[-1, 1, 1, -1])
        else:
            ax.imshow(imgs[i], cmap='gray', zorder=-1)

    '''Axes Method'''
    # for i in range(1, 4+1):
    #     ax = plt.axes([0, 0, 0.5, 0.5], aspect='equal')
    #     ax.set_xticks([])
    #     ax.set_yticks([])
    if show:
        plt.show()


def plt_add_images_3d(imgs, zs=None, text=None, show=True):
    if not zs:
        zs = np.linspace(0, len(imgs), len(imgs))
    for i, img in enumerate(imgs):
        plt_add_image_3d(img, zs[i], text=None, show=False)
    plt.title(text)
    if show:
        plt.show()


def plt_add_displacement_grid_2d(grid, text=None, show=True):
    ''' add displacement grid plot

    inputs:
        grid        image grid used to show deform field
                    numpy ndarray, shape: (h, w, 2), value range: (-1, 1)

    comments:
        * important: extent of the image must satisfy bottom > top, e.g. [-1, 1, 1, -1]
        * important: if no imshow, y axis will automatically invert
        * important: 2D image: x-y coords; 3D image: z-x-y coords
        * author: Timmymm
        * source: CSDN
        * url: https://blog.csdn.net/weixin_41699811/article/details/84259755
    '''
    if not plt.fignum_exists(1):
        fig, ax = _figure_settings(grid.shape[1]/DPI, grid.shape[0]/DPI, text=text)
    else:
        ax = plt.gca()
        ax.set_title(text)
    if not ax.yaxis_inverted():
        ax.invert_yaxis()

    h = grid.shape[0]; w = grid.shape[1]
    y = np.linspace(-1, 1, h)
    x = np.linspace(-1, 1, w)

    Y, X = np.meshgrid(y, x, indexing='ij')

    Z1 = grid[:, :, 0] + 2
    Z2 = grid[:, :, 1] + 2

    max_Z1, min_Z1 = np.max(Z1), np.min(Z1)
    max_Z2, min_Z2 = np.max(Z2), np.min(Z2)
    x_steps = 32
    ax.contour(X, Y, Z1, np.linspace(min_Z1, max_Z1, x_steps), colors='r', linewidths=0.5, zorder=1)
    ax.contour(X, Y, Z2, np.linspace(min_Z2, max_Z2, x_steps*int(h/w)), colors='r', linewidths=0.5, zorder=1)

    if show:
        plt.show()


def plt_add_displacement_grid_3d(grid, text=None, show=True):
    # TODO: plt_add_displacement_grid_3d
    pass


def plt_add_displacement_vector_field_2d(field, text=None, show=True):
    if not plt.fignum_exists(1):
        fig, ax = _figure_settings(field.shape[1]/DPI, field.shape[0]/DPI, text=text)
    else:
        ax = plt.gca()
        ax.set_title(text)
    if not ax.yaxis_inverted():
        ax.invert_yaxis()

    y = np.linspace(-1, 1, field.shape[0])
    x = np.linspace(-1, 1, field.shape[1])

    Y, X = np.meshgrid(y, x, indexing='ij')

    # from documents:
    #
    # 'uv': The arrow axis aspect ratio is 1 so that if U == V the orientation of the arrow
    #       on the plot is 45 degrees counter-clockwise from the horizontal axis (positive to the right).
    #       Use this if the arrows symbolize a quantity that is not based on X, Y data coordinates.
    #
    # 'xy': Arrows point from (x,y) to (x+u, y+v). Use this for plotting a gradient field, for example.
    #
    # Note: inverting a data axis will correspondingly invert the arrows *only with* angles='xy'.
    ax.quiver(X, Y, field[:, :, 0], field[:, :, 1], angles='xy', color='r', width=0.002, zorder=2)

    if show:
        plt.show()


def plt_add_displacement_vector_field_3d(field, text=None, show=True):
    if not plt.fignum_exists(1):
        fig, ax = _figure_settings_for_axes3d(text=text)
    else:
        ax = plt.gca()
        ax.set_title(text)

    z = np.linspace(-1, 1, field.shape[0])
    y = np.linspace(-1, 1, field.shape[1])
    x = np.linspace(-1, 1, field.shape[2])

    Z, Y, X = np.meshgrid(z, y, x, indexing='ij')

    ax.quiver(X, Y, Z, field[:, :, :, 0], field[:, :, :, 1], field[:, :, :, 2], color='r', length=0.1)

    if show:
        plt.show()


def plt_add_displacement_vector_image_2d(field, text=None, alpha=0.5, show=True):
    if not plt.fignum_exists(1):
        fig, ax = _figure_settings(field.shape[1]/DPI, field.shape[0]/DPI, text=text)
    else:
        ax = plt.gca()
        ax.set_title(text)

    h, w, d = field.shape
    field = (field + 1) / 2
    b = np.zeros((h, w))
    field = np.stack([field[:, :, 0], b, field[:, :, 1]], -1)
    # field = np.swapaxes(field, 0, 1)

    ax.imshow(field, zorder=2, alpha=alpha, extent=[-1, 1, 1, -1])

    if show:
        plt.show()


def plt_add_displacement_vector_image_3d(field, text=None, alpha=0.5, show=True):
    if not plt.fignum_exists(1):
        fig, ax = _figure_settings(field.shape[1]/DPI, field.shape[0]/DPI, text=text)
    else:
        ax = plt.gca()
        ax.set_title(text)

    h, w, d = field.shape
    field = (field + 1) / 2
    # field = np.swapaxes(field, 0, 1)

    ax.imshow(field, zorder=2, alpha=alpha, extent=[-1, 1, 1, -1])

    if show:
        plt.show()


def plt_add_3d_test():
    import matplotlib.tri as mtri

    fig = plt.figure(figsize=plt.figaspect(1), dpi=DPI)
    u = np.linspace(-2, 2, endpoint=True, num=20)
    v = np.linspace(-2, 2, endpoint=True, num=20)
    u, v = np.meshgrid(u, v)
    u, v = u.flatten(), v.flatten()
    x = u
    y = v
    z = 1 / 2 * u ** 2 - 1 / 2 * v ** 2
    tri = mtri.Triangulation(u, v)
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.plot_trisurf(x, y, z, triangles=tri.triangles, cmap='spring')
    # ax.plot_wireframe(x, y, z)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    # ax.set_zlim(-1, 1)
    plt.savefig('3d_plot.svg')
    plt.show()
    plt.close()


def plt_add_text_matrix(s='123456789', num_h=3, fontsize=32):
    _figure_settings(10, 10)

    sizes = ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large']
    for i in range(0, len(s)):
        xy = 0.9 - 0.1*(i//num_h), 0.9 - 0.1*(i%num_h)
        idx = np.random.randint(2, 5)
        # circ = plt.Rectangle(xy, 0.03, 0.03, fill=True, linewidth=0.2, edgecolor='r', facecolor='lightgray')
        # plt.gca().add_patch(circ)
        plt.text(xy[0], xy[1], s[i], fontdict={'size': fontsize}, ha='center',
                 bbox={'linewidth': 1, 'edgecolor': 'r', 'facecolor': 'white'})
    plt.savefig('text_array.svg')
    plt.show()
    plt.clf()
    plt.close()


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
    s += '\t\\hline\n'
    if clabels:
        if len(clabels) != w:
            raise ValueError('Wrong clabels length!')
        s += '\t'
        s += '~ & '
        for clabel in clabels[:-1]:
            clabel = r'\text{' + clabel + r'}'
            s += f'{clabel} & '
        clabel = r'\text{' + clabels[-1] + r'}'
        s += f'{clabel} \\\\\n'
        s += '\t\\hline\n'
    # contents of array
    for i in range(h):
        s_temp = '\t'
        if rlabels:
            if len(rlabels) != h:
                raise ValueError('Wrong rlabels length!')
            rlabel = rlabels[i]
            rlabel = r'\text{' + rlabel + r'}'
            s_temp += f'{rlabel} & '
        for j in range(w-1):
            s_temp += f'{f(mat[i, j])} & '
        s_temp += f'{f(mat[i, w-1])} \\\\\n'
        s += s_temp
    s += '\t\\hline\n'
    s += '\\end{array}'
    return s


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


def standardize_zero_mean(img):
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
