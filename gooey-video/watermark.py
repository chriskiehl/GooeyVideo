from gooey import Gooey, GooeyParser, options
import subprocess

positions = {
    'Center': 'overlay=(W-w)/2:(H-h)/2',
    'Top Left': 'overlay=5:5',
    'Top Right': 'overlay=W-w-5:5',
    'Bottom Left': 'overlay=5:H-h-5',
    'Bottom Right': 'overlay=W-w-5:H-h-5',
}

def watermark_parser(parent):
    parser = parent.add_parser('watermark', prog="Watermark Video", help='Where does this show??')
    input_group = parser.add_argument_group('Input', gooey_options=options.ArgumentGroup(
        show_border=True
    ))
    input_group.add_argument(
        'input',
        metavar='Input',
        help='The video you want to add a watermark to',
        default=r'C:\Users\Chris\Desktop\Recording #1.mp4',
        widget='FileChooser',
        gooey_options=options.FileChooser(
            wildcard='video files (*.mp4)|*.mp4',
            full_width=True
    ))
    input_group.add_argument(
        'watermark',
        metavar='Watermark',
        help='The watermark',
        default=r'C:\Users\Chris\Desktop\avatar.png',
        widget='FileChooser',
        gooey_options=options.FileChooser(
            wildcard='PNG files (*.png)|*.png|JPEG files (*.jpeg;*.jpg)|*.jpeg;*.jpg|BMP and GIF files (*.bmp;*.gif)|*.bmp;*.gif',
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
        default=True,
        const='-y',
        widget='CheckBox')

    settings = parser.add_argument_group('Settings', gooey_options=options.ArgumentGroup(
        show_border=True
    ))
    settings.add_argument(
        '--opacity',
        type=float,
        default=75,
        widget='Slider',
        help='Choose the opacity of the watermark (0-100)', gooey_options=options.DecimalField(
            min=0,
            max=100,
            increment_size=1,
        ))
    settings.add_argument(
        '--position',
        choices=list(positions.keys()),
        default='Center',
        help='Position of the watermark')
    return parser



def run(args):
    cmd_template = 'ffmpeg.exe -i "{input}" ' \
                   '-i "{watermark}" ' \
                   '{overwrite} ' \
                   '-filter_complex "[1]format=rgba,colorchannelmixer=aa={opacity}[logo];[0][logo]' \
                   '{overlay}" ' \
                   '-codec:a copy "{output}"'

    final_cmd = cmd_template.format(
        input=args.input,
        watermark=args.watermark,
        opacity=args.opacity / 100.0,
        overlay=positions[args.position],
        overwrite=args.overwrite,
        output=args.output
    )

    process = subprocess.Popen(
        final_cmd,
        bufsize=1,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        shell=True
    )
    for line in process.stdout:
        print(line)
