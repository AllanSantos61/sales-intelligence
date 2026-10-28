# Sales Intelligence — Case de Portfólio

**Desafio:** transformar pedidos comerciais em indicadores consistentes para tomada de decisão.

**Solução:** dados sintéticos reproduzíveis com seed fixa, validação ETL com Pandas, modelagem relacional PostgreSQL, SQL analítico, testes automatizados e dashboard estático.

**Principais decisões:** pedidos cancelados não compõem receita reconhecida; indicadores são derivados de pedidos concluídos; dados fictícios evitam exposição de informações reais.

**Arquitetura da demonstração:** o GitHub Actions executa Python e publica arquivos estáticos no GitHub Pages. O visitante não depende de um servidor Python, banco ativo ou Supabase.

**Limitação:** o dashboard não consulta o PostgreSQL em tempo real. O script de carga PostgreSQL está disponível para execução local ou em infraestrutura própria.

**Demonstração (após ativar Pages):** https://allansantos61.github.io/sales-intelligence/

**Código:** https://github.com/AllanSantos61/sales-intelligence
