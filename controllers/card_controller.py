from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.card import Card, cards_schema, card_schema
from controllers.comment_controller import comments_bp


cards_bp = Blueprint('cards', __name__, url_prefix='/cards')
cards_bp.register_blueprint(comments_bp)

# route to SEE all cards
@cards_bp.route('/')
def get_all_cards():
    stmt = db.select(Card).order_by(Card.date.desc())
    cards = db.session.scalars(stmt)
    return cards_schema.dump(cards)


# The R - read part of CRUD
# http://localhost:8888/cards/<4>   <- Dynamic || GET
@cards_bp.route('/<int:card_id>')
def get_one_card(card_id): # card_id = 4
    stmt = db.select(Card).filter_by(id=card_id) # select * from cards where id=4
    card = db.session.scalar(stmt)
    if card:
        return card_schema.dump(card)
    else:
        return {"error": f"Card with id {card_id} not found"}, 404

# The C create -  part of CRUD
# http://localhost:8888/cards/ || POST
@cards_bp.route("/", methods=["POST"])
@jwt_required() # this means the user needs to be logged in //
def create_card():
    body_data = request.get_json()
    # Create a new card model instance
    card = Card(
        title = body_data.get('title'),
        description = body_data.get('description'),
        date = date.today(),
        status = body_data.get('status'),
        priority = body_data.get('priority'),
        user_id = get_jwt_identity()
    )
    # add to the session and commit
    db.session.add(card)
    db.session.commit()
    # return the newly cerated card
    return card_schema.dump(card), 201

# The D - delete part of CRUD
# http://localhost:8888/cards/<4>    <- Dynamic || DELETE
@cards_bp.route('/<int:card_id>', methods=["DELETE"])
def delete_card(card_id):
    # get the card from the db with id = card_id
    stmt = db.select(Card).where(Card.id == card_id) # using where as filter by
            # stmt = db.select(Card).filter_by(email=body_data.get("email"))
    card =  db.session.scalar(stmt)
    # if card
    if card:
        #delete the card from the session and commit
        db.session.delete(card)
        db.session.commit()
        #return
        return {"message": f"Card '{card.title}' deleted succesfully"}
    #else
        # return error msg     
    else:
        return {"error": f"card with id {card_id} not found"}, 404    

# The U - update part of CRUD
# http://localhost:8888/cards/<4>   <- Dynamic || PUT PATCH
@cards_bp.route('/<int:card_id>', methods=["PUT", "PATCH"])
def update_card(card_id):
    # Get the data to be updated from the doby of the request
    body_data = request.get_json()
    # get the card from the db whose fields need to be updated
    stmt = db.select(Card).filter_by(id = card_id)
    card = db.session.scalar(stmt)
    # if card
    if card:
        # update fields  
        card.title = body_data.get('title') or card.title
        card.description = body_data.get('description') or card.description
        card.status = body_data.get('status') or card.status
        card.prio = body_data.get('priority') or card.priority
        # commit changes 
        db.session.commit()
        # return the updated card back
        return card_schema.dump(card)
    # else
    else:
        # return error msg
        return {"error": f"Card with id {card_id} not found"}, 404