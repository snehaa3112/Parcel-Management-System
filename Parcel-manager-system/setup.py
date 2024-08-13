from setuptools import setup, find_packages

setup(
    name='assignment',  # The name of your package
    version='0.1',  # The version of your package
    packages=find_packages(),  # Automatically find all packages and sub-packages
    install_requires=[  # List your package dependencies here
        'Flask==2.1.1',
        'Flask-SocketIO==5.1.1',
        'Flask-Bcrypt==0.7.1',
        'Flask-SQLAlchemy==2.5.1',
        'Flask-WTF==0.15.1',
        'pandas==1.3.5',
        'eventlet==0.32.0',
        'PyMySQL==1.0.2'
    ],
    entry_points={
        'console_scripts': [
            'assignment=app:main',  # Adjust to your main entry point if necessary
        ],
    },
)
