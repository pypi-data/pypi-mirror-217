import setuptools

setuptools.setup(
    name="play2048",
    version="5.0",
    license='MIT',
    author="5-23",
    author_email="yhanbyeol6@gmail.com",
    description="The 2048 Game",
    long_description=open('README.md').read(),
    url="https://github.com/objectiveTM/play2048",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)