from getpass import getpass

# 原谅我懒得写命令行参数了
user_name = ''  # 你的学号
# 不介意的话，密码可以改成明文
password = getpass('Your password: ')
start_date = '2019-10-06'
end_date = '2019-10-06'
# 会输出学号.json和学号.csv两个文件
output_file_name = user_name
