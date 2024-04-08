# Data Cleanser

## Project Overview

The aims of this project is to provide a web application that can processes data focusing on data type inference and conversion for datasets as accuractely as possible. The application comprises three main components:

1. **Python Packge (data_cleanser):** A python package that I have developed containing independent modules for type inference and data conversion (to specified type). Most of the data processing is handled by this package.

2. **Django Backend:** A Django Rest Framework (DRF) based backend application with essential apis to support uploading of datafiles, returning paginated data from dataset, caching processed data in cache for efficiency, delegate processing to the data_cleanser including inference and conversion.

3. **React Frontend:** A React-based frontend application to allow users to upload data files (CSV, Excel), View Processed Data and Types, Apply new data types on the uploaded data and immediately view the results of type conversion

## Setup Instructions

### Cloning the Project

Clone the project repository to your local machine:

```bash
git clone git@github.com:navdeepbeniwal16/data-cleanser.git
```

### Setting Up the Django/Python Environment

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install Django backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Move to the backend directory and perform the migrations:

   ```bash
   cd backend
   python manage.py migrate
   ```

### Setting Up the React Frontend

1. Move back to the root directory and then to the frontend directory:

   ```bash
   cd ../frontend
   ```

2. Install React dependencies:

   ```bash
   npm install
   ```

### Setting Up Redis for Caching

1. Install Redis using Homebrew (If on mac):

   ```bash
   brew install redis
   ```

   Otherwise navigate to the redis directory I have included in the repository (Fortunately made a backup copy just before Redis decided to revamp their website and make the downloads page return 404 haha.. )

2. Navigate to the Redis directory and compile Redis (only if you have installed the Redis zip package):

   ```bash
   make
   ```

## Starting Servers (Caching, Backend, Frontend)

1. Start the Redis server by running the following command (from anywhere):

   ```bash
   redis-server
   ```

2. Start the Django server by navigating to the backend directory and running:

   ```bash
   python manage.py runserver
   ```

3. Start the frontend development server by navigating to the frontend folder and running:

   ```bash
   npm start
   ```

4. Access the application at localhost:3000

## Design Choices

1. Seperation of concerns: Although it was already an expectation to have a seperate backend and a frontend. In this case, a Django based backend server and a React based frontend clinet. I still decided to go one step further to create a separate python package to handle all of the data processing required for type inference and conversion. This appraoch made things quite managable in the long run as I could individually test the package. Also, being a package it can be reused in another application if need arises. On a deeper level, I have created sepeate views (classes), models (only one was enough), and components in react (one for reach major task)

2. Using a cache in the backend: Although not so ideal for large datasets, they provide a much efficient solution for increasing the performance by temporarily (for a specified amount) the processed data in an application like this where there are extensive computations involved.

3. REST Based Interfaces: I might be a bit biased towards RESTful api's as I have always found them more intuitive to build and integrate systems with them, but it did provided a whole lot of flexibility and a lot more customisation options when it came to implementing the user scenarios. The django-rest-framework (DRS) further provided support for handling data serialization, parsing, validation and pagination, coming in handly for the majority of requirements.

4. Pagination: Implementing pagination across both backend and frontend avoided sending and rendering all of the data at once (posibly saving your broswer from crashing!). This significantly improved the performance and usability of the application.

## Possible Improvements

1. Performance: While adding caching, and support for pagination on both django backend and react frontend, there still quite a scope for improvement to use these solutions more effectively to churn more performance out of the system.

2. Testing: While going with a Test Driven Development and writing automated unit tests ended up serving quite well for the project, the testing can be much more comprehensive to restrict unpredictable behaviour.
