###
# Google Hash Code 2020
# This code aims at solving the practice problem - more pizza
#
# Author: Teki Chan
# Date: 28 Jan 2020
###
import sys

def read_file(in_file):
    """
    Read Intput File

    Args:
        in_file: input file path
    
    Returns:
        Maximum number of slices allowed
        , Number of Pizza to be selected
        , List of number of slices of each pizza
    """
    max_slices = 0
    no_of_types = 0
    slices_list = []
    # Read the file into variables    
    with open(in_file, 'r') as infile:
        [max_slices, no_of_types] = [int(x) for x in infile.readline().strip().split(' ')]
        slices_list = [int(x) for x in infile.readline().strip().split(' ')]
    return max_slices, no_of_types, slices_list

def process(max_slices, no_of_types, slices_list):
    """
    The main program reads the input file, processes the calculation
    and writes the output file

    Args:
        max_slices: Maximum number of slices allowed
        no_of_types: Number of Pizza to be selected
        slices_list: List of number of slices of each pizza
    
    Returns:
        total number of slices
        , the list of the types of pizza to order
    """    
    global_slices_sum = 0
    global_slices_ordered = []

    # Check each pizza from the most slices to the least
    for pizza_idx in range(1, len(slices_list) + 1):
        slices_sum = 0
        slices_ordered = []
        # try sum as much as possible
        for slice_idx in range(len(slices_list) - pizza_idx, -1, -1) :
            if slices_sum + slices_list[slice_idx] > max_slices:
                continue    # skip if over the max
            slices_sum += slices_list[slice_idx]
            slices_ordered.insert(0, slice_idx)
            if slices_sum == max_slices:
                break   # stop when max is reached
        if slices_sum > global_slices_sum:
            global_slices_sum = slices_sum
            global_slices_ordered = slices_ordered.copy()
        if global_slices_sum == max_slices:
            break   # stop when max is reached

        # Remove the last one to select another combination
        while len(slices_ordered) > 0 and global_slices_sum < max_slices:
            last_idx = slices_ordered[0]
            slices_sum -= slices_list[last_idx]
            slices_ordered = slices_ordered[1:]
            for slice_idx in range(last_idx - 1, -1, -1):
                if slices_sum + slices_list[slice_idx] > max_slices:
                    continue    # skip if over the max
                slices_sum += slices_list[slice_idx]
                slices_ordered.insert(0, slice_idx)
                if slices_sum == max_slices:
                    break            
            if slices_sum > global_slices_sum:
                global_slices_sum = slices_sum
                global_slices_ordered = slices_ordered.copy()
            if global_slices_sum == max_slices:
                break
    return global_slices_sum, global_slices_ordered

def write_file(out_file, global_slices_ordered):
    """
    Write the submission file

    Args:
        out_file: output file path
        global_slices_ordered: the list of the types of pizza to order
    """
    with open(out_file, 'w') as outfile:
        outfile.write('{}\n'.format(len(global_slices_ordered)))
        outfile.write('{}\n'.format(' '.join([str(s) for s in global_slices_ordered])))

def main(in_file, out_file):
    """
    The main program reads the input file, processes the calculation
    and writes the output file

    Args:
        in_file: input file path
        out_file: output file path
    """
    max_slices, no_of_types, slices_list = read_file(in_file)
    global_slices_sum, global_slices_ordered = process(max_slices, no_of_types, slices_list)
    print('Score: {}'.format(global_slices_sum))
    if out_file is not None:
        write_file(out_file, global_slices_ordered)
        print('{} is saved. The program completed.'.format(out_file))
    else:
        print('The program completed.')

if __name__ == "__main__":
    # Check arguments
    if len(sys.argv) < 2:
        print(sys.argv[0] + ' [in file] [out file: optional]')
    elif len(sys.argv) == 2:
        main(sys.argv[1], None)
    else:
        main(sys.argv[1], sys.argv[2])