from fastapi import APIRouter, HTTPException, Body
from bson import ObjectId
from datetime import datetime
from database import buildings_collection
from models import Building
from sms_config import send_sms
router = APIRouter()

@router.get('/api/buildings/')
async def get_buildings():
    buildings = await buildings_collection.find().to_list(length=100)
    return [Building(**building) for building in buildings]

@router.get('/api/buildings/{building_name}')
async def get_building(building_name: str):
    building = await buildings_collection.find_one({"name": building_name})
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return Building(**building)

@router.post('/api/buildings/')
async def create_building(building: Building):
    building = Building(**building.dict())
    building.calculate_pollution()
    building_dict = building.dict()
    result = await buildings_collection.insert_one(building_dict)
    if result.inserted_id:
        return {"inserted_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Building could not be created")


@router.put('/api/buildings/{building_name}')
async def update_building(building_name: str, building: Building):
    existing_building = await buildings_collection.find_one({"name": building_name})
    if not existing_building:
        raise HTTPException(status_code=404, detail="Building not found")

    update_data = building.dict(exclude_unset=True)

    updated_building = {**existing_building, **update_data}

    result = await buildings_collection.update_one({"name": building_name}, {"$set": updated_building})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Building not found")

    return {"message": "Building updated!"}


@router.delete('/api/buildings/{building_name}')
async def delete_building(building_name: str):
    result = await buildings_collection.delete_one({"name": building_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Building not found")
    return {"status": "Building deleted"}

@router.put('/api/buildings/{building_name}/pollution_event')
async def pollution_event(
        building_name: str,
        pollution_type: str = Body(...),
        increase_pollution: bool = Body(False)
):
    building_data = await buildings_collection.find_one({"name": building_name})
    if not building_data:
        raise HTTPException(status_code=404, detail="Building not found")

    building = Building(**building_data)

    pollution = 0
    action = None

    if pollution_type == "people smoke":
        action = "adding smoking people"
        pollution = 1
    elif pollution_type == "factory":
        action = "building factory next to the building"
        pollution = 5
    elif pollution_type == "Plant growth":
        action = "growing a plant"
        pollution = -3
    elif pollution_type == "Open windows":
        action = "open windows"
        pollution = -4

    building.pollution_percentage += pollution

    event = f"Pollution {'increased' if increase_pollution else 'decreased'} by {abs(pollution)}% after {action}"

    building.make_analysis(time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), event=event)

    await buildings_collection.update_one({"name": building_name}, {"$set": building.dict()})
    if building.pollution_percentage > 20:
        send_sms(message=f'Pollution in building: {building.name} exceed 20%.')

    return building.dict()
