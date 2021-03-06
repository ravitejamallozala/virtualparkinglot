import re
from heapq import heapify, heappush, heappop
from collections import defaultdict
import sys

from utils import FileUtility


class ParkingLot:
    """
       ParkingLot is a virtual parking lot with n number of parking slots.
       provides utility funtions :
         create_parkinglot() - this function to create a virtual parking lot with 'n' slots.
         get_emptyslot() - this function will return the next best available parking slot.
       Usage:
         slots:   intialises as empty list to store the vehicle info when car is parked
         total_slots: to maintain the maximum number of slots available in the parking lot
         avail_slot: to maintain the available parking slot number when we are first filling the parking lot
         reg_slot_dict: this dict is used to store the data of registration number mapped to its slot number
         age_slot_dict: this dict is used to store the data of all the slot numbers for a particular age
         slot_heap:  This is Min Heap used to store the slots which become empty after vehicle exits the parking lot.
                    Min heap is used to always get the minimum slot for the next car to park
    """

    def __init__(self, slots=None, total_slots=None, avail_slot=None, reg_slot_dict=None,
                 age_slot_dict=None, slot_heap=None):
        self.slots = slots if slots else list()
        self.total_slots = total_slots
        self.avail_slot = avail_slot
        self.reg_slot_dict = reg_slot_dict if reg_slot_dict else dict()
        self.age_slot_dict = defaultdict(list, age_slot_dict) if age_slot_dict else defaultdict(list)
        self.slot_heap = slot_heap if slot_heap else list()
        heapify(self.slot_heap)

    def create_parkinglot(self, command_toks):
        """
        Command-  "Create_parking_lot 6"
        :param command_toks: Array with the command and value example- ["Create_parking_lot", "6"]
        :return: None
        """
        if not len(command_toks) == 2 and not re.match(r'\d', command_toks[1]):
            print('Invalid "Create_parking_lot" Command Format')
        else:
            try:
                num_of_slots = int(command_toks[1])
                if not num_of_slots > 0:
                    print("Number of Parking slots should be a Positive integer")
                    return
                self.total_slots = int(command_toks[1])
                self.slots = [None for _ in range(num_of_slots)]
                print(f"Created parking of {num_of_slots} slots")
                if num_of_slots > 0:
                    self.avail_slot = 0
            except ValueError:
                print('Invalid "Create_parking_lot" Command Format')

    def get_emptyslot(self):
        """
        :param: Takes no Input
        :return: Integer value: Best least empty Slot in which the car can be parked
                None if there are no empty slots available
        avail_slot : to maintain the available parking slot number when we are first filling the parking lot
             if any slot is available in heap will return slotnum from slot_heap(comes only anyone leaves the parking)
             Min heap is used to always get the minimum slot for the next car to park
        """
        if not self.slot_heap and self.avail_slot < self.total_slots:
            slot = self.avail_slot
            self.avail_slot += 1
            return slot
        elif self.slot_heap:
            return heappop(self.slot_heap)
        else:
            print("Sorry! No Parking spaces available")
            return None


class ParkingProcessor:
    """
    ParkingProcessor is factory which process the commands on the Parkinglot
    """

    def __init__(self, parkinglot_obj):
        self.parkinglot_obj = parkinglot_obj

    def park_vehicle(self, command_toks):
        """
        Command-  "Park KA-01-HH-1234 driver_age 21"
        :param command_toks: Array with the command and value example- ["Park", "KA-01-HH-1234", "driver_age", "21"]
        :return: None
        """
        reg_num = re.match(r'[A-Z]{2}-\d{2}-[A-Z]{2}-\d{4}', command_toks[1])
        reg_num = reg_num.group() if reg_num else None
        age = re.match(r'\d+', command_toks[3])
        age = age.group() if age else None
        if len(command_toks) == 4 and not reg_num is None and command_toks[2] == "driver_age" and not age is None:
            reg_num = reg_num
            age = int(age)
            slot = self.parkinglot_obj.get_emptyslot()
            if slot is None:
                return
            # print("available slot: ", slot)
            """Parking the Car in that slot """
            self.parkinglot_obj.slots[slot] = {
                "reg_num": reg_num, "age": age}
            """Maintaing redundant data for ease of queriring"""
            self.parkinglot_obj.reg_slot_dict[reg_num] = slot
            self.parkinglot_obj.age_slot_dict[age].append(slot + 1)
            print(f"Car with vehicle registration number {reg_num} has been parked at slot number {slot + 1}")
        else:
            print('Invalid "Park" vehicle Command Format')

    def exit_vehicle(self, command_toks):
        """
        Command-  "Leave 2"
        :param command_toks: Array with the command and value example- ["Leave","2"]
        :return: None
        """
        slot = re.match(r'\d+', command_toks[1])
        slot = slot.group() if slot else None
        if len(command_toks) == 2 and slot:
            vehicle_data = self.parkinglot_obj.slots[int(slot) - 1]
            if vehicle_data:
                try:
                    self.parkinglot_obj.slots[int(slot) - 1] = None
                    if vehicle_data['reg_num'] in self.parkinglot_obj.reg_slot_dict:
                        del self.parkinglot_obj.reg_slot_dict[vehicle_data['reg_num']]
                    self.parkinglot_obj.age_slot_dict[vehicle_data['age']].remove(int(slot))
                    heappush(self.parkinglot_obj.slot_heap, int(slot) - 1)
                except ValueError:
                    pass
                print(
                    f"Slot number {slot} vacated, the car with vehicle registration number {vehicle_data['reg_num']} left the space, the driver of the car was of age {vehicle_data['age']}")
            else:
                print(f"Slot Already vacant")
        else:
            print('Invalid "Leave" Command Format')

    def get_slots_by_age(self, command_toks):
        """
        Command: "Slot_numbers_for_driver_of_age 21
        :param command_toks: Array with the command and value example- ["Slot_numbers_for_driver_of_age", "21"]
        :return: String: Returns the comma separated string with all the slots for the given age
                None if no slots are present for the given age
        """
        age = re.match(r'\d+', command_toks[1])
        age = age.group() if age else None
        if len(command_toks) == 2 and age:
            result = self.parkinglot_obj.age_slot_dict[int(age)]
            if not result is None:
                print(",".join(str(i) for i in result))
                return ",".join(str(i) for i in result)
            else:
                print("No parked car matches the query")
        else:
            print('Invalid "Slot_numbers_for_driver_of_age" Command Format')
        return None

    def get_slot_by_num(self, command_toks):
        """
        Command: "Slot_number_for_car_with_number PB-01-HH-1234"
        :param command_toks: Array with the command and value example- ["Slot_number_for_car_with_number", "PB-01-HH-1234"]
        :return: Integer: Returns the Slot num for the given registration number of vehicle
                None if no slots are present for the given registration number of vehicle
        """

        reg_num = re.match(r'[A-Z]{2}-\d{2}-[A-Z]{2}-\d{4}', command_toks[1])
        reg_num = reg_num.group() if reg_num else None
        if len(command_toks) == 2 and reg_num:
            result = self.parkinglot_obj.reg_slot_dict.get(reg_num, None)
            if not result is None:
                print(result + 1)  # adding +1  we are storing indexes in reg_slot_dict
                return result + 1
            else:
                print("No parked car matches the query")
        else:
            print('Invalid "Slot_number_for_car_with_number"  Command Format')

    def get_vehiclenums_by_age(self, command_toks):
        """

        Command: "Vehicle_registration_number_for_driver_of_age 18"
        :param command_toks: Array with the command and value example- ["Vehicle_registration_number_for_driver_of_age", "18"]
        :return: String: Returns the comma separated string with all the registration numbers of the vehicles for the given age
                None if no vehicles are present for the given age
        """
        # validating command and executing it
        """ Command: Vehicle_registration_number_for_driver_of_age 18 """
        age = re.match(r'\d+', command_toks[1]).group()
        if len(command_toks) == 2 and age:
            slots = self.parkinglot_obj.age_slot_dict[int(age)]
            if slots:
                reg_nums = [self.parkinglot_obj.slots[slot - 1].get('reg_num') for slot in slots]
                print(",".join(reg_nums))
                return ",".join(reg_nums)
            else:
                print("No parked car matches the query")
        else:
            print('Invalid "Vehicle_registration_number_for_driver_of_age" vehicle Command Format')


class CommandProcessor:
    """
    CommandProcessor process all the commands in the file and routes each command based on its type.

    """

    def __init__(self, file_obj, process_parking_obj):
        self.file_obj = file_obj
        self.process_parking_obj = process_parking_obj

    def execute_commands(self):
        """
        Will execute all the commands which are present in the input file
        :return: None
        """
        if not self.file_obj and self.file_obj.file:
            print("Input File not found to process")
            return
        line_num = 0
        for line in self.file_obj.file:
            line_num += 1
            command = line.strip(" \n ")
            cmd_tokens = command.split()
            if line_num == 0 and cmd_tokens[0] != "Create_parking_lot":
                print("Command to create parking lot is missing in input file")
                break
            self.process_command(cmd_tokens)

    def process_command(self, command_toks):
        """
        Router for the commands in the input file. This function process the command and
        calls the relevant function to execute the command.
        :param command_toks: array - each Command from the Input file
        :return: None
        """
        if not command_toks or not len(command_toks) > 0:
            print("Cannot process the command. Invalid Command Format")
            return
        if command_toks[0] == 'Create_parking_lot':
            self.process_parking_obj.parkinglot_obj.create_parkinglot(command_toks)
        elif command_toks[0] == 'Park':
            self.process_parking_obj.park_vehicle(command_toks)
        elif command_toks[0] == 'Leave':
            self.process_parking_obj.exit_vehicle(command_toks)
        elif command_toks[0] == 'Slot_numbers_for_driver_of_age':
            self.process_parking_obj.get_slots_by_age(command_toks)
        elif command_toks[0] == 'Slot_number_for_car_with_number':
            self.process_parking_obj.get_slot_by_num(command_toks)
        elif command_toks[0] == 'Vehicle_registration_number_for_driver_of_age':
            self.process_parking_obj.get_vehiclenums_by_age(command_toks)
        else:
            print("Command Not matched with valid commands set")


if __name__ == '__main__':
    filename = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    if not filename:
        filename = input("Enter the input file path:\n")
    plot = ParkingLot()
    file_obj = FileUtility()
    file_obj.load_file(filename)
    process_prk_obj = ParkingProcessor(plot)
    command_obj = CommandProcessor(file_obj, process_prk_obj)
    command_obj.execute_commands()
