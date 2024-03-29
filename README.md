# Data-Pipelines-with-Airflow

# Introduction 
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring us into the project and expect us to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

# Project Overview
This project will introduce us to the core concepts of Apache Airflow. To complete the project, we will need to create our own custom operators to perform tasks such as staging the data, filling the data warehouse, and running checks on the data as the final step.

# Datasets
We'll be working with two datasets that reside in S3. Here are the S3 links for each:

* Song data: ' s3://udacity-dend/song_data '
* Log data: ' s3://udacity-dend/log_data '

Example of ETL DAG:
![](images/example-dag.png)

# Add Airflow Connections to AWS
Here, we'll use Airflow's UI to configure your AWS credentials and connection to Redshift.

Click on the **Admin** tab and select **Connections**.

![](images/admin-connections.png)

Under **Connections**, select **Create**.

![](images/create-connection.png)

On the create connection page, enter the following values:

**Conn Id:** Enter `aws_credentials`.

**Conn Type:** Enter `Amazon Web Services`.

**Login:** Enter your **Access key ID** from the IAM User credentials you downloaded earlier.

**Password:** Enter your **Secret access key** from the IAM User credentials you downloaded earlier.

Once you've entered these values, select **Save and Add Another**.

![](images/connection-aws-credentials.png)

On the next create connection page, enter the following values:

**Conn Id**: Enter `redshift`.

**Conn Type**: Enter `Postgres`.

**Host**: Enter the endpoint of your Redshift cluster, excluding the port at the end. You can find this by selecting your cluster in the Clusters page of the Amazon Redshift console. See where this is located in the screenshot below. IMPORTANT: Make sure to **NOT** include the port at the end of the Redshift endpoint string.

**Schema**: Enter `dev`. This is the Redshift database you want to connect to.

**Login**: Enter `awsuser`.

**Password**: Enter the password you created when launching your Redshift cluster.

**Port**: Enter `5439`.

Once you've entered these values, select **Save**.

![](images/cluster-details.png)

![](images/connection-redshift.png)

# Project Template
To get started with the project:

The project template package contains three major components for the project:

- The dag template has all the imports and task templates in place, but the task dependencies have not been set
- The operators folder with operator templates
- A helper class for the SQL transformations
With these template files, we should be able see the new DAG in the Airflow UI. The graph view should look like this:

![](images/screenshot-2019-01-21-at-20.55.39.png)


# Building the operators
To complete the project, we need to build four different operators that will stage the data, transform the data, and run checks on data quality.

All of the operators and task instances will run SQL statements against the Redshift database. However, using parameters wisely will allow us to build flexible, reusable, and configurable operators we can later apply to many kinds of data pipelines with Redshift and with other databases.

*Stage Operator*
The stage operator is expected to be able to load any JSON formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided. The operator's parameters should specify where in S3 the file is loaded and what is the target table.

The parameters should be used to distinguish between JSON file. Another important requirement of the stage operator is containing a templated field that allows it to load timestamped files from S3 based on the execution time and run backfills.

# Fact and Dimension Operators
With dimension and fact operators, we can utilize the provided SQL helper class to run data transformations. Most of the logic is within the SQL transformations and the operator is expected to take as input a SQL statement and target database on which to run the query against. We can also define a target table that will contain the results of the transformation.

Dimension loads are often done with the truncate-insert pattern where the target table is emptied before the load. Thus, we could also have a parameter that allows switching between insert modes when loading dimensions. Fact tables are usually so massive that they should only allow append type functionality.

# Data Quality Operator
The final operator to create is the data quality operator, which is used to run checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests. For each the test, the test result and expected result needs to be checked and if there is no match, the operator should raise an exception and the task should retry and fail eventually.

For example one test could be a SQL statement that checks if certain column contains NULL values by counting all the rows that have NULL in the column. We do not want to have any NULLs so expected result would be 0 and the test would compare the SQL statement's outcome to the expected result.
