from dotenv import load_dotenv
from .api.commands.start_command import main


def start_up():
    load_dotenv()
    main()
