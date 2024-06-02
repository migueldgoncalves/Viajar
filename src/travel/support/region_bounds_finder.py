from travel.support import ways
from travel.support import osm_interface
from travel.support.osm_interface import OsmInterface

EXIT = 0
PORTUGAL = 1
SPAIN = 2
CANARY_ISLANDS = 3  # Part of Spain
ANDORRA = 4
GIBRALTAR = 5


def exit_by_user_option() -> None:
    print("You have chosen to exit")
    print("See you soon")
    exit(0)


def print_extreme_points_and_exit(name: str, administrative_level: int, desired_country: str) -> None:
    output = OsmInterface().get_region_extreme_points(name=name, admin_level=administrative_level, country=desired_country)
    print(output)
    exit(0)


def get_extreme_points():
    """
    Main routine
    """
    try:
        success: bool = OsmInterface().test_connections()
        if not success:  # As least one server is down
            print("At least one server is not connected")
            print("Please ensure all servers are running and try again")
            exit(1)

        print("Welcome to the region bounds finder")
        print("You will get the extreme points of a region")

        country: str = ''

        # Select the country or region

        print(f'{EXIT} - Exit\n'
              f'{PORTUGAL} - Portugal\n'
              f'{SPAIN} - Peninsular Spain + Balearic Islands + Ceuta + Melilla\n'
              f'{CANARY_ISLANDS} - Canary Islands\n'
              f'{ANDORRA} - Andorra\n'
              f'{GIBRALTAR} - Gibraltar')

        while True:
            try:
                option: int = int(input("Insert the desired country or region(s): "))
            except ValueError:
                print("You must insert a number")
                continue

            if option == EXIT:
                exit_by_user_option()

            elif option == PORTUGAL:
                country = ways.PORTUGAL
                print("You have chosen Portugal")
                break
            elif option == SPAIN:
                country = ways.SPAIN
                print("You have chosen Peninsular Spain, Balearic Islands, Ceuta, and Melilla")
                break
            elif option == CANARY_ISLANDS:  # Part of Spain, but in a different server
                country = ways.CANARY_ISLANDS
                print("You have chosen the Canary Islands")
                break
            elif option == ANDORRA:
                country = ways.ANDORRA
                print("You have chosen Andorra")
                break
            elif option == GIBRALTAR:
                country = ways.GIBRALTAR
                print("You have chosen Gibraltar")
                break

        # Select the region

        if country == ways.GIBRALTAR:  # No subdivisions - Instead, calculate the extreme points of Gibraltar
            print_extreme_points_and_exit("Gibraltar", osm_interface.GIBRALTAR_ADMIN_LEVEL, country)

        elif country == ways.ANDORRA:
            print(f'{EXIT} - Exit\n'
                  f'{osm_interface.COUNTRY} - Entire country\n'
                  f'{osm_interface.ANDORRAN_PARISH} - Parish')
            while True:
                try:
                    option = int(input("Insert the option representing the desired region type: "))
                except ValueError:
                    continue

                if option == EXIT:
                    exit_by_user_option()

                elif option == osm_interface.COUNTRY:
                    region_level = osm_interface.COUNTRY
                    print_extreme_points_and_exit("Andorra", region_level, country)

                elif option == osm_interface.ANDORRAN_PARISH:
                    region_level = osm_interface.ANDORRAN_PARISH

                    region_name = input("Insert the name of the desired parish: ").strip()
                    if not region_name:
                        continue
                    print_extreme_points_and_exit(region_name, region_level, country)

        elif country in [ways.SPAIN, ways.CANARY_ISLANDS]:
            print(f'{EXIT} - Exit\n'
                  f'{osm_interface.COUNTRY} - Country or Region\n'
                  f'{osm_interface.AUTONOMOUS_COMMUNITY} - Autonomous Community\n'
                  f'{osm_interface.PROVINCE} - Province\n'
                  f'{osm_interface.COMARCA} - Comarca\n'
                  f'{osm_interface.SPANISH_MUNICIPALITY} - Municipality\n'
                  f'{osm_interface.SPANISH_DISTRICT} - District')

            while True:
                try:
                    option = int(input("Insert the option representing the desired region type: "))
                except ValueError:
                    continue

                if option == EXIT:
                    exit_by_user_option()

                elif option == osm_interface.COUNTRY:
                    region_level = osm_interface.COUNTRY
                    print_extreme_points_and_exit("España", region_level, country)

                elif option in [osm_interface.AUTONOMOUS_COMMUNITY, osm_interface.PROVINCE, osm_interface.COMARCA,
                                osm_interface.SPANISH_MUNICIPALITY, osm_interface.SPANISH_DISTRICT]:
                    region_level = option

                    region_name = input("Insert the name of the desired region: ").strip()
                    if not region_name:
                        continue
                    print_extreme_points_and_exit(region_name, region_level, country)

        elif country == ways.PORTUGAL:
            print(f'{EXIT} - Exit\n'
                  f'{osm_interface.COUNTRY} - Entire country\n'
                  f'{osm_interface.PORTUGUESE_DISTRICT} - District\n'
                  f'{osm_interface.PORTUGUESE_MUNICIPALITY} - Municipality\n'
                  f'{osm_interface.PORTUGUESE_PARISH} - Parish')

            while True:
                try:
                    option = int(input("Insert the option representing the desired region type: "))
                except ValueError:
                    continue

                if option == EXIT:
                    exit_by_user_option()

                elif option == osm_interface.COUNTRY:
                    region_level = osm_interface.COUNTRY
                    print_extreme_points_and_exit("Portugal", region_level, country)

                elif option in [osm_interface.PORTUGUESE_DISTRICT, osm_interface.PORTUGUESE_MUNICIPALITY, osm_interface.PORTUGUESE_PARISH]:
                    region_level = option

                    region_name = input("Insert the name of the desired region: ").strip()
                    if not region_name:
                        continue
                    print_extreme_points_and_exit(region_name, region_level, country)

    except Exception as e:
        print("An exception has occurred")
        print(e.args)
        print("Exiting...")
        exit(1)
