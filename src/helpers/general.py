from datetime import datetime


def print_system_msg(msg: str, flush: bool = False, end: str = "\n") -> None:
    """
    Print a message to the terminal.

    Parameters:
        msg (str): Message to print
    """
    print(f"\r[{datetime.now().strftime('%d-%m-%G | %H:%M:%S')}] {msg}", flush=flush, end=end)
