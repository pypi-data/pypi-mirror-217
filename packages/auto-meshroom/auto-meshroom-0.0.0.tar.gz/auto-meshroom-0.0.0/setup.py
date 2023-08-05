# setup.py

import codecs

with codecs.open('build.py', 'r') as build_file:
    build_source = build_file.read()

source = dict()

exec(build_source, source)

setup = source['setup']

def main() -> None:
    """Runs the function to distribute the package."""

    setup(
        package="auto_meshroom",
        project="pyproject.toml",
        exclude=[
            "__pycache__",
            "auto_meshroom/source/Meshroom-2018.1.0/",
            "*.pyc"
        ],
        include=[
            "auto_meshroom/source/assets/",
            "auto_meshroom/source/dependencies/",
            "test.py"
        ],
        requirements="requirements.txt",
        dev_requirements="requirements-dev.txt",
        name='auto-meshroom',
        version='0.0.0',
        description=(
            "Photogrammetry is the science of making "
            "measurements from photographs. It infers the "
            "geometry of a scene from a set of unordered "
            "photographs or videos. Photography is the "
            "projection of a 3D scene onto a 2D plane, "
            "losing depth information. The goal of "
            "photogrammetry is to reverse this process."
        ),
        license='MIT',
        author="Shahaf Frank-Shapir",
        author_email='shahaffrs@gmail.com',
        url='https://github.com/Shahaf-F-S/auto-meshroom',
        long_description_content_type="text/markdown",
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Operating System :: OS Independent"
        ]
    )
# end main

if __name__ == "__main__":
    main()
# end if