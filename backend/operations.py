from flask import json, make_response, abort
from flask import jsonify
from datetime import datetime
import other_funcs as funcs
import hashlib, uuid
# imports related to database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.sql.expression import null


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

def read_one(device_id):
    """
    This function gets run when /api/alarms/{device_id} is run,
    and returns the relevant alarms for that device, if they exist

    :param device_id:   ID of device to fetch alarms
    :return:            200 on success, 404 if not found
    """
    '''
    # Check if device_id exists
    if device_id in ALARMS.keys():
        return jsonify(ALARMS[device_id])
    else:
        abort(404, f"Device ID: {device_id} does not exist")
    '''

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
