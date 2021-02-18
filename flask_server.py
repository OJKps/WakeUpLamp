from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegisterForm, LightForm, AlarmClockDeleteForm, AlarmClockForm, AlarmClockFormHTML5, BackPainFormHTML5, WorkModeFormHTML5, WorkModeDeleteForm, MoneyLogForm, SettingsFormAct, SettingsFormDeact
from alarm_clock import AlarmClock, strfdelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import time
from datetime import datetime, date, timedelta
from bme_sensor import get_bme_reads
from lamp import Lamp
from ir_sensor import IR_Sensor
from display import Display
from waitress import serve

import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/Documents/WakeUpLight/wakeup/Code/database.db' # change //// in ///
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

lamp_obj = Lamp()
alarm_clock_obj = AlarmClock(lamp_obj)
display_obj = Display()
ir_alarm_obj = IR_Sensor()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))
    # save for each user the work mode
    work_mode_active = db.Column(db.Boolean, default=False)
    work_start = db.Column(db.DateTime)
    work_end = db.Column(db.DateTime)

class BackPainDB(db.Model):
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    id = db.Column(db.Integer, primary_key=True)
    back_pain_level = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(30))

class MoneyLogDB(db.Model):
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    id = db.Column(db.Integer, primary_key=True)
    money_log_input = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(30))
    username = db.Column(db.String(30))

class WorkLogDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_start = db.Column(db.DateTime, nullable=False)
    work_end = db.Column(db.DateTime, nullable=False)
    work_delta_hours = db.Column(db.Integer, nullable=False)
    work_delta_mins = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(30))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    # display time and timer
    display_obj.display_clock(alarm_clock_obj.is_set, alarm_clock_obj.time_set_to)
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = LightForm()
    if lamp_obj.lamp_off:
        lamp_value = "Lamp_OFF.png"
    else:
        lamp_value = "Lamp_ON.png"
    if form.is_submitted():
        print("BUTTON A", form.choice_a.data)
        print("BUTTON B", form.choice_b.data)
        print("BUTTON C", form.choice_c.data)
        print("BUTTON D", form.choice_d.data)
        # data = get_bme_reads()
        # print("DATA BME sensor", data)
        # display time and timer
        display_obj.display_clock(alarm_clock_obj.is_set, alarm_clock_obj.time_set_to)
        #return redirect(url_for('dashboard'))
        if form.choice_a.data:
            #time.sleep(2)
            print("TURN LAMP ON")
            lamp_obj.turn_on()
            lamp_value = "Lamp_ON.png"
            #return render_template('dashboard.html', name=current_user.username, lamp=lamp_value, time_stamp=str(time.time()), time_bme=str(data.timestamp), temp_bme=str(data.temperature)[:-12], pres_bme=str(data.pressure)[:-12], hum_bme=str(data.humidity)[:-12], form=form)
        if form.choice_b.data:
            #time.sleep(2)
            print("TURN LAMP OFF")
            lamp_obj.turn_off_fast()
            lamp_value = "Lamp_OFF.png"
            #return render_template('dashboard.html', name=current_user.username, lamp=lamp_value, time_stamp=str(time.time()), time_bme=str(data.timestamp), temp_bme=str(data.temperature)[:-12], pres_bme=str(data.pressure)[:-12], hum_bme=str(data.humidity)[:-12], form=form)            
        if form.choice_c.data:
            #time.sleep(2)
            print("TURN DIMM DOWN")
            lamp_obj.dimm_down()
            lamp_value = "Lamp_Dimm_DOWN.png"
            #return render_template('dashboard.html', name=current_user.username, lamp=lamp_value, time_stamp=str(time.time()), time_bme=str(data.timestamp), temp_bme=str(data.temperature)[:-12], pres_bme=str(data.pressure)[:-12], hum_bme=str(data.humidity)[:-12], form=form)            
        if form.choice_d.data:
            #time.sleep(2)
            print("TURN DIMM UP")
            lamp_obj.dimm_up()
            lamp_value = "Lamp_Dimm_UP.png"
            #return render_template('dashboard.html', name=current_user.username, lamp=lamp_value, time_stamp=str(time.time()), time_bme=str(data.timestamp), temp_bme=str(data.temperature)[:-12], pres_bme=str(data.pressure)[:-12], hum_bme=str(data.humidity)[:-12], form=form)
        
        #else:
            #return form.choice_b.data

    form.choice_a.data = 'Light ON'
    form.choice_b.data = 'Light OFF'
    form.choice_c.data = 'Dimm light DOWN'
    form.choice_d.data = 'Dimm light UP'
    
    data = get_bme_reads()
    print("DATA BME sensor", data)
    print(str(data.temperature)[:-12])
    
    # display time and timer
    display_obj.display_clock(alarm_clock_obj.is_set, alarm_clock_obj.time_set_to)
    
    return render_template('dashboard.html', name=current_user.username, lamp=lamp_value, lamp_step=lamp_obj.lamp_step, time_stamp=str(time.time()), time_bme=str(data.timestamp), temp_bme=str(data.temperature)[:-12], pres_bme=str(data.pressure)[:-12], hum_bme=str(data.humidity)[:-12], form=form)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if ir_alarm_obj.activate:
        form = SettingsFormDeact()
    else:
        form = SettingsFormAct()
    if form.is_submitted():
        if form.choice_a.data:
            print("Reset Lamp")
            lamp_obj.reset()
        if form.choice_b.data:
            if ir_alarm_obj.activate:
                print("Stop IR alarm")
                ir_alarm_obj.stop_ir_sensor()
                #form = SettingsFormDeact()
            else:
                print("Set IR alarm")
                ir_alarm_obj.act_ir_sensor()
                #form = SettingsFormAct()
        
    form.choice_a.data = 'Reset Lamp'
    form.choice_b.data = 'IR alarm'
   
    return render_template('settings.html', lamp_step=lamp_obj.lamp_step, ir_state=ir_alarm_obj.activate, form=form)

def create_backpain_plot(database):
    query = db.session.query(BackPainDB.username.distinct().label("username"))
    # print(query)
    user_str_list = [row.username for row in query.all()]
    # user_in_db = database.UniqueConstraint("username") #database.query.order_by(database.username).all()
    # print(user_str_list)
    keep_user_plot = []
    date_list = []
    bpl_list = []
    for u_no, user in enumerate(user_str_list):
        print("User", user)
        # get every unique user
        db_list = database.query.filter_by(username=user).order_by(database.date).all()
        # do not show too old data
        if ((datetime.now() - db_list[-1].date).total_seconds() / (60*60*24)) > 14:
            # older than 7 days
            continue
        else:
            keep_user_plot.append(user)
        # print("Here", db_list)
        if len(db_list) > 100:
            # only keep the last 100 per user
            # delete everything older
            for del_col in range(0, (len(db_list) - 100)):
                db.session.delete(db_list[del_col])
            db_list = db_list[-(len(db_list) - 99):]
        user_date_list = []
        user_bpl_list = []
        for col in db_list:
            # get the data from the DB
            user_date_list.append(col.date)
            user_bpl_list.append(col.back_pain_level)
        date_list.append(user_date_list)
        bpl_list.append(user_bpl_list)

    print(date_list)
    print(bpl_list)
    #sns.set_style("darkgrid")

    for line_data in zip(date_list, bpl_list, keep_user_plot):
        print(line_data)
        plt.plot(line_data[0], line_data[1], label=line_data[2])

    plt.legend()
    plt.xticks(rotation=30)
    plt.ylim((0, 10))
    plt.title("Back pain plot over user")
    name_plot = "back_pain_plot.png"
    rel_path = "./static/images/back_pain_plot.png"
    plt.savefig(rel_path)
    plt.close()

    return name_plot

def create_moneylog_plot(database, cur_user_name):
    # all distinct usernames
    query = db.session.query(MoneyLogDB.username.distinct().label("username"))
    user_str_list = [row.username for row in query.all()]
    #reason_user_str_list = []
    # all rows for each users
    #query = db.session.query(MoneyLogDB.username.label("username"))
    #for user in user_str_list:
    #    reason_user_str_list.append([row.reason for row in query.all()])

    query = db.session.query(MoneyLogDB.reason.distinct().label("reason"))
    reason_str_list = [row.reason for row in query.all()]

    print("User", user_str_list)
    print("Reason", reason_str_list)

    # user_in_db = database.UniqueConstraint("username") #database.query.order_by(database.username).all()
    # print(user_str_list)
    user_amount_list = []
    user_reason_list = []
    user_reason_str_list = []
    user_no = 0
    for u_no, user in enumerate(user_str_list):
        print("User", user)
        if user == cur_user_name:
            user_no = u_no

        reasons_str_list = []
        db_list = database.query.filter_by(username=user).all()
        for col in db_list:
            if col.reason not in reasons_str_list:
                # print("Here", col.reason)
                reasons_str_list.append(col.reason)
        print("1", reasons_str_list)
        user_reason_str_list.append(reasons_str_list)

        u_amount = 0
        reasons_list = []
        for reason in user_reason_str_list[u_no]:
            print("Reason", reason)
            # get every unique user with reason
            db_list = database.query.filter_by(username=user, reason=reason).all()

            r_amount = 0
            for col in db_list:
                # get the data from the DB
                u_amount += col.money_log_input
                r_amount += col.money_log_input
            reasons_list.append(r_amount) # one reason summed up for a user

        user_amount_list.append(u_amount) # user total spending amount
        user_reason_list.append(reasons_list) # each reason summed up for users


    # pie chart with users reason expenses
    # pie chart of users amount spend

    fig, ax = plt.subplots(1, 3, sharey=True, figsize=(15,5))

    print(user_amount_list)
    print(user_reason_list[user_no])

    size = 0.3
    cmap = plt.get_cmap("tab20c")
    outer_colors = cmap(np.arange(len(user_amount_list)) * ((sum([len(listElem) for listElem in user_reason_list]))))
    inner_colors = cmap(np.arange((sum([len(listElem) for listElem in user_reason_list]))))
    ax[0].pie(user_amount_list, labels=user_str_list, radius=1, colors=outer_colors, wedgeprops=dict(width=size, edgecolor='w'))
    ax[0].pie([item for sublist in user_reason_list for item in sublist], labels=[item for sublist in user_reason_str_list for item in sublist], radius=1 - size, colors=inner_colors, wedgeprops=dict(width=size, edgecolor='w'), textprops=dict(color="r"))
    #ax[0].pie(user_amount_list, labels=user_str_list, autopct="%1.1f%%")
    ax[1].pie(user_amount_list, labels=user_str_list, colors=outer_colors, autopct="%1.1f%%", wedgeprops=dict(edgecolor='w'))
    ax[2].pie(user_reason_list[user_no], labels=user_reason_str_list[user_no], autopct="%1.1f%%", wedgeprops=dict(edgecolor='w'))

    #fig.legend()
    ax[0].set_title('Overall')
    ax[1].set_title('Overview of users')
    ax[2].set_title(cur_user_name)

    #plt.title("Money log plot")
    name_plot = "money_log_plot.png"
    rel_path = "./static/images/money_log_plot.png"
    fig.savefig(rel_path)
    plt.close()

    return name_plot

@app.route('/back_pain', methods=['GET', 'POST'])
@login_required
def back_pain():
    form = BackPainFormHTML5()

    if form.validate_on_submit():
        print(form.back_pain.data)
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
        # return redirect(url_for('alarm_clock'))

        new_bpdb = BackPainDB(back_pain_level=form.back_pain.data, username=current_user.username)
        db.session.add(new_bpdb)
        db.session.commit()
        print(BackPainDB.query.all()[-1].back_pain_level)
        print(BackPainDB.query.all()[-1].date)
        name_plot = create_backpain_plot(BackPainDB)
        #display_obj.display_image("./static/images/" + name_plot)
        return render_template('back_pain.html', name=current_user.username, name_plot=name_plot, time_stamp=str(time.time()), form=form)
    form.back_pain.data = "use the slider"
    return render_template('back_pain.html', name=current_user.username, name_plot="back_pain_plot.png", time_stamp=str(time.time()), form=form)

@app.route('/alarm_clock', methods=['GET', 'POST'])
@login_required
def alarm_clock():
    if alarm_clock_obj.is_set:
        # alarm clock is set
        form = AlarmClockDeleteForm()
        if form.is_submitted():
            # delete alarm
            alarm_clock_obj.delete_alarm()
            print("alarm deleted")
            print(form.delete_button.data)
            return redirect(url_for('alarm_clock'))
        # display time and timer
        display_obj.display_clock(alarm_clock_obj.is_set, alarm_clock_obj.time_set_to)
        # show active alarm
        form.delete_button.data = True
        active_alarm_mess = "Alarm is active: " + str(alarm_clock_obj.time_to_alarm())
        alarm_time = "Alarm set to: " + str(alarm_clock_obj.time_set_to)
        return render_template('alarm_clock_set.html', alarm_mess=active_alarm_mess, alarm_time=alarm_time, form=form)
    else:
        # alarm clock is NOT set
        form = AlarmClockFormHTML5() #AlarmClockForm()
        if form.validate_on_submit():
            # time for alarm clock is submitted
            print(form.time.data)
            alarm_clock_obj.set_time(form.time.data)
            print(alarm_clock_obj.time_set_to)
            return redirect(url_for('alarm_clock'))
        # display time and timer
        display_obj.display_clock(alarm_clock_obj.is_set, alarm_clock_obj.time_set_to)
        # show alarm input window
        active_alarm_mess = "No alarm is active" # not needed alarm_clock is different to alarm_clock_set
        return render_template('alarm_clock.html', alarm_mess=active_alarm_mess, form=form)

@app.route('/work_mode', methods=['GET', 'POST'])
@login_required
def work_mode():
    if current_user.work_mode_active:
        # work mode active
        form = WorkModeDeleteForm()
        if form.is_submitted():
            u = User.query.filter_by(username=current_user.username).first()
            # delete work mode
            u.work_mode_active = False
            # time put in DB
            u.work_end = datetime.now()
            db.session.commit()
            u = User.query.filter_by(username=current_user.username).first() # needed???
            delta_work_time = abs((u.work_start - u.work_end).total_seconds())
            work_delta_hours, work_delta_mins = int(delta_work_time // (60 * 60)), int((delta_work_time % (60 * 60)) // 60)
            # place into WorkLogDB table
            new_wldb = WorkLogDB(work_start=u.work_start, work_end=u.work_end, work_delta_hours=work_delta_hours, work_delta_mins=work_delta_mins, username=current_user.username)
            db.session.add(new_wldb)
            db.session.commit()

            print("work mode deleted. Worked ", delta_work_time, "date", work_delta_hours, "hours", work_delta_mins, "mins")
            print(form.end_work_mode_button.data)
            return render_template('work_mode_finished.html', name=current_user.username)
        form.end_work_mode_button.data = True
        time_work_start = current_user.work_start
        str_time_worked = strfdelta((datetime.now() - time_work_start), ", you have worked %H hours and %M minutes")
        str_time_worked = current_user.username + str_time_worked
        time_work_end = current_user.work_end
        if (time_work_end - datetime.now()).total_seconds() < 0:
            # overtime
            str_time_left = strfdelta((datetime.now() - time_work_end), "%H hours and %M minutes over time")
        else:
            str_time_left = strfdelta((time_work_end - datetime.now()), "%H hours and %M minutes to go")
        str_time_work_end = "Work mode end is set to: " + (time_work_end).strftime("%H:%M")
        print("Worked mode active", str_time_worked, str_time_left, str_time_work_end)
        return render_template('work_mode_active.html', name=current_user.username, time_worked=str_time_worked, time_work_end=str_time_work_end, time_left=str_time_left, form=form)
    else:
        # work mode not active
        form = WorkModeFormHTML5()
        if form.validate_on_submit():
            # set work mode
            # set time to when to work
            print(form.time.data)

            work_time_end = datetime.combine(date.today(), form.time.data)
            if (work_time_end - datetime.now()).total_seconds() < 0:
                work_time_end = work_time_end + timedelta(days=1)

            u = User.query.filter_by(username=current_user.username).first()
            print("u", u)
            u.work_mode_active = True
            # time put in DB
            u.work_start = datetime.now()
            u.work_end = work_time_end
            db.session.commit()

            return redirect(url_for('work_mode'))
        # table
        return render_template('work_mode.html', name=current_user.username, col_work_mode_entry=WorkLogDB.query.all(), form=form)

@app.route('/money_log', methods=['GET', 'POST'])
@login_required
def money_log():
    form = MoneyLogForm()

    if form.is_submitted():
        # amount input
        print(form.amount.data)
        print(form.reason.data)
        # add to DB
        new_mldb = MoneyLogDB(money_log_input=form.amount.data, reason=form.reason.data, username=current_user.username)
        db.session.add(new_mldb)
        db.session.commit()
        # update table
        return redirect(url_for('money_log'))
    # plot
    try:
        name_plot = create_moneylog_plot(MoneyLogDB, current_user.username)
    except:
        name_plot = "money_log_plot.png"
        print("Plot could not be generated")
    # show table
    return render_template('money_log.html', name=current_user.username, name_plot=name_plot, col_work_mode_entry=MoneyLogDB.query.all(), time_stamp=str(time.time()), form=form)

@app.route('/garlic_experience')
@login_required
def garlic_experience():
    return render_template('garlic.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/test')
def test():
    return render_template("test.html")

if __name__ == '__main__':
    #app.run(debug=True, ssl_context='adhoc') # ssl_context='adhoc' for https https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    # app.run(debug=False, host= '0.0.0.0')
    serve(app, host= '0.0.0.0', port=5000)
