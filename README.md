# veribot

Bot to automatically verify users based on database of ids.

## Installation

- Clone the repository
````
    git clone git@github.com:abhigyandsa/veribot.git
````
or, if you haven't configured ssh yet:
````
    git clone https://github.com/abhigyandsa/veribot.git
````
- Create a .env file in the root folder with two variables
    - VERIBOTTOKEN    your discord bot token
    - ROLE			role to assign to a verified user

refer to the .env.sample file for the format of the file

- Install the dependencies
````
    pip install discord pandas dotenv xlrd openpyxl
````
## Running
````
    python3 main.py
````
