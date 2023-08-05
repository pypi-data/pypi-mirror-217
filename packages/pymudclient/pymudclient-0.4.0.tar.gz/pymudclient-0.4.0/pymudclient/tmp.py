#ref: https://github.com/thomasballinger/curtsies/blob/master/curtsies/input.py

import atexit
import fcntl
import os
import sys
import termios
import time
import tty


def _get_reset_tc_attr_function(fd, attr_origin):
    def func():
        termios.tcsetattr(fd, termios.TCSANOW, attr_origin)
    return func


def getch():
    fd = sys.stdin.fileno()

    # Get origin tty control I/O attributes
    attr_origin = termios.tcgetattr(fd)

    atexit.register(_get_reset_tc_attr_function(fd, attr_origin))

    try:
        # Use raw terminal mode, therefore we can get ctrl-c, ctrl-z
        tty.setraw(fd, termios.TCSANOW)

        attr_new = termios.tcgetattr(fd)
        attr_new[3] &= ~termios.ECHO & ~termios.ICANON
        if sys.platform == 'darwin':
            VDSUSP = termios.VSUSP + 1
            attr_new[-1][VDSUSP] = 0
        termios.tcsetattr(fd, termios.TCSANOW, attr_new)

        return sys.stdin.read(1)
    except BlockingIOError:
        return None
    except Exception:
        return None
    finally:
        # fcntl.fcntl(fd, fcntl.F_SETFL, orig_fl)
        termios.tcsetattr(fd, termios.TCSANOW, attr_origin)


if __name__ == '__main__':
    while True:
        # ch = Nonblocking.read()
        ch = getch()
        if not ch:
            print('.')
            time.sleep(0.01)
            continue

        print(repr(ch))
        if ch == 'q':
            break
