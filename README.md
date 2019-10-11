# Glue python Shell to build Redshift workflow
In this lab you will learn how to build Glue workflow using Python shell to orchestrate COPY and UNLOAD tables in Amazon Redshift cluster. The sample data is taken from Global Surface Summary of Day data (https://registry.opendata.aws/noaa-gsod/) and is available in public S3 bucket s3://aws-gsod/.

Specifically you will:
* Launch a Redshift cluster from cloudformation template.
* Create AWS Glue jobs using Python shell.
	- Job 1 will copy the public data available in s3://aws-gsod/ into the cluster by running copy command.
	- Job 2 will unload a partition in an s3 location as CSV.
* Create a crawler to crawl the unloaded data.
* Create a AWS Glue workflow to orchestrate the pipeline using graphical interface.
* Run the workflow and validate the unloaded data using Athena and Spectrum.

## Steps for the lab

### Launch infrasturetuce- Redshift cluster, Glue crawler, job and workflow

[![Launch](../images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=ImmersionLab1&templateURL=https://s3-us-west-2.amazonaws.com/redshift-immersionday-labs/lab1.yaml)

Post requirements:
* Go to S3 console and create a folder "scripts" under the newly created S3 bucket.
* Unload the 2 files- aodrs-glue-copy and aodrs-glue-unload.

### Redshift Query Editor to run query

Login into the the Amazon Redshift console and connect to the Query Editor. Supply the below credentials

* Database: aoddc
* Database user: aodmaster
* Password: Welcome123

Once logged in navigate to Schema > Public. There should be no table.

Run the below DDL

```SQL
CREATE TABLE weather_data
(
	id VARCHAR(30) ENCODE zstd,
	usaf INTEGER ENCODE zstd,
	wban INTEGER ENCODE zstd,
	elevation NUMERIC(6, 2) ENCODE zstd,
	country_code VARCHAR(3) ENCODE bytedict,
	latitude NUMERIC(10, 3) ENCODE zstd,
	longitude NUMERIC(10, 3) ENCODE zstd,
	reported_date DATE ENCODE zstd,
	year INTEGER,
	month INTEGER,
	day INTEGER ENCODE zstd,
	mean_temp NUMERIC(6, 2) ENCODE delta32k,
	mean_temp_count INTEGER ENCODE zstd,
	mean_dewpoint NUMERIC(6, 2) ENCODE delta32k,
	mean_dewpoint_count INTEGER ENCODE zstd,
	mean_sea_level_pressure NUMERIC(6, 2) ENCODE delta32k,
	mean_sea_level_pressure_count INTEGER ENCODE delta,
	mean_station_pressure NUMERIC(6, 2) ENCODE delta32k,
	mean_station_pressure_count INTEGER ENCODE zstd,
	mean_visibility NUMERIC(6, 2) ENCODE bytedict,
	mean_visibility_count INTEGER ENCODE delta,
	mean_windspeed NUMERIC(6, 2) ENCODE bytedict,
	mean_windspeed_count INTEGER ENCODE delta,
	max_windspeed NUMERIC(6, 2) ENCODE bytedict,
	max_gust NUMERIC(6, 2) ENCODE bytedict,
	max_temp NUMERIC(6, 2) ENCODE delta32k,
	max_temp_quality_flag INTEGER ENCODE zstd,
	min_temp NUMERIC(6, 2) ENCODE delta32k,
	min_temp_quality_flag CHAR(1) ENCODE zstd,
	precipitation NUMERIC(6, 2) ENCODE zstd,
	precip_flag CHAR(1) ENCODE zstd,
	snow_depth NUMERIC(6, 2) ENCODE zstd,
	fog INTEGER ENCODE zstd,
	rain_or_drizzle INTEGER ENCODE zstd,
	snow_or_ice INTEGER ENCODE zstd,
	hail INTEGER ENCODE zstd,
	thunder INTEGER ENCODE zstd,
	tornado INTEGER ENCODE zstd
)
DISTSTYLE EVEN
SORTKEY
(
	year,
	month
);
```

### Glue workflow load data

Navigate the AWS Glue console > Workflows > AodRSWorkflow. Select > Action > Run.

Check the workflow execution in History tab. This should take 15-20 mintues. After the workflow finished-

* Sample data from public S3 bucket s3://aws-gsod for the year 2016 will be loaded into the Redshift cluster.
* The sample data will also be unloaded in CSV format in the newly created S3 bucket under tables/year=<year>/month=<month>/ 
* The unloaded S3 data is registered as AWS Glue table.


### Create Redshift cluster

1. Login into your AWS console and select CloudFormation service. Click "Create stack" and in next screen under Specify template select "Upload a template file". Choose the file from local system where you have downloaded the CFN template [vpc-redshift.json]( https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/src/cloudformation/vpc-redshift.json) file. Click Next.

![CFN Step 1](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/cfnstep1.gif)

2. Step 2 Specify stack details: Type in "AodRSGlue" as the Stack name. Review the other parameters for the Redshift cluster and click Next.

![CFN Step 2](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/cfnstep2.gif)

3. Step 3 Configure stack options: Leave blank and click Next.

4. Review AodRSGlue: Scroll down to bottom and select "I acknowledge that AWS CloudFormation might create IAM resources with custom names." option. Hit Create stack.

![CFN Step 4](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/cfnstep4.gif)

5. This will take 10-15 minutes to create all the resources including the Redshift cluster. You can monitor progress of your stack from the Events tab.

![CFN Events](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/cfnEvents.gif)

6. Finally the Stack creation will mark as CREATE_COMPLETE. Click on the Outputs tab. You will find all the necessary resources you will need for this lab.

![CFN Outputs](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/cfnsOutputs.gif)

#### Test Cluster connectivity

You can connect to your cluster using your favorite SQL client. I use SQL Workbench/ J. Remember to use details:

* Endpoint - find it from the CFN Outputs. The endpoint will be similar to aodrsstack-redshiftcluster-1vytmfve2c8p5.cqga9q1t5wyf.us-east-2.redshift.amazonaws.com
* Port - **8192**
* Database name - **aoddb**
* Username - **aodmaster**
* Password - **Welcome123**

The JDBC connection string will be 

``jdbc:redshift://aodrsstack-redshiftcluster-1vytmfve2c8p5.cqga9q1t5wyf.us-east-2.redshift.amazonaws.com:8192/aoddb?ssl=false``

### Create table
From your SQL client execute below statement.

```SQL
CREATE TABLE weather_data
(
	id VARCHAR(30) ENCODE zstd,
	usaf INTEGER ENCODE zstd,
	wban INTEGER ENCODE zstd,
	elevation NUMERIC(6, 2) ENCODE zstd,
	country_code VARCHAR(3) ENCODE bytedict,
	latitude NUMERIC(10, 3) ENCODE zstd,
	longitude NUMERIC(10, 3) ENCODE zstd,
	reported_date DATE ENCODE zstd,
	year INTEGER,
	month INTEGER,
	day INTEGER ENCODE zstd,
	mean_temp NUMERIC(6, 2) ENCODE delta32k,
	mean_temp_count INTEGER ENCODE zstd,
	mean_dewpoint NUMERIC(6, 2) ENCODE delta32k,
	mean_dewpoint_count INTEGER ENCODE zstd,
	mean_sea_level_pressure NUMERIC(6, 2) ENCODE delta32k,
	mean_sea_level_pressure_count INTEGER ENCODE delta,
	mean_station_pressure NUMERIC(6, 2) ENCODE delta32k,
	mean_station_pressure_count INTEGER ENCODE zstd,
	mean_visibility NUMERIC(6, 2) ENCODE bytedict,
	mean_visibility_count INTEGER ENCODE delta,
	mean_windspeed NUMERIC(6, 2) ENCODE bytedict,
	mean_windspeed_count INTEGER ENCODE delta,
	max_windspeed NUMERIC(6, 2) ENCODE bytedict,
	max_gust NUMERIC(6, 2) ENCODE bytedict,
	max_temp NUMERIC(6, 2) ENCODE delta32k,
	max_temp_quality_flag INTEGER ENCODE zstd,
	min_temp NUMERIC(6, 2) ENCODE delta32k,
	min_temp_quality_flag CHAR(1) ENCODE zstd,
	precipitation NUMERIC(6, 2) ENCODE zstd,
	precip_flag CHAR(1) ENCODE zstd,
	snow_depth NUMERIC(6, 2) ENCODE zstd,
	fog INTEGER ENCODE zstd,
	rain_or_drizzle INTEGER ENCODE zstd,
	snow_or_ice INTEGER ENCODE zstd,
	hail INTEGER ENCODE zstd,
	thunder INTEGER ENCODE zstd,
	tornado INTEGER ENCODE zstd
)
DISTSTYLE EVEN
SORTKEY
(
	year,
	month
);
```

### Create Glue Workflow

#### Create Redshift COPY job in AWS Glue

* Switch to AWS service AWS Glue and select Jobs from the left navigation. Click "Add job".
* Enter job details

  Name ->  AodRS
  
  IAM Role -> AWS-Glue-ServiceRole
  
  Type -> Python shell
  
  Add new script to be authored by you
  
  S3 path where the script is stored -> s3://aws-glue-scripts-<account#>-us-east-2/scripts
  
![AodRSGlueJob](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/AodRS-gluejob-properties1.gif)

* Expand "Security configuration, script libraries ...." and enter below job parameters as Key and their corresponding Value.

  * --host
  
  * --port
  
  * --dbname
  
  * --dbuser
  
  * --dbpassword
  
  * --iamrole
  

![AodRSGlueJobParam](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/AodRS-gluejob-parameters.gif)

* Hit "Save job and edit script" on Connections screen. Paste the [aodrs-glue-copy.py](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/src/scripts/aodrs-glue-copy.py) script in the page. Hit Save.


#### Create Redshift UNLOAD job in AWS Glue

Similarly create another Python shell job "AodRS_Unload". 

The script can be found in [aodrs-glue-unload.py](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/src/scripts/aodrs-glue-unload.py).

The parameters are

  * --host
  
  * --port
  
  * --dbname
  
  * --dbuser
  
  * --dbpassword
  
  * --iamrole
  
  * --s3location	--> s3://aodrsstack-s3bucket-1bchdtlq8nw17/**tables/weather_data/year=2016/month=01/**
  
  #### Create AWS Glue Crawler
  
  * Click on Crawlers > Add crawler.
  
  * Crawler name -> aodCrawler. Hit Next 2 times.
  
  * In the Add a data store screen specify the "Include path" as the s3 bucket created by the CFN as prefix to the file path. For example ```s3://aodrsstack-s3bucket-1bchdtlq8nw17/tables/```
  
  ![crawler-add-datastore](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/AodRS-gluecrawler-datastore.gif)
  
  * Hit Next 2 times. In the "Choose an IAM role" sreen select "Choose an existing IAM role" >  AWS-Glue-ServiceRole. Hit Next 2 times.
  
  * Configure the crawler's output select Database default and Prefix as aodrs_. Hit Next and Finish.
  
  ![crawler-output](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/AodRS-gluecrawler-output.gif)
  
  ### Create Workflow
  
  * Select ETL > Workflows > Add Workflow. Give a Workflow  name such as "AodWorkFlow". Hit Add workflow.
  
  * Select AoDWorkFlow by clicking the left radio button. In the Graph tab select Action > Add trigger.
  
  * Select Add new and give a name "StartWorkflow" and Trigger type as "On demand".
  
  * Click on "Add node" inside the graph. Select "AodRS" job and hit Add.
  ![glueworkflow-start](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/AodRS-gluewf-startwf.gif)
  
  * Click on the newly added node AodRS. It will display a placeholder Add trigger on its right. Click on the placeholder Add trigger and enter the trigger name as RSCopy-complete. Hit Add.
  ![Glue-trigger-RSCopy-complete](https://github.com/saunakc/glue-workflow-redshift/blob/master/images/Glue-trigger-RSCopy-complete.gif)
  
  * Once this is saved it will create 2 placeholder nodes. The one on the left side is for any additional conditional node(s). We will not add anything there. The right side node is for the triggered node. We will add the Unload job here.
  ![Glue-addnod](https://github.com/saunakc/glue-workflow-redshift/blob/master/images/Glue-addnode.gif)
  
  * Select that right node i.e triggered node and choose "AodRS_Unload" job and hit Add.
  ![Glue-node-RSUnload](https://github.com/saunakc/glue-workflow-redshift/blob/master/images/Glue-node-RSUnload.gif)
  
  * Add another trigger by selecting the "AodRS_Unload" node on the graph and then clicking on Add trigger. Name it "RSUnload-complete".
  
  * Click on the Add node of the right of "RSUnload-complete" and select Crawler aodCrawler.
  ![Glue-crawler-add](https://github.com/saunakc/glue-workflow-redshift/blob/master/images/Glue-crawler-add.gif)
  
  * The final workflow will look like below.
 ![glueworkflow-finalwf](https://github.com/saunakc/glue-workflow-redshift/blob/master/images/Glue-final-workflow.gif)


  ### Run the Workflow
  
  You can run the workflow by selecting the AoDWorkFlow > Actions > Run.
  
  Once the workflow is running you can check the dynaminc view by going to the History tab, selecting the Run ID with Run Status as Running and clicking on View run details.


### Run query on S3 data lake

#### via Athena
* Navigate to AWS GLue > Databases > Tables. The table created by the last step of the above workflow will appear. Name of the table is going to be "aodrs_tables" (if you have followed all the steps as per the instructions).

* Select the checkbox for the table > Actions > View data. Accept Preview data dialog. THis opens up Athena console in a separate tab and the sample query will automatically gets executed.

#### via Spectrum

Before proceeding with the below steps, update the IAM role that is attached to the REdshift cluster to give permission for Glue. Navigate to the IAM service > Roles and search for "AodrsStack-redshift-aod-s3". Click on the role > Permissions > Attach policies > search "AWSGlueServiceRole" > Check and Atatch policy.

* Open SQL client and connect to the Redshift cluster and execute below statement
```sql
create external schema spectrum_schema
from data catalog
database 'default'
region 'us-east-2' 
iam_role 'arn:aws:iam::413094830157:role/AodrsStack-redshift-aod-s3';
```
* Check if the Glue table is sourced into Spectrum
```sql
select * from svv_external_schemas;
```

* Query the table from Redshift

```sql
select * from spectrum_schema.aodrs_tables limit 10;
```

### Don't forget

Before deleting the stack, empty the s3 bucket otherwise delete stack will fail.

After you are done with the lab shut down the cluster and its associated resources by deleting the CFN stack.

![DeleteStack](https://github.com/saunakc/glue-workflow-redshift/blob/master/images/AodRS-deleteStack.gif)
