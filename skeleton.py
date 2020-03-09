###
# Google Hash Code 2020
#
# Author: Teki Chan
# Date: 21 Feb 2020
###
import sys

def read_file(in_file):
    """
    Read Intput File

    Args:
        in_file: input file path
    
    Returns:
        result_params: Resulted Parameters
    """
    # Define variables
    result_params = []

    # Read the file into variables    
    with open(in_file, 'r') as infile:
        # Process lines and save data into variables
        pass

    return result_params # return essential variables

def process(result_params):
    """
    The main program reads the input file, processes the calculation
    and writes the output file

    Args:
        result_params: Resulted Parameters  

    Returns:
        final_score: Final Score
        , final_result: Final Result    
    """
    final_score = 0
    final_result = []

    ### Logic here

    return final_score, final_result    # return process result

def write_file(out_file, final_result):
    """
    Write the submission file

    Args:
        out_file: output file path
    """
    with open(out_file, 'w') as outfile:
        # Save result into the output file
        pass

def main(in_file, out_file):
    """
    The main program reads the input file, processes the calculation
    and writes the output file

    Args:
        in_file: input file path
        out_file: output file path
    """

    # Read File
    result_params = read_file(in_file)
    # Process Algorithm
    final_score, final_result = process(result_params)
    # Print Score
    print('Score: {}'.format(final_score))
    # Save results into the output if instructed
    if out_file is not None:
        write_file(out_file, final_result)
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

### End of Program ###