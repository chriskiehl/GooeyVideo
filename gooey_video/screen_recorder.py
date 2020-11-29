"""
Recording the desktop using FFMPEG

Source: https://stackoverflow.com/questions/6766333/capture-windows-screen-with-ffmpeg
"""
from gooey import options

from gooey_video import ffmpeg


def add_parser(parent):
    parser = parent.add_parser('screen_recorder', prog="Record Screen", help='Where does this show??')

    input = parser.add_argument_group('Configure Input', gooey_options=options.ArgumentGroup(
        show_border=True,

    ))

    input.add_argument(
        '--width',
        metavar='Width',
        help='Width of the recorded region',
        widget='IntegerField',
        default=480,
        gooey_options=options.IntegerField(
            min=1,
            max=1920
        ))
    input.add_argument(
        '--height',
        metavar='Height',
        help='Height of the recorded region',
        widget='IntegerField',
        default=640,
        gooey_options=options.IntegerField(
            min=1,
            max=1080
        ))

    input.add_argument(
        '--offset-x',
        metavar='Margin left',
        help='Offsets the recording region from the left',
        widget='IntegerField',
        default=0,
        gooey_options=options.IntegerField(
            min=0,
            max=1080
        ))

    input.add_argument(
        '--offset-y',
        metavar='Margin top',
        help='Offsets the recording region from the top',
        widget='IntegerField',
        default=0,
        gooey_options=options.IntegerField(
            min=0,
            max=1080
        ))

    asdf = parser.add_argument_group('Options', gooey_options=options.ArgumentGroup(
        show_border=True,

    ))
    asdf.add_argument(
        '--framerate',
        type=int,
        default=10,
        widget='IntegerField',
        help='How many frames per second to record', gooey_options=options.IntegerField(
            min=1,
            max=100,
            increment_size=1,
        ))

    asdf.add_argument(
        '--show_region',
        choices=['0', '1'],
        default='1',
        help='Show the Region being recorded')

    asdf.add_argument(
        '--duration',
        help='How long to record the screen (in seconds)',
        metavar='Duration',
        default=10,
        widget='IntegerField',
        gooey_options=options.IntegerField(
            min=1,
            max=99999
        )
    )

    output_group = parser.add_argument_group('Output', gooey_options=options.ArgumentGroup(
        show_border=True
    ))
    output_group.add_argument(
        'output',
        help='Choose where to save the output video',
        default=r'C:\Users\Chris\Desktop\output.mp4',
        widget='FileSaver',
        gooey_options=options.FileSaver(
            wildcard='video files (*.mp4)|*.mp4',
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



    return parser



def run(args):
    template = 'ffmpeg.exe -f gdigrab ' \
               '-framerate {framerate} ' \
               '-show_region {show_region} ' \
               '-offset_x {offset_x} ' \
               '-offset_y {offset_y} ' \
               '-video_size {width}x{height} ' \
               '-t {duration} ' \
               '-i desktop {overwrite} {output}'

    cmd = template.format(**{**vars(args), 'overwrite': '-y' if args.overwrite else ''})
    ffmpeg.run(cmd)


