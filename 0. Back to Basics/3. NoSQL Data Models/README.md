## Data Modelling using NoSQL Databases
---
* NoSQL Databases stand for not only SQL databases
* When Not to Use SQL?
    * Need high Availability in the data: Indicates the system is always up and there is no downtime
    * Have Large Amounts of Data
    * Need Linear Scalability: The need to add more nodes to the system so   performance will increase linearly
    * Low Latency: Shorter delay before the data is transferred once the instruction for the transfer has been received.
    * Need fast reads and write

## Distributed Databases
---
* Data is stored on multiple machines
* Eventual Consistency:
Over time (if no new changes are made) each copy of the data will be the same, but if there are new changes, the data may be different in different locations. The data may be inconsistent for only milliseconds. There are workarounds in place to prevent getting stale data.
* CAP Theorem:
    * It is impossible for a distributed data store to simultaneously provide more than 2 out of 3 guarantees of CAP
    * **Consistency**: Every read from the database gets the latest (and correct) piece of data or an error
    * **Availability**: Every request is received and a response is given -- without a guarantee that the data is the latest update
    * **Partition Tolerance**: The system continues to work regardless of losing network connectivity between nodes
    * Which of these combinations is desirable for a production system - Consistency and Availability, Consistency and Partition Tolerance, or Availability and Partition Tolerance?
        * As the CAP Theorem Wikipedia entry says, "The CAP theorem implies that in the presence of a network partition, one has to choose between consistency and availability." So there is no such thing as Consistency and Availability in a distributed database since it must always tolerate network issues. You can only have Consistency and Partition Tolerance (CP) or Availability and Partition Tolerance (AP). Supporting Availability and Partition Tolerance makes sense, since Availability and Partition Tolerance are the biggest requirements.
* Data Modeling in Apache Cassandra:
    * Denormalization is not just okay -- it's a must, for fast reads
    * Apache Cassandra has been optimized for fast writes
    * ALWAYS think Queries first, one table per query is a great strategy
    * Apache Cassandra does not allow for JOINs between tables
    * Primary Key must be unique
        * The PRIMARY KEY is made up of either just the PARTITION KEY or may also include additional CLUSTERING COLUMNS
        * A Simple PRIMARY KEY is just one column that is also the PARTITION KEY. A Composite PRIMARY KEY is made up of more than one column and will assist in creating a unique value and in your retrieval queries
        * The PARTITION KEY will determine the distribution of data across the system
    * WHERE clause
        * Data Modeling in Apache Cassandra is query focused, and that focus needs to be on the WHERE clause
        * Failure to include a WHERE clause will result in an error

