from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from market.forms import RegisterForm,  LoginForm, PurchaseItemForm, SellItemForm
from market.models import Item, User
from market import db
from flask_login import login_user, logout_user, login_required, current_user # this can idedntify user logged in user or not
@app.route("/")
@app.route('/home')
def Home_Page():
    return render_template('home.html')


@app.route('/market',methods=['GET','POST'])
@login_required
def Market_Page():
    purchase_form=PurchaseItemForm()
    selling_form=SellItemForm()
    if request.method == 'POST':
        purchased_item= request.form.get('purchased_item')
        p_item_object= Item.query.filter_by(name=purchased_item).first()

        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You have Purchased {p_item_object.name} for {p_item_object.price}$", category ='success')
            else:
                flash(f"Unfortunately You do not have money to purchase {p_item_object.name}", category='danger')
        sold_item= request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You Sold {s_item_object.name} back to market ! ", category ='success')
            else:
                flash(f"Something went wrong with selling  {s_item_object.name}", category='danger')
        return redirect(url_for('Market_Page'))
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items,selling_form=selling_form)
#     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
#     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
#     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
# ]
    

@app.route('/register',methods=['POST','GET'])

def Register_Page():
    form= RegisterForm()
    if form.validate_on_submit(): # this check clicks the submit button
        user_to_create= User(username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data);
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account Created Successfully! You are now logged in as {user_to_create.username}",category='success')        
        return redirect(url_for('Market_Page'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a new user : {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])

def Login_Page():
    form= LoginForm()
    if form.validate_on_submit():
        attempted_user= User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Login successful! You are logged as: {attempted_user.username}',category='success')
            return redirect(url_for('Market_Page'))
        else:
            flash('Login failed! Username or password not match! Please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def Logout_Page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('Home_Page'))