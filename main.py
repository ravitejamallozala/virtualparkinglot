import re
from heapq import heapify, heappush, heappop
from collections import defaultdict


class Parking:
    def __init__(self):
        self.slots = None
        self.total_slots = None
        self.avail_slot = None
        self.reg_slot_dict = {}
        self.age_slot_dict = defaultdict(list)
        self.slot_heap = []
        heapify(self.slot_heap)

    def create_parkinglot(self, command_toks):
        # validating command and executing it
        # Command-  "Create_parking_lot 6"
        if not len(command_toks) == 2 and not re.match(r'\d', command_toks[1]):
            print('Invalid "Create_parking_lot" Command Format')
        else:
            num_of_slots = int(command_toks[1])
            self.total_slots = int(command_toks[1])
            self.slots = [None for _ in range(num_of_slots)]
            print(f"Created parking of {num_of_slots} slots")
            if num_of_slots > 0:
                self.avail_slot = 0

    def get_emptyslot(self):
        if not self.slot_heap and self.avail_slot < self.total_slots:
            slot = self.avail_slot
            self.avail_slot += 1
            return slot
        elif self.slot_heap:
            return heappop(self.slot_heap)
        else:
            print("Sorry! No Parking spaces available")
            return None

    def park_vehicle(self, command_toks):
        # validating command and executing it
        # Command-  "Park KA-01-HH-1234 driver_age 21"
        reg_num = re.match(r'[A-Z]{2}-\d{2}-[A-Z]{2}-\d{4}', command_toks[1]).group()
        age = re.match(r'\d+', command_toks[3]).group()
        if len(command_toks) == 4 and reg_num and command_toks[2] == "driver_age" and age:
            reg_num = reg_num
            age = int(age)
            slot = self.get_emptyslot()
            if slot is None:
                return
            # print("available slot: ", slot)
            """Parking the Car in that slot """
            self.slots[slot] = {
                "reg_num": reg_num, "age": age}
            """Maintaing redundant data for ease of queriring"""
            self.reg_slot_dict[reg_num] = slot
            self.age_slot_dict[age].append(slot + 1)
            print(f"Car with vehicle registration number {reg_num} has been parked at slot number {slot + 1}")
        else:
            print('Invalid "Park" vehicle Command Format')

    def exit_vehicle(self, command_toks):
        # validating command and executing it
        """ Command: Leave 2"""
        slot = re.match(r'\d+', command_toks[1]).group()
        if len(command_toks) == 2 and slot:
            vehicle_data = self.slots[int(slot) - 1]
            if vehicle_data:
                try:
                    self.slots[int(slot) - 1] = None
                    if vehicle_data['reg_num'] in self.reg_slot_dict:
                        del self.reg_slot_dict[vehicle_data['reg_num']]
                    self.age_slot_dict[vehicle_data['age']].remove(int(slot))
                    heappush(self.slot_heap, int(slot) - 1)
                except ValueError:
                    pass
                print(
                    f"Slot number {slot} vacated, the car with vehicle registration number {vehicle_data['reg_num']} left the space, the driver of the car was of age {vehicle_data['age']}")
            else:
                print(f"Parking space {slot} is already Empty")
        else:
            print('Invalid "Leave" Command Format')

    def get_slots_by_age(self, command_toks):
        """ Command: Slot_numbers_for_driver_of_age 21 """
        age = re.match(r'\d+', command_toks[1]).group()
        if len(command_toks) == 2 and age:
            result = self.age_slot_dict[int(age)]
            if result:
                print(",".join(str(i) for i in result))
            else:
                print("No parked car matches the query")
        else:
            print('Invalid "Slot_numbers_for_driver_of_age" Command Format')

    def get_slot_by_num(self, command_toks):
        # validating command and executing it
        """ Command: Slot_number_for_car_with_number PB-01-HH-1234 """
        reg_num = re.match(r'[A-Z]{2}-\d{2}-[A-Z]{2}-\d{4}', command_toks[1]).group()
        if len(command_toks) == 2 and reg_num:
            result = self.reg_slot_dict.get(reg_num, None)
            if result:
                print(result + 1)  # adding +1  we are storing indexes in reg_slot_dict
            else:
                print("No parked car matches the query")
        else:
            print('Invalid "Slot_number_for_car_with_number"  Command Format')

    def get_vehiclenums_by_age(self, command_toks):
        # validating command and executing it
        """ Command: Vehicle_registration_number_for_driver_of_age 18 """
        age = re.match(r'\d+', command_toks[1]).group()
        if len(command_toks) == 2 and age:
            slots = self.age_slot_dict[int(age)]
            if slots:
                reg_nums = [self.slots[slot - 1].get('reg_num') for slot in slots]
                print(",".join(reg_nums))
            else:
                print("No parked car matches the query")
        else:
            print('Invalid "Vehicle_registration_number_for_driver_of_age" vehicle Command Format')

    def process_command(self, command_toks):
        if command_toks[0] == 'Create_parking_lot':
            self.create_parkinglot(command_toks)
        elif command_toks[0] == 'Park':
            self.park_vehicle(command_toks)
        elif command_toks[0] == 'Leave':
            self.exit_vehicle(command_toks)
        elif command_toks[0] == 'Slot_numbers_for_driver_of_age':
            self.get_slots_by_age(command_toks)
        elif command_toks[0] == 'Slot_number_for_car_with_number':
            self.get_slot_by_num(command_toks)
        elif command_toks[0] == 'Vehicle_registration_number_for_driver_of_age':
            self.get_vehiclenums_by_age(command_toks)

    def load_file(self, filepath):
        try:
            return open(filepath, 'r')
        except IOError:
            print("Input File not found in given path")
        return

    def execute_commands(self, file):
        line_num = 0
        for line in file:
            line_num += 1
            command = line.strip(" \n ")
            cmd_tokens = command.split()
            if line_num == 0 and cmd_tokens[0] != "Create_parking_lot":
                print("Command to create parking lot is missing in input file")
                break
            self.process_command(cmd_tokens)


if __name__ == '__main__':
    # filename = input("Enter the input file path:\n")
    filename = "inp.txt"
    p = Parking()
    file = p.load_file(filename)
    if file:
        p.execute_commands(file)
        # print(p.slots)
        # print(p.slot_heap)
