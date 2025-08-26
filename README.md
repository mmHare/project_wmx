# Project WMX
Learning project

by Wojciech Zając, Maciej Zając

## About
This project written in Python 3.11 is meant for learning purposes. Console type program features:
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
        - Update is twofold: 
            1. schema check - depends on 'create if not exist'
            2. update scripts with version number - update execute from version in database up to (including) the version in program
        - Both databases have separate directories for scripts and both are checked against their respective version numbers
    - Helper function for query execution with variable parameters for given Db type (generally used for single queries of select, insert, update, delete, upsert and drop)
        - TODO: It should handle multiple queries (WZ)
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
    - Game scores are saved in selected database, game data (including user id, database where it was played and game progress) is stored locally in a db file with the use of TinyDB
    - Simple games can be chosen to play:
        1. 15 Puzzle (slider board)
        2. Bulls and Cows (number sequence guessing)
* Dictionary tables
    - Create table into database by defining table name, columns (varchar only), description and accessibility - table in database is created with prefix "ut_" and metadata are recorded in separate table
    - Delete table is done by DROP query, so there is no record of it afterwards (metadata are also deleted)
    - Visibility: as creating user is assigned as owner, the table can be given private or public access (can be seen by user only or everyone)
    - Adding, deleting items to table
    - Export and import table from CSV file (comma or semicolon delimeter can be set in configuration)


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