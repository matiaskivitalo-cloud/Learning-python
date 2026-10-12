"""Battleship game, where the player can shoot at ships on a 10x10 board.
 The game reads ship data from a file and allows the player to take shots until all ships are sunk or the player quits.
 Matias Kivitalo
 """

class Ship:
    """Ship class, which represents a ship with its type and coordinates."""

    def __init__(self, ship_type, coordinates):
        """Initializes a new instance of the Ship class."""
        self.__ship_type = ship_type
        self.__coordinates = coordinates

    def get_coordinates(self):
        """Returns the coordinates of the ship."""
        return self.__coordinates

    def get_ship_type(self):
        """Returns the type of the ship."""
        return self.__ship_type



def read_file(filename):
    """Reads ship data from a file and creates Ship objects for each ship, returning a list of these objects."""

    ships = [] 

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(';')
                ship = parts[0]
                coordinates = parts[1:]

                new_ship = Ship(ship, coordinates)
                ships.append(new_ship)

        return ships

    except FileNotFoundError:
        print("File can not be read!")
        return False

def coord_checker_file(ships_list):
    """Checks the coordinates of the ships in the list to ensure they are valid and do not overlap."""

    valid_letters = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
    all_coordinates = [] 

    for ship in ships_list:
        for coordinate in ship.get_coordinates():
            if len(coordinate) != 2:
                print("Error in ship coordinates!")
                return False

            letter = coordinate[0]

            try:
                number = int(coordinate[1:])
            except ValueError:
                print("Error in ship coordinates!")
                return False

            if letter not in valid_letters or not (0 <= number <= 9):
                print("Error in ship coordinates!")
                return False

            if coordinate in all_coordinates:
                print("There are overlapping ships in the input file!")
                return False

            all_coordinates.append(coordinate)

    return True

def shot_checker(cmd, ships_list, board, hits, shot_coordinates, misses, sunk):
    """Checks the shot command, updates the board and lists accordingly, and returns the updated board."""
    shot = cmd.capitalize()


    if len(shot) != 2:
        print("Invalid command!")
        return board

    shot_letter = shot[0]
    shot_number_string = shot[1]

    try:
        shot_number_int = int(shot[1])
    except ValueError:
        print("Invalid command!")
        return board

    if shot_letter not in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] or shot_number_int not in range(10):
        print("Invalid command!")
        return board

    if shot in shot_coordinates:
        print("Location has already been shot at!")
        return board
    else:
        shot_coordinates.append(shot)

    for ship in ships_list:
        for coordinate in ship.get_coordinates():
            if coordinate[0] == shot_letter and coordinate[1] == shot_number_string:

                hits.append(coordinate)

                if all(c in hits for c in ship.get_coordinates()):
                    sunk.append(ship)

                    ship_coordinates = ship.get_coordinates()

                    print(f"You sank a {ship.get_ship_type()}!")

                    ship_letter = ship.get_ship_type()[0].upper()

                    for coord in ship_coordinates:
                        coord_letter = coord[0]
                        coord_number = int(coord[1])
                        board[coord_letter, coord_number] = ship_letter

                    return board

                if ship not in sunk:
                    board[(shot_letter, shot_number_int)] = "X"
                    return board

    misses.append(shot.capitalize())
    board[(shot_letter, shot_number_int)] = "*"
    return board

def board_printer(board):
    """Prints the current state of the board."""

    column = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    title = "  " + " ".join(column)

    print()
    print(title)

    for y in range(10):
        print(f"{y} ", end="")

        for x in column:
            letter = board[(x, y)]
            print(f"{letter} ", end="")

        print(f"{y}")

    print(title)
    print()

def main():
    """Main function to run the Battleship game."""

    filename = input("Enter file name: ")

    ships_list = read_file(filename)
    if ships_list is False:
        return

    if coord_checker_file(ships_list) is False:
        return

    board = {}

    # Initialize the board with empty spaces
    for y in range(10):
        for x in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
            board[(x, y)] = " "

    hits = []
    shot_coordinates = []
    misses = []
    sunk = []
    board_printer(board)

    while True:
        cmd = input("Enter place to shoot (q to quit): ")

        if cmd in ["q", "Q"]:
            print("Aborting game!")
            return
        else:
            board = shot_checker(cmd, ships_list, board, hits, shot_coordinates, misses, sunk)

        if len(sunk) == len(ships_list):
            board_printer(board)
            print("Congratulations! You sank all enemy ships.")
            return

        board_printer(board)


if __name__ == "__main__":
    main()
