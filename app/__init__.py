import sqlalchemy
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort


from instance.config import app_config
from app.schemas import UrlQuerySchema


# initialize sql-alchemy
db = SQLAlchemy()


def model_exists(model_class):
    engine = db.get_engine(bind=model_class.__bind_key__)
    return model_class.metadata.tables[model_class.__tablename__].exists(engine)


def create_app(config_name):
    from app.models.PowerPlant import PowerPlant
    from app.models.State import State
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        if not model_exists(PowerPlant):
            db.create_all(bind=PowerPlant.__bind_key__)
            PowerPlant.populate_table()
        if not model_exists(State):
            db.create_all(bind=State.__bind_key__)
            State.populate_table()

    @app.route('/power_plants/', methods=['GET'])
    def power_plants():
        schema = UrlQuerySchema()

        errors = schema.validate(request.args)

        if errors:
            abort(400, str(errors))

        args = request.args

        power_plants = PowerPlant.get_n_power_plants(
            number_plants=args.get('number_plants'),
            state_abbreviation=args.get('state_abbreviation', '').upper())

        results = []

        for power_plant in power_plants:
            obj = {
                'facility_code': power_plant.facility_code,
                'name': power_plant.name,
                'state_abbreviation': power_plant.state_abbreviation,
                'annual_net_generation': power_plant.annual_net_generation
            }
            results.append(obj)

        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/states/', methods=['GET'])
    def states():
        schema = UrlQuerySchema()

        errors = schema.validate(request.args)

        if errors:
            abort(400, str(errors))

        args = request.args

        states = State.get_state_production(
            state_abbreviation=args.get('state_abbreviation', '').upper())
        results = []

        for state in states:
            obj = {
                'state_abbreviation': state.state_abbreviation,
                'annual_net_generation': state.annual_net_generation
            }
            results.append(obj)

        response = jsonify(results)
        response.status_code = 200
        return response

    return app
