from setuptools import setup, find_packages

setup(
    name='Advanced-Financial-Analytics-System',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'psycopg2-binary',
        'requests',
        'python-dotenv',
        'scikit-learn',
        'numpy',
        'pandas',
        'pytest',
    ],
)
