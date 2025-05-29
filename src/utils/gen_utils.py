def get_item_safe_check(my_list, index):
    """
    Safely get an item from a list by index.
    Returns None if the index is out of bounds.
    """
    if 0 <= index < len(my_list):
        return my_list[index]
    return None  

def parse_args(arg_string):
    """
    Takes a string of arguments, trims whitespace, splits on spaces,
    and returns a list of arguments in the same order.
    """
    return arg_string.strip().split()