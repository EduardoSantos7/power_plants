import os

import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app import db


class PowerPlant(db.Model):
    """This class represents the power plant table."""

    __tablename__ = 'powerplant'

    facility_code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    state_abbreviation = db.Column(db.String(2))
    annual_net_generation = db.Column(db.Integer, index=True)

    def __init__(self, name, facility_code, state_abbreviation, annual_net_generation):
        """initialize with name."""
        self.name = name
        self.facility_code = facility_code
        self.state_abbreviation = state_abbreviation
        self.annual_net_generation = annual_net_generation

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_n_power_plants(number_plants):
        return PowerPlant.query.limit(number_plants).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def populate_table():
        first_power_plant = PowerPlant.query.first()

        # If the table is populated then return
        if first_power_plant:
            return

        df = pd.read_csv(
            'app/power_plants_data.csv', skiprows=[0], thousands=',',
            usecols=['PSTATABB', 'PNAME', 'ORISPL', 'PLNGENAN'])
        df['PLNGENAN'] = df['PLNGENAN'].fillna(0)

        for _, row in df.iterrows():
            power_plant = PowerPlant(row['PNAME'], row['ORISPL'], row['PSTATABB'], row['PLNGENAN'])
            power_plant.save()

    def __repr__(self):
        return f"<PowerPlant: {self.name} State: {self.state_abbreviation}>"
