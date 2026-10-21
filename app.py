import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DATABASE = os.environ.get("DATABASE_PATH", "cupcakes_fernando.db")
CATALOGO = [
 ("Chocolate Belga","Massa de chocolate e ganache",15.90),
 ("Morango com Creme","Baunilha, creme e morango",14.50),
 ("Red Velvet","Massa aveludada e cobertura cremosa",16.90),
 ("Doce de Leite","Recheio e cobertura de doce de leite",15.50),
 ("Baunilha","Massa leve e cobertura de baunilha",12.90),
 ("Limão Siciliano","Massa cítrica com cobertura suave",14.90)
]

def conectar():
    db=sqlite3.connect(DATABASE)
    db.row_factory=sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db

def preparar():
    with closing(conectar()) as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, descricao TEXT NOT NULL, preco REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS pedidos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, telefone TEXT NOT NULL, endereco TEXT NOT NULL, forma_pagamento TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Recebido', total REAL NOT NULL, criado_em TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS itens_pedido (id INTEGER PRIMARY KEY AUTOINCREMENT, pedido_id INTEGER NOT NULL REFERENCES pedidos(id), produto_id INTEGER NOT NULL REFERENCES produtos(id), quantidade INTEGER NOT NULL CHECK(quantidade>0), preco_unitario REAL NOT NULL);
        """)
        if not db.execute("SELECT 1 FROM produtos LIMIT 1").fetchone():
            db.executemany("INSERT INTO produtos (nome,descricao,preco) VALUES (?,?,?)",CATALOGO)
        db.commit()

@app.get("/")
def inicio():
    return render_template("index.html")

@app.get("/api/produtos")
def produtos():
    with closing(conectar()) as db:
        return jsonify([dict(p) for p in db.execute("SELECT * FROM produtos ORDER BY id")])

@app.post("/api/pedidos")
def novo_pedido():
    dados=request.get_json(silent=True) or {}
    for campo in ("nome","telefone","endereco"):
        if not isinstance(dados.get(campo),str) or len(dados[campo].strip())<3:
            return jsonify(erro="Preencha corretamente: "+campo),400
    if dados.get("forma_pagamento") not in ("Pix demonstrativo","Cartão demonstrativo","Boleto demonstrativo"):
        return jsonify(erro="Forma de pagamento inválida"),400
    itens=dados.get("itens")
    if not isinstance(itens,list) or not 1<=len(itens)<=50:
        return jsonify(erro="Carrinho vazio ou inválido"),400
    with closing(conectar()) as db:
        produtos_validos=[]
        for item in itens:
            if not isinstance(item,dict) or type(item.get("id")) is not int or type(item.get("quantidade")) is not int or not 1<=item["quantidade"]<=50:
                return jsonify(erro="Item ou quantidade inválida"),400
            produto=db.execute("SELECT * FROM produtos WHERE id=?",(item["id"],)).fetchone()
            if produto is None:
                return jsonify(erro="Produto não encontrado"),400
            produtos_validos.append((produto,item["quantidade"]))
        total_centavos=sum(round(p["preco"]*100)*q for p,q in produtos_validos)
        cur=db.execute("INSERT INTO pedidos(nome,telefone,endereco,forma_pagamento,total,criado_em) VALUES(?,?,?,?,?,?)",
            (dados["nome"].strip()[:100],dados["telefone"].strip()[:40],dados["endereco"].strip()[:240],dados["forma_pagamento"],total_centavos/100,datetime.now(timezone.utc).isoformat()))
        db.executemany("INSERT INTO itens_pedido(pedido_id,produto_id,quantidade,preco_unitario) VALUES(?,?,?,?)",
            [(cur.lastrowid,p["id"],q,p["preco"]) for p,q in produtos_validos])
        db.commit()
        return jsonify(numero=cur.lastrowid,total=total_centavos/100,status="Recebido"),201

@app.get("/api/pedidos/<int:numero>")
def consultar(numero):
    telefone=request.args.get("telefone","").strip()
    if not telefone:
        return jsonify(erro="Informe o telefone do pedido"),400
    with closing(conectar()) as db:
        pedido=db.execute("SELECT id,status,total,criado_em FROM pedidos WHERE id=? AND telefone=?",(numero,telefone)).fetchone()
        return (jsonify(dict(pedido)),200) if pedido else (jsonify(erro="Pedido não encontrado"),404)

preparar()
if __name__=="__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG")=="1")
