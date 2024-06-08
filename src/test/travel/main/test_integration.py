import unittest
import unittest.mock
import io
import sys


from travel.main import travel


def _redirect_output() -> io.StringIO:
    """
    Redirects stdout to be monitorable inside tests

    :return: Object to where stdout is now being redirected
    """
    stdout_redirect: io.StringIO = io.StringIO()
    sys.stdout = stdout_redirect
    return stdout_redirect


class IntegrationTest(unittest.TestCase):
    """
    Performs integration tests on the journey
    """

    def setUp(self):
        self.initial_location: str = 'Guerreiros do Rio'
        with unittest.mock.patch('builtins.input', side_effect=["n"]):  # Provides option to car usage menu
            self.travel: travel.Travel = travel.Travel(self.initial_location, return_and_not_exit=True)

    def test_return_and_not_exit(self):
        # If test passes, mechanism to return from journey instead of exiting program is working
        stdout_redirect: io.StringIO = _redirect_output()
        with unittest.mock.patch('builtins.input', side_effect=["0"]):  # Exits menu loop and allows to get the journey state
            self.travel.make_journey()
        self.assertEqual('Guerreiros do Rio', self.travel.current_journey.get_current_location())

    def test_starting_location(self):
        """
        Starting location is Guerreiros do Rio, Portuguese village in the banks of the Guadiana River in Algarve, facing
            Spain across the river
        """
        stdout_redirect: io.StringIO = _redirect_output()
        with unittest.mock.patch('builtins.input', side_effect=["0"]):  # Exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Guerreiros do Rio, Alcoutim, Faro District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Laranjeiras (NW, 1.2 km)'
                        '\n2 -> Rotunda da Árvore (S, 0.7 km)'
                        '\n3 -> Bar do Rio (N, 0.1 km)'
                        '\n4 -> Show location information'
                        '\n5 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 18 meters'
                        '\nCoordinates: 37.396353, -7.446837'
                        '\nParish: Alcoutim e Pereiro'
                        '\nMunicipality: Alcoutim'
                        '\nDistrict: Faro'
                        '\nIntermunicipal entity: Algarve'
                        '\nRegion: Algarve'
                        '\nCountry: Portugal'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["5", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 0.0 km'
                        '\nYou have been travelling for 00:00:00'
                        '\nYou have consumed 0.0 liters of fuel'
                        '\nYou have spent 0.0 euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_with_one_surrounding_location(self):
        """
        Destination is Palmeira, Portuguese village not far from the banks of the Guadiana river in Algarve
        Route: Guerreiros do Rio > Car > Palmeira
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["2", "2", "1", "3", "1", "4", "0"]
        with unittest.mock.patch('builtins.input', side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Palmeira, Alcoutim, Faro District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> IC27 - Saída 6 (NE, 0.7 km)'
                        '\n2 -> Show location information'
                        '\n3 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["2", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 85 meters'
                        '\nCoordinates: 37.398627, -7.52961'
                        '\nParish: Alcoutim e Pereiro'
                        '\nMunicipality: Alcoutim'
                        '\nDistrict: Faro'
                        '\nIntermunicipal entity: Algarve'
                        '\nRegion: Algarve'
                        '\nCountry: Portugal'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["3", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 10.5 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_in_protected_area(self):
        """
        Destination is Pomarão, Portuguese village at the banks of the Guadiana river in Alentejo, at the start of the
            (final) section of the Guadiana river as the Portuguese-Spanish border
        Route: Guerreiros do Rio > Boat > Pomarão
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "0"]
        with unittest.mock.patch('builtins.input', side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Pomarão, Mértola, Beja District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Cais da Mesquita (SW, 0.1 km) » Rio Guadiana: Direction Mértola'
                        '\n2 -> Puerto de la Laja (S, 5.5 km) » Rio Guadiana: Direction Sanlúcar de Guadiana / Vila Real de Santo António'
                        '\n3 -> Return to the road'
                        '\n4 -> Board a train'
                        '\n5 -> Show location information'
                        '\n6 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["5", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 24 meters'
                        '\nCoordinates: 37.556289, -7.524924'
                        '\nParque Natural do Vale do Guadiana'
                        '\nParish: Santana de Cambas'
                        '\nMunicipality: Mértola'
                        '\nDistrict: Beja'
                        '\nIntermunicipal entity: Baixo Alentejo'
                        '\nRegion: Baixo Alentejo'
                        '\nCountry: Portugal'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["6", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 23.7 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_in_island(self):
        """
        Destination is Punta del Moral, a neighbourhood in Andalucía at the Portuguese-Spanish border, near the mouth
            of the Guadiana river
        Route: Guerreiros do Rio > Boat > Punta del Moral
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "2", "2", "2", "2", "2", "2", "0"]
        with unittest.mock.patch('builtins.input', side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Punta del Moral, Ayamonte, Huelva Province, Andaluzia'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Vila Real de Santo António (W, 11.8 km) » Costa Atlântica de Espanha Continental: Direction Faro / Portimão'
                        '\n2 -> Nuevo Portil (E, 29.6 km) » Costa Atlântica de Espanha Continental: Direction Huelva / Sevilha'
                        '\n3 -> Isla Cristina (NE, 1.6 km) » Marismas de Isla Cristina: Direction Isla Cristina'
                        '\n4 -> Return to the road'
                        '\n5 -> Show location information'
                        '\n6 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["5", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 4 meters'
                        '\nCoordinates: 37.189202, -7.34245'
                        '\nCanela Island'
                        '\nMunicipality: Ayamonte'
                        '\nComarca: Costa Occidental de Huelva'
                        '\nProvince: Huelva'
                        '\nAutonomous community: Andaluzia'
                        '\nCountry: Spain'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["6", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 36.9 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_with_altitude_zero_meters(self):
        """
        Destination is Guadiana International Bridge, near the mouth of the Guadiana river, connecting Vila Real de Santo
            António and Castro Marim in Portugal with Ayamonte in Spain
        Route: Guerreiros do Rio > Boat > Vila Real de Santo António > Car > Guadiana International Bridge
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "2", "2", "2", "2", "2", "4", "1", "1", "1", "2", "2", "0"]
        with unittest.mock.patch('builtins.input', side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Ponte Internacional do Guadiana, Ayamonte, Huelva Province, Andaluzia'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Área de Repouso de Castro Marim (W, 1.7 km) » A22: Direction Faro / Lisboa'
                        '\n2 -> A-49 - Saída 131 (E, 1.3 km) » A-49: Direction Ayamonte / Huelva'
                        '\n3 -> Show location information'
                        '\n4 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["3", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 0 meters'
                        '\nCoordinates: 37.237619, -7.419194'
                        '\nMunicipality: Ayamonte'
                        '\nComarca: Costa Occidental de Huelva'
                        '\nProvince: Huelva'
                        '\nAutonomous community: Andaluzia'
                        '\nCountry: Spain'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 33.2 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_with_altitude_one_meter(self):
        """
        Destination is North of the Castro Marim and Vila Real de Santo António Marsh, a wetland in Algarve at the
             mouth of the River Guadiana

        Route: Guerreiros do Rio > Boat > Vila Real de Santo António > Car > North of the Castro Marim and
            Vila Real de Santo António Marsh
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "2", "2", "2", "2", "2", "4", "1", "1", "1", "3", "4", "0"]
        with unittest.mock.patch('builtins.input', side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Norte do Sapal de Castro Marim e Vila Real de Santo António, Castro Marim, Faro District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> IC27 - Início (W, 2.0 km)'
                        '\n2 -> Show location information'
                        '\n3 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["2", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 1 meter'
                        '\nCoordinates: 37.24116, -7.426341'
                        '\nSapal de Castro Marim e Vila Real de Santo António'
                        '\nParish: Castro Marim'
                        '\nMunicipality: Castro Marim'
                        '\nDistrict: Faro'
                        '\nIntermunicipal entity: Algarve'
                        '\nRegion: Algarve'
                        '\nCountry: Portugal'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["3", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 32.9 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_with_boat(self):
        """
        Destination is Laranjeiras, another village in the banks of the river Guadiana in Algarve, facing Spain
        Route: Guerreiros do Rio > Car > Laranjeiras > Car
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["1", "0"]
        with unittest.mock.patch('builtins.input', side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Laranjeiras, Alcoutim, Faro District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Guerreiros do Rio (SE, 1.2 km)'
                        '\n2 -> Montinho das Laranjeiras (NW, 0.5 km)'
                        '\n3 -> Board a boat'
                        '\n4 -> Show location information'
                        '\n5 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["3", "0"]):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()  # Switches to boat

        self.assertTrue('You are aboard a boat' in stdout_redirect.getvalue())
        self.assertTrue('\nYou have new available destinations' in stdout_redirect.getvalue())
        self.assertTrue('\nYou are in Laranjeiras, Alcoutim, Faro District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Alcoutim (N, 9.5 km) » Rio Guadiana: Direction Alcoutim / Mértola / Sanlúcar de Guadiana'
                        '\n2 -> Bar do Rio (SE, 1.3 km) » Rio Guadiana: Direction Ayamonte / Vila Real de Santo António'
                        '\n3 -> Return to the road'
                        '\n4 -> Show location information'
                        '\n5 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["3", "0"]):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()  # Switches to boat

        self.assertTrue('You are back on the road' in stdout_redirect.getvalue())
        self.assertTrue('\nYou have new available destinations' in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 10 meters'
                        '\nCoordinates: 37.403058, -7.457947'
                        '\nParish: Alcoutim e Pereiro'
                        '\nMunicipality: Alcoutim'
                        '\nDistrict: Faro'
                        '\nIntermunicipal entity: Algarve'
                        '\nRegion: Algarve'
                        '\nCountry: Portugal'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["5", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 1.2 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_with_standard_train(self):
        """
        Destination is Vila Real de Santo António, a town at the mouth of the Guadiana River in Algarve, facing Spain
        Route: Guerreiros do Rio > Boat > Vila Real de Santo António
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "2", "2", "2", "2", "2", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Vila Real de Santo António, Vila Real de Santo António, Faro District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Quatro Águas (SE, 26.9 km) » Costa de Portugal Continental: Direction Faro / Portimão'
                        '\n2 -> Punta del Moral (E, 11.8 km) » Costa Atlântica de Espanha Continental: Direction Huelva / Sevilha'
                        '\n3 -> Ayamonte (NE, 2.2 km) » Rio Guadiana: Direction Alcoutim / Ayamonte / Mértola'
                        '\n4 -> Return to the road'
                        '\n5 -> Board a train'
                        '\n6 -> Show location information'
                        '\n7 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input',
                                 side_effect=["5", "0"]):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()  # Switches to train

        self.assertTrue('You are aboard a train' in stdout_redirect.getvalue())
        self.assertTrue('\nYou have new available destinations' in stdout_redirect.getvalue())
        self.assertTrue('\nYou are in Vila Real de Santo António, Vila Real de Santo António, Faro District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Estação de Monte Gordo (SW, 2.7 km) » Linha do Algarve - Regional: Direction Faro / Lagos'
                        '\n2 -> Return to the road'
                        '\n3 -> Board a boat'
                        '\n4 -> Show location information'
                        '\n5 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 8 meters'
                        '\nCoordinates: 37.194148, -7.418'
                        '\nParish: Vila Real de Santo António'
                        '\nMunicipality: Vila Real de Santo António'
                        '\nDistrict: Faro'
                        '\nIntermunicipal entity: Algarve'
                        '\nRegion: Algarve'
                        '\nCountry: Portugal'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["5", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 25.1 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_with_high_speed_train(self):
        """
        Destination is Faro Station, the main train station in Faro, the capital city of Algarve
        Route: Guerreiros do Rio > Boat > Vila Real de Santo António > Train > Faro
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "2", "2", "2", "2", "2", "5", "1", "2", "2", "2", "2", "2", "2", "2", "2", "2",
                              "2", "2", "2", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Estação de Faro, Faro, Faro District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Estação de Bom João (SE, 2.2 km) » Linha do Algarve - Regional: Direction Vila Real de Santo António'
                        '\n2 -> Estação de Parque das Cidades (NW, 8.1 km) » Linha do Algarve - Regional: Direction Lagos / Tunes'
                        '\n3 -> Estação de Loulé (NW, 15.8 km) » Linha do Algarve - Intercidades: Direction Lisboa - Oriente / Tunes'
                        '\n4 -> Return to the road'
                        '\n5 -> Board a high-speed train'
                        '\n6 -> Show location information'
                        '\n7 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input',
                                 side_effect=["5", "0"]):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()  # Switches to high-speed train

        self.assertTrue('You are aboard a high-speed train' in stdout_redirect.getvalue())
        self.assertTrue('\nYou have new available destinations' in stdout_redirect.getvalue())
        self.assertTrue('\nYou are in Estação de Faro, Faro, Faro District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Estação de Loulé (NW, 15.8 km) » Linha do Algarve: Direction Lisboa - Oriente / Tunes'
                        '\n2 -> Return to the road'
                        '\n3 -> Board a standard train'
                        '\n4 -> Show location information'
                        '\n5 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input',
                                 side_effect=["2", "0"]):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()  # Switches to car

        # "Standard" train and high-speed train options present at the same time
        self.assertTrue('You are back on the road' in stdout_redirect.getvalue())
        self.assertTrue('\nYou have new available destinations' in stdout_redirect.getvalue())
        self.assertTrue('\nYou are in Estação de Faro, Faro, Faro District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Faro - São Pedro (E, 0.8 km)'
                        '\n2 -> Board a standard train'
                        '\n3 -> Board a high-speed train'
                        '\n4 -> Show location information'
                        '\n5 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 2 meters'
                        '\nCoordinates: 37.018466, -7.939585'
                        '\nParish: Faro (Sé e São Pedro)'
                        '\nMunicipality: Faro'
                        '\nDistrict: Faro'
                        '\nIntermunicipal entity: Algarve'
                        '\nRegion: Algarve'
                        '\nCountry: Portugal'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["5", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 81.2 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_with_plane(self):
        """
        Destination is Beja Airport, near the city of Beja, the capital city of the Lower Alentejo in Portugal
        Route: Guerreiros do Rio > Boat > Mértola > Car > Beja
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "1", "1", "1", "2", "3", "1", "1", "1", "1", "3", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Aeroporto de Beja, Beja, Beja District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Beja (SE, 9.6 km)'
                        '\n2 -> Cuba (NE, 14.5 km)'
                        '\n3 -> Board a plane'
                        '\n4 -> Show location information'
                        '\n5 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input',
                                 side_effect=["3", "0"]):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()  # Switches to plane

        self.assertTrue('You are aboard a plane' in stdout_redirect.getvalue())
        self.assertTrue('\nYou have new available destinations' in stdout_redirect.getvalue())
        self.assertTrue('\nYou are in Aeroporto de Beja, Beja, Beja District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Aeroporto de Faro (S, 115.7 km)'
                        '\n2 -> Aeroporto de Sevilha (SE, 193.4 km)'
                        '\n3 -> Aeródromo de Portimão (SW, 116.4 km)'
                        '\n4 -> Aeroporto de Córdoba (E, 272.4 km)'
                        '\n5 -> Aeroporto de Jerez (SE, 222.3 km)'
                        '\n6 -> Aeroporto de Badajoz (NE, 132.4 km)'
                        '\n7 -> Aeroporto de Lisboa - Terminal 1 (NW, 130.9 km)'
                        '\n8 -> Aeródromo de Tires (NW, 143.5 km)'
                        '\n9 -> Aeródromo de Viseu (N, 293.9 km)'
                        '\n10 -> Aeroporto Internacional de Ciudad Real (E, 356.3 km)'
                        '\n11 -> Aeroporto do Porto (N, 357.7 km)'
                        '\n12 -> Return to the road'
                        '\n13 -> Show location information'
                        '\n14 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["13", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 188 meters'
                        '\nCoordinates: 38.063206, -7.939608'
                        '\nParish: Trigaches e São Brissos'
                        '\nMunicipality: Beja'
                        '\nDistrict: Beja'
                        '\nIntermunicipal entity: Baixo Alentejo'
                        '\nRegion: Baixo Alentejo'
                        '\nCountry: Portugal'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["14", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 103.8 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_with_subway(self):
        """
        Destination is Airport Station, the subway station serving the airport of the capital city of Portugal
        Route: Guerreiros do Rio > Boat > Mértola > Car > Beja > Plane > Lisbon
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "1", "1", "1", "2", "3", "1", "1", "1", "1", "3", "3",
                              "7", "17", "1", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Estação Aeroporto, Lisboa, Lisboa District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Aeroporto de Lisboa - Terminal 1'
                        '\n2 -> Return to the road'
                        '\n3 -> Board a subway train'
                        '\n4 -> Show location information'
                        '\n5 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input',
                                 side_effect=["3", "0"]):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()  # Switches to subway

        self.assertTrue('You are aboard a subway train' in stdout_redirect.getvalue())
        self.assertTrue('\nYou have new available destinations' in stdout_redirect.getvalue())
        self.assertTrue('\nYou are in Estação Aeroporto, Lisboa, Lisboa District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Estação Encarnação (NE, 1.3 km) » Linha Vermelha - Metro de Lisboa: Direction Oriente / São Sebastião'
                        '\n2 -> Transfer between means of transport'
                        '\n3 -> Return to the road'
                        '\n4 -> Show location information'
                        '\n5 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 92 meters'
                        '\nCoordinates: 38.768995, -9.128441'
                        '\nParish: Olivais'
                        '\nMunicipality: Lisboa'
                        '\nDistrict: Lisboa'
                        '\nIntermunicipal entity: Área Metropolitana de Lisboa'
                        '\nRegion: Estremadura'
                        '\nCountry: Portugal'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["5", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 234.7 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_location_with_transfer(self):
        """
        Destination is Lisbon Airport - Terminal 1, the main terminal of the airport serving the capital city of Portugal
        Route: Guerreiros do Rio > Boat > Mértola > Car > Beja > Plane > Lisbon
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "1", "1", "1", "2", "3", "1", "1", "1", "1", "3", "3",
                              "7", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Aeroporto de Lisboa - Terminal 1, Lisboa, Lisboa District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Aeroporto de Madrid-Barajas - Terminal 3 (NE, 512.4 km)'
                        '\n2 -> Aeroporto de Badajoz (E, 201.1 km)'
                        '\n3 -> Aeroporto de Beja (SE, 130.9 km)'
                        '\n4 -> Aeroporto de Faro (SE, 221.3 km)'
                        '\n5 -> Aeródromo de Portimão (SE, 187.7 km)'
                        '\n6 -> Aeroporto de Sevilha (SE, 322.2 km)'
                        '\n7 -> Aeroporto de Málaga - Costa del Sol (SE, 470.9 km)'
                        '\n8 -> Aeroporto de Gibraltar (SE, 444.4 km)'
                        '\n9 -> Aeroporto de Córdoba (SE, 389.1 km)'
                        '\n10 -> Aeroporto de Jerez (SE, 352.7 km)'
                        '\n11 -> Aeroporto de Salamanca (NE, 393.3 km)'
                        '\n12 -> Aeródromo de Tires (SW, 20.1 km)'
                        '\n13 -> Aeroporto de Alicante-Elche Miguel Hernández (E, 749.6 km)'
                        '\n14 -> Aeródromo de Viseu (NE, 240.8 km)'
                        '\n15 -> Aeroporto do Porto (N, 276.7 km)'
                        '\n16 -> Return to the road'
                        '\n17 -> Transfer between means of transport'
                        '\n18 -> Show location information'
                        '\n19 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input',
                                 side_effect=["17", "0"]):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()  # Switches to transfer between means of transport

        self.assertTrue('You are transferring between means of transport' in stdout_redirect.getvalue())
        self.assertTrue('\nYou have new available destinations' in stdout_redirect.getvalue())
        self.assertTrue('\nYou are in Aeroporto de Lisboa - Terminal 1, Lisboa, Lisboa District'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Estação Aeroporto, Metro de Lisboa'
                        '\n2 -> Return to the road'
                        '\n3 -> Board a plane'
                        '\n4 -> Show location information'
                        '\n5 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 97 meters'
                        '\nCoordinates: 38.770451, -9.12968'
                        '\nParish: Olivais'
                        '\nMunicipality: Lisboa'
                        '\nDistrict: Lisboa'
                        '\nIntermunicipal entity: Área Metropolitana de Lisboa'
                        '\nRegion: Estremadura'
                        '\nCountry: Portugal'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["5", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 234.7 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_spanish_location_with_district(self):
        # Also tests locations in the Madrid Community
        """
        Destination is Barajas Airport - Terminal 3, a terminal of the main airport serving Madrid
        Route: Guerreiros do Rio > Boat > Mértola > Car > Beja > Plane > Madrid
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "1", "1", "1", "2", "3", "1", "1", "1", "1", "3", "3",
                              "6", "5", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Aeroporto de Madrid-Barajas - Terminal 3, Madrid, Comunidade de Madrid'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Aeroporto de Badajoz (SW, 329.1 km)'
                        '\n2 -> Aeroporto de Córdoba (SW, 313.3 km)'
                        '\n3 -> Aeroporto de Faro (SW, 542.0 km)'
                        '\n4 -> Aeroporto de Gibraltar (S, 505.7 km)'
                        '\n5 -> Aeroporto de Lisboa - Terminal 1 (SW, 512.4 km)'
                        '\n6 -> Aeroporto de Málaga - Costa del Sol (S, 429.8 km)'
                        '\n7 -> Aeroporto de Sevilha (SW, 395.2 km)'
                        '\n8 -> Aeroporto Federico García Lorca Granada-Jaén (S, 367.0 km)'
                        '\n9 -> Aeroporto Internacional de Ciudad Real (S, 182.6 km)'
                        '\n10 -> Transfer between means of transport'
                        '\n11 -> Show location information'
                        '\n12 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["11", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 600 meters'
                        '\nCoordinates: 40.472124, -3.570989'
                        '\nDistrict: Barajas'
                        '\nMunicipality: Madrid'
                        '\nComarca: Área Metropolitana y Corredor del Henares'
                        '\nAutonomous community: Comunidade de Madrid'
                        '\nCountry: Spain'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["12", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 565.3 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_spanish_location_without_comarca(self):
        # Also tests locations in Extremadura
        """
        Destination is Badajoz Airport, the airport serving the city of Badajoz, a province capital and a major city of
            Extremadura in Spain, facing the border with Portugal
        Route: Guerreiros do Rio > Boat > Mértola > Car > Beja > Plane > Badajoz
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "1", "1", "1", "2", "3", "1", "1", "1", "1", "3", "3",
                              "6", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Aeroporto de Badajoz, Badajoz, Badajoz Province, Extremadura'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> Aeroporto de Beja (SW, 132.4 km)'
                        '\n2 -> Aeroporto de Faro (SW, 231.5 km)'
                        '\n3 -> Aeroporto de Sevilha (SE, 182.8 km)'
                        '\n4 -> Aeroporto de Córdoba (SE, 208.1 km)'
                        '\n5 -> Aeroporto de Madrid-Barajas - Terminal 3 (NE, 329.1 km)'
                        '\n6 -> Aeroporto de Lisboa - Terminal 1 (W, 201.1 km)'
                        '\n7 -> Aeroporto de Salamanca (N, 254.9 km)'
                        '\n8 -> Aeroporto de Alicante-Elche Miguel Hernández (E, 549.8 km)'
                        '\n9 -> Aeródromo de Viseu (NW, 223.4 km)'
                        '\n10 -> Aeroporto Internacional de Ciudad Real (E, 247.4 km)'
                        '\n11 -> Aeroporto do Porto (NW, 305.8 km)'
                        '\n12 -> Return to the road'
                        '\n13 -> Show location information'
                        '\n14 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["13", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 180 meters'
                        '\nCoordinates: 38.894054, -6.818687'
                        '\nMunicipality: Badajoz'
                        '\nMancomunidad integral: None'
                        '\nProvince: Badajoz'
                        '\nAutonomous community: Extremadura'
                        '\nCountry: Spain'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["14", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 236.2 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_spanish_location_with_two_comarcas(self):
        """
        Destination is A-4 - Exit 523, a freeway exit in the municipality of Carmona, a city in Seville province in Spain
        Route: Guerreiros do Rio > Boat > Mértola > Car > Beja > Plane > Seville > A-4 > Carmona
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "1", "1", "1", "2", "3", "1", "1", "1", "1", "3", "3",
                              "2", "16", "2", "2", "2", "2", "2", "2", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in A-4 - Saída 523, Carmona, Sevilha Province, Andaluzia'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> A-4 - Saída 524 (SW, 1.2 km) » A-4: Direction Sevilha'
                        '\n2 -> A-4 - Saída 521 (NE, 2.7 km) » A-4: Direction Córdoba'
                        '\n3 -> Show location information'
                        '\n4 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["3", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 65 meters'
                        '\nCoordinates: 37.435568, -5.808407'
                        '\nMunicipality: Carmona'
                        '\nComarcas: Campiña de Carmona, Los Alcores'
                        '\nProvince: Sevilha'
                        '\nAutonomous community: Andaluzia'
                        '\nCountry: Spain'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 306.4 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_spanish_murcia_location_without_district(self):
        """
        Destination is A-7 - Exit 661, a freeway exit in the municipality of Puerto Lumbreras, a city in Murcia Region
            in Spain, next to the border with the Andalucía region
        Route: Guerreiros do Rio > Boat > Mértola > Car > Beja > Plane > Almería > A-7 > Puerto Lumbreras
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "1", "1", "1", "2", "3", "1", "1", "1", "1", "3", "3",
                              "2", "11", "6", "1", "1", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2",
                              "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in A-7 - Saída 661, Puerto Lumbreras, Região de Murcia'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> A-7 - Saída 565 (SW, 2.0 km) » A-7: Direction Almería / Vera'
                        '\n2 -> A-7 - Saída 655 (NE, 6.3 km) » A-7: Direction Murcia'
                        '\n3 -> Show location information'
                        '\n4 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["3", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 454 meters'
                        '\nCoordinates: 37.49118, -1.852587'
                        '\nMunicipality: Puerto Lumbreras'
                        '\nComarca: Alto Guadalentín'
                        '\nAutonomous community: Região de Murcia'
                        '\nCountry: Spain'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 731.8 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_spanish_murcia_location_with_district(self):
        """
        Destination is A-7 - Exit 585, a freeway exit in the municipality of Murcia, the capital city of the
            Murcia Region in Spain
        Route: Guerreiros do Rio > Boat > Mértola > Car > Beja > Plane > Almería > A-7 > Murcia
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "1", "1", "1", "2", "3", "1", "1", "1", "1", "3", "3",
                              "2", "11", "6", "1", "1", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2",
                              "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2",
                              "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2",
                              "2", "2", "2", "2", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in A-7 - Saída 585, Murcia, Região de Murcia'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> A-7 - Saída 586 (SW, 1.6 km) » A-7: Direction Alhama de Murcia / Almería / Granada'
                        '\n2 -> A-7 - Saída 584 (NE, 0.6 km) » A-7: Direction Murcia'
                        '\n3 -> Show location information'
                        '\n4 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["3", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 123 meters'
                        '\nCoordinates: 37.927779, -1.284138'
                        '\nDistrict/pedanía: Sangonera la Seca'
                        '\nMunicipality: Murcia'
                        '\nComarca: Huerta de Murcia'
                        '\nAutonomous community: Região de Murcia'
                        '\nCountry: Spain'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 810.2 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_spanish_galicia_location(self):
        """
        Destination is A-55 - Exit 30, a freeway exit in the municipality of Tui, a city in the Galicia region of Spain
            in the banks of the Minho (pt) / Miño (es and gl) river, facing the border with Portugal
        Route: Guerreiros do Rio > Boat > Mértola > Car > Beja > Plane > Lisbon > High-Speed Train > Coimbra (close to) >
            > A1 > Porto > A3 > Tui
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "1", "1", "1", "2", "3", "1", "1", "1", "1", "3", "3",
                              "7", "17", "1", "3", "1", "2", "2", "4", "2", "2", "2", "3", "2", "2", "2", "2", "2", "2",
                              "2", "2", "2", "2", "2", "3", "1", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2",
                              "2", "2", "2", "2", "2", "2", "2", "2", "2", "3", "3", "3", "3", "2", "2", "2", "2", "2",
                              "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in A-55 - Saída 30, Tui, Pontevedra Province, Galiza'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> A3 - Saída 15 (SE, 0.7 km) » A3: Direction Porto / Valença'
                        '\n2 -> A-55 - Saída 29 (N, 1.3 km) » A-55: Direction A-52 - Ourense / Pontevedra / Vigo'
                        '\n3 -> Show location information'
                        '\n4 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["3", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 30 meters'
                        '\nCoordinates: 42.040413, -8.659667'
                        '\nParish/parroquia: Areas'
                        '\nMunicipality/concello: Tui'
                        '\nComarca: O Baixo Miño'
                        '\nProvince: Pontevedra'
                        '\nAutonomous community: Galiza'
                        '\nCountry: Spain'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 672.5 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())

    def test_spanish_multilanguage_location(self):
        """
        Destination is the Alicante-Elche Airport, in the south of the Valencian Community in Spain near the Mediterranean Coast,
            where Valencian is a co-official language and coexists with Spanish
        Route: Guerreiros do Rio > Boat > Mértola > Car > Beja > Plane > Lisbon > Plane > Close to Alacant (Valencian) / Alicante (Spanish)
        """
        stdout_redirect: io.StringIO = _redirect_output()
        options: list[str] = ["3", "2", "1", "1", "1", "1", "1", "1", "1", "1", "2", "3", "1", "1", "1", "1", "3", "3",
                              "7", "13", "11", "0"]
        with unittest.mock.patch('builtins.input',
                                 side_effect=options):  # Final 0 exits menu loop and allows to get the journey state
            self.travel.make_journey()

        self.assertTrue('\nYou are in Aeroporto de Alicante-Elche Miguel Hernández, Elx / Elche, Alacant / Alicante Province, Comunidade Valenciana'
                        '\nSelect one of the following options'
                        '\n0 -> Exit program'
                        '\n1 -> N-338 - Saída 2 (N, 0.5 km)'
                        '\n2 -> Board a plane'
                        '\n3 -> Show location information'
                        '\n4 -> Show journey statistics'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["3", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nAltitude: 28 meters'
                        '\nCoordinates: 38.2883, -0.5569'
                        '\nMunicipality: Elx / Elche'
                        '\nComarca: Baix Vinalopó / Bajo Vinalopó'
                        '\nProvince: Alacant / Alicante'
                        '\nAutonomous community: Comunidade Valenciana'
                        '\nCountry: Spain'
                        in stdout_redirect.getvalue())

        with unittest.mock.patch('builtins.input', side_effect=["4", "0"]):
            self.travel.make_journey()

        self.assertTrue('\nYou have traveled 984.3 km'
                        f'\nYou have been travelling for {self.travel.current_journey.get_elapsed_time()}'
                        f'\nYou have consumed {self.travel.current_journey.get_fuel_consumption()} liters of fuel'
                        f'\nYou have spent {self.travel.current_journey.get_consumed_fuel_price()} euros in fuel'
                        in stdout_redirect.getvalue())
