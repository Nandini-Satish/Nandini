 # FastAPI Assignment

This is a FastAPI application that performs CRUD operations for two entities: Items and User Clock-In Records.

## Requirements

- Python 3.x
- MongoDB (Atlas or local)

## Installation

1. Clone this repository.
2. Create a virtual environment and activate it:
    
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    
3. Install the required packages:
    
    pip install fastapi[all] motor pydantic
    

## Running the Application

To run the application, use:
```bash
uvicorn main:app --reload

