import os

script_path = os.path.dirname(os.path.realpath(__file__))
disk_map = open("day_09_input.txt").read()

# disk_map = "2333133121414131402"
print(f"Length of the disk map: {len(disk_map)}")


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


def defrag(block_map):
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
        checksum += i * int(file_number) if file_number is not None else 0
    return checksum


def part1():
    block_map = get_block_map_from_disk_map(disk_map)
    defrag(block_map)
    print(calc_checksum(block_map))


part1()
