# TODO: Wrap this in a class
from colorama import init, Fore, Style

# Initializes Colorama and auto-resets styles after each print
# (!) Doesn't work on custom loggers
init(autoreset=True)


def brighten(log_str):
    """ Apply bright style to a string. """
    return f"{Style.BRIGHT}{log_str}{Style.NORMAL}"


def colorize(log_str, color):
    """ Apply color to a string, resetting when done. """
    return f"{color}{log_str}{Fore.RESET}"


def colorize_path(log_str):
    """ Apply a path-related color (CYAN) to a string. """
    return f"{Fore.CYAN}{log_str}{Fore.RESET}"


def colorize_action(log_str):
    """ Apply an action-related color (YELLOW) to a string. """
    return f"{Fore.YELLOW}{log_str}{Fore.RESET}"


def colorize_success(log_str):
    """ Apply a success-related color (GREEN) to a string. """
    return f"{Fore.GREEN}{log_str}{Fore.RESET}"


def colorize_warning(log_str):
    """ Apply a success-related color (MAGENTA) to a string. """
    return f"{Fore.MAGENTA}{log_str}{Fore.RESET}"


def colorize_error(log_str):
    """ Apply a success-related color (RED) to a string. """
    return f"{Fore.RED}{log_str}{Fore.RESET}"


def colorize_cli_cmd(log_str):
    """ Apply a CLI command-related color (MAGENTA) to a string. """
    return f"{Fore.MAGENTA}{log_str}{Fore.RESET}"
