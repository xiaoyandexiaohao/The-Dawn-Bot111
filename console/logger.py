from colorama import Fore


def error_log(message: str):
    print(Fore.RED + ">> 错误 |" + Fore.LIGHTBLACK_EX + f" {message}")


def success_log(message: str):
    print(Fore.GREEN + ">> 成功 |" + Fore.LIGHTBLACK_EX + f" {message}")


def info_log(message: str):
    print(Fore.LIGHTBLACK_EX + f">> INFO | {message}")
