Prerequisites
=============
1. Install Postgre on your local machine This is an [clink on link to open PostgreSql download page](https://www.postgresql.org/download/).

2. Setup your username and password(remember those,we will need that later)
3. When the installation is finished open pgAdmin
4. On the left side click on the Servers field and then right click to create new Database
5. Configure the user(you can leave the default  "postgres user)


Cleaning and storing data
=============
### Parsing
Parsing data from jsonl files, script will check first if there are desired jsonl files and parse it and save it in database.This way data is parsed only first time when we running our server.When data is parsed jsonl files are moved to backup directory and if we want to parse new data from some other files(or we have new data in same files) we need to put those files in root dir of the project.This way even if we run our server multiple times there won't be necessery trying to store data in db because we have that data already in database.

### Cleaning
1. `Every event that doesn't have all properties` will be discarded even if we can parse that data(for example if event doesn't have event_type field but we can figure out that this event is login event for example,it will be discarded because we can't be sure that data isn't damaged or malicious).

2. `Events with id that already exist` will be discarded,we will keep the first event that is already in database.

3. For registration event all events `that doesn't have valid device_os` will be discarded.I assume that country won't be bigger then 3 characters(beacuse every valid country from dataset has 2 characters), so every country field `that have more then 3 characters` will be discarded.

4. Registration with user_id `that is already in database` will be discarded also because one user can't register more than once.

5. In transaction event every that have transaction_amount or transaction_currency that aren't in valid set(valid amounts are `0.99, 1.99, 2.99, 4.99, 9.99` and valid currencies are `EUR,USD`).

### Storing

`Databse schema looks like this`


`users table`

`user_id(PK) name country device date_of_registration(Date)`

`transactions table`

`user_id(FK) transaction_amount transaction_currency date`

`logins table`

`user_id(FK) login_date`

`exchanges table`

`currency(PK) rate`

Seting up the project
=============
1. Run `python setup.py` from your terminal.It will download all necessary packages(if something unexpected happens try `pip install -r requirements.txt` )
2. Script will ask you to enter your postgre credentials.If you mistype something remove `.env` file and run it again.
3. Script will automatically start server on [127.0.0.1:58929](https://127.0.0.1:58929).
4. You can also manually start server with `uvicorn main:app --reload`, only first time you need to run setup.py file

Running and documentation
=============

# bk1 
## bk2
### bk3

This is an [example link](http://example.com/).

