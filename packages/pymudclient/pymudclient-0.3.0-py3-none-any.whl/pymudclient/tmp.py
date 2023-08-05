import atexit
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
        # Use raw terminal mode
        tty.setraw(fd, termios.TCSANOW)
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
            time.sleep(0.01)
            continue

        print(repr(ch))
        if ch == 'q':
            break
