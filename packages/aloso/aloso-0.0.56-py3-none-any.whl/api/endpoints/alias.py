import json
from datetime import datetime

from fastapi import APIRouter, Query, Response

from output.models.activity_logs_database import ActivityLogsData
from output.record_dns_bind9 import Bind9
from output.shell.equipment_shell import EquipmentShell

router = APIRouter(
    prefix="/alias",
    tags=["Alias"],
)


@router.get("/")
def check_alias(alias_name: str = Query(...)):
    # TODO récuperation liste des alias
    alias = Bind9()
    alias.open_data = ["alias", "switch", "montre", "sel", "souris"]
    alias.name = alias_name

    return alias.alias_is_available()


@router.get("/hosts")
async def check_host(host_name: str = Query(...)):
    equipment = EquipmentShell()
    equipment.name = host_name

    return equipment.server_exists()


@router.post("/")
async def create_alias(data: dict):
    alias = Bind9()
    alias.name = data["alias_name"]
    alias.host = data["host_name"]
    # alias.create_alias()
    value = True  # depends on method create_alias()

    if value:
        activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                    action=f"Création de l'alias {alias.name} vers {alias.host}")
        activity.save()
        response_content = {"message": "L'alias a été créé avec succès !"}
        response_status = 200
    else:
        response_content = {"message": "Une erreur est survenue lors de la création de l'alias"}
        response_status = 500

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")
