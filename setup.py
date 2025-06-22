from setuptools import setup, find_packages

setup(
    name="expense-tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'Flask==2.3.3',
        'Flask-Cors==4.0.0',
        'pymongo==4.5.0',
        'python-dotenv==1.0.0',
    ],
    extras_require={
        'dev': [
            'pytest==8.2.0',
            'pytest-cov==4.1.0',
            'pytest-mock==3.14.0',
            'pytest-flask==1.3.0',
            'mongomock==4.1.2',
        ],
    },
    python_requires='>=3.8',
)
