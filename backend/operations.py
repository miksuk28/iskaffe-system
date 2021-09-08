from flask import json, make_response, abort
from flask import jsonify
from datetime import datetime
import other_funcs as funcs
import hashlib, uuid
# imports related to database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.sql.expression import null

# keeps sqlalchemy from shitting its pants ¯\_(ツ)_/¯ 
engine = create_engine("sqlite:///iskaffe_db.db", echo=True, connect_args={"check_same_thread":False})
meta = MetaData()
conn = engine.connect()

users = Table(
    "users", meta,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("fname", String, nullable=False),
    Column("lname", String, nullable=False),
    Column("balance", Float, nullable=False),
    Column("password", String, nullable=False)
)


def add_user(user):
    fname = user.get("fname")
    lname = user.get("lname")
    password = user.get("password")
    username = user.get("username")

    if None not in (fname, lname, password, username):
        # act.create_user(fname, lname, username, password)
        salt = funcs.generate_salt()

        pasword_salt = password + salt
        hashed_password = hashlib.sha512(pasword_salt.encode("utf-8")).hexdigest()

        ins = users.insert().values(fname=fname, lname=lname, password=hashed_password, username=username, balance=0, salt=salt)
        result = conn.execute(ins)
        print(result)

        return jsonify(fname, lname, username)
    else:
        abort(400, "Missing parameters, user not created")
