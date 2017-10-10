from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Time, Numeric
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('mysql+pymysql://root:root@localhost:3306/recipe')

Base = declarative_base()
Session = sessionmaker(bind=engine)

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    prep = Column(Integer)
    description = Column(String)
    instruction = Column(String)
    def __repr__(self):
        return "<Recipe(id='%s' name='%s', prep='%s')>" % (
            self.id, self.name, self.prep)

class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True)
    iname = Column(String)
    amount = Column(Integer)
    units = Column(String)
    recipe_id = Column(Integer, primary_key=True)
    def __repr__(self):
        return "<PriceType(id='%s', name = '%s',amount='%s',units='%s')>" % (self.id, self.name, self.amount, self.units)

#returns all recipes as a list
#List is formatted as follows:
#   [
#    recipe.id_show
#    recipe.title,
#    recipe.description, 
#    [recipe.ing_1, recipe.ing_amt_1],
#        ... ,
#    [recipe.ing_n, recipe.ing_amt_n]
#   ]

def get_Recipe(filter_results=True):
    session = Session()
    if filter_results:
        li = session.query(Recipe.id, Recipe.name, Recipe.prep, Recipe.description,\
                           Recipe.instruction,Ingredient.iname,Ingredient.units).\
            filter(Recipe.id==Ingredient.recipe_id).\
            all()
        return create_Recipe_List(li)
    else: # return all shows
        li = session.query(Recipe.name,Recipe.id).all()
        return li
    
    session.close();

def get_Recipe_By_Name(term):
    session = Session()
    li = session.query(Recipe.id, Recipe.name, Recipe.prep, Recipe.description,\
                      Recipe.instruction,Ingredient.iname,Ingredient.units).\
                      filter(Recipe.id==Ingredient.recipe_id).\
                      all()
    li2 = []
    if term is not None:
        
        i = 0
        while i<len(li):
            print(term)
            print(li[i][1])
            lookstr = li[i][1]
            if term.lower() in lookstr.lower():
                print("Found Match")
                li2.append(li[i])
            i+=1
    else:
        li2 = li
    return create_Recipe_List(li2)
    session.close();

def create_Recipe_List(showList):
    li = []
    show = []

    if len(showList) == 0:
        return []
    #print(showList)

    prevName = showList[0].name
    show.append(showList[0].id)
    show.append(showList[0].name)
    show.append(showList[0].prep)
    show.append(showList[0].description)
    show.append(showList[0].instruction)
    show.append(showList[0].iname)
    show.append(showList[0].units)
            
    for i in range(1, len(showList)):
        
        if showList[i].name == show[1]:
            show.append(showList[i].iname)
            show.append(showList[i].units)
        else:
            li.append(show)
            show = []
            prevName = showList[i].name
            show.append(showList[i].id)
            show.append(showList[i].name)
            show.append(showList[i].prep)
            show.append(showList[i].description)
            show.append(showList[i].instruction)
            show.append(showList[i].iname)
            show.append(showList[i].units)

    li.append(show)
    return li

def get_recipe_by_id(show_id):
    session = Session()
    query = session.query(Recipe.id, Recipe.name, Recipe.prep, Recipe.description,\
            Recipe.instruction).\
            filter(Recipe.id==show_id).all()

    return recipe_to_obj(query)

def recipe_to_obj(query):
    show_obj={}
    show_obj['id'] = query[0][0]
    show_obj['name'] = query[0][1]
    show_obj['prep'] = str(query[0][2])
    show_obj['description'] = str(query[0][3])
    show_obj['instruction'] = str(query[0][4])

    return show_obj



def add_recipe_to_db(show_info,ingredient_info):
    session = Session()
    try:
        new_show = Recipe(name=show_info['name'], prep=show_info['prep'],\
                          description=show_info['description'],instruction=show_info['instruction'])
        session.add(new_show)
        session.commit()
        for ingredient_type, ingredient in ingredient_info.items():
            new_ingredient = Ingredient(recipe_id=new_show.id,iname=ingredient_type,units=ingredient)
            session.add(new_ingredient)
    except exc.SQLAlchemyError: #Attenpt at doing some error checking. Not working
        session.rollback()
        session.close()
        print("In rollback")
        raise
    finally:
        session.commit()
        session.close()

def edit_recipe_in_db(show_info):
    session = Session()
    try:


        old_show = session.query(Recipe).filter_by(id=show_info['id']).one()
        old_show.description = show_info['description']
        old_show.name = show_info['name']
        old_show.prep = show_info['prep']
        old_show.instruction = show_info['instruction']

        
    except exc.SQLAlchemyError: #Attenpt at doing some error checking. Not working
        session.rollback()
        session.close()
        print("In rollback")
        raise
    finally:
        session.commit()
        session.close()


def delete_recipe_from_db(show_info):
    session = Session()
    try:
        old_ing = session.query(Ingredient).filter_by(id=show_info['id']).all()
        old_recipe = session.query(Recipe).filter_by(id=show_info['id']).all()
        for o in old_ing:
            session.delete(o)

        for o in old_recipe:
            session.delete(o)

        
    except exc.SQLAlchemyError: #Attempt at doing some error checking. Not working
        session.rollback()
        session.close()
        print("In rollback")
        raise
    finally:
        session.commit()
        session.close()

