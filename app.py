from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# application init 
#create the SQLAlchemy instance
db = SQLAlchemy()
def create_app():
    #create flask aplication 
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY']='password'
    # initialize sqlalchemy with flask application
    db.init_app(app)

    with app.app_context():
        #create table product
        db.create_all()
    
    return app
app = create_app()
#login manager 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# database tables
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(88), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.title}>'

# routes
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)
    


# products routes
@app.route('/create_product', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = user.query.filter_by(username-username).first()
        
        #check if user exist and password is correct 
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect (url_for('home'))
        return'inavalid user name or password'
    return render_template('login.html')



@app.route('/products/delete/<int:id>', methods=['GET','POST'])
def create_product():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        product = Product(title=title, description=description, price=price)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_product.html')
def delete_product(id):
    product = Product.query.get(id)
    if product: 
        db.session.delete(product)
        db.session.commit() 
    return redirect(url_for('home'))


# run application
if __name__ == '__main__':
    app.run(debug=True)





    
