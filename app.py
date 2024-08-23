
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from forms import LoginForm, RegistrationForm, ParcelForm, UpdateParcelForm
from threading import Thread
import time
import logging

# Configuration
class Config:
    SECRET_KEY = 'f9dc74e302dd410511b72d8e25350cbb56ce1a84026798ee'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:flaskpassword@localhost/parcel_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


 
app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'   

 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Parcel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parcel_name = db.Column(db.String(150), nullable=False)
    sender = db.Column(db.String(150), nullable=False)
    recipient = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    estimated_date = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(150), nullable=True)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@socketio.on('connect', namespace='/admin')
def admin_connect():
    print('Admin connected')

@socketio.on('connect', namespace='/user')
def user_connect():
    print('User connected')

@socketio.on('parcel_update', namespace='/user')
def handle_user_update(data):
    socketio.emit('parcel_update', data, namespace='/user')

 
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/show_parcels')
@login_required
def show_parcels():
    # Query all parcels from the database
    parcels = Parcel.query.all()
    # Render a template to display the parcels
    return render_template('show_parcels.html', parcels=parcels)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            if user.is_admin == 1:   
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        else:
            flash('Login unsuccessful. Check email and/or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():

    parcels = Parcel.query.all()
    form = ParcelForm()
    update_form = UpdateParcelForm()  

    if form.validate_on_submit():
        parcel = Parcel(
            parcel_name = form.parcel_name.data,
            sender=form.sender.data,
            recipient=form.recipient.data,
            status=form.status.data,   
            estimated_date=form.estimated_date.data,
            location=form.location.data
        )
        db.session.add(parcel)
        db.session.commit()
        socketio.emit('parcel_update', {
            'parcel_name': parcel.parcel_name,
            'sender': parcel.sender,
            'recipient': parcel.recipient,
            'status': parcel.status,
            'estimated_date': parcel.estimated_date,
            'location': parcel.location,
        }, namespace='/admin')
        flash('Parcel added successfully', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin.html', form=form, parcels=parcels, update_form=update_form)



@app.route('/get_parcel_details', methods=['GET'])
@login_required
def get_parcel_details():
    parcel_id = request.args.get('parcel_id')
    if parcel_id and parcel_id.isdigit():
        parcel_id = int(parcel_id)
        parcel = Parcel.query.get(parcel_id)
        if parcel:
            return jsonify({
                'id': parcel.id,
                'parcel_name': parcel.parcel_name,
                'sender': parcel.sender,
                'recipient': parcel.recipient,
                'status': parcel.status,
                'estimated_date': parcel.estimated_date,
                'location': parcel.location
            })
        else:
            return jsonify({'error': 'Parcel not found'}), 404
    else:
        return jsonify({'error': 'Invalid parcel ID'}), 400

     
@app.route('/update_parcel', methods=['POST'])
@login_required
def update_parcel():
    parcel_id = request.form.get('parcel_id')
    status = request.form.get('status')
    estimated_date = request.form.get('estimated_date')
    location = request.form.get('location')

    parcel = Parcel.query.get(parcel_id)
    if parcel:
        parcel.status = status
        parcel.estimated_date = estimated_date
        parcel.location = location
        db.session.commit()
        socketio.emit('parcel_updated', {'id': parcel_id, 'status': status, 'estimated_date': estimated_date, 'location': location}, namespace='/admin')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Parcel not found', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    parcels = Parcel.query.all()
    update_form = UpdateParcelForm()  # Create an instance of the form
    return render_template('user.html', parcels=parcels, update_form=update_form)

@app.route('/add_parcel', methods=['POST'])
@login_required
def add_parcel():
    if current_user.is_admin == 1:
        return redirect(url_for('admin_dashboard'))

    sender = request.form.get('sender')
    recipient = request.form.get('recipient')
    if sender and recipient:
        parcel = Parcel(sender=sender, recipient=recipient, status='Received')
        db.session.add(parcel)
        db.session.commit()
        socketio.emit('parcel_update', {'sender': parcel.sender, 'recipient': parcel.recipient, 'status': parcel.status}, namespace='/user')
        flash('Parcel added successfully', 'success')
    else:
        flash('Failed to add parcel. Please ensure all fields are filled out.', 'danger')

    return redirect(url_for('user_dashboard'))

@app.route('/delete_parcel', methods=['POST'])
@login_required
def delete_parcel():
    print("Delete request received")
    parcel_id = request.form.get('parcel_id')

    if not parcel_id:
        return jsonify({'success': False, 'message': 'Parcel ID is required'}), 400

    # Check if the user is admin
    # if current_user.is_admin != 1:
    #     return jsonify({'success': False, 'message': 'Unauthorized access'}), 403

    # Fetch the parcel
    parcel = Parcel.query.get(parcel_id)

    if not parcel:
        return jsonify({'success': False, 'message': 'Parcel not found'}), 404

    try:
        db.session.delete(parcel)
        db.session.commit()

        # Emit the parcel update to the admin namespace
        socketio.emit('parcel_update', {'id': parcel_id, 'action': 'delete'}, namespace='/admin')
        
        return jsonify({'success': True, 'message': 'Parcel deleted successfully'})
    except Exception as e:
        # Rollback if there is an error
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Error deleting parcel', 'error': str(e)}), 500



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

def bulk_parcel_processing():
    while True:
        
        time.sleep(10)   
        parcels = Parcel.query.filter_by(status='Received').all()
        for parcel in parcels:
            parcel.status = 'Pending'
            db.session.commit()
            socketio.emit('parcel_update', {'sender': parcel.sender, 'recipient': parcel.recipient, 'status': parcel.status}, namespace='/admin')
        time.sleep(60)   
# Start a background thread for bulk processing
thread = Thread(target=bulk_parcel_processing)
thread.daemon = True
thread.start()


if __name__ == '__main__':
    socketio.run(app, debug=True)