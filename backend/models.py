from flask_sqlalchemy import SQLAlchemy

# Create the database instance
db = SQLAlchemy()

# Define the database model for scenarios
class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scenario_name = db.Column(db.String(255), nullable=False)
    monthly_invoice_volume = db.Column(db.Integer)
    num_ap_staff = db.Column(db.Integer)
    avg_hours_per_invoice = db.Column(db.Float)
    hourly_wage = db.Column(db.Float)
    error_rate_manual = db.Column(db.Float)
    error_cost = db.Column(db.Float)
    time_horizon_months = db.Column(db.Integer)
    one_time_implementation_cost = db.Column(db.Float)

    def to_dict(self):
        """Converts the model instance to a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}