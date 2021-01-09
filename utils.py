import re
import colorsys as cs


''' ----------------------------------------------------------------------------------------- '''
''' ************************************ color utilities ************************************ '''
''' ----------------------------------------------------------------------------------------- '''


def hex2float(hex_color_string):
    search_obj = re.search(r'(?<=#)(?P<r>[\dabcdef]{2})(?P<g>[\dabcdef]{2})(?P<b>[\dabcdef]{2})', hex_color_string)
    return [int(search_obj[s], 16) / 255 for s in ['r', 'g', 'b']]


def float2hex(dec_color_list):
    return '#' + ''.join([f'{int(k * 255):02x}' for k in dec_color_list])


def rgb_shader(t, t_min=0, t_max=1, color1=(0.94, 0.02, 0.55), color2=(0.11, 0.78, 0.72)):
    """
    Linear interpolation between 2 colors `color1` and `color2`
    :param t: variable
    :param t_min: lower bound of variable `t`
    :param t_max: upper bound of variable `t`
    :param color1: hex or float color in RGB
    :param color2: hex or float color in RGB
    :return: float color in RGB
    """
    # proportion of `t`
    t = (t - t_min) / (t_max - t_min)
    # if input colors are hex strings, convert them to float triples
    if isinstance(color1, str):
        color1 = hex2float(color1)
    if isinstance(color2, str):
        color2 = hex2float(color2)
    # convert `color1` and `color2` to yiq space for better gradient visuals
    color1 = cs.rgb_to_yiq(*color1)
    color2 = cs.rgb_to_yiq(*color2)
    # return color at `t` using linear interpolation
    return cs.yiq_to_rgb(*[t * c2 + (1.00-t) * c1 for (c1, c2) in zip(color1, color2)])


def hsv_shader(t, t_min=0, t_max=1, color1=(0.00, 0.80, 0.75), color2=(1.00, 0.80, 0.75)):
    # proportion of `t`
    t = (t - t_min) / (t_max - t_min)
    # return color at `t` using linear interpolation
    return cs.hsv_to_rgb(*[t * c2 + (1.00-t) * c1 for (c1, c2) in zip(color1, color2)])


def cst_shader(t, t_min=0, t_max=1, color=(1.00, 0.00, 0.00)):
    return color
