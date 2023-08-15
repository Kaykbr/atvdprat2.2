from flask_restful import Resource, reqparse
from flask import jsonify
from models import db, Tutor, Pet, TutorSchema, PetSchema

class TutorResource(Resource):
    def get(self, tutor_id=None): 
        if tutor_id is None:
            tutors = Tutor.query.all()
            return TutorSchema(many=True).dump(tutors), 200

        tutor = Tutor.query.get(tutor_id)
        return TutorSchema().dump(tutor), 200
    
    def post(self, tutor_id=None):
        parse = reqparse.RequestParser()
        parse.add_argument('nome_tutor', type=str, required=True)
        args = parse.parse_args()
        tutor = Tutor(nome=args['nome_tutor'])
        db.session.add(tutor)
        db.session.commit()
        return TutorSchema().dump(tutor), 201
    
    def put(self, tutor_id=None):
        parse = reqparse.RequestParser()
        parse.add_argument('nome_tutor', type=str, required=True)
        args = parse.parse_args()
        tutor = Tutor(nome=args['nome_tutor'])
        tutor = Tutor.query.get(tutor_id)  
        tutor.nome = args['nome_tutor']
        db.session.commit()
        return TutorSchema().dump(tutor), 200
    
    def delete(self, tutor_id=None):
        tutor = Tutor.query.get(tutor_id)
        for pet in tutor.pets:
            db.session.delete(pet)
        db.session.delete(tutor)
        db.session.commit()
        return {"message": "delete"}, 200

    
class PetResource(Resource):
    
    def get(self, pet_id=None):
        if pet_id is None:
            pets = Pet.query.all()
            return PetSchema(many=True).dump(pets), 200

        pet = Pet.query.get(pet_id)
        return PetSchema().dump(pet), 200
        
        
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('nome_pet', type=str, required=True)
        parse.add_argument('tutor_id', type=int, required=True)
        args = parse.parse_args()
        
        tutor = Tutor.query.get(args['tutor_id'])
        if tutor is None:
            return {"message": "Tutor not found"}, 404
        
        novo_pet = Pet(nome=args['nome_pet'], tutor_id=args['tutor_id'])
        db.session.add(novo_pet)
        db.session.commit()
        return PetSchema().dump(novo_pet), 201

    
    def put(self, pet_id=None):
        parse = reqparse.RequestParser()
        parse.add_argument('nome_pet', type=str, required=True)
        parse.add_argument('tutor_id', type=int, required=True)
        args = parse.parse_args()
        pet = Pet.query.get(pet_id)
        pet.nome = args['nome_pet']
        pet.tutor_id = args['tutor_id']
        db.session.commit()
        return PetSchema().dump(pet), 200
    
    def delete(self, pet_id=None):
        pet = Pet.query.get(pet_id)
        db.session.delete(pet)
        db.session.commit()
        return {"message": "delete"}, 200