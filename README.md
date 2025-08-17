# Project WMX
Learning project

by Wojciech Zając, Maciej Zając

## About
This project is meant for learning purposes. Console type program features:
* Menu system
    - As console program the UI bases on series of menus with option selection input
    - Helper function for showing consistent menus of provided functions
* Configuration
    - Dictionary type configuration used throughout program
    - Stored in json file
    - If not found, the file is created
    - Database credentials saved with two-way symmetrical encryption
* Database connection 
    - "Central" connection with Postgre (server and credentials must be provided, user also needs permissions to select, insert, update and delete)
    - "Local" connection with SQLite database (can be created if does not exist)
    - Script executed database schema update (triggered by comparing database version number) - structure can be provided in scripts in sources and database will be updated
        - Update is based on upserts and was not tested for changes in table structure
        - Both databases have separate directories for scripts and both are checked against their respective version numbers
    - Helper function for query execution with variable parameters for given Db type (generally used for simple queries of select, insert, update, delete or upsert)
        - 'Simple queries' are mainly due to limitations of SQLite
        - It should handle multiple queries, but I cannot guarantee the performance (WZ)
    - Database can be switched in program settings
* User management system
    - Added/deleted users are in database table
    - User password is hashed
    - User can Log in/log out
    - Permissions of Admin and User enable/disable certain actions
    - List of users
    - "IP registration" - users can register into Db field their current IP Address (right now just local) and it will be shown on user list
* Minigames
    - While user is logged in the minigames menu is available
    - Simple games can be chosen to play:
        1. 15 Puzzle (slider board)
        2. Bulls and Cows (number sequence guessing)


## Setup

1. Create virtual environment:
python -m venv venv

2. Activate:
source venv/bin/activate (Linux/macOS)
venv\Scripts\activate (Windows)

3. Install dependencies:
pip install -r requirements.txt

4. Run the program:
python main.py