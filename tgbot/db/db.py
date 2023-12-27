import asyncpg
from aiogram.types import Message
from asyncpg import Pool

from db.db_config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASS    

class Database:
    def __init__(self):
        self.connection = None

    async def connect(self):
        if self.connection is None or self.connection.is_closed():
            self.connection = await asyncpg.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASS
            )
            print("Database connected successfully")

    async def close(self):
        if self.connection and not self.connection.is_closed():
            await self.connection.close()
            print("Database connection closed")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

async def get_keyless_employees():
    async with Database() as db:
        rows = await db.connection.fetch("""
            SELECT *
            FROM keycontrol_employee
            WHERE id NOT IN (
                SELECT employee_id_id
                FROM keycontrol_byemployeetakedkey
                WHERE is_returned = false
            );""")
        result = [f"{row['last_name']} {row['first_name']}" for row in rows]
    return result

async def get_free_audience():  
    async with Database() as db:
        rows = await db.connection.fetch(""" SELECT room_number
            FROM keycontrol_auditorium
            WHERE id NOT IN (
                SELECT auditorium_id
                FROM keycontrol_byemployeetakedkey
                WHERE is_returned = false
            );""")
        result = [str(row['room_number']) for row in rows]

    return result

async def get_employee_has_not_taken_key(username):  
    async with Database() as db:
        rows = await db.connection.fetch("""
SELECT *
FROM keycontrol_employee
WHERE id NOT IN (
    SELECT employee_id_id
    FROM keycontrol_byemployeetakedkey
    WHERE is_returned = false 
) AND (tg_username != $1 OR tg_username IS NULL);;""", username)
        result = [f"{row['last_name']} {row['first_name']}" for row in rows]
    return result

async def have_a_key_full_table(username):
    async with Database() as db:
        rows = await db.connection.fetch("""SELECT *
FROM keycontrol_byemployeetakedkey
WHERE employee_id_id IN (
    SELECT id
    FROM keycontrol_employee
    WHERE tg_username = $1
) AND is_returned = false;;""", username)
    result = [f"{row['auditorium_id']} {row['employee_id_id']}" for row in rows]
    return result

async def have_a_key(username):
    async with Database() as db:
        rows = await db.connection.fetch("""SELECT ka.room_number
FROM keycontrol_byemployeetakedkey bk
JOIN keycontrol_employee ke ON bk.employee_id_id = ke.id
JOIN keycontrol_auditorium ka ON bk.auditorium_id = ka.id
WHERE ke.tg_username = $1 AND bk.is_returned = false;""", username)
    result = [str(row['room_number']).replace('\ufeff', '') for row in rows]
    return result

async def search_employee(like, username):
    async with Database() as db:
        rows = await db.connection.fetch("""SELECT *
            FROM keycontrol_employee
            WHERE (last_name || ' ' || first_name) ILIKE $1
            AND id NOT IN (
                SELECT employee_id_id
                FROM keycontrol_byemployeetakedkey
                WHERE is_returned = false
            ) AND (tg_username != $2 OR tg_username IS NULL);;""", f"%{like}%", username)
    result = [f"{row['last_name']} {row['first_name']}" for row in rows]
    return result

async def reg_check(id_card_code):
    async with Database() as db:
        rows = await db.connection.fetch("""
                SELECT *
                FROM keycontrol_employee
                WHERE id_card_code = $1 AND tg_username IS NULL""", id_card_code)
    return rows


async def insert_into_keytransfer(from_emp_id, last_name,first_name, aud_id, nnow):
    async with Database() as db:
       await db.connection.execute("INSERT INTO keycontrol_keytransfer (from_employee_id, to_employee_id, auditorium_id, transfer_time) VALUES ($1, (SELECT id from keycontrol_employee WHERE last_name=$2 AND first_name=$3), $4, $5)",
                              int(from_emp_id), last_name, first_name, int(aud_id), nnow)
       
async def insert_into_byemptakedkey(last_name, first_name, aud_id, username):
    async with Database() as db:
       await db.connection.execute("""INSERT INTO keycontrol_byemployeetakedkey (employee_id_id, auditorium_id, take_time, return_time, is_returned, key_transferred)
VALUES (
    (SELECT id FROM keycontrol_employee WHERE last_name = $1 AND first_name = $2),
    $3,
    (SELECT take_time FROM keycontrol_byemployeetakedkey WHERE employee_id_id IN (
        SELECT id FROM keycontrol_employee WHERE tg_username = $4
    ) AND is_returned = false LIMIT 1),
    (SELECT return_time FROM keycontrol_byemployeetakedkey WHERE employee_id_id IN (
        SELECT id FROM keycontrol_employee WHERE tg_username = $4
    ) AND is_returned = false LIMIT 1),
    false,
    true
); """, last_name, first_name, int(aud_id), username)
              
async def update_byemptakedkey(username):
    async with Database() as db:
       await db.connection.execute("""UPDATE keycontrol_byemployeetakedkey
SET is_returned = true
WHERE employee_id_id IN (
    SELECT id
    FROM keycontrol_employee
    WHERE tg_username = $1
) AND is_returned = false;
""", username)
              
async def register_tg_user(username, id):
    async with Database() as db:
       await db.connection.execute("""UPDATE keycontrol_employee
SET tg_username = $1
WHERE id = $2
""", username, id)
       
