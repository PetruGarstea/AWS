# Importing aws and xlsx libraries
import boto3
import xlsxwriter
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

# Global xlsx objects and variables
workbook = None
volumes = None
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

        get_describe_volumes(region, ec2_client, ec2_resource)

# List of all volumes function      
def get_describe_volumes(region, ec2_client, ec2_resource):
    
    global row
    
    desc_volumes = ec2_client.describe_volumes()
    
    for volume in desc_volumes['Volumes']:
        
        volume_attachments = volume['Attachments']
        
        volume_id = volume['VolumeId']
        volume_state = volume['State']
        volume_size = volume['Size']
        volume_snapshot_id = volume['SnapshotId']
        volume_encrypted = volume['Encrypted']
        volume_type = volume['VolumeType']
        volume_createtime = volume['CreateTime']
        
        volume_iops, volume_tags = get_volume_data(volume_id, ec2_resource)
        
        if volume_attachments:
            
            for attachment in volume_attachments:
            
                volume_instance_id = attachment['InstanceId']
                
                volume_instance = get_instance_name(volume_instance_id, ec2_resource)
            
                print '%s Region: %s Id: %s State: %s Size: %s SnapshotId %s Encrypted: %s Type: %s CreateTime: %s AttachToInstanceId: %s AttachedToInstance: %s IOPS: %s Tags: %s' % (
                       
                    row, region, volume_id, volume_state, volume_size,
                    volume_snapshot_id, volume_encrypted, volume_type,
                    volume_createtime, volume_instance_id, volume_instance,
                    volume_iops, volume_tags
                    
                )

                row += 1
                        
                add_data_xlsx(region, volume_id, volume_state, volume_size, volume_snapshot_id, volume_encrypted, volume_type, volume_createtime, volume_instance_id, volume_instance, volume_iops, volume_tags)
                
        else:
            
            volume_instance_id = 'NULL'
            
            volume_instance = 'NULL'
            
            print '%s Region: %s Id: %s State: %s Size: %s SnapshotId %s Encrypted: %s Type: %s CreateTime: %s AttachToInstanceId: %s AttachedToInstance: %s IOPS: %s Tags: %s' % (
                                   
                row, region, volume_id, volume_state, volume_size,
                volume_snapshot_id, volume_encrypted, volume_type,
                volume_createtime, volume_instance_id, volume_instance,
                volume_iops, volume_tags
                               
            )
            
            row += 1
            
            add_data_xlsx(region, volume_id, volume_state, volume_size, volume_snapshot_id, volume_encrypted, volume_type, volume_createtime, volume_instance_id, volume_instance, volume_iops, volume_tags)

# Identifying instance name tag function
def get_instance_name(InstanceId, ec2_resource):
    
    desc_instance = ec2_resource.Instance(InstanceId)
    instance_tags = desc_instance.tags
    
    try:
        
        for tag in instance_tags:
        
            if tag['Key'] == 'Name':
            
                value = tag['Value']
                break           
    except:
        
        value= None
        
    return value

# Identifying Volume IOPS function
def get_volume_data(VolumeId, ec2_resource):
    
    desc_volume = ec2_resource.Volume(VolumeId)

    volume_tags = desc_volume.tags

    volume_iops = desc_volume.iops
    
    try:
        
        for tag in volume_tags:
        
            if tag['Key'] == 'Name':
            
                value = tag['Value']
                
                break           

    except:
        
        value= None
        
    return volume_iops, value

# Create xlsx object function
def mk_xlsx():
    
    global workbook, volumes, format_header, format_data 
    
    workbook = xlsxwriter.Workbook('ec2-volumes-report.xlsx')
    volumes = workbook.add_worksheet('VOLUMES')
    format_header = workbook.add_format({'bold': True, 'align': 'center'})
    format_data = workbook.add_format({'align': 'center'})
        
    volumes.set_column('A:A', 10)
    volumes.set_column('B:B', 25)
    volumes.set_column('C:C', 10)
    volumes.set_column('D:D', 10)
    volumes.set_column('E:E', 25)
    volumes.set_column('F:F', 15)
    volumes.set_column('G:G', 10)
    volumes.set_column('H:H', 30)
    volumes.set_column('I:I', 25)
    volumes.set_column('J:J', 40)
    volumes.set_column('K:K', 10)
    volumes.set_column('L:L', 15)
                       
    volumes.write('A1', 'Region', format_header)
    volumes.write('B1', 'Id', format_header)
    volumes.write('C1', 'State', format_header)
    volumes.write('D1', 'Size', format_header)
    volumes.write('E1', 'SnapshotId', format_header)
    volumes.write('F1', 'Encrypted', format_header)
    volumes.write('G1', 'Type', format_header)
    volumes.write('H1', 'CreateTime', format_header)
    volumes.write('I1', 'AttachedToInstanceId', format_header)
    volumes.write('J1', 'AttachedToInstance', format_header)
    volumes.write('K1', 'IOPS', format_header)
    volumes.write('L1', 'Tags', format_header)    
    
    volumes.freeze_panes(1, 0)
    
# Add data to xlsx object function
def add_data_xlsx(region, volume_id, volume_state, volume_size, volume_snapshot_id, volume_encrypted, volume_type, volume_createtime, volume_instance_id, volume_instance, volume_iops, volume_tags):

    global volumes, format_data, row 
    col = 0

    volumes.write(row, col, region, format_data)
    volumes.write(row, col + 1, volume_id, format_data)
    volumes.write(row, col + 2, volume_state, format_data)
    volumes.write(row, col + 3, volume_size, format_data)
    volumes.write(row, col + 4, volume_snapshot_id, format_data)
    volumes.write(row, col + 5, volume_encrypted, format_data)
    volumes.write(row, col + 6, volume_type, format_data)
    volumes.write(row, col + 7, unicode('%s' % volume_createtime, "utf-8"), format_data)
    volumes.write(row, col + 8, volume_instance_id, format_data)
    volumes.write(row, col + 9, volume_instance, format_data)
    volumes.write(row, col + 10, volume_iops, format_data)
    volumes.write(row, col + 11, volume_tags, format_data)
    

def send_email():

    email_headers = MIMEMultipart()
    email_headers['From'] = ''
    email_headers['To'] = ''
    email_headers['Subject'] = "DEV AWS: Volumes Inventory"    
    email_body = "This email was generated automatically by Infra team" 
    email_headers.attach(MIMEText(email_body, 'plain'))
    
    attachment = open('ec2-volumes-report.xlsx', 'rb')
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename=ec2-volumes-report.xlsx")
     
    email_headers.attach(part)    
    
    smtp = smtplib.SMTP('outlook.office365.com', '587')
    smtp.starttls()  
    smtp.login('', '')
    
    email = email_headers.as_string()
    
    smtp.sendmail(email_headers['From'], email_headers['To'], email)
    smtp.quit()

# Main function                        
if __name__ == "__main__":
    
    mk_xlsx()           
    get_ec2_regions()
    volumes.autofilter(0,0,row,11)
    workbook.close()
    send_email()