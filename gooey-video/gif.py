"""
Creating a high quality GIF using FFMPEG

Source: http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html
"""
from gooey import Gooey, GooeyParser, options
import subprocess

import ffmpeg


def add_parser(parent):
    parser = parent.add_parser('gif', prog="High Quality GIF", help='Where does this show??')
    input_group = parser.add_argument_group('Input', gooey_options=options.ArgumentGroup(
        show_border=True
    ))
    input_group.add_argument(
        'input',
        metavar='Input',
        help='Source video you want to convert to a high quality gif (pronounced "jif")',
        widget='FileChooser',
        gooey_options=options.FileChooser(
            wildcard='Video files (*.mp4)|*.mp4|All files (*.*)|*.*',
            full_width=True
    ))
    scale = parser.add_argument_group('Crop Settings', gooey_options=options.ArgumentGroup(
        show_border=True
    ))

    scale.add_argument(
        '--scale-width',
        metavar='Width',
        help='Scale the video to this width (-1 preserves aspect ratio)',
        default=-1,
        widget='IntegerField',
        gooey_options=options.IntegerField(
            min=-1,
            max=1920
        ))
    scale.add_argument(
        '--scale-height',
        metavar='Height',
        help='Scale the video to this height (-1 preserves aspect ratio)',
        default=-1,
        widget='IntegerField',
        gooey_options=options.IntegerField(
            min=-2,
            max=1080
        ))
    output_group = parser.add_argument_group('Output', gooey_options=options.ArgumentGroup(
        show_border=True
    ))
    output_group.add_argument(
        'output',
        help='Choose where to save the output video',
        default=r'C:\Users\Chris\Desktop\output.mp4',
        widget='FileSaver',
        gooey_options=options.FileSaver(
            wildcard='video files (*.gif)|*.gif',
            default_file='output.mp4',
            full_width=True
        ))

    output_group.add_argument(
        '--overwrite',
        metavar='Overwrite existing',
        help='Overwrite the output video if it already exists?',
        action='store_const',
        default=True,
        const='-y',
        widget='CheckBox')
    output_group.add_argument(
        '--fps',
        metavar='Frames per second',
        help='FPS of the output GIF',
        default=15,
        widget='IntegerField',
        gooey_options=options.IntegerField(
            min=1,
            max=100
        ))




def run(args):
    palette_template = 'ffmpeg.exe -i "{input}" ' \
                       '-vf "scale={scale_width}:{scale_height}:flags=lanczos,palettegen" ' \
                       '-y ' \
                       'palette.png'
    gif_template = 'ffmpeg.exe -i {input} ' \
                   '-i palette.png ' \
                   '-lavfi "fps={fps},scale={scale_width}:{scale_height}:flags=lanczos [x]; [x][1:v] paletteuse" -y ' \
                   '{output}'

    ffmpeg.run(palette_template.format(**vars(args)))
    import time
    time.sleep(1)
    print('running next one')
    ffmpeg.run(gif_template.format(**vars(args)))

