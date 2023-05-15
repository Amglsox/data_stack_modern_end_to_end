{{ config(
    materialized='table',
    partition_by={
      "field": "dt_atualizado_em",
      "data_type": "timestamp",
      "granularity": "day"
    }
)}}

with stg_tb_customer as ( 
    SELECT 
    id_cliente
    ,ds_sexo
    ,nr_cpf
    ,dt_criado_em.member0 as dt_criado_em
    ,nome_cliente
    ,dt_atualizado_em.member0 as dt_atualizado_em
    ,ds_email
    ,dt_nascimento.member0  as dt_nascimento 
    FROM shopping_bronze.tb_customer 
    WHERE DATE(_PARTITIONTIME) = (select max(DATE(_PARTITIONTIME)) from shopping_bronze.tb_customer )
)
select * from stg_tb_customer