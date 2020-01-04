# partition_poc
# Authors
- DC (dc@accionlabs.com)

## Description
The project is a POC that may solve FPG Partition Issue.  
This program should be ideally ran with a scheduler such as Airflow  
For the time being we can just simulate.
Steps:  
* Run the Spark Job  
* Then run a swap program. This program will lock all the users so that no more calls can be made. Lock account in MySQL is 
non blocking and it does not kill any transaction thats going on
* There is a wait time that is given. Once the waity time is passed the program will get all the process id from the 
information_schema.processlist table and kill those processes
* Then it will rename the old table to new and archive the new table
* There is a finally block that will unlock the users so that even if something fails users will not remain locked

## How to Simulate
* In MYSQL create two users super_user with pwd super and report_user with pwd report under a DB called swap_test (They are hardcoded as its a POC)
* To populate the big_table_temp use
spark-submit  --packages mysql:mysql-connector-java:8.0.18 <Your_dir>/partition_poc/spark_job_fill_table.py 
* There are two simulations:
    * In one case there is a long running query. For that change the simulation.py and pass change
    execute_a_long_running_query("long"). Then start one terminal and run python simulation.py
    * Start another terminal and run  loc_poc.py
    * You will see that after 60 seconds the query will be killed (simulation.py will throw error) and then the table name swap will happen and then account will be unlocked
    * In second case run a short query For that change the simulation.py and pass change
    execute_a_long_running_query("short"). Then start one terminal and run python simulation.py
    * Start another terminal and run  loc_poc.py
    * You will see both the terminals will give exit 0

## Heartache to users connected
* This solution is not 100% user friendly as users for a minute or two get a error message
* However the swap of name in MySQL is very fast. I was able to swap a table with 20 MN rows in less than 5 seconds

## When it will not work
* This solution may not work if there is no uniformity in the way the end users are connected to Database
    
## TODO List
* If the POC is good to go wrap it with Airflow. This may give a chance to migrate the other spark jobs to Airflow which is the defacto standard for orchestration
 

