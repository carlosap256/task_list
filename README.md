
## Install virtual environment
For easy dependency management, install virtualenv and pip
```
    sudo apt-get install python3 python3-virtualenv python3-pip

```

## Initialize a new virtual environment
This will create a virtual environment to install the requirements
```
    sudo  virtualenv venv
    source venv/bin/activate

```

## Install the requirements
```
    cd online_manager
    sudo pip install -r requirements.txt

```

## How to set up

The app comes with an autogenerator of test data that creates 15 tasks with the following users:
```
username: alice
password: alice

username: bob
password: bob

username: eve
password: eve
```

To reset the data and regenerate it again run:
```
./manage.py flush
./manage.py test_set

```

## Run the server

To start the server run
```
./manage.py runserver 0:8000

```
This will expose the server at http://localhost:8000
