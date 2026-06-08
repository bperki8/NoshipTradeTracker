import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
_env_path = Path(__file__).resolve().parent.parent/".env"
load_dotenv(_env_path)

# Port of New Orleans customs district code.
NOLA_DISTRICT_CODE = "2101"
NOLA_CENSUS_PORT_CODE = "2002"
NOLA_PORT_NAME = "New Orleans, LA"

#API keys from environment variables.
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")
COMTRADE_API_KEY = os.getenv("COMTRADE_API_KEY")
USITC_API_KEY = os.getenv("USITC_API_KEY")

# Census Bureau API base URL
CENSUS_BASE_URL = "https://api.census.gov/data/timeseries/intltrade"

# UN Comtrade API base URL
COMTRADE_BASE_URL = "https://comtradeapi.un.org/data/v1/get"

# USITC Dataweb API base URL
USITC_BASE_URL = "https://datawebws.usitc.gov/dataweb"

# Port NOLA cargo stats URL
PORT_NOLA_BASE_URL = "https://portnola.com"


def require_census_key():
  """Raise an error if the Census API key is not configured."""
  if not CENSUS_API_KEY:
    raise EnvironmentError(
      f"CENSUS_API_KEY is not set. Instead set to `{CENSUS_API_KEY}`."
      "Get a free key at https://api.census.gov/data/key_signup.html "
      "and add it to your .env file."
    )
  return CENSUS_API_KEY


def require_comtrade_key():
  """Raise an error if the Comtrade API key is not configured."""
  if not COMTRADE_API_KEY:
    raise EnvironmentError(
      "COMTRADE_API_KEY is not set. "
      "Get a free key at https://comtradeplus.un.org/ "
      "and add it to your .env file."
    )
  return COMTRADE_API_KEY


def require_usitc_key():
  """Raise an error if the USITC Dataweb API key is not configured."""
  if not USITC_API_KEY:
    raise EnvironmentError(
      "USITC_API_KEY is not set. "
      "Create a free account at https://dataweb.usitc.gov/sign-in "
      "and copy your API token from the Dataweb API tab into your .env file."
    )
  return USITC_API_KEY
