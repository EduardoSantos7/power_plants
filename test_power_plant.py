import unittest
import os
import json

from sqlalchemy.orm import query
from app import create_app, db
from app.models import PowerPlant


class PowerPlantTestCase(unittest.TestCase):
    """This class represents the power plant test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.power_plant_query = {'n': 2, 'state_abbreviation': 'AK'}
        self.number_power_plants = [i for i in range(1, 100)]

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_api_can_get_n_power_plants(self):
        """Test API can get a power plants (GET request)."""
        for n in self.number_power_plants:
            response = self.client().get(f'/power_plants/', query_string={'number_plants': n})
            power_plants = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(power_plants), n)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()