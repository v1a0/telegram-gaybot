from aiogram.dispatcher.filters.state import State, StatesGroup


class Branch(StatesGroup):
    banned = State()
    default = State()
    settings = State()
    add_xword_response = State()

    admin_panel = State()
    get_msg_info = State()
    add_admin = State()
    rem_admin = State()
