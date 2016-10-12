# Importing aws and xlsx libraries
import boto3
import xlsxwriter

# Global xlsx objects and variables
workbook = None
instances = None
format_header = None
format_data = None
row = 0

# List of all regions and session creation function
def get_ec2_regions():

    session_regions = boto3.session.Session()
    ec2_regions = session_regions.get_available_regions('ec2') 

    for region in ec2_regions:
    
        # AWS credintials
        session = boto3.session.Session(
            aws_access_key_id = '',
            aws_secret_access_key = '',
            region_name = region
        )    

        # Creating aws client and aws resource sessions
        ec2_client = session.client('ec2')
        ec2_resource = session.resource('ec2')

        get_describe_instances(region, ec2_client, ec2_resource)

# List of all described instances function
def get_describe_instances(region, ec2_client, ec2_resource):
    
    global row

    desc_instances = ec2_client.describe_instances()

    for reservations in desc_instances['Reservations']:

        for instance in reservations['Instances']:
        
            try:
            
                instance_id = instance['InstanceId']
                
            except:
            
                instance_id = 'NULL' 
                
            try:
                
                instance_name = get_instance_name(instance_id, ec2_resource)
                
            except:
                
                instance_name = 'NULL'
                
            try:
            
                instance_state = instance['State']['Name']
            
            except:
            
                instance_state = 'NULL'
            
            try:
            
                instance_type = instance['InstanceType']
           
            except:
            
                instance_type = 'NULL'
            
            try:
            
                instance_launchtime = instance['LaunchTime']
            
            except:
            
                instance_launchtime = 'NULL'
            
            try:
            
                instance_privateip = instance['PrivateIpAddress']
            
            except:
            
                instance_privateip = 'NULL'
            
            try:
                        
                instance_publicip = instance['PublicIpAddress']
                        
            except:
                        
                instance_publicip = 'NULL'            
            
            try:
            
                instance_subnetid = instance['SubnetId']
                                
            except:
            
                instance_subnetid = 'NULL'
                                
            try:
                
                instance_subnetname = get_subnet_name(instance_subnetid, ec2_resource)
            
            except:
                
                instance_subnetname = 'NULL'
                
            try:
                      
                instance_vpcid = instance['VpcId']
                        
            except:
                        
                instance_vpcid = 'NULL'

            try:

                instance_vpcname = get_vpc_name(instance_vpcid, ec2_resource)
                
            except:
                
                instance_vpcname = 'NULL'
                
            try:
               
                availability_zone = instance['Placement']['AvailabilityZone']
               
            except:
                
                availability_zone = 'NULL'
        
            print region, instance_id, instance_name, instance_state, instance_type, instance_launchtime, instance_privateip, instance_publicip, instance_subnetid,  instance_subnetname, instance_vpcid, instance_vpcname, availability_zone
            
            row += 1
            
            add_data_xlsx(region, instance_id, instance_name, instance_state, instance_type, instance_launchtime, instance_privateip, instance_publicip, instance_subnetid, instance_subnetname, instance_vpcid, instance_vpcname, availability_zone)
                        
# Identifying instance name tag function
def get_instance_name(InstanceId, ec2_resource):
    
    desc_instance = ec2_resource.Instance(InstanceId)
    instance_tags = desc_instance.tags
    
    for tag in instance_tags:
        
        if tag['Key'] == 'Name':
            
            value = tag['Value']
            break           
    
    return value

# Identifying subnet name tag function
def get_subnet_name(SubnetId, ec2_resource):
    
    desc_subnet = ec2_resource.Subnet(SubnetId) 
    subnet_tags = desc_subnet.tags
                
    for tag in subnet_tags:
        
        if tag['Key'] == 'Name':
            
            value = tag['Value']
            break    

    return value

# Identifying vpc name tag function
def get_vpc_name(VpcId, ec2_resource):
    
    desc_vpc = ec2_resource.Vpc(VpcId) 
    vpc_tags = desc_vpc.tags
                
    for tag in vpc_tags:
        
        if tag['Key'] == 'Name':
            
            value = tag['Value']
            break    

    return value

# Create xlsx object function
def mk_xlsx():
    
    global workbook, instances, format_header, format_data 
    
    workbook = xlsxwriter.Workbook('ec2-instances-report.xlsx')
    instances = workbook.add_worksheet('INSTANCES')
    format_header = workbook.add_format({'bold': True, 'align': 'center'})
    format_data = workbook.add_format({'align': 'center'})
        
    instances.set_column('A:A', 10)
    instances.set_column('B:B', 20)
    instances.set_column('C:C', 30)
    instances.set_column('D:D', 10)
    instances.set_column('E:E', 10)
    instances.set_column('F:F', 25)
    instances.set_column('G:G', 15)
    instances.set_column('H:H', 15)
    instances.set_column('I:I', 20)
    instances.set_column('J:J', 20)
    instances.set_column('K:K', 15)
    instances.set_column('L:L', 15)
    instances.set_column('M:M', 15)
                       
    instances.write('A1', 'Region', format_header)
    instances.write('B1', 'Id', format_header)
    instances.write('C1', 'Name', format_header)
    instances.write('D1', 'Sate', format_header)
    instances.write('E1', 'Type', format_header)
    instances.write('F1', 'Launch', format_header)
    instances.write('G1', 'PrivateIp', format_header)
    instances.write('H1', 'PublicIp', format_header)
    instances.write('I1', 'SubnetId', format_header)
    instances.write('J1', 'SubnetName', format_header)
    instances.write('K1', 'VpcId', format_header)
    instances.write('L1', 'VpcName', format_header)
    instances.write('M1', 'AvailabilityZone', format_header)
    
    instances.freeze_panes(1, 0)    

# Add data to xlsx object function
def add_data_xlsx(region, instance_id, instance_name, instance_state, instance_type, instance_launchtime, instance_privateip, instance_publicip, instance_subnetid, instance_subnetname, instance_vpcid, instance_vpcname, availability_zone):

    global instances, format_data, row 
    col = 0

    instances.write(row, col, region, format_data)
    instances.write(row, col + 1, instance_id, format_data)
    instances.write(row, col + 2, instance_name, format_data)
    instances.write(row, col + 3, instance_state, format_data)
    instances.write(row, col + 4, instance_type, format_data)
    instances.write(row, col + 5, unicode('%s' % instance_launchtime, "utf-8"), format_data)
    instances.write(row, col + 6, instance_privateip, format_data)
    instances.write(row, col + 7, instance_publicip, format_data)
    instances.write(row, col + 8, instance_subnetid, format_data)
    instances.write(row, col + 9, instance_subnetname, format_data)
    instances.write(row, col + 10, instance_vpcid, format_data)
    instances.write(row, col + 11, instance_vpcname, format_data)
    instances.write(row, col + 12, availability_zone, format_data)    

# Main function                        
if __name__ == "__main__":
    
    mk_xlsx()
    get_ec2_regions()
    workbook.close()
