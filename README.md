# Finance Transaction ETL Pipeline 

## Overview 
A Python ETL pipeline that reads financial transactions from CSV files, validates records, and exports cleaned and rejected transactions separately 

## Features 
- CSV ingestion 
- Transaction validation 
- Duplicate detection 
- Rejection, with reason tracking 
- CSV export 
- logging and error handling
- Testing with pytest 

## Project Structure
finance-project/
├── app/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── ingestion.py
│   └── export.py
├── data/
│   ├── transactions.csv
│   ├── clean_transactions.csv
│   └── rejected_transactions.csv
├── tests/
│   ├── test_cleaning.py
│   ├── test_ingestion.py
│   ├── test_export.py
│   └── test_pipeline.py
├── main.py
└── README.md 
### Application Modules  
- ingestion.py: reads transaction data from CSV files normalizes values into appropriate Python data types.
- cleaning.py: validates transaction records and identifies invalid records (missing customer ids, missing transaction ids, duplicate transaction ids, invalid amounts).
- export.py: Writes valid and invalid transactions into separate CSV files. 

### Data files 
- transactions.csv: simulated input transaction data
- clean_transactions.csv: output file containing valid transactions.  
- rejected_transactions.csv: output file containing invalid transactions.  


### Tests
Contains: 
- test_cleaning.py: tests transaction validation
- test_ingestion.py: tests CSV ingestion and data conversion 
- test_export.py: tests CSV export functionality 
- test_pipeline.py: tests complete pipeline

### main.py
- main.py: Coordinates ingestion, cleaning, logging, and CSV exports through the run_pipeline() function.

## How to Run 
Clone or download the repository and navigate to the project directory.

Run the pipeline:
```bash
python main.py
```

The pipeline reads data/transactions.csv and generates two output files:
- data/clean_transactions.csv
- data/rejected_transactions.csv

## Testing 
Install pytest if necessary:
```bash
python -m pip install pytest
```
Run all automated tests:
```bash
python -m pytest -v
```
The test suite covers ingestion, validation, CSV exports, and end-to-end pipeline functionality.