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


### Create Glue Workflow

#### Create 
