###
# Google Hash Code 2020
# Qualification Round
#
# Authors: Jonathan Janetzki, Mohamed Abdel Nasser, Teki Chan
# Date: 21 Feb 2020 - 9 Mar 2020
###
import sys

def read_file(in_file):
    """
    Read Intput File

    Args:
        in_file: input file path
    
    Returns:
        days_scan: Number of Days available for scanning
        , book_score_list: List of Book Scores
        , lib_books: List of Book Count with Library as Index
        , lib_supdays: List of Sign-up Period with Library as Index
        , lib_daily_ships: List of Number of Books available shipped daily with Library as Index
        , lib_book_lists: List of Book List with Library as Index
    """
    # Define variables
    books = 0               # = len of book_score_list
    libraries = 0           # = len of lib_* list
    days_scan = 0
    book_score_list = []    # idx is book id
    lib_books = []          # idx is library id
    lib_supdays = []        # idx is library id
    lib_daily_ships = []    # idx is library id
    lib_book_lists = []     # idx is library id

    # Read the file into variables    
    with open(in_file, 'r') as infile:
        # Process lines and save data into variables
        books, libraries, days_scan = [int(x) for x in infile.readline().strip().split(' ')]
        book_score_list = [int(x) for x in infile.readline().strip().split(' ')]
        lib_idx= 0
        while lib_idx < libraries:
            lib_book, lib_supday, lib_daily_ship = [int(x) for x in infile.readline().strip().split(' ')]
            lib_book_list = [int(x) for x in infile.readline().strip().split(' ')]
            lib_books.append(lib_book)
            lib_supdays.append(lib_supday)
            lib_daily_ships.append(lib_daily_ship)
            lib_book_lists.append(lib_book_list)
            lib_idx += 1
    
    return days_scan, book_score_list, lib_books, lib_supdays, lib_daily_ships, lib_book_lists  # return essential variables

def flatten(given_list):
    """
    Utility function to flatten list of list to a single list

    Args:
        given_list: list of list
    
    Returns:
        flatted list
    """
    return [item for sublist in given_list for item in sublist]

def get_sorted_lib_book_lists(lib_idx, sorted_lib_book_lists, remain_day, lib_daily_ships):
    """
    Helper function to get a list of sorted Book List with Library Index

    Args:
        lib_idx: Library Index
        , sorted_lib_book_lists: List of Full Book List sorted by score
        , remain_day: Remaing Day
        , lib_daily_ships: List of Number of Books available shipped daily with Library as Index
    
    Returns:
         a list of sorted Book List with Library Index
    """
    return sorted_lib_book_lists[lib_idx][:remain_day * lib_daily_ships[lib_idx]] if remain_day * lib_daily_ships[lib_idx] < len(sorted_lib_book_lists[lib_idx]) else sorted_lib_book_lists[lib_idx]

def sum_book_score(book_idx_list, book_score_list):
    """
    Helper function to get sum of book scores

    Args:
        book_idx_list: List of Book Index
        , book_score_list: List of Book Scores
    
    Returns:
        sum of book scores
    """
    return sum(book_score_list[book_idx] for book_idx in book_idx_list)

def heuristic1(remain_days, book_score):
    """
    Heuristic function 1

    Args:
        remain_days: Remaining Day
        , book_score: Book Score

    Returns:
        Heuristic score
    """
    return (remain_days * book_score)

def heuristic2(signup_days, book_score):
    """
    Heuristic function 2

    Args:
        signup_days: Sign Up Period
        , book_score: Book Score

    Returns:
        Heuristic score
    """    
    return (book_score / signup_days)    

def method1(lib_books, lib_supdays, days_scan, sorted_lib_book_lists, lib_daily_ships, book_score_list):
    """
    Estimation method 1 with sorting by sign up period

    Args:
        lib_books: List of Book Count with Library as Index
        , lib_supdays: List of Sign-up Period with Library as Index
        , days_scan: Number of Days available for scanning
        , sorted_lib_book_lists: List of Full Book List sorted by score
        , lib_daily_ships: List of Number of Books available shipped daily with Library as Index
        , book_score_list: List of Book Scores

    Returns:
        List of Library, Estimated Score
    """
    # sort library by sign up day and calculate score
    lib_list = list(sorted(range(len(lib_books)), key=lambda lib_idx: lib_supdays[lib_idx]))
    remain_day_dict = {lib_idx: days_scan - lib_supdays[lib_idx] - (sum([lib_supdays[lib_idx] for lib_idx in lib_list[:n]]) if n > 0 else 0) for n, lib_idx in enumerate(lib_list)}
    book_idx_lists = {lib_idx: get_sorted_lib_book_lists(lib_idx, sorted_lib_book_lists, remain_day_dict[lib_idx], lib_daily_ships) for lib_idx in filter(lambda lib_idx: remain_day_dict[lib_idx] > 0, lib_list)}
    book_idx_set = set(flatten(book_idx_lists.values()))
    estimated_score = sum(book_score_list[book_idx] for book_idx in book_idx_set)

    # sort the included library by book scores
    best_lib_list = lib_list.copy()
    best_estimated_score = estimated_score

    list_list_loser = list(filter(lambda lib_idx: remain_day_dict[lib_idx] <= 0, best_lib_list))
    lib_list = list(sorted(filter(lambda lib_idx: remain_day_dict[lib_idx] > 0, best_lib_list), key=lambda lib_idx: sum_book_score(book_idx_lists[lib_idx], book_score_list), reverse=True))
    remain_day_dict = {lib_idx: days_scan - lib_supdays[lib_idx] - (sum([lib_supdays[lib_idx] for lib_idx in lib_list[:n]]) if n > 0 else 0) for n, lib_idx in enumerate(lib_list)}
    book_idx_lists = {lib_idx: get_sorted_lib_book_lists(lib_idx, sorted_lib_book_lists, remain_day_dict[lib_idx], lib_daily_ships) for lib_idx in filter(lambda lib_idx: remain_day_dict[lib_idx] > 0, lib_list)}
    book_idx_set = set(flatten(book_idx_lists.values()))
    estimated_score = sum(book_score_list[book_idx] for book_idx in book_idx_set)

    if estimated_score > best_estimated_score:
        best_estimated_score = estimated_score
        best_lib_list = lib_list.copy() + list_list_loser
        print('......... method1: book score after signup days')
    else:
        print('......... method1: signup days only')

    return best_lib_list, best_estimated_score

def method2(lib_books, lib_supdays, days_scan, sorted_lib_book_lists, lib_daily_ships, book_score_list):
    """
    Estimation method 2 with sorting by book score subtotal

    Args:
        lib_books: List of Book Count with Library as Index
        , lib_supdays: List of Sign-up Period with Library as Index
        , days_scan: Number of Days available for scanning
        , sorted_lib_book_lists: List of Full Book List sorted by score
        , lib_daily_ships: List of Number of Books available shipped daily with Library as Index
        , book_score_list: List of Book Scores

    Returns:
        List of Library, Estimated Score
    """    
    book_idx_lists = {lib_idx: get_sorted_lib_book_lists(lib_idx, sorted_lib_book_lists, days_scan - lib_supdays[lib_idx], lib_daily_ships) for lib_idx in filter(lambda lib_idx: days_scan - lib_supdays[lib_idx] > 0, range(len(lib_books)))}
    # sort library by sub total score of books and calculate score
    lib_list = list(sorted(range(len(lib_books)), key=lambda lib_idx: sum_book_score(book_idx_lists[lib_idx], book_score_list), reverse=True))
    remain_day_dict = {lib_idx: days_scan - lib_supdays[lib_idx] - (sum([lib_supdays[lib_idx] for lib_idx in lib_list[:n]]) if n > 0 else 0) for n, lib_idx in enumerate(lib_list)}
    book_idx_lists = {lib_idx: get_sorted_lib_book_lists(lib_idx, sorted_lib_book_lists, remain_day_dict[lib_idx], lib_daily_ships) for lib_idx in filter(lambda lib_idx: remain_day_dict[lib_idx] > 0, lib_list)}
    book_idx_set = set(flatten(book_idx_lists.values()))
    estimated_score = sum(book_score_list[book_idx] for book_idx in book_idx_set)

    # sort the included library by sign up days
    best_lib_list = lib_list.copy()
    best_estimated_score = estimated_score

    return best_lib_list, best_estimated_score

def method3(lib_books, lib_supdays, days_scan, sorted_lib_book_lists, lib_daily_ships, book_score_list):
    """
    Estimation method 3 with sorting by heuristic functions

    Args:
        lib_books: List of Book Count with Library as Index
        , lib_supdays: List of Sign-up Period with Library as Index
        , days_scan: Number of Days available for scanning
        , sorted_lib_book_lists: List of Full Book List sorted by score
        , lib_daily_ships: List of Number of Books available shipped daily with Library as Index
        , book_score_list: List of Book Scores

    Returns:
        List of Library, Estimated Score
    """    
    tmp_book_idx_lists = {lib_idx: get_sorted_lib_book_lists(lib_idx, sorted_lib_book_lists, days_scan - lib_supdays[lib_idx], lib_daily_ships) for lib_idx in filter(lambda lib_idx: days_scan - lib_supdays[lib_idx] > 0, range(len(lib_books)))}
    tmp_lib_list = list(sorted(range(len(lib_books)), key=lambda lib_idx: lib_supdays[lib_idx]))

    best_lib_list = []
    best_estimated_score = -1

    lib_score_dict = {lib_idx: heuristic1(days_scan - lib_supdays[lib_idx], sum_book_score(tmp_book_idx_lists[lib_idx], book_score_list)) for lib_idx in tmp_lib_list}
    # sort library by internal scoring and calculate score
    lib_list = list(sorted(range(len(lib_books)), key=lambda lib_idx: lib_score_dict[lib_idx], reverse=True))    
    remain_day_dict = {lib_idx: days_scan - lib_supdays[lib_idx] - (sum([lib_supdays[lib_idx] for lib_idx in lib_list[:n]]) if n > 0 else 0) for n, lib_idx in enumerate(lib_list)}
    book_idx_lists = {lib_idx: get_sorted_lib_book_lists(lib_idx, sorted_lib_book_lists, remain_day_dict[lib_idx], lib_daily_ships) for lib_idx in filter(lambda lib_idx: remain_day_dict[lib_idx] > 0, lib_list)}
    book_idx_set = set(flatten(book_idx_lists.values()))
    estimated_score = sum(book_score_list[book_idx] for book_idx in book_idx_set)

    # sort the included library by book scores
    best_lib_list = lib_list.copy()
    best_estimated_score = estimated_score

    lib_score_dict = {lib_idx: heuristic2(lib_supdays[lib_idx], sum_book_score(tmp_book_idx_lists[lib_idx], book_score_list)) for lib_idx in tmp_lib_list}
    # sort library by internal scoring and calculate score
    lib_list = list(sorted(range(len(lib_books)), key=lambda lib_idx: lib_score_dict[lib_idx], reverse=True))    
    remain_day_dict = {lib_idx: days_scan - lib_supdays[lib_idx] - (sum([lib_supdays[lib_idx] for lib_idx in lib_list[:n]]) if n > 0 else 0) for n, lib_idx in enumerate(lib_list)}
    book_idx_lists = {lib_idx: get_sorted_lib_book_lists(lib_idx, sorted_lib_book_lists, remain_day_dict[lib_idx], lib_daily_ships) for lib_idx in filter(lambda lib_idx: remain_day_dict[lib_idx] > 0, lib_list)}
    book_idx_set = set(flatten(book_idx_lists.values()))
    estimated_score = sum(book_score_list[book_idx] for book_idx in book_idx_set)

    if estimated_score > best_estimated_score:
        print('......... method3: heuristic2')
        best_estimated_score = estimated_score
        best_lib_list = lib_list.copy()
    else:
        print('......... method3: heuristic1')

    return best_lib_list, best_estimated_score

def process(days_scan, book_score_list, lib_books, lib_supdays, lib_daily_ships, lib_book_lists):
    """
    The main program reads the input file, processes the calculation
    and writes the output file

    Args:
        days_scan: Number of Days available for scanning
        , book_score_list: List of Book Scores
        , lib_books: List of Book Count with Library as Index
        , lib_supdays: List of Sign-up Period with Library as Index
        , lib_daily_ships: List of Number of Books available shipped daily with Library as Index
        , lib_book_lists: List of Book List with Library as Index

    Returns:
        final_score: Final Score
        , final_result: Final Result
    """
    final_score = 0
    final_result = []

    # Approach 2:
    """
    sort books in each library
    lib n scoring: (days_scan - lib_supdays[n]) * sum(book_score_list in lib_book_lists[n])
    sort out lib_list with the scoring
    for each day
        for each library in sorted lib_list
            check if signup process in place or start
            start to ship maximum books from sorted book_list
    """
    print('... preparing process')
    # sorted_lib_book_lists = []
    sorted_lib_book_lists = [list(sorted(lib_book_list, key=lambda lib_book: book_score_list[lib_book], reverse=True)) for lib_book_list in lib_book_lists]

    # sort library list
    best_lib_list = []
    best_score = -1
    for method_idx, method in enumerate([method1, method2, method3]):
        lib_list, estimated_score = method(lib_books, lib_supdays, days_scan, sorted_lib_book_lists, lib_daily_ships, book_score_list)
        if estimated_score > best_score:
            best_lib_list = lib_list.copy()
            best_score = estimated_score
            print('...... selected method {}!'.format(method_idx + 1))
        print('...... finished method {}'.format(method_idx + 1))
    print('Estimated Score: {}'.format(best_score))

    print('... running days')
    signup_now = [-1, -1]   # (lib_idx, remaining day)
    signup_lib_list = []
    shipped_books = set()
    lib_shipped_books = {}
    for day_idx in range(days_scan):
        if day_idx % int(days_scan * 0.1 + 1.0) == 0: print('...... up to {:.2f}%'.format(day_idx * 100 / days_scan)) 
        if len(best_lib_list) != 0 and (signup_now[0] == -1 or signup_now[1] <= 0):
            # Sign-up is available
            lib_idx = best_lib_list.pop(0)
            signup_now = [lib_idx, lib_supdays[lib_idx]]
            lib_shipped_books[lib_idx] = []
        for lib_idx in signup_lib_list:
            # Able to ship
            sorted_lib_book_lists[lib_idx] = list(filter(lambda lib_book: lib_book not in shipped_books, sorted_lib_book_lists[lib_idx]))
            today_shipped_books = sorted_lib_book_lists[lib_idx][:lib_daily_ships[lib_idx]]
            shipped_books.update(today_shipped_books)
            lib_shipped_books[lib_idx].extend(today_shipped_books)
            del sorted_lib_book_lists[lib_idx][:lib_daily_ships[lib_idx]]
        # End of Day
        if signup_now[0] != -1 and signup_now[1] > 0:
            signup_now[1] -= 1
        if signup_now[0] != -1 and signup_now[1] == 0:
            signup_lib_list.append(signup_now[0])
            signup_now[1] -= 1
    
    print('... calculate score')
    final_score = sum([book_score_list[book_idx] for book_idx in shipped_books])
    final_result = [(lib_idx, lib_shipped_books[lib_idx]) for lib_idx in signup_lib_list if len(lib_shipped_books[lib_idx]) > 0]

    return final_score, final_result    # return process result

def write_file(out_file, final_result):
    """
    Write the submission file

    Args:
        out_file: output file path
    """
    with open(out_file, 'w') as outfile:
        # Save result into the output file
        outfile.write('{}\n'.format(len(final_result)))
        for result in final_result:
            outfile.write('{} {}\n'.format(result[0], len(result[1])))
            outfile.write('{}\n'.format(
                ' '.join([str(s) for s in result[1]])
            ))

    # End of write_file

def main(in_file, out_file):
    """
    The main program reads the input file, processes the calculation
    and writes the output file

    Args:
        in_file: input file path
        out_file: output file path
    """
    # Read File
    days_scan, book_score_list, lib_books, lib_supdays, lib_daily_ships, lib_book_lists = read_file(in_file)
    # Process Algorithm
    final_score, final_result = process(days_scan, book_score_list, lib_books, lib_supdays, lib_daily_ships, lib_book_lists)
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