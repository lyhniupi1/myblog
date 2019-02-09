from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from myblog import create_app

app = create_app('production')
