# test.py

from auto_meshroom import render

def main() -> None:
    """Runs a test program."""

    render(
        source="datasets/lion",
        destination='results/lion',
        output='temp',
        color=True,
        progress=True
    )
# end main

if __name__ == "__main__":
    main()
# end if