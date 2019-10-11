import pg
import sys
from awsglue.utils import getResolvedOptions

#iamrole= 'arn:aws:iam::413094830157:role/AodrsStack-redshift-aod-s3'

def get_connection(host):
    rs_conn_string = "host=%s port=%s dbname=%s user=%s password=%s" % (
        host, port, dbname, dbuser, dbpassword)

    rs_conn = pg.connect(dbname=rs_conn_string)
    #rs_conn.query("set statement_timeout = 1200000")
    print("Connection to Redshift cluster %s establised successfully" %host)
    return rs_conn

def query(con):
    stmt = "SELECT year, lpad(month, 2, '0') as month FROM weather_data GROUP BY year, month ORDER by year, month;"
    print("Intitial statement  %s\n" %stmt)
    out = con.query(stmt)
    print("%s statement execute successfully\n" %stmt)
    
    for iterator in out.namedresult():
        print ("Year=", iterator.year , " Month=", iterator.month)
        #statement ="UNLOAD (\'SELECT id,usaf,wban,elevation,country_code,latitude,longitude,day,mean_temp,mean_temp_count,mean_dewpoint,mean_dewpoint_count,mean_sea_level_pressure,mean_sea_level_pressure_count,mean_station_pressure,mean_station_pressure_count,mean_visibility,mean_visibility_count,mean_windspeed,mean_windspeed_count,max_windspeed,max_gust,max_temp,max_temp_quality_flag,min_temp,min_temp_quality_flag,precipitation,precip_flag,snow_depth,fog,rain_or_drizzle,snow_or_ice,hail,thunder,tornado FROM weather_data WHERE year=2016 and month=1 ORDER BY country_code,latitude,longitude\') TO \'%s\' IAM_ROLE \'%s\' HEADER FORMAT CSV GZIP ALLOWOVERWRITE;" % (s3location , iamrole)
        statement ="UNLOAD (\'SELECT id,usaf,wban,elevation,country_code,latitude,longitude,day,mean_temp,mean_temp_count,mean_dewpoint,mean_dewpoint_count,mean_sea_level_pressure,mean_sea_level_pressure_count,mean_station_pressure,mean_station_pressure_count,mean_visibility,mean_visibility_count,mean_windspeed,mean_windspeed_count,max_windspeed,max_gust,max_temp,max_temp_quality_flag,min_temp,min_temp_quality_flag,precipitation,precip_flag,snow_depth,fog,rain_or_drizzle,snow_or_ice,hail,thunder,tornado FROM weather_data WHERE year=%s and month=%s ORDER BY country_code,latitude,longitude\') TO \'%sweather_data/year=%s/month=%s/\' IAM_ROLE \'%s\' HEADER FORMAT CSV GZIP ALLOWOVERWRITE;" % (iterator.year, iterator.month, s3location,iterator.year, iterator.month, iamrole)
        print ("statement: %s" % statement)
        con.query(statement)
    
    
args = getResolvedOptions(sys.argv, [ 'host',
                                        'port',
                                        'dbname',
                                        'dbuser',
                                        'dbpassword',
                                        'iamrole',
                                        's3location'
                                    ]
                        )

#### Read the parameters
host = args['host']
port =  args['port']
dbname = args['dbname']
dbuser = args['dbuser']
dbpassword = args['dbpassword']
iamrole = args['iamrole']
s3location = args['s3location']

try:
    con1 = get_connection(host)
    query(con1)
    print("Data unloaded successfully.")

except:
    print("Data unload unsuccessful: exception %s" % sys.exc_info()[1])
