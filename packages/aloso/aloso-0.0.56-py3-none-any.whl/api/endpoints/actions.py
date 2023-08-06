import json

from fastapi import APIRouter, Response

from output.external_api.tickets.actions_impl import ActionsAPI

router = APIRouter(
    prefix="/actions",
    tags=["Actions"],
)


@router.post("/")
async def create_action(data: dict):
    user_matricule = data.get("userMatricule")
    description = data.get("description")
    ticket_id = data.get("ticketId")
    type_action = data.get("typeAction")
    analysis = data.get("analysis")

    action = ActionsAPI()

    response_content = {"message": "Un problème est survenu lors de la création de l'action"}
    response_status = 500

    action.apply_action(type_action=type_action, user_matricule=user_matricule, ticket_id=ticket_id, analysis=analysis)

    if action.save():
        response_content = {
            "message": "Action créée avec succès !"
        }
        response_status = 200

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")
