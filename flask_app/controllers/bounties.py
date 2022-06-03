from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.bounty import Bounty

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/bounty/new')
def new_bounty():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("new_bounty.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/bounty/create',methods=['POST'])
def create_bounty():
    if not Bounty.add_bounty(request.form):
        return redirect('/bounty/new')
    print(request.form)
    # bounty_data = {
    #     'id': session['user_id'],
    #     "title": request.form['title'],
    #     "description": request.form['description'],
    #     'price': request.form['price']
    # }
    Bounty.save(request.form)
    return redirect('/bounties')

# TODO READ ALL
@app.route('/bounties')
def bounties():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("bounties.html",bounties=Bounty.get_all_with_users())

# TODO READ ONE
@app.route('/bounty/show/<int:id>')
def show_bounties(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id":id
    }
    return render_template("show_bounty.html",bounty=Bounty.get_one_with_user(data))

# ! ///// UPDATE /////
# TODO UPDATE REQUIRES TWO ROUTES
# TODO ONE TO SHOW THE FORM
@app.route('/bounty/edit/<int:id>')
def edit_bounty(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id":id
    }
    return render_template("edit_bounty.html",bounty=Bounty.get_one(data))

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/bounty/update',methods=['POST'])
def update_bounty():
    print(request.form)
    Bounty.update(request.form)
    return redirect('/bounties')

# ! SEARCH
@app.route('/search')
def searching():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("search.html")

@app.route('/searched', methods=["POST"])
def searched():
    print(bool(request.form["searched"]))
    if request.form['searched']:
        formatted = f'{request.form["searched"]}%%'
    else:
        formatted = ""
    search = {'title': formatted}
    results = Bounty.search_form(search)
    session['data'] = results
    print(results)
    return redirect('/search')

# ! ///// DELETE //////
@app.route('/bounty/destroy/<int:id>')
def destroy_bounty(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Bounty.destroy(data)
    return redirect('/bounties')