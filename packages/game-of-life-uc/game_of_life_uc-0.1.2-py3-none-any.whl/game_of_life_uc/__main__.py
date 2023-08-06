#!/opt/homebrew/bin/python3
#CHANGE THE SHEBANG LINE TO THE PATH OF YOUR PYTHON INTERPRETER

#Parse the command line arguments

def main():
    import argparse
    from . import game_code as game_of_life

    parser = argparse.ArgumentParser()

    parser.add_argument("-w", "--wrap", help="Wrap around the edges of the grid", action="store_true")
    parser.add_argument("-s", "--speed", type=float, default=0.1, help="Time between iterations in seconds, default [0.1]")
    parser.add_argument("-c", "--colour", help="Use colour", action="store_true")

    game_of_life.call_game_of_life(parser.parse_args())

if __name__ == "__main__":
    main()
