#### Project Summary
The startup Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app

Task: Create a ETL pipeline based on Apache Cassandra. Model data to answer the stated queries.

#### How to Run
- set up Cassandra if not already installed, e.g. run `docker-compose up -d` to start a Cassandra container on port `9042`
- open the project notebook and run the individual cells to get the query results