#!/usr/bin/env python
import subprocess
import shlex
import platform
import sys

def start_xvfb(display, config_path=None):
    if platform.system() != 'Linux':
        raise Exception("Xvfb is only supported on Linux")

    # Build the command-line arguments.
    # Note: Xvfb (which stands for X Virtual FrameBuffer) normally does not use a configuration file,
    # so the '-config' option is not supported in most cases.
    # Likewise, while you can pass extension toggles (like +extension GLX), these might be ignored
    # or even rejected if your Xvfb build was not compiled with support for such extensions.
    args = [
        "Xvfb",
        ":%d" % display,
        "-noreset",
        "+extension", "GLX",
        "+extension", "RANDR",
        "+extension", "RENDER",
        "-screen", "0", "1024x768x24",
    ]
    
    # If (and only if) your build of Xvfb supports a configuration file (which most do not),
    # you can add the -config parameter. In most cases you will simply omit this.
    if config_path:
        args.extend(["-config", config_path])

    print("Starting Xvfb with command:", " ".join(args))
    subprocess.call(args)

if __name__ == '__main__':
    # Use display 0 by default; optionally specify a display number and config file.
    display = 0
    config_path = None
    if len(sys.argv) > 1:
        try:
            display = int(sys.argv[1])
        except ValueError:
            sys.exit("Display must be an integer.")
    if len(sys.argv) > 2:
        config_path = sys.argv[2]

    print("Starting Xvfb on DISPLAY=:%s" % display)
    start_xvfb(display, config_path)