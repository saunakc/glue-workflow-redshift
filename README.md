# glue-shellworkflow-redshift
Building workflow using AWS Glue python shell to load and unload sample data

## Steps for the lab

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

#### Create Glue jobs

* Switch to AWS service AWS Glue and select Jobs from the left navigation. Click "Add job".
* Enter job information

  Name ->  AodRS
  
  IAM Role -> AWS-Glue-ServiceRole
  
  Type -> Python shell
  
  S3 path where the script is stored -> s3://aws-glue-scripts-<account#>-us-east-2/scripts
  
![AodRSGlueJob](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/AodRS-gluejob-properties1.gif)

* Expand "Security configuration, script libraries ...." and enter below job parameters as Key-Value pair

  ** --host
  ** --port
  ** --dbname
  ** --dbuser
  ** --dbpassword
  ** --iamrole

![AodRSGlueJobParam](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/images/AodRS-gluejob-parameters.gif)

* Hit "Save job and edit script" on Connections screen. Paste the [aodrs-glue-copy.py](https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/src/scripts/aodrs-glue-copy.py) script in the page. Hit Save.
