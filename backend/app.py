
import os
import json

from dotenv import load_dotenv,dotenv_values


from flask import Flask, jsonify,render_template, request
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
from sqlalchemy import MetaData, inspect,create_engine,Table,select,and_

app = Flask(__name__)


"""
    Generacion de coneccion a la base de datos usando alchemy
"""

# path_uri:str= f''
load_dotenv()

sql_uri = os.getenv('SQL_ALCHEMY_URI')

# configuraciones 
app.config['SQLALCHEMY_DATABASE_URI'] = sql_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#obtener de la base de datos
db = SQLAlchemy(app)

engine = create_engine(sql_uri)

table = Table(
    'usuarios',
    MetaData(bind=True),
    autoload = True,
    autoload_with = engine
) 


query_st = select([
    table.columns.id_usuario,
    table.columns.nombre,
    table.columns.edad]
)



@app.route('/usuarios')
def users():
    

    cnn = engine.connect()

    res =  cnn.execute(query_st).fetchall()

    headers = ['id_usuario','nombre','edad']

    json_data =[]

    for res in res:
        json_data.append(dict(zip(headers,res)))


    data = json.dumps(json_data)

    return data

@app.route('/usuario/<int:id>')
def usuario(id):
    cnn = engine.connect()

    query_st = select([
    table.columns.id_usuario,
    table.columns.nombre,
    table.columns.edad]
    ).where(and_(
        table.columns.id_usuario == id
    ))

    res =  cnn.execute(query_st).fetchall()

    if (len(res) != 0 ):
   
        headers = ['id_usuario','nombre','edad']

        json_data = []

        for res in res:
            json_data.append(dict(zip(headers,res)))


        data = json.dumps(json_data)

    else:
        data = [
            {
                'mensaje': 'No hay datos'
            }
        ]


    return data

    

app.run(port= 5000 or os.getenv('PORT_SERVER'),debug=True)