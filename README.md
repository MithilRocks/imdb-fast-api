# Elements and Commodities Project

### Step 1: Clone repo
Clone this repository in the location of your choice using `git clone https://github.com/MithilRocks/commodities.git`

### Step 2: Setup and installation 
Change directory to `commodities` folder.

Run the command `pipenv shell` to run virtual environment. Wait for a few minutes for the virtual environment to finish the setup.

*(If pipenv not available, install it using `pip install pipenv`)*

Next, run the command `pipenv sync` to install all the dependencies. Give it another minute. 

### Step 3: Run application
The application is ready to run. Ensure virual enviroment is active before doing so. One can check this by looking at the virtual environment name displayed in the command line.

Run the command: `uvicorn main:app --reload`

Finally visit `http://127.0.0.1:8000/docs`
