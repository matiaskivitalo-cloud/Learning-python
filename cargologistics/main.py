"""
The main function of the cargo logistics application.
It initializes the application, sets up the necessary configurations, and starts the main event loop.
The application is designed to have the user handle the logistics of cargo transportation, managing inventory and tracking ship locations.
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
            tuple: The geographical location of the cargo ship as [latitude, longitude].
        """
        return self.__location

    def __str__(self):
        """
        Returns a string representation of the cargo ship.
        
        Returns:
            str: A string representation of the cargo ship.
        """
        return f"Cargoship(id={self.__id}, name={self.__name})"
    
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
            str: The geographical location of the harbor.
        """
        return self.__location

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
    








if __name__ == "__main__":
    main()
