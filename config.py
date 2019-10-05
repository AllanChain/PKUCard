from getpass import getpass

# 如果你不介意的话，是可以把下面两行改成明文的
user_name = input('Your student ID: ')
password = getpass('Your password: ')
start_date = '2019-08-17'
end_date = '2019-10-05'
# 会输出output.json和output.csv两个文件
output_file_name = 'output'