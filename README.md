# IMDB Project

### Step 1: Clone repo
Open command prompt. Clone this repository in the location of your choice using `git clone https://github.com/MithilRocks/imdb-fast-api.git`

### Step 2: Setup and installation 
Change directory to `imdb-fast-api` folder.

Run the command `pipenv shell` to run virtual environment. Wait for a few minutes for the virtual environment to finish the setup.

[If pipenv not available, install it using `pip install pipenv`](https://pypi.org/project/pipenv/)

Next, run the command `pipenv sync` to install all the dependencies. Give it another minute. 

### Step 3: Run application
The application is ready to run. Ensure virual enviroment is active before doing so. One can check this by looking at the virtual environment name displayed in the command line.

Run the command: `uvicorn main:app --reload`

Finally visit `http://127.0.0.1:8000/docs`

### Step 4: Authentication
As per the project requirements, the application requires authentication before accessing the endpoints. Click the green Authorize button on top right and enter username and password

For admin user, username is admin and password is admin
For general user, username is mithilbhoras and password is mithil
