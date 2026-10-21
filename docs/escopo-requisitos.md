# Revisão da documentação — PIT I para PIT II

**Fernando Miranda Paixão — RGM 33982236**

## Situação-problema
Na PIT I foi selecionada a situação-problema 1, relacionada ao desenvolvimento de um aplicativo móvel de vendas de cupcakes gourmet. A solução foi concebida para oferecer catálogo, pedidos, pagamento e entrega, com levantamento ágil das necessidades do negócio.

## Objetivo geral
Transformar a especificação inicial da PIT I em aplicação funcional, intuitiva e responsiva, com recursos para seleção de produtos, montagem de pedidos e acompanhamento básico de solicitações.

## Revisão conceitual
A PIT I adotou Engenharia de Requisitos Ágeis, Scrum, User Story Mapping, mapa de afinidade e priorização MoSCoW. A PIT II aprofunda modelagem de dados, interface humano-computador, codificação de front-end e back-end, versionamento e testes.

## Requisitos funcionais propostos para implementação
- RF01: apresentar vitrine de cupcakes com nome, descrição e preço.
- RF02: permitir pesquisa de produtos.
- RF03: adicionar e remover itens do carrinho e alterar quantidade.
- RF04: calcular automaticamente o subtotal e o total.
- RF05: registrar pedidos com dados de contato e entrega.
- RF06: informar o identificador do pedido.
- RF07: consultar a situação de um pedido.
- RF08: apresentar meios de pagamento em modo demonstrativo. Integração financeira real permanece fora do MVP.

## Requisitos não funcionais
- RNF01: interface responsiva para celular e computador.
- RNF02: validação de entradas no cliente e no servidor.
- RNF03: tratamento de erros com mensagens compreensíveis.
- RNF04: persistência dos pedidos em banco de dados.
- RNF05: organização modular do código, documentação e versionamento Git.

## Priorização do MVP (proposta)
**Must have:** catálogo, carrinho, cálculo do total, formulário e registro de pedido.  
**Should have:** pesquisa e consulta básica de status.  
**Could have:** categorias, filtros mais elaborados e promoções.  
**Won't have nesta versão:** integração bancária, rastreamento logístico real e aplicativos nativos.

## Observação sobre escopo
A PIT I menciona a intenção de contemplar mais de 40 sabores. A implementação inicial poderá utilizar um catálogo reduzido e demonstrativo, mantendo a ampliação como evolução futura. Nenhum pagamento real será processado na versão acadêmica.
