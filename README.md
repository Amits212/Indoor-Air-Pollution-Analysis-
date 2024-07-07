This project is a FastAPI-based application that allows users to manage buildings and track pollution events. The application provides a RESTful API for creating, reading, updating, and deleting buildings, as well as tracking pollution events related to these buildings.

Features
Get all buildings: Retrieve a list of all buildings.
Get a specific building: Retrieve details of a specific building by name.
Create a new building: Add a new building to the system.
Update an existing building: Modify details of an existing building.
Delete a building: Remove a building from the system.
Track pollution events: Increase or decrease pollution for a building based on specific events.
Requirements
Python 3.8+
Docker
MongoDB


git clone https://https://github.com/Amits212/Indoor-Air-Pollution-Analysis
cd project

run docker-compose up --build


API Endpoints
Get all buildings:

URL: /api/buildings/
Method: GET
Response: A list of buildings.
Get a specific building:

URL: /api/buildings/{building_name}
Method: GET
Path Parameters:
building_name (str): The name of the building.
Response: Details of the specified building.
Create a new building:

URL: /api/buildings/
Method: POST
Request Body:
Building (JSON): The building data.
Response: The ID of the created building.
Update an existing building:

URL: /api/buildings/{building_name}
Method: PUT
Path Parameters:
building_name (str): The name of the building.
Request Body:
Building (JSON): The updated building data.
Response: Success message.
Delete a building:

URL: /api/buildings/{building_name}
Method: DELETE
Path Parameters:
building_name (str): The name of the building.
Response: Success message.
Track pollution events:

URL: /api/buildings/{building_name}/pollution_event
Method: PUT
Path Parameters:
building_name (str): The name of the building.
Request Body:
pollution_type (str): The type of pollution event (e.g., "people smoke", "factory", "Plant growth", "Open windows").
increase_pollution (bool): Whether to increase or decrease pollution.
