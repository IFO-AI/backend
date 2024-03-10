from os import environ, path
from dotenv import dotenv_values

basedir = path.abspath(path.dirname(__file__))
print(basedir)
Config = dotenv_values(path.join(basedir, '../.env'))