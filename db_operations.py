
from sqlalchemy import text,select

import streamlit as st

import pandas as pd


# Initialize connection.
conn = st.connection('mysql', type='sql')

def insert_records(text_info):
    with conn.session as s:
        # s.execute(
        #     'INSERT INTO users (id, name, father_name, dob, id_type, embedding) VALUES (:id, :name, :father_name, :dob,:id_type, :embedding );',
        #     params=dict(id=text_info['ID'], name=text_info['Name'], father_name=text_info["Father's Name"],
        #                 dob=text_info['DOB'], id_type=text_info['ID Type'])
        # )
        s.execute(
            text('INSERT INTO users (id, name, father_name, dob, id_type, embedding) VALUES (:id, :name, :father_name, :dob, :id_type, :embedding);'),
            {
                'id': text_info['ID'],
                'name': text_info['Name'],
                'father_name': text_info["Father's Name"],
                'dob': text_info['DOB'],  # Make sure this is formatted as a string 'YYYY-MM-DD'
                'id_type': text_info['ID Type'],
                'embedding': str(text_info['Embedding'])
            }
            )
        s.commit()

#  select_query = select(users).where(users.c.id == id)

def fetch_record(text_info):
    # Perform query.
    # id =  str(text_info['ID'])
    # select_query = "SELECT * from users where id = 'CCNPA';"
    # df = conn.query(select_query, ttl=600)
    df = pd.DataFrame(conn.query('SELECT * from users;', ttl=600))
    return df

# def fetch_record(text_info):
#     # Extract ID as a string.
#     id_value = str(text_info['ID'])
    
    
#     result_proxy = None
#     # Execute the query safely by passing parameters separately from the query.
#     with conn.session as s:
#         select_query = text("SELECT * FROM users WHERE id = :id;")
#         result_proxy = s.query(select_query, {'id': id_value})

#         s.close()
#     # Fetch result into a DataFrame (assuming you're using Pandas).
#     # Ensure you have a result set conversion method appropriate for your setup.
#     df = pd.DataFrame(result_proxy.fetchall())
    
#     return df

def check_duplicacy(text_info):

    is_duplicate = False
    df = fetch_record(text_info)
    df = df[df['id'] == text_info['ID']] 
    if df.shape[0] > 0:
        is_duplicate = True
    return is_duplicate
