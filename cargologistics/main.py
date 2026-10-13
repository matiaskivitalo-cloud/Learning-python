"""
The main function of the cargo logistics application.
It initializes the application, sets up the necessary configurations, and starts the main event loop.
The application is designed to have the user handle the logistics of cargo transportation, managing inventory and tracking ship locations.
Matias Kivitalo
"""
class Cargoship():
    """
    A class representing a cargo ship in the logistics application.
    """
    
    def __init__(self, id, name, capacity, current_load=0.0, location=(0, 0)):
        """ 
        Initializes a new instance of the Cargoship class.
        
        Args:
            id (str): The unique identifier for the cargo ship.
            name (str): The name of the cargo ship.
            capacity (float): The maximum cargo capacity of the ship in tons.
        """
        self.__id = id
        self.__name = name
        self.__capacity = capacity
        self.__current_load = current_load
        self.__location = location

    def get_id(self):
        """
        Returns the unique identifier of the cargo ship.
        
        Returns:
            str: The unique identifier of the cargo ship.
        """
        return self.__id

    def get_name(self):
        """
        Returns the name of the cargo ship.
        
        Returns:
            str: The name of the cargo ship.
        """
        return self.__name
    
    def get_current_load(self):
        """
        Returns the current load of the cargo ship.
        
        Returns:
            float: The current load of the cargo ship in tons.
        """
        return self.__current_load
    
    def get_location(self):
        """
        Returns the geographical location of the cargo ship.
        
        Returns:
            tuple: The geographical location of the cargo ship as (latitude, longitude).
        """
        return self.__location
    
    def set_location(self, location):
        """
        Sets the geographical location of the cargo ship.
        
        Args:
            location (tuple): The new geographical location of the cargo ship as (latitude, longitude).
        """
        if not (isinstance(location, tuple) and len(location) == 2 and all(isinstance(coord, int) for coord in location)):
            raise ValueError("Location must be a tuple of two numeric values (latitude, longitude).")
        
        self.__location = location

    def __str__(self):
        """
        Returns a string representation of the cargo ship.
        
        Returns:
            str: A string representation of the cargo ship.
        """
        return f"Cargoship(id={self.__id}, name={self.__name}, location={self.__location}, current_load={self.__current_load}, capacity={self.__capacity})"
    
    def add_cargo(self, cargo):
        """
        Adds cargo to the current load of the cargo ship.
        
        Args:
            cargo (float): The amount of cargo to add in tons.
        
        Raises:
            ValueError: If adding the cargo exceeds the ship's capacity.
        """
        if self.__current_load + cargo > self.__capacity:
            raise ValueError("Adding this cargo exceeds the ship's capacity.")
        self.__current_load += cargo

    def remove_cargo(self, cargo):
        """
        Removes cargo from the current load of the cargo ship.
        
        Args:
            cargo (float): The amount of cargo to remove in tons.
        """
        if cargo > self.__current_load:
            raise ValueError("Removing this cargo exceeds the current load.")
        self.__current_load -= cargo

class Harbor():
    """
    A class representing a harbor in the logistics application.
    """
    
    def __init__(self, name, location=(0, 0)):
        """
        Initializes a new instance of the Harbor class.
        
        Args:
            name (str): The name of the harbor.
            location (tuple): The geographical location of the harbor as (latitude, longitude).
        """
        self.__name = name
        self.__location = location

    def get_name(self):
        """
        Returns the name of the harbor.
        
        Returns:
            str: The name of the harbor.
        """
        return self.__name

    def get_location(self):
        """
        Returns the geographical location of the harbor.
        
        Returns:
            tuple: The geographical location of the harbor.
        """
        return self.__location
    
    def __str__(self):
        """
        Returns a string representation of the harbor.
        
        Returns:
            str: A string representation of the harbor.
        """
        return f"Harbor(name={self.__name}, location={self.__location})"

def read_harbors():
    """
    Reads harbor data from a file and populates the harbors dictionary.
    
    Returns:
        dict: A dictionary of Harbor objects with harbor names as keys.
            Returns False if the file is not found or an error occurs during reading.
    """
    harbors = {}
    try:
        with open("harbors.txt", "r") as file:
            for line in file:
                parts = line.strip().split(";")
                name = parts[0]

                try:
                    latitude = int(parts[1])
                    longitude = int(parts[2])
                except ValueError:
                    print(f"Invalid location data for harbor '{name}'. Skipping this entry.")
                    continue
                location = (latitude, longitude)
                harbors[name] = Harbor(name, location)
        return harbors
    
    except FileNotFoundError:
        print("Harbor data file not found.")
        return False
    
    except Exception as e:
        print(f"An error occurred while reading harbors: {e}")
        return False

def read_cargoships():
    """
    Reads cargo ship data from a file and populates the cargoships dictionary.

    Returns:
        dict: A dictionary of Cargoship objects with ship IDs as keys.
            Returns False if the file is not found or an error occurs during reading.
    """
    cargoships = {}

    try:
        with open("cargoships.txt", "r") as file:
            for line in file:
                parts = line.strip().split(";")
                id = parts[0]
                name = parts[1]
                try:
                    capacity = int(parts[2])
                except ValueError:
                    print(f"Invalid capacity data for cargoship '{name}'. Skipping this entry.")
                    continue
                cargoships[id] = Cargoship(id, name, capacity)
        return cargoships

    except FileNotFoundError:
        print("Cargoship data file not found.")
        return False
    
    except Exception as e:
        print(f"An error occurred while reading cargoships: {e}")
        return False

def main():
    """
    The main function of the cargo logistics application.
    It initializes the application, sets up the necessary configurations, and starts the main event loop.
    """
    
    cargoships = read_cargoships()
    harbors = read_harbors()

    if  harbors is False or cargoships is False:
        print("Error reading data files. Exiting application.")
        return
    
    print("Cargo Logistics Application")

    print("1. 'Quit' - Exit the application")
    print("2. 'List' - List all cargoships and harbors")
    print("3. 'Add' - Add cargo to a cargoship")
    print("4. 'Remove' - Remove cargo from a cargoship")
    print("5. 'Move' - Move a cargoship to a new location")

    while True:

        choice = input("Enter your choice: ").strip().lower()

        if choice in ("quit", "1"):
            print("Exiting the application.")
            break

        elif choice in ("list", "2"):
            print("Harbors:")
            for harbor in harbors.values():
                print(harbor)
            print("\nCargoships:")
            for ship in cargoships.values():
                print(ship)

        elif choice in ("add", "3"):
            ship_id = input("Enter the ID of the cargoship: ").strip()
            if ship_id in cargoships:
                try:
                    cargo_amount = float(input("Enter the amount of cargo to add (in tons): ").strip())
                    cargoships[ship_id].add_cargo(cargo_amount)
                    print(f"Added {cargo_amount} tons of cargo to {cargoships[ship_id].get_name()}.")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Cargoship not found.")

        elif choice in ("remove", "4"):
            ship_id = input("Enter the ID of the cargoship: ").strip()
            if ship_id in cargoships:
                try:
                    cargo_amount = float(input("Enter the amount of cargo to remove (in tons): ").strip())
                    cargoships[ship_id].remove_cargo(cargo_amount)
                    print(f"Removed {cargo_amount} tons of cargo from {cargoships[ship_id].get_name()}.")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Cargoship not found.")

        elif choice in ("move", "5"):
            ship_id = input("Enter the ID of the cargoship: ").strip()
            if ship_id in cargoships:
                harbor_name = input("Enter the name of the harbor to move to: ").strip()
                if harbor_name in harbors:
                    cargoships[ship_id].set_location(harbors[harbor_name].get_location())
                    print(f"Moved {cargoships[ship_id].get_name()} to {harbors[harbor_name].get_name()}.")
                else:
                    print("Harbor not found.")
            else:
                print("Cargoship not found.")

        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()
