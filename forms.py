from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired


leagues = ["PRO", "FORMER PRO", "NBA","FORMER NBA", "AMATEUR"]

class DunkerForm(FlaskForm):
    name = StringField("Enter Dunker Name", validators=[DataRequired(message="Must Enter A Name")], id="dunker_autocomplete", render_kw={"placeholder": "Search"})
    # league = RadioField("League/Level", choices=leagues)
    search = SubmitField("Search")
