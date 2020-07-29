import re

headers_str = '''
user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36
'''

for i in headers_str.splitlines():
    print(re.sub(' ', '', re.sub('^(.*?):(.*)$', '\'\\1\':\'\\2\',', i)))
