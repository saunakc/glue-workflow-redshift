import pg
import sys
from awsglue.utils import getResolvedOptions

#iam_role= 'arn:aws:iam::413094830157:role/AodrsStack-redshift-aod-s3'

def get_connection(host):
    rs_conn_string = "host=%s port=%s dbname=%s user=%s password=%s" % (
        host, port, dbname, dbuser, dbpassword)

    rs_conn = pg.connect(dbname=rs_conn_string)
    #rs_conn.query("set statement_timeout = 1200000")
    return rs_conn

def query(con):
    statement = "copy weather_data from \'s3://aws-gsod/2016/\' iam_role \'%s\' REGION \'us-east-1\'  DELIMITER \',\'  REMOVEQUOTES IGNOREHEADER as 1;" % iamrole
    print ("statement: %s" % statement)
    con.query(statement)
    
    
args = getResolvedOptions(sys.argv, [ 'host',
                                        'port',
                                        'dbname',
                                        'dbuser',
                                        'dbpassword',
                                        'iamrole'
                                    ]
                        )

#### Read the parameters
host = args['host']
port =  args['port']
dbname = args['dbname']
dbuser = args['dbuser']
dbpassword = args['dbpassword']
iamrole = args['iamrole']

try:
    con1 = get_connection(host)
    query(con1)
    print("Data copied successfully.")

except:
    print("Data copy unsuccessful: exception %s" % sys.exc_info()[1])
