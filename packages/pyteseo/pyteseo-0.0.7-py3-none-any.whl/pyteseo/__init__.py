"""Python package developed to simplify and facilitate the setup and postprocessing of TESEO(v1.2.8) simulations (https://ihcantabria.com/en/specialized-software/teseo/)
"""
from pathlib import Path
from dotenv import load_dotenv

# __name__ = "pyTESEO"
__version__ = "0.0.7"

print(f"\n____ pyTESEO v{__version__} ____\n")
print("Loading env variables...")
if Path(".env").exists():
    load_dotenv(Path(".env"))
else:
    print("\nWARNING - .env file has not been loaded!")
