import logging

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, sessionmaker
from domain.equipes import Equipe

from output.database.database_base import engine, Base
from output.models.equipes_users_database import EquipesUsers


class Equipes(Base, Equipe):
    __tablename__ = "Equipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    users = relationship("Equipes", secondary="Equipes_Users", overlaps="equipes")

    @staticmethod
    def get_all_o():
        try:
            with sessionmaker(bind=engine)() as session:
                data = session.query(Equipes).all()
                equipes = Equipes()
                json_all_equipes = {}
                for equipe in data:
                    json_all_equipes[equipe.id] = {
                        equipe.get_all(db_session=session),
                        # "users": equipe.get_users_by_equipes_id()
                    }
                return equipes.get_all(load_related=True)
        except Exception as e:
            logging.error(e)

    def get_users_by_equipes_id(self):
        try:
            with sessionmaker(bind=engine)() as session:
                data = session.query(EquipesUsers).join(Equipes).filter(Equipes.id == self.id).all()
                print(data)
                json_users_by_contact_id = {}

                for equipe_user in data:
                    json_users_by_contact_id[equipe_user.user_id] = {
                        "user_id": equipe_user.user_id
                    }
                return json_users_by_contact_id
        except Exception as e:
            logging.error(e)

    @staticmethod
    def get_by_id(id_equipment):
        try:
            with sessionmaker(bind=engine)() as session:
                return session.query(Equipes).filter(Equipes.id == id_equipment).first()
        except Exception as e:
            logging.error(e)


