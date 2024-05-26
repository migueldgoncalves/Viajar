import unittest
import time

from car.car_simulator import CarSimulator
from car import car_simulator
from car import vehicle


class CarSimulatorTest(unittest.TestCase):

    def setUp(self):
        self.car_simulator: CarSimulator = CarSimulator()

    def test_constructor(self):
        self.assertEqual(0.0, self.car_simulator.speed)
        self.assertEqual(0.0, self.car_simulator.rpm)
        self.assertEqual(vehicle.NEUTRAL_GEAR, self.car_simulator.gear)
        self.assertEqual(0.0, self.car_simulator.travelled_distance)
        self.assertEqual(car_simulator.MODE_IDLE, self.car_simulator.mode)
        self.assertEqual(0.0, self.car_simulator.last_read_input)

    def test_print_instructions(self):
        CarSimulator.print_instructions()  # Ensure no exception is raised

    def test_change_gear_invalid_gear(self):
        self.car_simulator.change_gear(-2)
        self.assertEqual(vehicle.NEUTRAL_GEAR, self.car_simulator.gear)
        self.assertEqual(0, self.car_simulator.rpm)

        self.car_simulator.change_gear(self.car_simulator.car.get_forward_gear_count() + 1)
        self.assertEqual(vehicle.NEUTRAL_GEAR, self.car_simulator.gear)
        self.assertEqual(0, self.car_simulator.rpm)

    def test_change_gear_while_stopped(self):
        self.car_simulator.change_gear(vehicle.NEUTRAL_GEAR)
        self.assertEqual(vehicle.NEUTRAL_GEAR, self.car_simulator.gear)
        self.assertEqual(0, self.car_simulator.rpm)

        self.car_simulator.change_gear(vehicle.REVERSE_GEAR)
        self.assertEqual(vehicle.REVERSE_GEAR, self.car_simulator.gear)
        self.assertEqual(0, self.car_simulator.rpm)

        self.car_simulator.change_gear(1)
        self.assertEqual(1, self.car_simulator.gear)
        self.assertEqual(0, self.car_simulator.rpm)

        self.car_simulator.change_gear(self.car_simulator.car.get_forward_gear_count())
        self.assertEqual(self.car_simulator.car.get_forward_gear_count(), self.car_simulator.gear)
        self.assertEqual(0, self.car_simulator.rpm)

    def test_change_gear_while_moving(self):
        self.car_simulator.speed = 30

        self.car_simulator.change_gear(vehicle.NEUTRAL_GEAR)
        self.assertEqual(vehicle.NEUTRAL_GEAR, self.car_simulator.gear)
        self.assertEqual(0.0, self.car_simulator.rpm)

        self.car_simulator.change_gear(vehicle.REVERSE_GEAR)
        self.assertEqual(vehicle.REVERSE_GEAR, self.car_simulator.gear)
        self.assertEqual(4875.0, self.car_simulator.rpm)

        self.car_simulator.change_gear(1)
        self.assertEqual(1, self.car_simulator.gear)
        self.assertEqual(4875.0, self.car_simulator.rpm)

        self.car_simulator.change_gear(self.car_simulator.car.get_forward_gear_count())
        self.assertEqual(self.car_simulator.car.get_forward_gear_count(), self.car_simulator.gear)
        self.assertEqual(975.0, self.car_simulator.rpm)

    def test_accelerate_car_for_an_instant(self):
        test_start_time: float = time.time()

        self.car_simulator.accelerate_car()
        self.assertTrue(self.car_simulator.last_read_input >= test_start_time)
        self.assertEqual(car_simulator.MODE_ACCELERATING, self.car_simulator.mode)
        self.assertEqual(0.0, self.car_simulator.speed)
        self.assertEqual(0.0, self.car_simulator.rpm)
        self.assertEqual(vehicle.NEUTRAL_GEAR, self.car_simulator.gear)

    def test_accelerate_car_neutral_gear(self):
        test_start_time: float = time.time()

        for _ in range(10):
            self.car_simulator.accelerate_car()  # Simulates holding accelerate button
            time.sleep(car_simulator.WAIT_FOR_INPUT / 2)  # Prevents acceleration commands from being sent in a very short time interval
        self.assertTrue(self.car_simulator.last_read_input >= test_start_time)
        self.assertEqual(car_simulator.MODE_ACCELERATING, self.car_simulator.mode)
        self.assertEqual(0.0, self.car_simulator.speed)
        self.assertEqual(0.0, self.car_simulator.rpm)
        self.assertEqual(vehicle.NEUTRAL_GEAR, self.car_simulator.gear)

    def test_accelerate_car_forward_gear(self):
        gear = 1
        test_start_time: float = time.time()
        self.car_simulator.change_gear(gear)

        # Acceleration to valid RPM
        for _ in range(10):  # Accelerates for 1 s
            self.car_simulator.accelerate_car()  # Simulates holding accelerate button
            time.sleep(car_simulator.WAIT_FOR_INPUT / 2)  # Prevents acceleration commands from being sent in a very short time interval
        self.assertTrue(self.car_simulator.last_read_input >= test_start_time)
        self.assertEqual(car_simulator.MODE_ACCELERATING, self.car_simulator.mode)
        self.assertTrue(18 < self.car_simulator.speed < 21)
        self.assertTrue(2900 < self.car_simulator.rpm < 3300)
        self.assertEqual(gear, self.car_simulator.gear)

        current_time: float = time.time()

        # Trying to accelerate past max RPM
        for _ in range(20):  # Accelerates for another 2 s
            self.car_simulator.accelerate_car()  # Simulates holding accelerate button
            time.sleep(car_simulator.WAIT_FOR_INPUT / 2)  # Prevents acceleration commands from being sent in a very short time interval
        self.assertTrue(self.car_simulator.last_read_input >= current_time)
        self.assertEqual(car_simulator.MODE_ACCELERATING, self.car_simulator.mode)
        self.assertTrue(49 < self.car_simulator.speed < 51)
        self.assertTrue(8100 < self.car_simulator.rpm < 8300)
        self.assertEqual(gear, self.car_simulator.gear)

    def test_accelerate_car_reverse_gear(self):
        gear = -1
        test_start_time: float = time.time()
        self.car_simulator.change_gear(gear)

        # Acceleration to valid RPM
        for _ in range(10):  # Accelerates for 1 s
            self.car_simulator.accelerate_car()  # Simulates holding accelerate button
            time.sleep(car_simulator.WAIT_FOR_INPUT / 2)  # Prevents acceleration commands from being sent in a very short time interval
        self.assertTrue(self.car_simulator.last_read_input >= test_start_time)
        self.assertEqual(car_simulator.MODE_ACCELERATING, self.car_simulator.mode)
        self.assertTrue(-20 < self.car_simulator.speed < -18)
        self.assertTrue(2900 < self.car_simulator.rpm < 3250)
        self.assertEqual(gear, self.car_simulator.gear)

        current_time: float = time.time()

        # Trying to accelerate past max RPM
        for _ in range(20):  # Accelerates for another 2 s
            self.car_simulator.accelerate_car()  # Simulates holding accelerate button
            time.sleep(car_simulator.WAIT_FOR_INPUT / 2)  # Prevents acceleration commands from being sent in a very short time interval
        self.assertTrue(self.car_simulator.last_read_input >= current_time)
        self.assertEqual(car_simulator.MODE_ACCELERATING, self.car_simulator.mode)
        self.assertTrue(-51 < self.car_simulator.speed < -49)
        self.assertTrue(7962 < self.car_simulator.rpm < 8288)
        self.assertEqual(gear, self.car_simulator.gear)

    def test_decelerate_car_for_an_instant(self):
        test_start_time: float = time.time()
        gear = 4
        self.car_simulator.change_gear(gear)
        self.car_simulator.speed = 100
        self.car_simulator.update_rpm()

        # Brake car - No speed reduction should happen
        self.car_simulator.decelerate_car(car_simulator.MODE_BRAKING)
        self.assertTrue(self.car_simulator.last_read_input >= test_start_time)
        self.assertEqual(car_simulator.MODE_BRAKING, self.car_simulator.mode)
        self.assertEqual(100.0, self.car_simulator.speed)
        self.assertEqual(4062.5, self.car_simulator.rpm)
        self.assertEqual(gear, self.car_simulator.gear)

        test_start_time = time.time()

        # Decelerate car through friction - Speed reduction should happen
        self.car_simulator.decelerate_car(car_simulator.MODE_IDLE)
        self.assertTrue(self.car_simulator.last_read_input < test_start_time)  # No user input was simulated
        self.assertEqual(car_simulator.MODE_IDLE, self.car_simulator.mode)
        self.assertEqual(98.0, self.car_simulator.speed)
        self.assertEqual(3981.25, self.car_simulator.rpm)
        self.assertEqual(gear, self.car_simulator.gear)

    def test_brake_while_going_forward(self):
        test_start_time: float = time.time()
        gear = 4
        self.car_simulator.change_gear(gear)
        self.car_simulator.speed = 100
        self.car_simulator.update_rpm()

        # Reduces speed
        for _ in range(10):
            self.car_simulator.decelerate_car(car_simulator.MODE_BRAKING)  # Simulates holding brake button
            time.sleep(car_simulator.WAIT_FOR_INPUT / 2)
        self.assertTrue(self.car_simulator.last_read_input >= test_start_time)
        self.assertEqual(car_simulator.MODE_BRAKING, self.car_simulator.mode)
        self.assertTrue(60 < self.car_simulator.speed < 64)
        self.assertTrue(2437 < self.car_simulator.rpm < 2600)
        self.assertEqual(gear, self.car_simulator.gear)

        test_start_time = time.time()

        # Stops car and ensure speed remains at 0
        for _ in range(20):
            self.car_simulator.decelerate_car(car_simulator.MODE_BRAKING)  # Simulates holding brake button
            time.sleep(car_simulator.WAIT_FOR_INPUT / 2)
        self.assertTrue(self.car_simulator.last_read_input >= test_start_time)
        self.assertEqual(car_simulator.MODE_BRAKING, self.car_simulator.mode)
        self.assertEqual(0.0, self.car_simulator.speed)
        self.assertEqual(0.0, self.car_simulator.rpm)
        self.assertEqual(gear, self.car_simulator.gear)

    def test_decelerate_while_going_forward(self):
        gear = 4
        self.car_simulator.change_gear(gear)
        self.car_simulator.speed = 100
        self.car_simulator.update_rpm()

        # Expected to be reset when decelerating through friction
        self.car_simulator.last_read_input = 1.0
        self.car_simulator.mode = car_simulator.MODE_ACCELERATING

        # Reduces speed
        for _ in range(10):
            self.car_simulator.decelerate_car(car_simulator.MODE_IDLE)  # Simulates holding brake button
            time.sleep(car_simulator.WAIT_FOR_INPUT)
        self.assertEqual(0.0, self.car_simulator.last_read_input)
        self.assertEqual(car_simulator.MODE_IDLE, self.car_simulator.mode)
        self.assertEqual(80.0, self.car_simulator.speed)
        self.assertEqual(3250.0, self.car_simulator.rpm)
        self.assertEqual(gear, self.car_simulator.gear)

        # Stops car and ensure speed remains at 0
        for _ in range(50):
            self.car_simulator.decelerate_car(car_simulator.MODE_IDLE)  # Simulates holding brake button
            time.sleep(car_simulator.WAIT_FOR_INPUT)
        self.assertEqual(0.0, self.car_simulator.last_read_input)
        self.assertEqual(car_simulator.MODE_IDLE, self.car_simulator.mode)
        self.assertEqual(0.0, self.car_simulator.speed)
        self.assertEqual(0.0, self.car_simulator.rpm)
        self.assertEqual(gear, self.car_simulator.gear)

    def test_brake_while_reversing(self):
        test_start_time: float = time.time()
        gear = vehicle.REVERSE_GEAR
        self.car_simulator.change_gear(gear)
        self.car_simulator.speed = -30
        self.car_simulator.update_rpm()

        # Reduces speed
        for _ in range(2):
            self.car_simulator.decelerate_car(car_simulator.MODE_BRAKING)  # Simulates holding brake button
            time.sleep(car_simulator.WAIT_FOR_INPUT / 2)
        self.assertTrue(self.car_simulator.last_read_input >= test_start_time)
        self.assertEqual(car_simulator.MODE_BRAKING, self.car_simulator.mode)
        self.assertTrue(-27 < self.car_simulator.speed < -25)
        self.assertTrue(4062 < self.car_simulator.rpm < 4388)
        self.assertEqual(gear, self.car_simulator.gear)

        test_start_time = time.time()

        # Stops car and ensure speed remains at 0
        for _ in range(30):
            self.car_simulator.decelerate_car(car_simulator.MODE_BRAKING)  # Simulates holding brake button
            time.sleep(car_simulator.WAIT_FOR_INPUT / 2)
        self.assertTrue(self.car_simulator.last_read_input >= test_start_time)
        self.assertEqual(car_simulator.MODE_BRAKING, self.car_simulator.mode)
        self.assertEqual(0.0, self.car_simulator.speed)
        self.assertEqual(0.0, self.car_simulator.rpm)
        self.assertEqual(gear, self.car_simulator.gear)

    def test_decelerate_while_reversing(self):
        gear = vehicle.REVERSE_GEAR
        self.car_simulator.change_gear(gear)
        self.car_simulator.speed = -30
        self.car_simulator.update_rpm()

        # Expected to be reset when decelerating through friction
        self.car_simulator.last_read_input = 1.0
        self.car_simulator.mode = car_simulator.MODE_ACCELERATING

        # Reduces speed
        for _ in range(10):
            self.car_simulator.decelerate_car(car_simulator.MODE_IDLE)  # Simulates holding brake button
            time.sleep(car_simulator.WAIT_FOR_INPUT)
        self.assertEqual(0.0, self.car_simulator.last_read_input)
        self.assertEqual(car_simulator.MODE_IDLE, self.car_simulator.mode)
        self.assertEqual(-10.0, self.car_simulator.speed)
        self.assertEqual(1625.0, self.car_simulator.rpm)
        self.assertEqual(gear, self.car_simulator.gear)

        # Stops car and ensure speed remains at 0
        for _ in range(20):
            self.car_simulator.decelerate_car(car_simulator.MODE_IDLE)  # Simulates holding brake button
            time.sleep(car_simulator.WAIT_FOR_INPUT)
        self.assertEqual(0.0, self.car_simulator.last_read_input)
        self.assertEqual(car_simulator.MODE_IDLE, self.car_simulator.mode)
        self.assertEqual(0.0, self.car_simulator.speed)
        self.assertEqual(0.0, self.car_simulator.rpm)
        self.assertEqual(gear, self.car_simulator.gear)

    def test_print_gear(self):
        self.car_simulator.print_gear()  # Ensure no exception is raised

    def test_print_rpm(self):
        self.car_simulator.print_rpm()  # Ensure no exception is raised

    def test_print_distance(self):
        self.car_simulator.print_distance(0, None)  # Ensure no exception is raised
        self.car_simulator.print_distance(1.0, 'Guerreiros do Rio')

    def test_print_car_state(self):
        self.car_simulator.print_car_state(0, None)  # Ensure no exception is raised
        self.car_simulator.print_car_state(1.0, 'Guerreiros do Rio')

    def test_update_rpm(self):
        self.car_simulator.update_rpm()
        self.assertEqual(0.0, self.car_simulator.rpm)

        self.car_simulator.speed = 100
        self.car_simulator.gear = 4
        self.car_simulator.update_rpm()
        self.assertEqual(4062.5, self.car_simulator.rpm)

        self.car_simulator.speed = -30
        self.car_simulator.gear = vehicle.REVERSE_GEAR
        self.car_simulator.update_rpm()
        self.assertEqual(4875.0, self.car_simulator.rpm)

    def test_increment_distance_while_stopped(self):
        elapsed_time = 0
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(0.0, self.car_simulator.travelled_distance)

        elapsed_time = 1.0
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(0.0, self.car_simulator.travelled_distance)

        elapsed_time = -1.0  # Invalid
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(0.0, self.car_simulator.travelled_distance)

    def test_increment_distance_while_moving_forward(self):
        self.car_simulator.speed = 100

        elapsed_time = 0
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(0.0, self.car_simulator.travelled_distance)

        elapsed_time = 1.0
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(0.027777777777777776, self.car_simulator.travelled_distance)

        elapsed_time = -1.0  # Invalid
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(0.027777777777777776, self.car_simulator.travelled_distance)

    def test_increment_distance_while_reversing(self):
        self.car_simulator.speed = -30

        elapsed_time = 0
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(0.0, self.car_simulator.travelled_distance)

        elapsed_time = 1.0
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(-0.008333333333333333, self.car_simulator.travelled_distance)

        elapsed_time = -1.0  # Invalid
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(-0.008333333333333333, self.car_simulator.travelled_distance)

    def test_increment_distance_forward_then_reversing(self):
        self.car_simulator.speed = 30

        elapsed_time = 1.0
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(0.008333333333333333, self.car_simulator.travelled_distance)

        self.car_simulator.speed = -30

        elapsed_time = 2.0
        self.car_simulator.increment_distance_by_elapsed_time(elapsed_time)
        self.assertEqual(-0.008333333333333333, self.car_simulator.travelled_distance)

    def test_reset_simulation(self):
        # Setup
        self.car_simulator.speed = 100
        self.car_simulator.rpm = 5000
        self.car_simulator.gear = 4
        self.car_simulator.travelled_distance = 4.0

        self.car_simulator.reset_car_simulation()

        self.assertEqual(0.0, self.car_simulator.speed)
        self.assertEqual(0.0, self.car_simulator.rpm)
        self.assertEqual(vehicle.NEUTRAL_GEAR, self.car_simulator.gear)
        self.assertEqual(0.0, self.car_simulator.travelled_distance)
