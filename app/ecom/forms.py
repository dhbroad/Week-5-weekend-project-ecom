from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    caption = StringField('Caption', validators=[])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField()

class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    caption = StringField('Caption', validators=[])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField()
