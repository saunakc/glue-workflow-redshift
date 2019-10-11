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

**Step 1** Login into your AWS console and select CloudFormation service. Click "Create stack" and in next screen under Specify template select "Upload a template file". Choose the file from local system where you have downloaded the CFN template [CFN_Redshift_GlueJob.json]( https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/src/cloudformation/vpc-redshift.jsonhttps://github.com/saunakc/glue-workflow-redshift/blob/master/src/cloudformation/CFN_Redshift_GlueJob.json) file. Click Next.

**Step 2 Specify stack details**: Type in a name as Stack name. Enter the VPC parameter and review the other parameters and click Next.

**Step 3 Configure stack options**: Leave blank and click Next.

**Step 4** Scroll down to bottom and select "I acknowledge that AWS CloudFormation might create IAM resources with custom names." option. Hit Create stack.

**Step 5** This will take 10-15 minutes to create all the resources including the Redshift cluster. You can monitor progress of your stack from the Events tab.

**Step 6** Finally the Stack creation will mark as CREATE_COMPLETE. Click on the Outputs tab. You will find all the necessary resources you will need for this lab.

**Post requirements**:
* Go to S3 console and create a folder "**scripts**" under the newly created S3 bucket.
* Unload the 2 files- aodrs-glue-copy.py and aodrs-glue-unload.py.

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
