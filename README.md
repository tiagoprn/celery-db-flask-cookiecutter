# minimal flask app

This project is a minimalistic flask template that can be used as a base to develop simple APIs on the Flask Framework.

## Architecture

Since we are in the era of "microservices", your project should contain only an `api` blueprint .

## Features
- Python 3 (by default, 3.7.0)
- Flask installed
- Gunicorn to run in production
- A sample endpoint working
- A Makefile to ease project management, with commands to run the development server, the shell,
  etc...

## How to use this cookiecutter

- Install cookiecutter on your distribution (e.g. Ubuntu 18.04):

    `$ sudo apt install cookiecutter`

- If you want to clone this repository locally to run the cookiecutter also locally:

    ```
    $ mkdir -p ~/cookiecutters
    $ cd ~/cookiecutters
    $ git clone  https://github.com/tiagoprn/minimal_flask_app_cookiecutter
    ```

- Enter the folder where your want to create your project locally:

    ```
    cd ~/projects/
    ```

- Run the cookiecutter:

* From a local copy:

    `$ cookiecutter ~/cookiecutters/minimal_flask_app_cookiecutter`

* Directly from github (recommended):

    `$ cookiecutter gh:tiagoprn/minimal_flask_app_cookiecutter`

It will ask some questions with sane defaults, and then will generate a folder with the value you
indicated for `project_slug`. Congratulations, this is your new minimal flask project! :)

- Enter the project directory:

    `$ cd ~/projects/your-project_slug`

- Create a virtualenv to the project. If you're using pyenv:

    ```
    $ pyenv virtualenv 3.7.0 your-project_slug
    $ pyenv activate your-project_slug
    ```

- Install the development requirements:

    `$ make requirements`

- Run the make command to create the sample configuration file:

    ```
    $ cd ../../
    $ make init-env
    ```
- Start the development server:

    `$ make runserver-dev`

... or start the production server (gunicorn):

    `$ make runserver`

