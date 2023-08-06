import json
import logging
from datetime import datetime

from fastapi import APIRouter, Response

from output.building_ansible import BuildingAnsible
from output.models.activity_logs_database import ActivityLogsData
from output.models.building_database import BuildingData
from output.models.equipments_group_database import EquipmentsGroupData
from output.models.equipments_database import EquipmentsData

router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"],
)


@router.get("/")
async def get_wifis_buildings():
    return BuildingData.get_all(load_related=True)


@router.post("/commands")
async def enable_building_wifi(data: dict):
    wifi = BuildingAnsible()
    wifi.name = data["building"]
    # wifi.execute("script_ansible")

    activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                action=f"Activiation du wifi dans le batiment {wifi.name}")
    activity.save()


@router.post("/")
async def create_building(data: dict):
    name = data.get("building")
    building_to_create = BuildingData(name=name)

    try:
        assert building_to_create.name != ""
        building_to_create.save()
        logging.info(f"{name} a été créé avec succès !")
        response_content = {f"message": f"{name} créé avec succès !"}
        response_status = 200
    except Exception as e:
        logging.error(f"Erreur lors de la création du bâtiment {name} : {e}")
        response_content = {"message": "Un problème est survenu lors de la création du bâtiment"}
        response_status = 500
    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.delete("/")
async def delete_building(data: dict):
    try:
        building_to_delete = BuildingData().get_by_id(data["buildingId"])
        name = building_to_delete.name
        building_to_delete.delete()
        logging.info(f"{name} a été supprimé avec succès !")
        response_content = {f"message": f"{name} a été supprimé avec succès !"}
        response_status = 200
    except Exception as e:
        logging.error(f"Erreur lors de la suppression du bâtiment : {e}")
        response_content = {"message": "Un problème est survenu lors de la suppression du bâtiment"}
        response_status = 500
    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.put("/")
async def update_building(data: dict):
    new_name = data.get("name")
    try:
        building_to_update = BuildingData().get_by_id(data["buildingId"])
        building_to_update.name = new_name
        building_to_update.save()
        logging.info(f"{new_name} a été modifié avec succès !")
        response_content = {f"message": f"{new_name} a été modifié avec succès !"}
        response_status = 200
    except Exception as e:
        logging.error(f"Erreur lors de la modification du bâtiment : {e}")
        response_content = {"message": "Un problème est survenu lors de la modification du bâtiment"}
        response_status = 500
    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.put("/equipments")
async def link_unlink_equipments_to_building(data: dict):
    building = BuildingData().get_by_id(data["buildingId"])
    building_name = building.name
    previous_equipments = [equipment.id for equipment in building.equipments]
    new_equipments = [equipment for equipment in data["equipmentsIds"]]
    equipments_to_add = [equipment for equipment in new_equipments if equipment not in previous_equipments]
    equipments_to_remove = [equipment for equipment in previous_equipments if equipment not in new_equipments]

    try:
        equipments_list = [EquipmentsData().get_equipment_by_id(id_equipment=equipment_id) for equipment_id in
                           equipments_to_add + equipments_to_remove]
        building.update_building_equipment_link(equipments=equipments_list)

        logging.info(f"Les équipements du bâtiment {building_name} ont été mis à jour avec succès !")
        response_content = {"message": f"Les équipements du bâtiment {building_name} ont été mis à jour avec succès !"}
        response_status = 200

    except Exception as e:
        logging.error(f"Erreur lors de la modification des équipements du bâtiment {building_name} : {e}")
        response_content = {
            "message": f"Un problème est survenu lors de la modification des équipements du bâtiment {building_name}"}
        response_status = 500
    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")
