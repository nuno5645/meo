# MEO Deals Tracker

The MEO Deals Tracker is an application designed to monitor and display the latest promotional offers available on the MEO website. Intended to provide a seamless and user-friendly experience, the app aggregates current deals, presenting them in an easy-to-navigate interface, ensuring that users never miss out on the best available offers.

## First Draft of the App
![image](https://github.com/nuno5645/meo/assets/21297421/14fdd05a-71df-4356-a206-99a1070d7167)



# Getting Started
To get the application running, you need to have Python installed on your system, along with the Kivy and KivyMD libraries. You also need to set up the Django backend and have Docker installed to run the services defined in the docker-compose.yml file.

# Prerequisites
* Python 3.x
* Kivy
* KivyMD
* Docker

# Installation
## Install Python dependencies:

`pip install kivy kivymd`

## Clone the repository:

`git clone <repository_url>`

Navigate to the cloned repository and build the Docker containers:


``docker-compose up --build``

#Running the Application

After setting up the Docker containers, you can run the KivyMD application with:


``python app.py``


# Application Structure

## KivyMD Frontend

* ModernGridApp: The main app class that initializes the app and loads the product grid.
* ProductCard: A custom card widget that represents a single product in the grid.
* refresh_grid: Fetches data from the API and updates the UI.
  
## Django Backend API
* ScrapeData: An APIView class that scrapes product data from an external source and returns it as JSON.
  
## Docker Compose
The docker-compose.yml file defines the following services:

* djangoapp: The Django application container.
* nginx: The NGINX server used as a reverse proxy.
* database: The PostgreSQL database.
* pgadmin: The web-based PostgreSQL administration tool.
* redis: An in-memory data structure store used as a database, cache, and message broker.
##API Endpoints
/api/scrape_data/: The endpoint to fetch scraped product data.

# Usage
Once the application is running, you can view a grid of products. The grid can be refreshed by clicking the 'Refresh' button, which will fetch the latest product data from the Django backend.

# Development
To modify the application:

1. Edit the KivyMD frontend files for UI changes.
2. Modify the Django backend for changes in API logic or data scraping.
3. Update the docker-compose.yml and associated configurations for changes in the Docker setup.
   
# Contributing
Contributions are welcome. Please open an issue first to discuss what you would like to change or add.

# License
Please ensure you have the right to use and distribute all the dependencies and assets in your project. Your project should include an open-source license if it is to be open-sourced.

