# Importing aws xlsx and regular expresion libraries
import boto3
import xlsxwriter
import re

# AWS credintials
session = boto3.session.Session(
          aws_access_key_id='',
          aws_secret_access_key='',
		  region_name=''
)

# Creating aws client and aws resource sessions
ec2_client = session.client('ec2')
ec2_resource = session.resource('ec2')

# List of all security groups
all_sec_groups = ec2_client.describe_security_groups()

# Security group patern, for instance
# if you would like to dump security groups 
# that start with PRDO or PRD or prod or prd
# then use the following variable regex = '(PROD.*|PRD.*|prod.*|prd.*)'
# by default all security groups are dumped
regex = '(.*)'

# Creating xlsx
workbook = xlsxwriter.Workbook('aws-sec-group-report.xlsx')
inbound = workbook.add_worksheet('INBOUND')
outbound = workbook.add_worksheet('OUTBOUND')
format_header = workbook.add_format({'bold': True, 'align': 'center'})
format_data = workbook.add_format({'align': 'center'})

# Security group dump function
def get_security_groups(flow, worksheet, pattern):

    row = 0
    col = 0
    
    worksheet.set_column('A:A', 35)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 10)
    worksheet.set_column('F:F', 30)
    worksheet.set_column('G:G', 15)
      
    worksheet.write('A1', 'GroupName', format_header)
    worksheet.write('B1', 'GroupID', format_header)
    worksheet.write('C1', 'FromPort', format_header)
    worksheet.write('D1', 'ToPort', format_header)
    worksheet.write('E1', 'Protocol', format_header)
    worksheet.write('F1', 'Source', format_header)
    worksheet.write('G1', 'SourceID', format_header)
    
    worksheet.freeze_panes(1, 0)
    
    row += 1
    
    for sec_group in all_sec_groups['SecurityGroups']:
        
        if re.match( r'%s' % pattern, sec_group['GroupName'] ) is not None:
            
            for ip_permission in sec_group[flow]:
                
                if ip_permission.has_key('FromPort') and ip_permission.has_key('ToPort'):
                    
                    for ip_range in ip_permission['IpRanges']:
                        
                        if ip_permission['IpProtocol'] == 'icmp' and ip_permission['FromPort'] == -1 and ip_permission['ToPort'] == -1:
                            
                            worksheet.write(row, col, sec_group['GroupName'], format_data)
                            worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                            worksheet.write(row, col + 2, 'ALL', format_data)
                            worksheet.write(row, col + 3, 'ALL', format_data)
                            worksheet.write(row, col + 4, ip_permission['IpProtocol'], format_data)
                            worksheet.write(row, col + 5, ip_range['CidrIp'], format_data)                        
                    
                        elif ip_permission['IpProtocol'] == 'icmp' and ip_permission['FromPort'] != -1 and ip_permission['ToPort'] == -1:
                        
                            worksheet.write(row, col, sec_group['GroupName'], format_data)
                            worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                            worksheet.write(row, col + 2, ip_permission['FromPort'], format_data)
                            worksheet.write(row, col + 3, 'ALL', format_data)
                            worksheet.write(row, col + 4, ip_permission['IpProtocol'], format_data)
                            worksheet.write(row, col + 5, ip_range['CidrIp'], format_data)
                        
                        else:
                        
                            worksheet.write(row, col, sec_group['GroupName'], format_data)
                            worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                            worksheet.write(row, col + 2, ip_permission['FromPort'], format_data)
                            worksheet.write(row, col + 3, ip_permission['ToPort'], format_data)
                            worksheet.write(row, col + 4, ip_permission['IpProtocol'], format_data)
                            worksheet.write(row, col + 5, ip_range['CidrIp'], format_data)                        
                    
                        row += 1
                                
                    for user_id_group_pair in ip_permission['UserIdGroupPairs']:
                    
                        user_name_group_pair = ec2_resource.SecurityGroup(user_id_group_pair['GroupId'])
                    
                        try:
                        
                            if ip_permission['IpProtocol'] == 'icmp' and ip_permission['FromPort'] == -1 and ip_permission['ToPort'] == -1:
                            
                                worksheet.write(row, col, sec_group['GroupName'], format_data)
                                worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                                worksheet.write(row, col + 2, 'ALL', format_data)
                                worksheet.write(row, col + 3, 'ALL', format_data)
                                worksheet.write(row, col + 4, ip_permission['IpProtocol'], format_data)
                                worksheet.write(row, col + 5, user_name_group_pair.group_name, format_data)
                                worksheet.write(row, col + 6, user_id_group_pair['GroupId'], format_data)                            
                            
                            elif ip_permission['IpProtocol'] == 'icmp' and ip_permission['FromPort'] != -1 and ip_permission['ToPort'] == -1:
                            
                                worksheet.write(row, col, sec_group['GroupName'], format_data)
                                worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                                worksheet.write(row, col + 2, ip_permission['FromPort'], format_data)
                                worksheet.write(row, col + 3, 'ALL', format_data)
                                worksheet.write(row, col + 4, ip_permission['IpProtocol'], format_data)
                                worksheet.write(row, col + 5, user_name_group_pair.group_name, format_data)
                                worksheet.write(row, col + 6, user_id_group_pair['GroupId'], format_data)                            
                            
                            else:
                            
                                worksheet.write(row, col, sec_group['GroupName'], format_data)
                                worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                                worksheet.write(row, col + 2, ip_permission['FromPort'], format_data)
                                worksheet.write(row, col + 3, ip_permission['ToPort'], format_data)
                                worksheet.write(row, col + 4, ip_permission['IpProtocol'], format_data)
                                worksheet.write(row, col + 5, user_name_group_pair.group_name, format_data)
                                worksheet.write(row, col + 6, user_id_group_pair['GroupId'], format_data)
                                            
                            row += 1                        

                        except:
                        
                            if ip_permission['IpProtocol'] == 'icmp' and ip_permission['FromPort'] == -1 and ip_permission['ToPort'] == -1:
                            
                                worksheet.write(row, col, sec_group['GroupName'], format_data)
                                worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                                worksheet.write(row, col + 2, 'ALL', format_data)
                                worksheet.write(row, col + 3, 'ALL', format_data)
                                worksheet.write(row, col + 4, ip_permission['IpProtocol'], format_data)
                                worksheet.write(row, col + 5, 'NULL', format_data)
                                worksheet.write(row, col + 6, user_id_group_pair['GroupId'], format_data)
                            
                            elif ip_permission['IpProtocol'] == 'icmp' and ip_permission['FromPort'] != -1 and ip_permission['ToPort'] == -1:
                            
                                worksheet.write(row, col, sec_group['GroupName'], format_data)
                                worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                                worksheet.write(row, col + 2, ip_permission['FromPort'], format_data)
                                worksheet.write(row, col + 3, 'ALL', format_data)
                                worksheet.write(row, col + 4, ip_permission['IpProtocol'], format_data)
                                worksheet.write(row, col + 5, 'NULL', format_data)
                                worksheet.write(row, col + 6, user_id_group_pair['GroupId'], format_data)                            
                        
                            else:
                            
                                worksheet.write(row, col, sec_group['GroupName'], format_data)
                                worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                                worksheet.write(row, col + 2, ip_permission['FromPort'], format_data)
                                worksheet.write(row, col + 3, ip_permission['ToPort'], format_data)
                                worksheet.write(row, col + 4, ip_permission['IpProtocol'], format_data)
                                worksheet.write(row, col + 5, 'NULL', format_data)
                                worksheet.write(row, col + 6, user_id_group_pair['GroupId'], format_data)
                                            
                            row += 1
                        
                else:
            
                    for ip_range in ip_permission['IpRanges']:
                    
                        worksheet.write(row, col, sec_group['GroupName'], format_data)
                        worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                        worksheet.write(row, col + 2, 'ALL', format_data)
                        worksheet.write(row, col + 3, 'ALL', format_data)
                        worksheet.write(row, col + 4, 'ALL', format_data)
                        worksheet.write(row, col + 5, ip_range['CidrIp'], format_data)
                    
                        row += 1
                
                    for user_id_group_pair in ip_permission['UserIdGroupPairs']:
                    
                        user_name_group_pair = ec2_resource.SecurityGroup(user_id_group_pair['GroupId'])
                    
                        try:
                        
                            worksheet.write(row, col, sec_group['GroupName'], format_data)
                            worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                            worksheet.write(row, col + 2, 'ALL', format_data)
                            worksheet.write(row, col + 3, 'ALL', format_data)                        
                            worksheet.write(row, col + 4, 'ALL', format_data)
                            worksheet.write(row, col + 5, user_name_group_pair.group_name, format_data)
                            worksheet.write(row, col + 6, user_id_group_pair['GroupId'], format_data)                       
                    
                            row += 1
                        
                        except:
                        
                            worksheet.write(row, col, sec_group['GroupName'], format_data)
                            worksheet.write(row, col + 1, sec_group['GroupId'], format_data)
                            worksheet.write(row, col + 2, 'ALL', format_data)
                            worksheet.write(row, col + 3, 'ALL', format_data)                        
                            worksheet.write(row, col + 4, 'ALL', format_data)
                            worksheet.write(row, col + 5, user_id_group_pair['GroupId'], format_data)                       
                                            
                            row += 1 

# Main function                        
if __name__ == "__main__":
    
    get_security_groups('IpPermissions', inbound, regex)
    get_security_groups('IpPermissionsEgress', outbound, regex)
    workbook.close()