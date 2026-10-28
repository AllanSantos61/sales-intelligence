# Arquitetura e regras de negócio

## Fluxo de dados

`generate_data.py` → CSV sintético → `etl.py` (validação + medidas) → CSV limpo → modelagem PostgreSQL → consultas SQL → futura camada de visualização.

## Granularidade

Cada linha representa um pedido com um único produto e um vendedor. Não é uma estrutura de itens múltiplos por pedido. O identificador `order_id` é único.

## Indicadores

- Receita bruta: quantidade × preço unitário.
- Receita líquida: receita bruta × (1 − desconto).
- Custo: quantidade × custo unitário.
- Lucro bruto: receita líquida − custo.
- Receita reconhecida: receita líquida somente de pedidos `completed`.
- Ticket médio: receita reconhecida / quantidade de pedidos concluídos.
- Margem bruta: lucro bruto / receita líquida, somente pedidos concluídos.

## Cuidados

Os dados são sintéticos, não correspondem a operações reais. A coluna `customer_name` vazia na geração é intencional; a chave `customer_id` identifica o cliente. O schema SQL e as consultas são entregues como referência; a carga automática no PostgreSQL ainda não está implementada. Não há dashboard Power BI nesta etapa.
