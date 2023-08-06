from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='Faloodeh',
    version='0.0.2',
    description='this package is alpha version of faloodeh framwork from iran',
    long_description='hello every one this package is python web framwork and our goal is learning and follow me in my github : https://github.com/amirmohammaddehghan/',
    license='MIT',
    packages=find_packages(),
    author='Amir Mohammad Dehghan',
    author_email='faloodehproject@gmail.com',
    keywords=['Faloodeh', 'FaloodehSearch', 'FaloodehStack'],
    url='https://github.com/AmirMohammadDehghan/Faloodeh',
    download_url='https://pypi.org/project/Faloodeh/'
)

install_requires = [
    'attrs==22.2.0',
    'certifi==2022.12.7',
    'charset-normalizer==3.1.0',
    'colorama==0.4.6',
    'exceptiongroup==1.1.1',
    'greenlet==2.0.2',
    'idna==3.4',
    'iniconfig==2.0.0',
    'Jinja2==3.1.2',
    'MarkupSafe==2.1.2',
    'packaging==23.0',
    'parse==1.19.0',
    'pluggy==1.0.0',
    'pytest==7.2.2',
    'requests==2.28.2',
    'requests-wsgi-adapter==0.4.1',
    'SQLAlchemy==2.0.9',
    'tomli==2.0.1',
    'typing_extensions==4.5.0',
    'urllib3==1.26.15',
    'WebOb==1.8.7',
    'whitenoise==6.4.0',
    'WTForms==3.0.1',

]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)