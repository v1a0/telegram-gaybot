from sqllex import *
from sqllex.types import DBTemplateType
from settings import DB_PATH
from sqllex.debug import debug_mode

#debug_mode(True)
db = SQLite3x(path=DB_PATH)


def default_init():
    template: DBTemplateType = {
        'users': {
            'user_id': [INTEGER, PRIMARY_KEY, NOT_NULL],
            'username': TEXT,
            'name': TEXT,
            'custom_name': TEXT,
            'admin': [TEXT, DEFAULT, 'False']
        },
        'members': {
            'group_id': [INTEGER, NOT_NULL],
            'user_id': [INTEGER, NOT_NULL],
            FOREIGN_KEY: {
                'user_id': ['users', 'user_id']
            }
        },
        'coins': {
            'user_id': [INTEGER, PRIMARY_KEY, NOT_NULL],
            'balance': [INTEGER, DEFAULT, '0'],
            FOREIGN_KEY: {
                'user_id': ['users', 'user_id']
            }
        },
        'karma': {
            'user_id': [INTEGER, PRIMARY_KEY, NOT_NULL],
            'karma': [INTEGER, DEFAULT, '0'],
            FOREIGN_KEY: {
                'user_id': ['users', 'user_id']
            }
        },
        'xwords': {
            'id': [INTEGER, PRIMARY_KEY, AUTOINCREMENT],
            'word': [TEXT, UNIQUE, NOT_NULL]
        },
        'shippers': {
            'group_id': [INTEGER, PRIMARY_KEY, NOT_NULL],
            'id_first': [INTEGER, NOT_NULL],
            'id_scond': [INTEGER],
            'time': [NUMERIC, NOT_NULL],
            FOREIGN_KEY: {
                'id_first': ['users', 'user_id'],
                'id_scond': ['users', 'user_id'],
            }
        },
        'ship_count': {
            'group_id': [INTEGER, NOT_NULL],
            'user_id': [INTEGER, NOT_NULL],
            'count': [INTEGER, DEFAULT, '0'],
        }

    }

    db.markup(template=template)

