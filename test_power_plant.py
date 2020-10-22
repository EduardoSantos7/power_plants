import unittest
import os
import json

from app import create_app, db


class PowerPlantTestCase(unittest.TestCase):
    """This class represents the power plant test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        print("ENTTREEE")
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.number_power_plants = [i for i in range(1, 100)]
        self.test_state = "CA"

    def test_api_can_get_n_power_plants(self):
        """Test API can get N power plants (GET request)."""
        for n in self.number_power_plants:
            response = self.client().get(f'/power_plants/', query_string={'number_plants': n})
            power_plants = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(power_plants), n)

    def test_api_can_get_n_power_plants_from_state(self):
        """Test API can get N power plants of a given state (GET request)."""
        for n in self.number_power_plants:
            response = self.client().get(
                f'/power_plants/', query_string={
                    'number_plants': n,
                    'state_abbreviation': self.test_state
                })
            self.assertEqual(response.status_code, 200)
            power_plants = json.loads(response.data)
            self.assertEqual(len(power_plants), n)

            for power_plant in power_plants:
                self.assertEqual(self.test_state, power_plant.get('state_abbreviation'))

    def test_api_can_get_all_power_plants_from_state(self):
        """Test API can get all the power plants of a given state (GET request)."""
        for n in self.number_power_plants:
            response = self.client().get(
                f'/power_plants/', query_string={
                    'state_abbreviation': self.test_state
                })
            power_plants = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(1613, len(power_plants))

            for power_plant in power_plants:
                self.assertEqual(self.test_state, power_plant.get('state_abbreviation'))

    def test_api_can_get_all_plants(self):
        """Test API can get all the power plants (GET request)."""
        for n in self.number_power_plants:
            response = self.client().get(f'/power_plants/')
            power_plants = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(10964, len(power_plants))

    def test_api_can_get_state_data(self):
        """Test API can get the state data of a given state (GET request)."""
        for n in self.number_power_plants:
            response = self.client().get(
                f'/states/', query_string={
                    'state_abbreviation': self.test_state
                })
            states = json.loads(response.data)
            self.assertEqual(200, response.status_code)
            self.assertEqual(len(states), 1)
            self.assertEqual(self.test_state, states[0].get('state_abbreviation'))
            self.assertEqual(195_212_860, states[0].get('annual_net_generation'))

    def test_api_can_get_all_states_data(self):
        """Test API can get all the states (GET request)."""
        for n in self.number_power_plants:
            response = self.client().get(f'/states/')
            states = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(51, len(states))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()



if __name__ == "__main__":
    unittest.main()
