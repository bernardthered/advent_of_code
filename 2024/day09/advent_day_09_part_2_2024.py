import os
from typing import List

script_path = os.path.dirname(os.path.realpath(__file__))
disk_map = open("day_09_input.txt").read()

# disk_map = "2333133121414131402"
print(f"Length of the disk map: {len(disk_map)}")


class File:
    def __init__(self, number, size):
        self.number = number
        self.size = size

    def __repr__(self):
        return str(self.number) * self.size


class FileList(list):
    def __repr__(self):
        return "".join([str(file) for file in self])

    def to_block_list(self):
        block_list = [file.number for file in self for _ in range(file.size)]
        return block_list


def calc_checksum(block_list: List[int]) -> int:
    checksum = 0
    for i, file_number in enumerate(block_list):
        checksum += i * int(file_number) if file_number not in [None, "."] else 0
    return checksum


def get_file_list_from_disk_map(disk_map) -> tuple[FileList, int]:
    """
    Return a 2-tuple of the FileList and the highest file number
    """
    file_list = FileList()
    file_index = 0
    for i, char in enumerate(disk_map):
        try:
            blocks_used = int(char)
        except ValueError:
            print(f"Character '{char}' found, assumed to be the end of the disk map.")
            break
        if i % 2 == 0:
            # This is the # of blocks this file uses
            file_list.append(File(file_index, blocks_used))
            file_index += 1
        else:
            # This is the # of empty blocks
            file_list.append(File(".", blocks_used))
    return file_list, file_index - 1


def find_file_to_move_and_destination(file_blocks, file_number):
    for file_index, file in reversed(list(enumerate(file_blocks))):
        if file.number != file_number:
            # It's not the file we were told to move
            continue
        break
    if file.number != file_number:
        print(
            "Weird, we did not find the file we were asked to move. This shouldn't happen."
        )
        return None, None

    for possibly_empty_index, possibly_empty_block in enumerate(file_blocks):
        if (
            possibly_empty_block.number == "."
            and possibly_empty_block.size >= file.size
        ):
            return file_index, possibly_empty_index
    # We've got the right file #, but didn't find an empty suitable destination for it, we can give up
    return None, None


def move_file(file_blocks, file_index, empty_index):
    """
    Move the file block to the location of the empty block in the file_blocks list
    """
    # print(
    #     f"Moving file {file_blocks[file_index].number} from {file_index} to {empty_index}"
    # )
    if file_blocks[empty_index].size == file_blocks[file_index].size:
        # Swap the empty block w/ the file block's number
        file_blocks[empty_index].number = file_blocks[file_index].number
        file_blocks[file_index].number = "."
    else:
        empty_size = file_blocks[empty_index].size
        file_size = file_blocks[file_index].size
        file_blocks[empty_index].number = file_blocks[file_index].number
        file_blocks[empty_index].size = file_size
        # Change the old file block (further toward the end of the disk) to empty
        file_blocks[file_index].number = "."

        # Add a new empty block whose size is the leftover empty space from the old empty block
        # Note: we could combine this with other empty File objects at the end of the chain to
        # clean things up, but it's not necessary.
        file_blocks.insert(empty_index + 1, File(".", empty_size - file_size))


def defrag(file_list, highest_file_number):
    for file_number in range(highest_file_number, 0, -1):
        file_index, empty_index = find_file_to_move_and_destination(
            file_list, file_number
        )
        if file_index and file_index > empty_index:
            move_file(file_list, file_index, empty_index)
    return file_list


def part2():
    file_list, highest_file_number = get_file_list_from_disk_map(disk_map)
    print(f"Found {highest_file_number+1} files, now defragging.")
    file_list = defrag(file_list, highest_file_number)
    block_list = file_list.to_block_list()
    print(f"Computing checksum of {len(block_list)} blocks.")
    print(calc_checksum(block_list))


part2()
