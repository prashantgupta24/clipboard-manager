from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

APP = ['src/clippy.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': 'clipboard.icns'
}

setup(
    name="clippy",
    version="0.0.1",
    author="Prashant Gupta",
    author_email="prashantgupta24@gmail.com",
    description="Clipboard manager using tkinter",
    python_requires=">=3.6.0",
    long_description=long_description,
    url="https://github.com/prashantgupta24/clipboard-manager",
    keywords=['clipboard', 'clipboard-manager'],
    app=APP,
    data_files=DATA_FILES,
    install_requires=["pyperclip>=1.6.4", "py2app==0.13"],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    test_suite='test',
    license='MIT',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
