import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

from iv2 import VERSION

setuptools.setup(
    name="iv2",
    version=VERSION,
    author="ponponon",
    author_email="1729303158@qq.com",
    maintainer='ponponon',
    maintainer_email='1729303158@qq.com',
    license='MIT License',
    platforms=["all"],
    description="image2vector: The first 47 layers of the resnet50 model of the deep learning neural network are used to extract the vector of the picture, and the output dimension is 512",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ponponon/iv2",
    packages=setuptools.find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "pillow",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
