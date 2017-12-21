
from flask import Flask, render_template, url_for, request, redirect, make_response 
from database.dataconnector import *
import json
import uuid
import cgi
import requests
import sys

from datetime import *

app = Flask(__name__)

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('login.html'), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return render_template('login.html'), 500

@app.route('/debug/<file>')
def hello_world(file):
    return render_template(file+'.html')

@app.route('/', methods=['GET', 'POST'])
def welcome():
    print (sys.version)
    print("base")
    show_List = get_Recipe()
    return render_template('recipe.html', shows=show_List)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        account = request.json
        toShow = login_to_db(account)
        print(toShow)
        if toShow[0] == 0:  
            resp = make_response(render_template('login.html'))
            resp.set_cookie('userID',toShow[2][1])
        return resp


@app.route('/logout', methods=['GET', 'POST'])
def logout():
            show_List = get_Recipe()
            resp = make_response(render_template('recipe.html', shows=show_List))
            resp.set_cookie('userID',  '', expires=0)
            return resp


@app.route('/game', methods=['GET', 'POST'])
def game():
    
    show_List = get_Recipe()
    return render_template('game.html')

@app.route('/recipe', methods=['GET', 'POST'])
def generate_recipe():
    if request.method == 'GET':
        term = request.args.get('searchvalue')
        shows_list = get_Recipe_By_Name(term)
        name = request.cookies.get('userID')
        return render_template('recipe.html', shows=shows_list)
    elif request.method == 'POST':
        term = request.json
        shows_list = get_Recipe_By_Name(term)
        return render_template('add_recipe.html')

@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'GET':
        return render_template('add_account.html')
    elif request.method == 'POST':
        new_account = request.json
        toShow = add_account_to_db(new_account)
        return render_template('add_account.html')

@app.route('/add_favorite', methods=['GET', 'POST'])
def add_favorite():
    if request.method == 'POST':
        shows_list = get_Recipe()
        if 'userID' in request.cookies:
            name = request.cookies.get('userID')
            new_favorite = request.json
            print(new_favorite)
            return render_template('recipe.html',shows=shows_list)
        else:
            return render_template('recipe.html',shows=shows_list)
        
        
        



@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'GET':
        return render_template('add_recipe.html')
    elif request.method == 'POST':
        new_show = request.json
        new_ingredients={}
        for ingredient_type, ingredient in new_show['prices'].items():
            new_ingredients[ingredient_type] = ingredient
        add_recipe_to_db(new_show,new_ingredients)
        return render_template('add_recipe.html')

@app.route('/edit_recipe', methods=['GET', 'POST'])
def edit_recipe():
    if request.method == 'GET':
        shows_list = get_Recipe_By_Name("")
        print(shows_list)
        return render_template('edit_recipe.html',shows=shows_list)
    elif request.method == 'POST':
        show_id = int(request.data)
        requested_show = get_recipe_by_id(show_id)
        return json.dumps(requested_show)

@app.route('/update_recipe', methods=['POST'])
def edit_recipe_db_entry():
    if request.method == 'POST':
        response = request.json
        updated_show={}
        
       
        updated_show['id'] = response['id']
        updated_show['name'] = response['name']
        updated_show['prep'] = response['prep']
        updated_show['description'] = response['description']
        updated_show['instruction'] = response['instruction']
        new_ingredients={}
        for ingredient_type, ingredient in response['ingredients'].items():
            new_ingredients[ingredient_type] = ingredient
        print(new_ingredients)
        edit_recipe_in_db(updated_show,new_ingredients)
        shows_list = get_Recipe(False)
        return render_template('edit_recipe.html',shows=shows_list)
   
@app.route('/delete_recipe',methods=['POST'])
def delete_recipe():
    if request.method =='POST':
        response = request.json
        updated_show={}
        updated_show['id'] = response['recipe_id']
        delete_recipe_from_db(updated_show)
        shows_list = get_Recipe()
        return render_template('recipe.html',shows=shows_list)


if __name__ == "__main__":
   app.run()
