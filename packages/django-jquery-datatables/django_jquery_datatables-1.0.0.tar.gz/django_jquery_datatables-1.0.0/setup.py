from setuptools import setup, find_packages

setup(
    name='django_jquery_datatables',
    version='1.0.0',
    description='Python library that integrates the popular jQuery DataTables library with Django projects.',
    author='Salik Sheraz',
    author_email='salik.sheraz@it-masons.com',
    url='https://github.com/yourusername/mylibrary',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0.0',
        'requests>=2.0.0',
        'django-rest-framework>=0.1.0'
    ],
)
