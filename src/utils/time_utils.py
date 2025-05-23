def get_now(format: str = "%Y-%m-%dT%H:%M:%S") -> str:
    """
    Get the current time in the specified format.
    
    Args:
        format (str): The format string for the output time. Default is "%Y-%m-%dT%H:%M:%S".
        
    Returns:
        str: The current time formatted as a string.
    """
    from datetime import datetime
    return datetime.now().strftime(format)

def get_now_in_millis() -> int:
    """
    Get the current time in milliseconds since the epoch.
    
    Returns:
        int: The current time in milliseconds since the epoch.
    """
    from datetime import datetime
    return int(datetime.now().timestamp() * 1000)

def get_err_report_filename() -> str:
    """
    Generate a filename for the error report based on the current date and time.
    
    Returns:
        str: The generated filename for the error report.
    """
    return f"jadn_cli_error_report_{get_now('%Y%m%d')}.csv"