from gooey import options

from gooey_video import ffmpeg


def add_parser(parent):
    parser = parent.add_parser('trim_crop', prog="Trim, Crop & Scale Video", help='Where does this show??')
    input_group = parser.add_argument_group('Input', gooey_options=options.ArgumentGroup(
        show_border=True
    ))
    # basic details
    input_group.add_argument(
        'input',
        metavar='Input',
        help='The video you want to add a watermark to',
        default=r'C:\Users\Chris\Dropbox\pretty_gui\Gooey\demo-screen-recording.mp4',
        widget='FileChooser',
        gooey_options=options.FileChooser(
            wildcard='video files (*.mp4)|*.mp4',
            full_width=True
    ))

    settings = parser.add_argument_group(
        'Trim Settings',
        gooey_options=options.ArgumentGroup(
            show_border=True
    ))
    start_position = settings.add_mutually_exclusive_group(gooey_options=options.MutexGroup(
        initial_selection=0
    ))
    start_position.add_argument(
        '--start-ss',
        metavar='Start position',
        help='Start position in seconds',
        widget='IntegerField',
        gooey_options=options.IntegerField(
            min=0,
            max=99999,
            increment_size=1
        ))
    start_position.add_argument(
        '--start-ts',
        metavar='Start position',
        help='start-position as a concrete timestamp',
        gooey_options=options.TextField(
            placeholder='HH:MM:SS',
            validator=options.RegexValidator(
                test='^\d{2}:\d{2}:\d{2}$',
                message='Must be in the format HH:MM:SS'
            )
        ))

    end = settings.add_mutually_exclusive_group(
        gooey_options=options.MutexGroup(
        initial_selection=0
    ))
    end.add_argument(
        '--end-ss',
        metavar='End position',
        help='Total duration from the start (seconds)',
        widget='IntegerField',
        gooey_options=options.IntegerField(
            min=0,
            max=99999,
            increment_size=1
        ))
    end.add_argument(
        '--end-ts',
        metavar='End position',
        help='End position as a concrete timestamp',
        gooey_options=options.TextField(
            placeholder='HH:MM:SS',
            validator=options.RegexValidator(
                test='^\d{2}:\d{2}:\d{2}$',
                message='Must be in the format HH:MM:SS'
            )
        ))

    crop_settings = parser.add_argument_group('Crop Settings', gooey_options=options.ArgumentGroup(
        show_border=True
    ))
    crop_settings.add_argument(
        '--enable-crop',
        metavar='Crop Video',
        help='Enable the cropping filters',
        action='store_true',
        gooey_options=options.LayoutOptions(
            full_width=True,
            show_label=False
        )

    )

    crop_settings.add_argument(
        '--crop-width',
        metavar='Width',
        help='Width of the cropped region',
        default=640,
        widget='IntegerField',
        gooey_options=options.IntegerField(
            min=1,
            max=1920
        ))
    crop_settings.add_argument(
        '--crop-height',
        metavar='Height',
        help='Height of the cropped region',
        default=480,
        widget='IntegerField',
        gooey_options=options.IntegerField(
            min=1,
            max=1080
        ))

    crop_settings.add_argument(
        '--crop-x',
        metavar='Margin left',
        help='X position where to position the crop region',
        widget='IntegerField',
        gooey_options=options.IntegerField(
            min=0,
            max=1920
        ))

    crop_settings.add_argument(
        '--crop-y',
        metavar='Margin top',
        help='Y position where to position the crop region',
        widget='IntegerField',
        gooey_options=options.IntegerField(
            min=0,
            max=1080
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
    template = 'ffmpeg.exe ' \
               '-i "{input}" ' \
               '-ss {trim_start} ' \
               '-to {trim_end} ' \
               '-filter:v "crop={crop_w}:{crop_h}:{crop_x}:{crop_y},scale={scale_w}:{scale_h}" ' \
               '{overwrite} ' \
               '"{output}"'

    cmd = template.format(
        input=args.input,
        trim_start=args.start_ts or args.start_ss or 0,
        trim_end=args.end_ts or args.end_ss or '99:59:59',
        crop_w=args.crop_width if args.enable_crop else 'iw',
        crop_h=args.crop_height if args.enable_crop else 'ih',
        crop_x=args.crop_x if args.enable_crop else 0,
        crop_y=args.crop_y if args.enable_crop else 0,
        scale_w=args.scale_width,
        scale_h=args.scale_height,
        overwrite=args.overwrite,
        output=args.output
    )
    ffmpeg.run(cmd)