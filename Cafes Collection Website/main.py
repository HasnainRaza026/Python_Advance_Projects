import pandas as pd
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, URL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for CSRF protection


class Add_Cafes(FlaskForm):
    choices_coffee = [
        ('☕', '☕'),
        ('☕☕', '☕☕'),
        ('☕☕☕', '☕☕☕'),
        ('☕☕☕☕', '☕☕☕☕'),
        ('☕☕☕☕☕', '☕☕☕☕☕')
    ]
    choices_wifi = [
        ('✘', '✘'),
        ('💪', '💪'),
        ('💪💪', '💪💪'),
        ('💪💪💪', '💪💪💪'),
        ('💪💪💪💪', '💪💪💪💪'),
        ('💪💪💪💪💪', '💪💪💪💪💪')
    ]
    choices_power = [
        ('✘', '✘'),
        ('🔌', '🔌'),
        ('🔌🔌', '🔌🔌'),
        ('🔌🔌🔌', '🔌🔌🔌'),
        ('🔌🔌🔌🔌', '🔌🔌🔌🔌'),
        ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')
    ]
    name = StringField(label='Cafe Name', validators=[DataRequired()])
    location = StringField(label='Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL(message=('Invalid URL!'))])
    open_time = StringField(label='Opening Time eg. 8:00 AM', validators=[DataRequired()])
    close_time = StringField(label='Closing Time eg. 5:30 PM', validators=[DataRequired()])
    coffee = SelectField(label='Coffee Rating', choices=choices_coffee, validators=[DataRequired()])
    wifi = SelectField(label='WIFI Strength Rating', choices=choices_wifi , validators=[DataRequired()])
    power = SelectField(label='Power Socket Available', choices=choices_power , validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/cafes")
def cafes():
    df = pd.read_csv('./cafe-data.csv')
    global headers
    headers = df.columns.tolist()
    values = []
    for index in range (0, df.shape[0]):
        subset = df.iloc[index].tolist()
        values.append(subset)
    return render_template('cafes.html', columns=headers, rows=values)

@app.route('/cafes/add', methods=['GET', 'POST'])
def add_cafe():
    form = Add_Cafes()
    if form.validate_on_submit(): # form is submited successfully (POST request) (returns true)\
        save_to_csv(form)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

def save_to_csv(form):
    data_form = [form.name.data, form.location.data, form.open_time.data, form.close_time.data, form.coffee.data, form.wifi.data, form.power.data]
    new_row = {}
    for header, data in zip(headers, data_form):
        new_row[header] = data

    # Create a DataFrame for the new row
    new_row_df = pd.DataFrame([new_row])

    # Append the new row to the CSV file
    new_row_df.to_csv('./cafe-data.csv', mode='a', header=False, index=False)


if __name__ == '__main__':
    app.run(debug=True)