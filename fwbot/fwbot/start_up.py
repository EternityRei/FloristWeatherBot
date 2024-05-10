from dotenv import load_dotenv
from .api.commands.start_command import main
from .db.create import create_db
from .db.insert import insert_data


def start_up():
    load_dotenv()
    create_db()
    insert_data()
    main()
