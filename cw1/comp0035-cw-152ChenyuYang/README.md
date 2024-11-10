# COMP0035 Coursework starter repository for 2024-25

Edit the contents of this readme before submitting your coursework on Moodle.

1.Project Overview
This project is a coursework assignment for COMP0035 and aims to analyse affordable housing supply data for regions across the UK and local authority waiting list data using Python and SQLite.

2.Project structure
project-root/
│
├── section1.py          # Main code, analyze data, generate charts
├── section2.1.md        # Code to draw ERD
├── section2.2.py        # Create SQLite database
├── requirements.txt     # Software that needs to be installed
├── pyproject.toml       # Project Configuration File
├── README.md            # This file
├── dclg-affordable-housing-borough.csv                 # Affordable Housing Dataset
├── dclg-affordable-housing-borough.xlsx                # Affordable Housing Dataset
├── households-on-local-authority-waiting-list.xlsx     # Waiting List Dataset
└── households-on-local-authority-waiting-list1.xlsx    # Waiting List Dataset

3.Project Details
Database Structure
AREA
code: Area code
name: Area name
YEAR
year: Year
WAITING_LIST
waiting_id: Primary key
year: Year
areaCode: Area code
householdsCount: Number of households on the waiting list
AFFORDABLE_HOUSING
housing_id: Primary key
year: Year
areaCode: Area code
housingUnits: Number of affordable housing units
