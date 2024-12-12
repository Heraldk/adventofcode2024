import argparse
import importlib
import os

argParser = argparse.ArgumentParser()
argParser.add_argument(
    "-d", "--day", type=int, required=True, choices=range(1, 26), help="Day Number"
)
argParser.add_argument(
    "-t", "--test", action="store_true", help="Run using test input file"
)
argParser.add_argument(
    "-s", "--skip", choices=range(3), default=0, help="skip one part or the other"
)

args = argParser.parse_args()

moduleName = f"day{args.day:02d}"
className = f"Day{args.day:02d}"
if args.test:
    filename = f"test_input_files/{moduleName}"
else:
    filename = f"input_files/{moduleName}"

if not os.path.isfile(f"{filename}.txt"):
    raise ValueError(f"Input file {filename}.txt does not exist")

# Initialise the Class
module = importlib.import_module(moduleName)
DayClass = getattr(module, className)
instance = DayClass()

# Part One
part_one_filename = f"{filename}.txt"
if args.skip != 1:
    instance.part_one(part_one_filename)

# Part Two
if os.path.isfile(f"{filename}_part2.txt"):
    part_two_filename = f"{filename}_part2.txt"
else:
    part_two_filename = part_one_filename
if args.skip != 2:
    instance.part_two(part_two_filename)
