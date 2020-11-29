import os
import subprocess

def get_path_to():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'executables',
        'ffmpeg.exe'
    )

def run(cmd):
    print(get_path_to())
    print('running command:')
    print(cmd.replace('ffmpeg.exe', f'"{get_path_to()}"'))
    process = subprocess.Popen(
        cmd.replace('ffmpeg.exe', f'"{get_path_to()}"'),
        bufsize=1,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        shell=True
    )
    for line in process.stdout:
        print(line)


def clean(args):
    """
    Clean the args namespace object of any
    None values replacing them with empty strings
    so that replacement targets work as expected.
    """
    return {k:v if v is not None else ''
            for k,v in vars(args).items()}