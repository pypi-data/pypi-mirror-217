import json
from datetime import datetime

from fastapi import APIRouter, Response

from output.models.activity_logs_database import ActivityLogsData
from output.models.favorite_links_database import FavoriteLinksData

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"],
)


@router.get("/")
async def get_favorites():
    return FavoriteLinksData.get_all_links()


@router.post("/")
async def create_favorites(data: dict):
    name = data["name"]
    url = data["url"]

    response_content = {"message": "Une erreur est survenue lors de la création du favoris"}
    response_status = 500

    favorite = FavoriteLinksData(name=name, url=url)
    if favorite.add_favorite_link():
        activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                    action=f"Ajout du favori {name} | Lien: {url}")
        activity.save()
        response_content = {"message": "Création du favoris avec succès"}
        response_status = 200

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.delete("/")
async def delete_favorites(data: dict):
    response_content = {"message": "Une erreur est survenue lors de la suppression du favoris"}
    response_status = 500
    favorite = FavoriteLinksData().get_favorite_link_by_id(data["id"])
    if favorite.delete_favorite_link():
        activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                    action=f"Suppression du favori {favorite.name} | Lien: {favorite.url}")
        activity.save()
        response_content = {"message": "Suppression du favoris avec succès"}
        response_status = 200

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")


@router.put("/")
async def update_favorites(data: dict):
    response_content = {"message": "Une erreur est survenue lors de la modification du favoris"}
    response_status = 500
    favorite = FavoriteLinksData(id=data["id"], name=data["name"], url=data["url"])
    if favorite.edit_favorite_link():
        activity = ActivityLogsData(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"), author=data["user"],
                                    action=f"Modification du favori {favorite.name} | Lien: {favorite.url}")
        activity.save()
        response_content = {"message": "Modification du favoris avec succès"}
        response_status = 200

    return Response(status_code=response_status, content=json.dumps(response_content), media_type="application/json")
