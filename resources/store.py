from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required

from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("Stores", "stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
            return {"message": f"Store id: {store_id} Deleted"}
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Store already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred inserting the store.")

        return store
