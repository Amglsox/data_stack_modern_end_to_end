{{ config(
    materialized = 'table',
    partition_by = {
      "field": "dt_venda",
      "data_type": "timestamp",
      "granularity": "day"
    },
    cluster_by = ["ds_categoria", "ds_shopping"]
)}}

select sum(preco) as preco_venda, 
       sum(quantidade) as quantidade_venda,
       dt_venda,
       ds_categoria,
       ds_shopping
from {{ref('stage_tb_vendas')}}
group by ds_categoria, ds_shopping, dt_venda