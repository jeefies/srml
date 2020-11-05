from setuptools import setup

# from blog.csdn.net/tcy23456/article/details/91886555

with open('README.md') as f:
    long_des=f.read()

with open('requirements.txt') as f:
    reqs = f.read().strip().split()

setup(
        name = 'jsrml',
        author = 'Jeef',
        version = '0.0.1',
        packages = ['srml'],
        author_email = 'jeefy163@163.com',
        description = 'A module to send or recieve emails',
        maintainer = 'Jeef',
        maintainer_email = 'jeefy163@163.com',
        python_requires = '>=3.4',
        package_data = {'': ['*.hy']},
        url = 'https://gituhb.com/jeefies/srml',
        long_description = long_des,
        long_description_content_type = 'text/markdown',
        install_requires = reqs
        )
