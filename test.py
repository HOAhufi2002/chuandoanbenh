import random

# Tạo chuỗi ngẫu nhiên
global random_string
random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

# Sử dụng chuỗi ngẫu nhiên
print(random_string)
print(random_string)
