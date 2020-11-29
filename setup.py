import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Gooey-Video",
    version="0.0.1",
    author="Chris Kiehl",
    author_email="audionautic@gmail.com",
    description="A small collection of useful FFMPEG tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chriskiehl/GooeyVideo",
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "Topic :: Multimedia :: Graphics :: Capture"
    ],
    python_requires='>=3.6',
)