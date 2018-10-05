# A clipboard manager in python, built using tkinter and pyperclip

## Demo

![](https://github.com/prashantgupta24/clipboard-manager/blob/master/clippy-demo.gif)

## How to run Clippy

- Clone the repo
- Run `python setup.py install` (it will install all the required dependencies)
- Run `python src/clippy.py`

## How to run tests

- Run `python setup.py test`

## How to make it a standalone Mac OS X application file

I used [`py2app`](https://py2app.readthedocs.io/en/latest/) to make standalone application bundles.

To make the standalone app, just run:

- `python setup.py py2app`

It will create the `.app` file under the `dist` folder, which you can copy to your `Applications` folder in your Mac, and open `Clippy` just like any other application!

> Note: If you are using macOS 10.7 or later, the Apple-supplied Tcl/Tk 8.5 still has serious bugs that can cause application crashes while using `py2app`. If you wish to use IDLE or Tkinter, install and use a newer version of Python and of Tcl/Tk. Use [this](https://www.tcl.tk/doc/howto/compile.html) link to update.
