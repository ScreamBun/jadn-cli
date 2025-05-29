def get_item_safe_check(my_list, index):
    """
    Safely get an item from a list by index.
    Returns None if the index is out of bounds.
    """
    if 0 <= index < len(my_list):
        return my_list[index]
    return None 

def get_nested_value(data, keys, default=None):
    """
    Safely retrieves a value from a nested dictionary given a list of keys.

    Args:
        data (dict): The dictionary to search within.
        keys (list): A list of keys representing the path to the desired value.
        default: The value to return if the key path doesn't exist. Defaults to None.

    Returns:
        The value at the specified path or the default value if not found.
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
 

def get_schema_roots(schema_data):
    """
    Extracts the root names from a JADN schema.
    Returns a list of root names.
    """
    if not isinstance(schema_data, dict):
        return None

    roots = get_nested_value(schema_data, ['info', 'exports'], None)
    if roots is None:
        roots = get_nested_value(schema_data, ['info', 'roots'], None)
    
    return roots

def parse_args(arg_string):
    """
    Takes a string of arguments, trims whitespace, splits on spaces,
    and returns a list of arguments in the same order.
    """
    return arg_string.strip().split()