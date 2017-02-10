# Importing aws
import boto3
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

aws_id = ''
aws_key = ''

ird_asgs = {}

# Here is Jmeter instance located in London region
instances = ['']

# List of all regions and session creation function
def get_ec2_regions():

    session_regions = boto3.session.Session()
    ec2_regions = session_regions.get_available_regions('ec2') 

    for region in ec2_regions:
    
        # AWS credintials
        session = boto3.session.Session(
            aws_access_key_id = aws_id,
            aws_secret_access_key = aws_key,
            region_name = region           
        )   

        # Creating aws client
        autoscaling_client = session.client('autoscaling')
        
        get_describe_asg(region, autoscaling_client)

def get_describe_asg(region, autoscaling_client):

    desc_asgs = autoscaling_client.describe_auto_scaling_groups()
    
    for asg in desc_asgs['AutoScalingGroups']:
        
        asg_name = asg['AutoScalingGroupName']
        asg_desired = asg['DesiredCapacity']
        
#       print 'Region: %s Name: %s DesiredCapacity: %s' %(region, asg_name, asg_desired)
        
        if (asg_name == 'IRD_AP_ASGroup' and asg_desired > 0):
            
            ird_asgs[asg_name] = asg_desired
             
        elif (asg_name == 'IRD_BE2_ASGroup' and asg_desired > 0):
            
            ird_asgs[asg_name] = asg_desired
            
        elif (asg_name == 'IRD_DE_ASGroup' and asg_desired > 0):
                        
            ird_asgs[asg_name] = asg_desired
            
        elif (asg_name == 'IRD_E3_ASGroup' and asg_desired > 0):                                  
                                    
            ird_asgs[asg_name] = asg_desired
            
        elif (asg_name == 'IRD_FE_ASGroup' and asg_desired > 0):                                    
            
            ird_asgs[asg_name] = asg_desired
            
        elif (asg_name == 'IRD_VH_ASGroup' and asg_desired > 0):                                    
                        
            ird_asgs[asg_name] = asg_desired
            
        elif (asg_name == 'IRD_WF_ASGroup' and asg_desired > 0):                                    
                                    
            ird_asgs[asg_name] = asg_desired   

def ird_status():
    
    if (len(ird_asgs) == 7):
        
        start_instances()
        
    elif (len(ird_asgs) == 0):
        
        stop_instances()
        
def start_instances():
    
    event = 'start'
    
    # AWS credintials
    session = boto3.session.Session(
        aws_access_key_id = aws_id,
        aws_secret_access_key = aws_key,        
        region_name = 'eu-west-2'
    )     
    
    ec2_client = session.client('ec2')

    ec2_client.start_instances(InstanceIds=instances)
    
    send_email(event)
    
def stop_instances():

    event = 'stop'
    
    # AWS credintials
    session = boto3.session.Session(
        aws_access_key_id = aws_id,
        aws_secret_access_key = aws_key,        
        region_name = 'eu-west-2'
    )     
    
    ec2_client = session.client('ec2')

    ec2_client.stop_instances(InstanceIds=instances)
    
    send_email(event)

def send_email(event):

    email_headers = MIMEMultipart()
    email_headers['From'] = ''
    email_headers['To'] = ''
    
    if (event == 'start'):
        
        email_headers['Subject'] = "DEV AWS: Instance has been started"
        
    elif (event == 'stop'):
        
        email_headers['Subject'] = "DEV AWS: Instance has been stopped"
        
    email_body = "This email was generated automatically by Infra team" 
    email_headers.attach(MIMEText(email_body, 'plain'))   
    
    smtp = smtplib.SMTP('outlook.office365.com', '587')
    smtp.starttls()  
    smtp.login('', '')
    
    email = email_headers.as_string()
    
    smtp.sendmail(email_headers['From'], email_headers['To'], email)
    smtp.quit()

# Main function                        
if __name__ == "__main__":
               
    get_ec2_regions()
    ird_status()