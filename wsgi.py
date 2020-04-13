import os
from dotenv import load_dotenv

# 载入环境变量
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from xthonblog import create_app

app = create_app('production')