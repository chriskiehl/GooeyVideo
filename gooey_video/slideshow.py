from gooey import options

from gooey_video import ffmpeg


def add_parser(parent):
    parser = parent.add_parser('slideshow', prog="Slideshow / Timelapse", help='Where does this show??')
    input_group = parser.add_argument_group('Input', gooey_options=options.ArgumentGroup(
        show_border=True
    ))
    # basic details
    input_group.add_argument(
        'dir',
        metavar='Input',
        help='Directory which has the images',
        widget='DirChooser',
        gooey_options=options.FileChooser(
            full_width=True
    ))
    input_group.add_argument(
        'pattern',
        metavar='Pattern',
        help='Naming convention of the images (e.g. img%03.png)',
        gooey_options=options.FileChooser(
            placeholder='File pattern (e.g. img%03d.png)',
            full_width=True
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
            wildcard='video files (*.mp4)|*.mp4',
            default_file='output.mp4',
            full_width=True
        ))

    output_group.add_argument(
        '--overwrite',
        metavar='Overwrite existing',
        help='Overwrite the output video if it already exists?',
        action='store_const',
        const='-y',
        widget='CheckBox',
        gooey_options=options.CheckBox(
            initial_value=True
        )
    )

    settings = parser.add_argument_group('Settings', gooey_options=options.ArgumentGroup(
        show_border=True
    ))
    settings.add_argument(
        '--framerate',
        type=int,
        default=24,
        widget='Slider',
        help='The input framerate', gooey_options=options.DecimalField(
            min=1,
            max=100,
            increment_size=1,
        ))
    return parser



def run(args):
    template = 'cd "{dir}" && ' \
                   'ffmpeg.exe ' \
                   '-framerate {framerate} ' \
                   '-i "{pattern}" ' \
                   '{overwrite} ' \
                   '"{output}"'

    cmd = template.format(**ffmpeg.clean(args))
    ffmpeg.run(cmd)
