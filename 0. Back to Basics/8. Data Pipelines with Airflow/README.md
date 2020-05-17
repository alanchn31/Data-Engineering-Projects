## What is a Data Pipeline?
---
* A data pipeline is simply, a series of steps in which data is processed

## Data Partitioning
---
* Pipeline data partitioning is the process of isolating data to be analyzed by one or more attributes, such as time, logical type or data size
* Data partitioning often leads to faster and more reliable pipelines
* <ins>Types of Data Partitioning:</ins>
    1. Schedule partitioning
        * Not only are schedules great for reducing the amount of data our pipelines have to process, but they also help us guarantee that we can meet timing guarantees that our data consumers may need
    2. Logical partitioning
        * Conceptually related data can be partitioned into discrete segments and processed separately. This process of separating data based on its conceptual relationship is called logical partitioning. 
        * With logical partitioning, unrelated things belong in separate steps. Consider your dependencies and separate processing around those boundaries
        * Examples of such partitioning are by date and time
    3. Size partitioning
        * Size partitioning separates data for processing based on desired or required storage limits
        * This essentially sets the amount of data included in a data pipeline run
* Why partition data?
    * Pipelines designed to work with partitioned data fail more gracefully. Smaller datasets, smaller time periods, and related concepts are easier to debug than big datasets, large time periods, and unrelated concepts
    * If data is partitioned appropriately, tasks will naturally have fewer dependencies on each other 
    * Airflow will be able to parallelize execution of DAGs to produce results even faster

## Data Validation
---
* Data Validation is the process of ensuring that data is present, correct & meaningful. Ensuring the quality of data through automated validation checks is a critical step in building data pipelines at any organization

## Data Quality
---
* Data Quality is a measure of how well a dataset satisfies its intended use
* <ins>Examples of Data Quality Requirements</ins>
    * Data must be a certain size
    * Data must be accurate to some margin of error
    * Data must arrive within a given timeframe from the start of execution
    * Pipelines must run on a particular schedule
    * Data must not contain any sensitive information

## Directed Acyclic Graphs
---
* Directed Acyclic Graphs (DAGs): DAGs are a special subset of graphs in which the edges between nodes have a specific direction, and no cycles exist. 

## Apache Airflow
---
* What is Airflow?
    * Airflow is a platform to programmatically author, schedule and monitor workflows
    * Use airflow to author workflows as directed acyclic graphs (DAGs) of tasks
    * The airflow scheduler executes your tasks on an array of workers while following the specified dependencies
    * When workflows are defined as code, they become more maintainable, versionable, testable, and collaborative

* Airflow concepts (Taken from Airflow documentation)
    * <ins>Operators</ins>
        * Operators determine what actually gets done by a task. An operator describes a single task in a workflow. Operators are usually (but not always) atomic. The DAG will make sure that operators run in the correct order; other than those dependencies, operators generally run independently
    * <ins>Tasks</ins>
        * Once an operator is instantiated, it is referred to as a "task" The instantiation defines specific values when calling the abstract operator, and the parameterized task becomes a node in a DAG
        * A task instance represents a specific run of a task and is characterized as the combination of a DAG, a task, and a point in time. Task instances also have an indicative state, which could be “running”, “success”, “failed”, “skipped”, “up for retry”, etc
    * <ins>DAGs</ins>
        * In Airflow, a DAG – or a Directed Acyclic Graph – is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies
        * A DAG run is a physical instance of a DAG, containing task instances that run for a specific execution_date. A DAG run is usually created by the Airflow scheduler, but can also be created by an external trigger
    * <ins>Hooks</ins>
        * Hooks are interfaces to external platforms and databases like Hive, S3, MySQL, Postgres, HDFS, and Pig. Hooks implement a common interface when possible, and act as a building block for operators
        * They also use the airflow.models.connection.Connection model to retrieve hostnames and authentication information
        *  Hooks keep authentication code and information out of pipelines, centralized in the metadata database
    * <ins>Connections</ins>
        * The information needed to connect to external systems is stored in the Airflow metastore database and can be managed in the UI (Menu -> Admin -> Connections)
        * A conn_id is defined there, and hostname / login / password / schema information attached to it
        * Airflow pipelines retrieve centrally-managed connections information by specifying the relevant conn_id
    * <ins>Variables</ins>
        * Variables are a generic way to store and retrieve arbitrary content or settings as a simple key value store within Airflow
        * Variables can be listed, created, updated and deleted from the UI (Admin -> Variables), code or CLI. In addition, json settings files can be bulk uploaded through the UI
    * <ins>Context & Templating</ins>
        * Airflow leverages templating to allow users to "fill in the blank" with important runtime variables for tasks
        * See: https://airflow.apache.org/docs/stable/macros-ref for a list of context variables

* Airflow functionalities
    * Airflow Plugins
        * Airflow was built with the intention of allowing its users to extend and customize its functionality through plugins. 
        * The most common types of user-created plugins for Airflow are Operators and Hooks. These plugins make DAGs reusable and simpler to maintain
        * To create custom operator, follow the steps
            1. Identify Operators that perform similar functions and can be consolidated
            2. Define a new Operator in the plugins folder
            3. Replace the original Operators with your new custom one, re-parameterize, and instantiate them
    * Airflow subdags
        * Commonly repeated series of tasks within DAGs can be captured as reusable SubDAGs
        * Benefits include:
            * Decrease the amount of code we need to write and maintain to create a new DAG
            * Easier to understand the high level goals of a DAG
            * Bug fixes, speedups, and other enhancements can be made more quickly and distributed to all DAGs that use that SubDAG
        * Drawbacks of Using SubDAGs:
            * Limit the visibility within the Airflow UI
            * Abstraction makes understanding what the DAG is doing more difficult
            * Encourages premature optimization

    * Monitoring
        * Airflow can surface metrics and emails to help you stay on top of pipeline issues
        * SLAs
            * Airflow DAGs may optionally specify an SLA, or “Service Level Agreement”, which is defined as a time by which a DAG must complete
            * For time-sensitive applications these features are critical for developing trust amongst pipeline customers and ensuring that data is delivered while it is still meaningful
        * Emails and Alerts
            * Airflow can be configured to send emails on DAG and task state changes
            * These state changes may include successes, failures, or retries
            * Failure emails can easily trigger alerts
        * Metrics
            * Airflow comes out of the box with the ability to send system metrics using a metrics aggregator called statsd
            *  Statsd can be coupled with metrics visualization tools like Grafana to provide high level insights into the overall performance of DAGs, jobs, and tasks

* Best practices for data pipelining
    * Task Boundaries  
    DAG tasks should be designed such that they are:
        * Atomic and have a single purpose
        * Maximize parallelism
        * Make failure states obvious