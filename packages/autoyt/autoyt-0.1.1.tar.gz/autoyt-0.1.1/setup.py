import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoyt",
    version="0.1.1",
    author="Two-Six",
    author_email="twopsix@gmail.com",
    url="https://github.com/two-six/autoYT",
    description="Python script for quickly searching and downloading new content out of YouTube.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["autoyt"],
    license="AGPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["autoyt"],
    package_dir={'':'autoyt/src'},
    install_requires=['yt-dlp', 'ffmpeg']
)