import logging
import random

from datetime import datetime
from datetime import timedelta

import psycopg2

from faker import Faker


class Config:
    def __init__(self) -> None:
        self.user = "pythonapp"
        self.password = "Amglsox123@"
        self.host = "34.27.49.72"
        self.port = "5432"
        self.database = "exemplo_dados_airbyte"

    def _to_dict(self) -> dict:
        obj = {
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "database": self.database,
        }
        return obj


obj_connection_postrges = Config()


def get_connection():
    params = obj_connection_postrges._to_dict()
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    return conn


def execute_multiple_insert(values, params, table):
    conn = get_connection()
    cur = conn.cursor()
    args = ",".join(cur.mogrify(params, i).decode("utf-8") for i in values)
    cur.execute(f"INSERT INTO {table} VALUES " + (args))


def execute_sql_command(query: str, params_query: tuple) -> str:
    rows = []
    retorno = ""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, params_query)
        row = cur.fetchone()[0]
        cur.close()
        print("close db")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if len(rows) > 0:
            retorno = "Cliente Existe"
        elif conn is not None:
            conn.close()
            retorno = "OK"
    return retorno, row


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def get_metodo_pagamento():
    return random.choice(list(set(["Debit Card", "Credit Card", "Cash"])))


def get_shopping_pagamento():
    return random.choice(
        list(
            set(
                [
                    "Metrocity",
                    "Kanyon",
                    "Mall of Istanbul",
                    "Viaport Outlet",
                    "Cevahir AVM",
                    "Istinye Park",
                    "Emaar Square Mall",
                    "Zorlu Center",
                    "Metropol AVM",
                    "Forum Istanbul",
                ]
            )
        )
    )


def get_category():
    return random.choice(
        list(set(["Food & Beverage", "Souvenir", "Cosmetics", "Books", "Clothing", "Toys", "Shoes", "Technology"]))
    )


def generate_compra(id_cliente=random.randint(1, 541)):
    sql = """INSERT INTO public.tb_vendas (ds_categoria, quantidade, preco, ds_metodo_pagamento, ds_shopping, dt_venda, dt_criado_em, dt_atualizado_em, id_cliente)
       VALUES(%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s) RETURNING id_venda;
    """
    i = 0
    lista_insert = []
    while i < 1000:
        ds_categoria = get_category()
        quantidade = random.randint(1, 10)
        preco = round(random.uniform(5.23, 5250), 2)
        ds_shopping = get_shopping_pagamento()
        ds_metodo_pagamento = get_metodo_pagamento()
        ds_categoria = get_category()
        d1 = datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        d2 = datetime.strptime("2023-05-11 23:59:59", "%Y-%m-%d %H:%M:%S")
        dt_venda = random_date(d1, d2)
        tuple_venda = (ds_categoria, quantidade, preco, ds_metodo_pagamento, ds_shopping, dt_venda, id_cliente)
        i += 1
        lista_insert.append(tuple_venda)
    execute_multiple_insert(
        lista_insert,
        "(%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s)",
        table="public.tb_vendas (ds_categoria, quantidade, preco, ds_metodo_pagamento, ds_shopping, dt_venda, dt_criado_em, dt_atualizado_em, id_cliente)",
    )


def generate_cliente():
    sql = """INSERT INTO public.tb_customer (nr_cpf, nome_cliente, dt_nascimento, ds_sexo, ds_email, dt_criado_em, dt_atualizado_em)
       VALUES(%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)  RETURNING id_cliente;
    """
    fake = Faker("pt_BR")
    person = fake.profile()

    tuple_cliente = (
        person["ssn"],
        person["name"],
        person["birthdate"].strftime("%Y-%m-%d"),
        person["sex"],
        person["mail"],
    )
    retorno, id_cliente = execute_sql_command(sql, tuple_cliente)
    return id_cliente


def main():
    i = 0
    while i < 10000:
        print(i)
        # id_cliente = generate_cliente()
        id_cliente = random.randint(1, 541)
        id_venda = generate_compra()
        i += 1
    return 0


main()
