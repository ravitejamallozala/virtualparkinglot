import unittest
from virtual_parking import ParkingProcessor, ParkingLot, CommandProcessor, FileUtility


class ParkingLotTest(unittest.TestCase):
    """
    Test class: ParkingLotTest
        Contains unittest cases to test functions of ParkingLot class
    """

    def setUp(self) -> None:
        self.plot = ParkingLot()

    def test_create_parking_lot_valid(self):
        """ Testing create_parkinglot() function with 6 slots """
        command = ['Create_parking_lot', '6']
        self.plot.create_parkinglot(command)
        self.assertEqual(len(self.plot.slots), 6)
        self.assertEqual(self.plot.total_slots, 6)
        self.assertEqual(self.plot.avail_slot, 0)
        self.assertEqual(self.plot.slot_heap, [])

    def test_create_parking_lot_neg(self):
        """ Testing create_parkinglot() function with invalid negative number of slots"""
        command = ['Create_parking_lot', '-6']
        self.plot.create_parkinglot(command)
        self.assertEqual(len(self.plot.slots), 0)
        self.assertEqual(self.plot.total_slots, None)
        self.assertEqual(self.plot.avail_slot, None)
        self.assertEqual(self.plot.slot_heap, [])

    def test_create_parking_lot_char(self):
        """  Testing create_parkinglot() with invalid input char for slot """
        command = ['Create_parking_lot', 's']
        self.plot.create_parkinglot(command)
        self.assertEqual(len(self.plot.slots), 0)
        self.assertEqual(self.plot.total_slots, None)
        self.assertEqual(self.plot.avail_slot, None)
        self.assertEqual(self.plot.slot_heap, [])

    def test_get_slot_valid(self):
        """ Testing creation of parking lot with 4 slots and checking get_emptyslot() function """
        command = ['Create_parking_lot', '4']
        self.plot.create_parkinglot(command)
        self.assertEqual(self.plot.get_emptyslot(), 0)
        self.assertEqual(self.plot.get_emptyslot(), 1)
        self.assertEqual(self.plot.get_emptyslot(), 2)
        self.assertEqual(self.plot.get_emptyslot(), 3)

    def test_get_slot_slotsfull(self):
        """
         Testing creation of parking lot with 3 slots and\
         checking get_emptyslot() function till no slots available
        """
        command = ['Create_parking_lot', '3']
        self.plot.create_parkinglot(command)
        self.assertEqual(self.plot.get_emptyslot(), 0)
        self.assertEqual(self.plot.get_emptyslot(), 1)
        self.assertEqual(self.plot.get_emptyslot(), 2)
        self.assertEqual(self.plot.get_emptyslot(), None)

    def test_get_slot_del(self):
        """
            Testing creation of parking lot with 3 slots and checking get_emptyslot() function after \
            parking 2 vehicles and Leave one vehicle
        """

        command = ['Create_parking_lot', '3']
        self.plot.create_parkinglot(command)
        process_prk_obj = ParkingProcessor(self.plot)
        veh1 = "Park PB-01-TG-2361 driver_age 40".split()
        process_prk_obj.park_vehicle(veh1)
        self.assertEqual(self.plot.get_emptyslot(), 1)
        veh1 = "Park AB-01-TG-1234 driver_age 10".split()
        self.assertEqual(self.plot.get_emptyslot(), 2)
        process_prk_obj.park_vehicle(veh1)
        leave1 = "Leave 2".split()
        process_prk_obj.exit_vehicle(leave1)
        self.assertEqual(self.plot.get_emptyslot(), None)


class CommandProcessorTest(unittest.TestCase):
    """
        Test class: CommandProcessorTest
            Contains unittest cases to test functions of CommandProcessor class
    """

    def setUp(self) -> None:
        """ Setting up default objects to check the functionalities  """

        self.file_obj = FileUtility()
        self.plot = ParkingLot()
        self.park_processor_obj = ParkingProcessor(self.plot)
        # self.cmd_processor_obj = CommandProcessor(self.file, self.park_processor_obj)

    def test_process_command_valid(self):
        """ Testing process_command() function with use of create_parking_lot command """

        cmd_proc_obj = CommandProcessor(self.file_obj, self.park_processor_obj)
        cmd = "Create_parking_lot 7".split()
        cmd_proc_obj.process_command(cmd)
        self.assertEqual(len(self.plot.slots), 7)

    def test_process_command_invalid(self):
        """ Testing process_command() function with and invalid command as input """
        cmd_proc_obj = CommandProcessor(self.file_obj, self.park_processor_obj)
        cmd = "".split()
        cmd_proc_obj.process_command(cmd)
        self.assertEqual(len(self.plot.slots), 0)
        self.assertEqual(self.plot.total_slots, None)

    def test_execute_command_valid(self):
        """
         Testing execute_command() function with use of create_parking_lot and \
         Park vehicle commands present in test1.txt file
         """
        self.file_obj.load_file("test_files/test1.txt")
        cmd_proc_obj = CommandProcessor(self.file_obj, self.park_processor_obj)
        cmd_proc_obj.execute_commands()
        self.assertEqual(len(self.plot.slots), 2)
        self.assertEqual(self.plot.total_slots, 2)
        self.assertEqual(self.plot.age_slot_dict, {21: [], 12: [2]})


class ParkingProcessorTest(unittest.TestCase):
    """
        Test class: CommandProcessorTest
            Contains unittest cases to test functions of ParkingProcessor class
    """

    def setUp(self) -> None:
        self.plot = ParkingLot()


if __name__ == '__main__':
    unittest.main()
