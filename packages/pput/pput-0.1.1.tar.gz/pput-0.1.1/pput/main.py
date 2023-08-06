"""
pput.main
"""


import tyro


class class_test(object):
    def __init__(self):
        print("class success.")


def func_test(name: str) -> None:
    print(f"{name} function success.")


def main():
    tyro.cli(func_test)


if __name__ == "__main__":
    main()
