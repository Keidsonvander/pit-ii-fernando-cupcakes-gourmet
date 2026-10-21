# Planejamento técnico — PIT II

**Fernando Miranda Paixão — RGM 33982236**

Este documento descreve uma **proposta de arquitetura**, não uma implementação já concluída.

## Tecnologias previstas
- Front-end: HTML5, CSS3 e JavaScript.
- Back-end: Python 3 com Flask.
- Banco de dados: SQLite para a demonstração.
- Hospedagem prevista: Render, condicionada à publicação.
- Modo de codificação: tradicional.

## Modelo de dados preliminar
**Produto**: id (PK), nome, descrição, preço, disponível.  
**Pedido**: id (PK), cliente, telefone, endereço, status, valor_total, criado_em.  
**ItemPedido**: id (PK), pedido_id (FK), produto_id (FK), quantidade, preço_unitário.  

Um Pedido contém um ou mais ItensPedido; um Produto pode constar em diferentes ItensPedido. O valor do pedido deve ser calculado no servidor a partir dos produtos armazenados.

## Fluxo previsto
1. Usuário acessa a vitrine.
2. Seleciona produtos e quantidades.
3. Revisa o carrinho.
4. Informa contato e endereço.
5. Envia a solicitação.
6. O servidor valida e registra os dados.
7. O sistema devolve o número do pedido.

## Qualidade e validação
Testar navegação, cálculos, validação de campos, pedidos e consulta. Após disponibilizar o software, convidar cinco colegas/profissionais para testes, registrar resultados reais, anexar evidências e corrigir os problemas identificados.

## Limitações planejadas
Pagamentos e entregas reais exigem integrações adicionais, fora do MVP acadêmico. A versão demonstrativa não deve solicitar dados de cartão nem prometer entregas reais.
