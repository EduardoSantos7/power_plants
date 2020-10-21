import os

import pandas as pd
from sqlalchemy import desc

from app import db


class State(db.Model):
    """This class represents the power plant table."""

    __tablename__ = 'states'
    __bind_key__ = 'states'

    state_abbreviation = db.Column(db.String(2), primary_key=True, index=True)
    annual_net_generation = db.Column(db.Integer)

    def __init__(self, state_abbreviation, annual_net_generation):
        self.state_abbreviation = state_abbreviation
        self.annual_net_generation = annual_net_generation

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_state_production(state_abbreviation=None):
        """If a state is provided then return a list with that state else return
        a list will the data of all the states.

        Args:
            state_abbreviation (String, optional): abbreviation of the state (ej. CA -> California).
                                                    Defaults to None.

        Returns:
            [List]: List of states.
        """
        if state_abbreviation:
            return [State.query.filter(State.state_abbreviation == state_abbreviation).first()]

        return State.query.order_by(
                desc(State.annual_net_generation)).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def populate_table():
        """If the table is empty then populate it.
        """

        first_state = State.query.first()

        # If the table is populated then return
        if first_state:
            return

        df = pd.read_csv(
            'app/states_data.csv', skiprows=[0], thousands=',',
            usecols=['PSTATABB', 'STNGENAN'])
        df['STNGENAN'] = df['STNGENAN'].fillna(0)

        for _, row in df.iterrows():
            power_plant = State(row['PSTATABB'], row['STNGENAN'])
            power_plant.save()

    def __repr__(self):
        return f"<State: {self.state_abbreviation}>"
