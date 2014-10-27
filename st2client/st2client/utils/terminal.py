import os
import struct
import subprocess

__all__ = [
    'get_terminal_size'
]


def get_terminal_size(default=(80, 20)):
    """
    :return: (lines, cols)
    """
    def ioctl_GWINSZ(fd):
        import fcntl
        import termios
        return struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
    # try stdin, stdout, stderr
    for fd in (0, 1, 2):
        try:
            return ioctl_GWINSZ(fd)
        except:
            pass
    # try os.ctermid()
    try:
        fd = os.open(os.ctermid(), os.O_RDONLY)
        try:
            return ioctl_GWINSZ(fd)
        finally:
            os.close(fd)
    except:
        pass
    # try `stty size`
    try:
        process = subprocess.Popen(['stty', 'size'],
                                   shell=False,
                                   stdout=subprocess.PIPE,
                                   stderr=open(os.devnull, 'w'))
        result = process.communicate()
        if process.returncode == 0:
            return tuple(int(x) for x in result[0].split())
    except:
        pass
    # try environment variables
    try:
        return tuple(int(os.getenv(var)) for var in ('LINES', 'COLUMNS'))
    except:
        pass
    #  return default.
    return default