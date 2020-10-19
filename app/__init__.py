from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort


from instance.config import app_config
from app.schemas import UrlQuerySchema


# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import PowerPlant
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        PowerPlant.populate_table()

    @app.route('/power_plants/', methods=['GET'])
    def bucketlists():
        schema = UrlQuerySchema()

        errors = schema.validate(request.args)

        if errors:
            abort(400, str(errors))

        args = request.args

        power_plants = PowerPlant.get_n_power_plants(args.get('number_plants'))

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

    return app
