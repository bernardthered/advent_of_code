import os

script_path = os.path.dirname(os.path.realpath(__file__))
# disk_map = open(os.path.join(script_path, "day_09_input.txt")).read()
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


def get_block_map_from_disk_map(disk_map):
    block_map = []
    file_index = 0
    for i, char in enumerate(disk_map):
        blocks_used = int(char)
        if i % 2 == 0:
            # This is the # of blocks this file uses
            block_map += [file_index for _ in range(blocks_used)]
            file_index += 1
        else:
            # This is the # of empty blocks
            block_map += [None for _ in range(blocks_used)]
    return block_map


def defrag1(block_map):
    def reposition_next_empty_and_last_filled_blocks(
        block_map, last_filled_block, next_empty_block
    ):
        next_empty_block = block_map.index(None, next_empty_block)
        while block_map[last_filled_block] is None:
            last_filled_block -= 1
        return next_empty_block, last_filled_block

    next_empty_block, last_filled_block = reposition_next_empty_and_last_filled_blocks(
        block_map, len(block_map) - 1, 0
    )

    while next_empty_block < last_filled_block:
        block_map[next_empty_block] = block_map[last_filled_block]
        block_map[last_filled_block] = None
        next_empty_block, last_filled_block = (
            reposition_next_empty_and_last_filled_blocks(
                block_map, last_filled_block, next_empty_block
            )
        )
    return block_map


def calc_checksum(block_map):
    checksum = 0
    for i, file_number in enumerate(block_map):
        checksum += i * int(file_number) if file_number not in [None, "."] else 0
    return checksum


def part1():
    block_map = get_block_map_from_disk_map(disk_map)
    defrag1(block_map)
    print(calc_checksum(block_map))


def get_file_list_from_disk_map(disk_map) -> tuple[FileList, int]:
    """
    Returns a 2-tuple of the FileList and the highest file number
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
    """move the file block to the location of the empty block in the file_blocks list"""
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
        file_blocks.insert(empty_index + 1, File(".", empty_size - file_size))


def defrag2(file_blocks, highest_file_number):
    for file_number in range(highest_file_number, 0, -1):
        file_index, empty_index = find_file_to_move_and_destination(
            file_blocks, file_number
        )
        if file_index and file_index > empty_index:
            move_file(file_blocks, file_index, empty_index)
    return file_blocks
    # NOTE: need to keep track of which file # it is. Probably makes sense to define a new class to store both the length of the file and its file number, then rearrange those in a list


def part2():
    file_blocks, highest_file_number = get_file_list_from_disk_map(disk_map)
    print(f"Found {highest_file_number} files, now defragging.")
    defragged_disk_map = defrag2(file_blocks, highest_file_number)
    # print(defragged_disk_map)
    # block_map = get_block_map_from_disk_map(defragged_disk_map)
    # print(file_blocks)
    print(calc_checksum(str(file_blocks)))


part2()
