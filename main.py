
from flask import Flask, render_template, url_for, request, redirect
from database.dataconnector import *
import json
import uuid
import cgi
import requests
import sys

from datetime import *

app = Flask(__name__)

@app.route('/debug/<file>')
def hello_world(file):
    return render_template(file+'.html')

@app.route('/', methods=['GET', 'POST'])
def welcome():
    print (sys.version) 
    show_List = get_Recipe()
    return render_template('recipe.html', shows=show_List)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    show_List = get_Recipe()
    return render_template('game.html')

@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'GET':
        return render_template('add_account.html')
    elif request.method == 'POST':
        new_account = request.json
        add_account_to_db(new_account)
        return render_template('add_account.html')

@app.route('/recipe', methods=['GET', 'POST'])
def generate_recipe():
    if request.method == 'GET':
        term = request.args.get('searchvalue')
        shows_list = get_Recipe_By_Name(term)
        print(shows_list)
        return render_template('recipe.html', shows=shows_list)
    elif request.method == 'POST':
        term = request.json
        shows_list = get_Recipe_By_Name(term)
        return render_template('add_recipe.html')

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
