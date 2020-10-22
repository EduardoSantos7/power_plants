# power_plants
-----------------

Power_plants is a backend app that allows clients to get data on the annual net production of the power plants and states across the US. This app is built-in `Python 3` using `Flask` to build the API and `Pandas`, `SQLAlchemy`, `Postgres` to save the [data] of power plants and states. `Unittest` is used to verify that the core function is still working after each commit. 

### Features!
-----------------

  - Return the Top N power plants.
  - Return the State(s) and national production (allowing the client to get the percentage using different criteria).
  - The top N plans can be selected from one given State.
  - Data persist
  - Dockerized 
  - Tests

### Tech
-----------------

Power_plants uses a number of open source projects to work properly:

* [Python 3] - algorithms, DB connection and tests!
* [SQLAlchemy] - ORM
* [Postgres] - relational database.
* [Unittest] - framework for test.
* [Docker] - containers.
* [Pandas] - manipulate csv.


The `powerplant`table in the database has 4 columns (`facility_code`, `name`, `state_abbreviation` and `annual_net_generation` which has an index) and looks like this:

![Alt text](documentation/power_plants_table.png?raw=true "Table example")


The `state`table in the database has 2 columns (`state_abbreviation` which has an index and `annual_net_generation`) and looks like this:

![Alt text](documentation/states_table.png?raw=true "Table example")

### Considerations!
-----------------

  - `None` values in the `annual net generation data` are considered as zero due to ignoring the row will be not convenient in order to add future features or results.
  - The arguments (`number_plants` and `state_abbreviation`) are not required. if their values are `None` then the default behavior is `take all` (get all the states or all the plants)
  - The `annual_net_generation` field in the `powerplant`table is indexed.
  - The `state_abbreviation` field in the `states_table` table is indexed.

### Installation
-----------------

1) Clone the repository (`.env` and `database.env` files are exposed for demonstration purposes, that said, this doesn't represent security leaks)

2) Build the containers

    ```sh
    $ docker-compose up
    ```
    After this step you should see a message from the DB container like this: `database system is ready to accept connections` and other from the backend service: 
    ```
        * Serving Flask app "run.py"
    web_1  |  * Environment: production
    web_1  |    WARNING: This is a development server. Do not use it in a production deployment.
    web_1  |    Use a production WSGI server instead.
    web_1  |  * Debug mode: off
    ```
    The first time the data from the `.csv` files will be loaded and after this, you should see this message:
    `Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`
    At this point, the backend is running and ready to serve client requests.

*If you want to run the tests:*

3) Open other terminal run: 
    ```sh
    $ docker exec -ti power_plants_web_1 sh
    ```
4) Now you can run the tests using the next command:

    ```python
    python test_power_plant.py 
    ```
    
    You should see this message:
    
    ```
    Ran 6 tests in 356.068s

    OK
    ```

### API Examples
-----------------

1) Getting the top 3 plants:

Request:
  ```json
  localhost:5000/power_plants?number_plants=3
  ```
Respone:
  ```json
  [
      {
          "annual_net_generation": 31097259,
          "facility_code": 6008,
          "name": "Palo Verde",
          "state_abbreviation": "AZ"
      },
      {
          "annual_net_generation": 25397781,
          "facility_code": 46,
          "name": "Browns Ferry",
          "state_abbreviation": "AL"
      },
      {
          "annual_net_generation": 21680116,
          "facility_code": 3166,
          "name": "Peach Bottom",
          "state_abbreviation": "PA"
      }
  ]
  ```
  
  2) Getting the production of California:
  
  Request:
  ```json
  localhost:5000/states?state_abbreviation=ca
  ```
  Respone:
  ```json
  [
    {
        "annual_net_generation": 195212860,
        "state_abbreviation": "CA"
    }
  ]
  ```


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [Python 3]: <https://www.python.org/>
   [SQLAlchemy]: <https://www.sqlalchemy.org/>
   [Postgres]: <https://www.postgresql.org/>
   [Unittest]: <https://docs.python.org/3/library/unittest.html>
   [Docker]: <https://www.docker.com/>
   [data]: <https://www.epa.gov/egrid/data-explorer>
   [Pandas]: <https://pandas.pydata.org/>
