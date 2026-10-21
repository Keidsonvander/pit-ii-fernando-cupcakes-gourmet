import importlib
import os
import tempfile
import unittest

class AplicativoTestes(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        os.environ["DATABASE_PATH"]=os.path.join(self.temp.name,"teste.db")
        import app
        self.app=importlib.reload(app).app.test_client()
    def tearDown(self):
        self.temp.cleanup()
    def test_catalogo(self):
        resposta=self.app.get("/api/produtos")
        self.assertEqual(resposta.status_code,200)
        self.assertEqual(len(resposta.json),6)
    def test_pedido(self):
        dados={"nome":"Pessoa Teste","telefone":"11999999999","endereco":"Rua Teste, 10","forma_pagamento":"Pix demonstrativo","itens":[{"id":1,"quantidade":2}]}
        resposta=self.app.post("/api/pedidos",json=dados)
        self.assertEqual(resposta.status_code,201)
        consulta=self.app.get(f"/api/pedidos/{resposta.json['numero']}?telefone=11999999999")
        self.assertEqual(consulta.status_code,200)
    def test_carrinho_vazio(self):
        dados={"nome":"Pessoa Teste","telefone":"11999999999","endereco":"Rua Teste, 10","forma_pagamento":"Pix demonstrativo","itens":[]}
        self.assertEqual(self.app.post("/api/pedidos",json=dados).status_code,400)

if __name__=="__main__":
    unittest.main()
