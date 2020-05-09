## What is Spark?
---
* Spark is a general-purpose distributed data processing engine. 
* On top of the Spark core data processing engine, there are libraries for SQL, machine learning, graph computation, and stream processing, which can be used together in an application.
* Spark is often used with distributed data stores such as Hadoop's HDFS, and Amazon's S3, with popular NoSQL databases such as Apache HBase, Apache Cassandra, and MongoDB, and with distributed messaging stores such as MapR Event Store and Apache Kafka.
* Pyspark API
    * Pyspark supports imperative (Spark Dataframes) and declarative syntax (Spark SQL)

## How a Spark Application Runs on a Cluster
---
* A Spark application runs as independent processes, coordinated by the SparkSession object in the driver program.
* The resource or cluster manager assigns tasks to workers, one task per partition.
* A task applies its unit of work to the dataset in its partition and outputs a new partition dataset.
* Because iterative algorithms apply operations repeatedly to data, they benefit from caching datasets across iterations.
* Results are sent back to the driver application or can be saved to disk.
* Spark supports the following resource/cluster managers:
    * Spark Standalone – a simple cluster manager included with Spark
    * Apache Mesos – a general cluster manager that can also run Hadoop applications
    * Apache Hadoop YARN – the resource manager in Hadoop 2
    * Kubernetes – an open source system for automating deployment, scaling, and management of containerized applications

## Spark's Limitations
---
* Spark Streaming’s latency is at least 500 milliseconds since it operates on micro-batches of records, instead of processing one record at a time. Native streaming tools such as Storm, Apex, or Flink can push down this latency value and might be more suitable for low-latency applications. Flink and Apex can be used for batch computation as well, so if you're already using them for stream processing, there's no need to add Spark to your stack of technologies.

* Another limitation of Spark is its selection of machine learning algorithms. Currently, Spark only supports algorithms that scale linearly with the input data size. In general, deep learning is not available either, though there are many projects integrate Spark with Tensorflow and other deep learning tools.