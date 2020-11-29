from gooey import Gooey, GooeyParser

import gif
import screen_recorder
import slideshow
import trim_crop
import watermark


@Gooey(program_name='FFGooey: FFMPEG wrapper')
def main():
    parser = GooeyParser(description='A collection of the FFMPEG commands I most often use (and forget)')
    subparsers = parser.add_subparsers(help='commands', dest='command')
    screen_recorder.add_parser(subparsers)
    gif.add_parser(subparsers)
    trim_crop.add_parser(subparsers)
    slideshow.add_parser(subparsers)
    watermark.watermark_parser(subparsers)

    args = parser.parse_args()
    globals()[args.command].run(args)


if __name__ == '__main__':
    main()