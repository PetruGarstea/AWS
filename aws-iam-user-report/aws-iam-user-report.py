# Importing aws and xlsx libraries
import boto3
import xlsxwriter

session = boto3.session.Session(
          aws_access_key_id='',
          aws_secret_access_key='',
	  region_name=''
)

# Creating aws client session
iam_client = session.client('iam')

# All users
all_users = iam_client.list_users()

# Creating xlsx
workbook = xlsxwriter.Workbook('aws-iam-user-report.xlsx')
users = workbook.add_worksheet('USERS')
format_header = workbook.add_format({'bold': True, 'align': 'center'})
format_data = workbook.add_format({'align': 'center'})

# Getting user groups and policies function
def get_user_groups_and_policies():

    row = 0
    col = 0
      
    users.set_column('A:A', 40)
    users.set_column('B:B', 25)
    users.set_column('C:C', 25)
    users.set_column('D:D', 15)
    users.set_column('E:E', 25)
    users.set_column('F:F', 30)
           
    users.write('A1', 'UserName', format_header)
    users.write('B1', 'UserCreateDate', format_header)
    users.write('C1', 'PasswordLastUsed', format_header)
    users.write('D1', 'GroupName', format_header)
    users.write('E1', 'GroupCreateDate', format_header)
    users.write('F1', 'PolicyName', format_header)
      
    users.freeze_panes(1, 0)
      
    row += 1    

    for user in all_users['Users']:
        
        all_groups_for_user = iam_client.list_groups_for_user(UserName = user['UserName'])
        all_user_policies = iam_client.list_attached_user_policies(UserName = user['UserName'])
    
        for group in all_groups_for_user['Groups']:
            
            try:
                
                users.write(row, col, user['UserName'], format_data)                
                users.write(row, col + 1, unicode('%s' % user['CreateDate'], "utf-8"), format_data)
                users.write(row, col + 2, unicode('%s' % user['PasswordLastUsed'], "utf-8"), format_data)
                users.write(row, col + 3, group['GroupName'], format_data)
                users.write(row, col + 4, unicode('%s' % group['CreateDate'], "utf-8"), format_data)
                users.write(row, col + 5, 'NULL', format_data)
                
                row += 1       
                               
            except:
                
                users.write(row, col, user['UserName'], format_data)                
                users.write(row, col + 1, unicode('%s' % user['CreateDate'], "utf-8"), format_data)
                users.write(row, col + 2, 'NULL', format_data)
                users.write(row, col + 3, group['GroupName'], format_data)
                users.write(row, col + 4, unicode('%s' % group['CreateDate'], "utf-8"), format_data)
                users.write(row, col + 5, 'NULL', format_data)
                
                row += 1 
                
        for policy in all_user_policies['AttachedPolicies']:
            
            try:
                
                users.write(row, col, user['UserName'], format_data)
                users.write(row, col + 1, unicode('%s' % user['CreateDate'], "utf-8"), format_data)
                users.write(row, col + 2, unicode('%s' % user['PasswordLastUsed'], "utf-8"), format_data)
                users.write(row, col + 3, 'NULL', format_data)
                users.write(row, col + 4, 'NULL', format_data)
                users.write(row, col + 5, policy['PolicyName'], format_data)
                
                row += 1
                
            except:
                
                users.write(row, col, user['UserName'], format_data)
                users.write(row, col + 1, unicode('%s' % user['CreateDate'], "utf-8"), format_data)
                users.write(row, col + 2, 'NULL', format_data)
                users.write(row, col + 3, 'NULL', format_data)
                users.write(row, col + 4, 'NULL', format_data)
                users.write(row, col + 5, policy['PolicyName'], format_data)                
            
                row += 1   
           
if __name__ == "__main__":

    get_user_groups_and_policies()
    workbook.close()