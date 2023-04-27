import os
from dotenv import load_dotenv
from deta import Deta
load_dotenv()

deta = Deta(os.getenv("DETA_PROJECT_KEY"))
db = deta.Base("chatData")