# Sales Intelligence | End-to-End Data Analytics

**Projeto de portfólio com dados 100% sintéticos**, criado para demonstrar engenharia de dados, modelagem relacional, SQL, Python e regras de Business Intelligence.

## Objetivo

Simular uma operação comercial e construir um pipeline reproduzível: **geração de dados → validação e transformação → indicadores → modelagem PostgreSQL → visualização futura**.

## Estrutura

```text
src/generate_data.py     Gerador determinístico de pedidos fictícios
src/etl.py               Limpeza, validação e métricas financeiras
sql/01_schema.sql        Modelo relacional PostgreSQL
sql/02_kpis.sql          Consultas analíticas SQL
tests/test_etl.py        Testes automatizados com pytest
docs/architecture.md    Arquitetura, granularidade e regras de negócio
.github/workflows/ci.yml  Integração contínua
```

## Executar

Requer Python 3.12+.

```bash
python -m pip install -r requirements.txt
python -m src.generate_data
python -m src.etl
python -m pytest -q
```

A geração cria `data/sales_synthetic.csv` e o ETL produz `data/sales_clean.csv`. A saída limpa está no `.gitignore`.

## Indicadores

- Receita bruta, descontos, receita líquida e lucro bruto.
- Receita reconhecida: somente pedidos concluídos.
- Ticket médio por pedido concluído.
- Faturamento mensal e receita por vendedor.
- Preparação para segmentação de clientes e visualizações executivas.

## Escopo atual

**Implementado:** scripts Python, validação, consultas SQL, schema de referência, testes e workflow de CI.

**Ainda não implementado:** carga automática no PostgreSQL, dashboard Power BI, integração com API, orquestração e testes de integração com banco. O pipeline é executável localmente; a aprovação do workflow pode ser verificada na aba Actions.

Todos os nomes e valores são fictícios. Não há dados, credenciais ou código de clientes.

Desenvolvido por [Allan Santos](https://github.com/AllanSantos61).
