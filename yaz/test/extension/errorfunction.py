#!/usr/bin/env python3

import yaz


@yaz.task
def yaz_error(message: str = "There was an error", return_code: int = 1):
    raise yaz.Error(message, return_code)


@yaz.task
def return_integer(value: int):
    return value


@yaz.task
def return_boolean(value: bool):
    return value


if __name__ == "__main__":
    yaz.main()
