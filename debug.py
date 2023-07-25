
debug_state: bool = False  # True


def dout(pmessage: str):
    """Выводит диагностические сообщения."""
    global debug_state
    if debug_state:

        print(pmessage)

