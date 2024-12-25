# Solution to
# https://adventofcode.com/2024/day/5

from collections import OrderedDict
import os


LOGLEVEL = 100


def are_any_numbers_out_of_order(print_queue, what_must_not_be_after):
    while print_queue:
        page_number, _ = print_queue.popitem(last=False)
        # We use a set operation here for maximum efficiency.
        # If there is anything left in the print queue that is also in the list of what
        # must not be after this page #, then this is an illegal print queue.
        if (
            page_number in what_must_not_be_after
            and print_queue.keys() & what_must_not_be_after[page_number]
        ):
            return True


def construct_ordering_dict(input_lines) -> dict:
    """
    Returns a dict where the keys are any numbers that must go before some other numbers, and
    the values are a set of all the numbers that must go after this one.
    """
    what_must_not_be_after = {}

    for i, line in enumerate(input_lines):
        line = line.strip()
        if not line:
            break
        before, after = line.split("|")
        if int(after) not in what_must_not_be_after:
            what_must_not_be_after[int(after)] = set([int(before)])
        else:
            what_must_not_be_after[int(after)].add(int(before))
    return what_must_not_be_after, i


def part1(input_lines):
    what_must_not_be_after, i = construct_ordering_dict(input_lines)
    answer = 0

    print(
        f"First {i} lines of the file were rules, remaining {len(lines) - 1 - i} are queues"
    )

    for line in input_lines[i:]:
        line = line.strip()
        if not line:
            continue
        page_numbers = [int(i) for i in line.split(",")]
        # We use a dict as a form of ordered set, so we can use efficient set operations
        print_queue = OrderedDict.fromkeys(page_numbers)
        if are_any_numbers_out_of_order(print_queue, what_must_not_be_after):
            continue

        answer += page_numbers[int((len(page_numbers) - 1) / 2)]
    print(answer)


def get_illegal_queues(input_lines, i, what_must_not_be_after):
    illegal = []
    for line in input_lines[i:]:
        line = line.strip()
        if not line:
            continue
        page_numbers = [int(i) for i in line.split(",")]
        # We use a dict as a form of ordered set, so we can use efficient set operations
        print_queue = OrderedDict.fromkeys(page_numbers)
        if are_any_numbers_out_of_order(print_queue, what_must_not_be_after):
            illegal.append(OrderedDict.fromkeys(page_numbers))
            continue
    return illegal


def part2(input_lines):
    # The format of this is an integer key, whose value is a list of integers that cannot come after
    # the key in the print queue
    what_must_not_be_after, i = construct_ordering_dict(input_lines)
    answer = 0

    print(
        f"First {i} lines of the file were rules, remaining {len(lines) - 1 - i} are queues"
    )

    illegal_queues = get_illegal_queues(input_lines, i, what_must_not_be_after)

    for print_queue in illegal_queues:
        new_list = []
        while print_queue:
            page_number, _ = print_queue.popitem(last=False)
            if (
                page_number in what_must_not_be_after
                and print_queue.keys() & what_must_not_be_after[page_number]
            ):
                # There's something still in the print queue that must not be after
                # the current number.
                # Pop this page # back onto the queue and come back to it later.
                print_queue[page_number] = None
            else:
                new_list.append(page_number)
        answer += new_list[int((len(new_list) - 1) / 2)]
    print(answer)


def log(msg, level=10):
    if level >= LOGLEVEL:
        print(msg)


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__))
    input = open(os.path.join(script_path, "input_2.txt"))
    lines = input.readlines()
    part1(lines)
