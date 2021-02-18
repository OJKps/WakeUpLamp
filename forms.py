from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField, FloatField, SelectField
from wtforms.widgets import html_params, HTMLString
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms.fields.html5 import TimeField, IntegerRangeField

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

# from https://gist.github.com/doobeh/239b1e4586c7425e5114
class ButtonWidget(object):
    """
    Renders a multi-line text area.
    `rows` and `cols` ought to be passed as keyword args when rendering.
    """
    input_type = 'submit'

    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id) # choice_a ....
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        # add class="btn btn-primary btn-lg" for CSS
        html_return = HTMLString('<button class="btn btn-primary btn-lg" {params}>{label}</button>'.format(
            params=self.html_params(name=field.name, **kwargs),
            label=field.label.text)
        )
        # html_return example: <button class="btn btn-primary btn-lg" id="choice_b" name="choice_b" type="submit" value="Light OFF">Light OFF</button>
        return html_return

class ButtonField(StringField):
    widget = ButtonWidget()

class LightForm(FlaskForm):
    choice_a = ButtonField('Light ON')
    choice_b = ButtonField('Light OFF')
    choice_c = ButtonField('Dimm DOWN')
    choice_d = ButtonField('Dimm UP')

class SettingsFormAct(FlaskForm):
    choice_a = ButtonField('Reset lamp')
    choice_b = ButtonField('IR alarm')

class SettingsFormDeact(FlaskForm):
    choice_a = ButtonField('Reset lamp')
    choice_b = ButtonField('Stop IR alarm')

class AlarmClockForm(FlaskForm):
    time = DateTimeField('wake up time', format='%Y-%m-%d %H:%M:%S', validators=[InputRequired()])

class AlarmClockDeleteForm(FlaskForm):
    delete_button = ButtonField('Delete current alarm')

class AlarmClockFormHTML5(FlaskForm):
    time = TimeField('wake up time', format='%H:%M', validators=[InputRequired()])

class BackPainFormHTML5(FlaskForm):
    back_pain = IntegerRangeField('back pain', validators=[InputRequired()])

class WorkModeFormHTML5(FlaskForm):
    time = TimeField('time till when to work', format='%H:%M', validators=[InputRequired()])

class WorkModeDeleteForm(FlaskForm):
    end_work_mode_button = ButtonField('Stop work mode', validators=[InputRequired()])

def positive_check(form, field):
    print("Here Val")
    if field.data > 0.0:
        raise ValidationError('Amount must be positive')


class MoneyLogForm(FlaskForm):
    amount = FloatField('Amount in €.Cent', validators=[InputRequired()])
    def positive_check(form, field):
        print("Here Val")
        if field.data > 0.0:
            raise ValidationError('Amount must be positive')
    reason = SelectField(u'Choose Category', choices=[('Einkauf', 'Einkauf'), ('Freizeit', 'Freizeit'), ('Fahrtkosten', 'Fahrtkosten'), ('Miete', 'Miete'), ('Nebenkosten', 'Nebenkosten')], validators=[InputRequired()])
