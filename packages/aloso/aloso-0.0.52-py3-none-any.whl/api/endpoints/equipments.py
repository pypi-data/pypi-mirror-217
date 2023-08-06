import json

from fastapi import APIRouter, Response

import config
from output.external_api.cisco_prime_output import CiscoPrimeOutput
from output.models.equipments_database import EquipmentsData
from output.models.equipments_directories_database import EquipmentsDirectoriesData
from output.models.equipments_group_database import EquipmentsGroupData
from output.shell.equipment_shell import EquipmentShell

router = APIRouter(
    prefix="/equipments",
    tags=["Equipments"],
)


@router.get("/groups/primes")
async def get_cisco_prime_equipments():
    return CiscoPrimeOutput.get_all_devices()


@router.get("/groups")
async def get_equipments_and_groups():
    # V1.0 : Inventory
    # inventory_path = config.inventory_local_directory
    # inventory_name = config.inventory_file_name
    # return EquipmentShell.load_all(f"{inventory_path}/{inventory_name}")
    # V2.0 : Database
    return EquipmentsGroupData.get_all()


@router.post("/groups")
async def create_equipments_group(data: dict):
    value = False
    try:
        new_equipment_group = data["new_equipment"]
        values: str = data["values"]
        list_equipment_group_values = values.split('\n')

        if new_equipment_group != '':
            # V1.0 : Inventory
            # new_group_of_equipments = EquipmentShell()
            # value = new_group_of_equipments.create(name_group=new_equipment_group,
            #                                        list_values=list_equipment_group_values)
            # V2.0 : Database
            new_group_of_equipments = EquipmentsGroupData()
            value = new_group_of_equipments.new_group_and_equipments(new_name_group=new_equipment_group,
                                                                     list_equipments=list_equipment_group_values)
        if value:
            response_content = {"message": f"Le groupe d'équipement {new_equipment_group} a bien été créé"}
            response_status = 200
        else:
            response_content = {
                "message": f"Une erreur est survenu lors de la création du groupe d'équipement {new_equipment_group}"}
            response_status = 500

    except Exception as err:
        response_content = {"message": f"Une erreur est survenu lors de la modification du groupe d'équipement {err}"}
        response_status = 500

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.put("/groups")
async def edit_equipments_and_group(data: dict):
    value = False
    try:
        equipment_group_selected = data["equipment_selected"]
        values: str = data["values"]
        id_group_selected = data["id_group_selected"]
        list_equipment_group_values = values.split('\n')

        if equipment_group_selected != '':
            # V1.0 : Inventory
            # edit_group_of_equipments = EquipmentShell()
            # value = edit_group_of_equipments.edit(name_group=equipment_group_selected,
            #                                       list_values=list_equipment_group_values)
            # V2.0 : Database
            new_group_of_equipments = EquipmentsGroupData.get_group_equipment_by_id(id_group_selected)
            value = EquipmentsGroupData.update_group_and_equipments(my_group=new_group_of_equipments,
                                                                    name_group=equipment_group_selected,
                                                                    list_values=list_equipment_group_values)
        if value:
            response_content = {"message": f"Le groupe d'équipement {equipment_group_selected} a bien été modifié"}
            response_status = 200
        else:
            response_content = {
                "message": f"Une erreur est survenu lors de la modification du groupe d'équipements {equipment_group_selected}"}
            response_status = 500

    except Exception as err:
        response_content = {"message": f"Une erreur est survenu lors de la modification du groupe d'équipements {err}"}
        response_status = 500

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.delete("/groups")
async def delete_equipments_group(data: dict):
    value = False
    try:
        equipment_group_to_remove = data["group_selected"]

        if equipment_group_to_remove != '':
            # V1.0 : Inventory
            # remove_group_of_equipments = EquipmentShell()
            # value = remove_group_of_equipments.remove(name_group=equipment_group_to_remove)
            # V2.0 : Database
            id_group_selected = data["id_group_selected"]
            my_group = EquipmentsGroupData.get_group_equipment_by_id(id_group_selected)
            value = my_group.delete()
        if value:
            response_content = {
                "message": f"Suppression du groupe d'équipement {equipment_group_to_remove} avec succès"}
            response_status = 200
        else:
            response_content = {
                "message": f"Une erreur est survenu lors de la suppression du groupe d'équipement {equipment_group_to_remove}"}
            response_status = 500

    except Exception as err:
        response_content = {"message": f"Une erreur est survenu lors de la suppression du groupe d'équipement {err}"}
        response_status = 500

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.get("/")
async def get_equipments():
    return EquipmentsData.get_all()


@router.post("/")
async def create_equipment(data: dict):
    value = False
    try:
        id_group = data["id_group_selected"]
        values: str = data["values"]
        name_equipment = values.split(' ')[0]

        if id_group is not None:
            new_equipment = EquipmentsData(name=name_equipment, ip=values.split(' ')[1])
            new_equipment.group = EquipmentsGroupData.get_group_equipment_by_id(id_group)
            value = new_equipment.create()

        if value:
            response_content = {"message": f"L'équipement {name_equipment} a bien été créé"}
            response_status = 200
        else:
            response_content = {
                "message": f"Une erreur est survenu lors de la création du nouvel équipement {name_equipment}"}
            response_status = 500

    except Exception as err:
        response_content = {"message": f"Une erreur est survenu lors de la suppression du nouvel équipement {err}"}
        response_status = 500

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.put("/")
async def update_equipment(data: dict):
    value = False
    try:
        id_equipment = data["id_equipment_selected"]
        name_group = data["name_group_selected"]
        values: str = data["values"]
        name_equipment = values.split(' ')[0]

        if id_equipment is not None:
            my_equipment = EquipmentsData.get_equipment_by_id(id_equipment)
            if my_equipment is not None:
                my_equipment.name = name_equipment
                my_equipment.ip = values.split(' ')[1]
                value = my_equipment.update()

        if value:
            response_content = {"message": f"L'équipement {name_equipment} dans {name_group} a bien été modifié"}
            response_status = 200
        else:
            response_content = {
                "message": f"Une erreur est survenu lors de la modification de l'équipement {name_equipment}"}
            response_status = 500

    except Exception as err:
        response_content = {"message": f"Une erreur est survenu lors de la modification de l'équipement {err}"}
        response_status = 500

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.delete("/")
async def delete_equipment(data: dict):
    value = False
    try:
        id_equipment = data["id_equipment_selected"]
        name_equipment = data["name_equipment_selected"]
        name_group = data["name_group_selected"]

        if id_equipment is not None:
            my_equipment = EquipmentsData.get_equipment_by_id(id_equipment)
            value = my_equipment.delete()

        if value:
            response_content = {"message": f"L'équipement {name_equipment} dans {name_group} a bien été supprimé"}
            response_status = 200
        else:
            response_content = {
                "message": f"Une erreur est survenu lors de la suppression de l'équipement {name_equipment} dans {name_group}"}
            response_status = 500

    except Exception as err:
        response_content = {"message": f"Une erreur est survenu lors de la suppression de l'équipement {err}"}
        response_status = 500

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.get("/directories")
async def get_equipments_directories():
    return EquipmentsDirectoriesData.get_all()


@router.get("/directories/files")
async def get_equipments_directories_files():
    return EquipmentShell.get_equipments_directories_files_date_and_size()


@router.get("/versions")
async def get_equipments_diff_versions():
    return EquipmentShell.version_alert(
        actual_version=f"{config.inventory_local_directory}/{config.inventory_file_name}",
        new_version=f"{config.inventory_local_directory}/{config.inventory_file_version}")
