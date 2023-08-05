# main.py

import argparse

from auto_meshroom.modeling import Modeler

__all__ = [
    "main"
]

def main() -> None:
    """Runs the program to visualize in an image a model."""

    parser = argparse.ArgumentParser(
        description='3D Reconstruction - CAD 3D from 2D Images Software.'
    )
    parser.add_argument(
        'source', metavar='SOURCE_IMAGE_DIRECTORY',
        help='the source directory with the images', nargs='?'
    )
    parser.add_argument(
        '--color', help=(
            "add texture to the 3D model, based on "
            "the images coloration"
        ),
        action='store_true', default=False
    )
    parser.add_argument(
        '--silence', help="hide the destination of the process",
        action='store_true', default=False
    )
    parser.add_argument(
        '--destination', help="the destination directory to save the 3D model files in",
        type=str, default="results"
    )

    args = parser.parse_args()

    Modeler().render(
        source=args.source, destination=args.output,
        progress=not args.silence, color=args.color
    )
# end main

if __name__ == '__main__':
    main()
# end if