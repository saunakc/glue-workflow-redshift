# glue-shellworkflow-redshift
Building workflow using AWS Glue python shell to load and unload sample data

## Steps for the lab

1. Login into your AWS console and select CloudFormation service. Click "Create stack" and in next screen under Specify template select "Upload a template file". Choose the file from local system where you have downloaded the CFN template [vpc-redshift.json]( https://github.com/saunakc/glue-shellworkflow-redshift/blob/master/src/cloudformation/vpc-redshift.json) file. Click Next.

2. Step 2 Specify stack details: Type in "AodRSGlue" as the Stack name. Review the other parameters for the Redshift cluster and click Next.

3. Step 3 Configure stack options: Leave blank and click Next.

4. Review AodRSGlue: Scroll down to bottom and select "I acknowledge that AWS CloudFormation might create IAM resources with custom names." option. Hit Create stack.
