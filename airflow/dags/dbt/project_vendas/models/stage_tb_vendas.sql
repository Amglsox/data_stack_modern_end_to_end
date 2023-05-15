{{ config(
    materialized='table',
    partition_by={
      "field": "dt_atualizado_em",
      "data_type": "timestamp",
      "granularity": "day"
    }
)}}
SELECT preco
    ,ds_metodo_pagamento
    ,id_cliente
    ,ds_categoria
    ,ds_shopping
    ,dt_criado_em.member0 as dt_criado_em
    ,dt_atualizado_em.member0 as dt_atualizado_em
    ,id_venda
    ,quantidade
    ,dt_venda.member0 as dt_venda
FROM shopping_bronze.tb_vendas 
WHERE DATE(_PARTITIONTIME) = (SELECT MAX(DATE(_PARTITIONTIME)) FROM shopping_bronze.tb_vendas)



