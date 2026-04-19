"""
Gera dados fictícios da barbearia.
Adiciona ao gerar_dados.py principal.
Rodar: python gerar_barbearia.py
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

OUT_DIR = "dados"
os.makedirs(OUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# NOMES REALISTAS (clientes de barbearia, majoritariamente masculino)
# ═══════════════════════════════════════════════════════════════
NOMES_CLIENTES = [
    "Carlos Silva", "Rafael Almeida", "Bruno Ferreira", "Gabriel Lima",
    "Lucas Martins", "Thiago Pereira", "Leonardo Gomes", "André Nascimento",
    "Eduardo Cardoso", "Matheus Rocha", "Daniel Freitas", "Rodrigo Teixeira",
    "Felipe Correia", "Vinícius Ramos", "Gustavo Fonseca", "Henrique Campos",
    "Alexandre Batista", "Raphael Nunes", "Fábio Duarte", "Marcelo Costa",
    "Ricardo Brito", "Paulo Henrique", "Sérgio Lopes", "Otávio Guimarães",
    "Marcos Vieira", "João Paulo", "Tiago Santos", "Diego Oliveira",
    "Cesar Ribeiro", "Igor Moreira", "Fernando Castro", "Vitor Araújo",
    "Arthur Pinto", "Pedro Henrique", "Luiz Augusto", "Caio Rodrigues",
    "Murilo Barbosa", "Renan Mendes", "Douglas Souza", "Robson Lima",
    "Wagner Dias", "Anderson Moraes", "Jefferson Pires", "Cleber Torres",
    "Josué Carvalho", "Mateus Vieira", "Natan Rocha", "Samuel Freitas",
    "Enzo Martins", "Davi Oliveira", "Breno Santos", "Erick Campos",
    "Yuri Monteiro", "Bernardo Silva", "Lorenzo Fernandes", "Heitor Almeida",
    "Benjamin Costa", "Miguel Santos", "Nicolas Ramos", "Levi Pereira",
]

# ═══════════════════════════════════════════════════════════════
# SERVIÇOS REALISTAS DE BARBEARIA
# ═══════════════════════════════════════════════════════════════
SERVICOS = {
    "Corte masculino":          {"preco_min": 35, "preco_max": 55},
    "Corte + Barba":            {"preco_min": 50, "preco_max": 85},
    "Barba completa":           {"preco_min": 30, "preco_max": 50},
    "Pezinho":                  {"preco_min": 15, "preco_max": 25},
    "Sobrancelha":              {"preco_min": 20, "preco_max": 35},
    "Hidratação capilar":       {"preco_min": 40, "preco_max": 70},
    "Pigmentação de barba":     {"preco_min": 60, "preco_max": 100},
    "Combo Premium (VIP)":      {"preco_min": 90, "preco_max": 150},
    "Corte infantil":           {"preco_min": 25, "preco_max": 40},
    "Relaxamento":              {"preco_min": 70, "preco_max": 120},
}

# ═══════════════════════════════════════════════════════════════
# BARBEIROS (equipe típica de barbearia de bairro)
# ═══════════════════════════════════════════════════════════════
BARBEIROS = [
    {"nome": "Tiago (Dono)",     "comissao_pct": 0.00,  "experiencia_anos": 12},
    {"nome": "Marcos",           "comissao_pct": 0.45,  "experiencia_anos": 8},
    {"nome": "Léo",              "comissao_pct": 0.40,  "experiencia_anos": 4},
    {"nome": "Jr (aprendiz)",    "comissao_pct": 0.30,  "experiencia_anos": 1},
]

# ═══════════════════════════════════════════════════════════════
# PRODUTOS VENDIDOS NA LOJA
# ═══════════════════════════════════════════════════════════════
PRODUTOS = {
    "Pomada modeladora":        {"preco": 45, "custo": 22},
    "Óleo para barba":          {"preco": 55, "custo": 28},
    "Shampoo para cabelo":      {"preco": 40, "custo": 18},
    "Balm pós barba":           {"preco": 35, "custo": 15},
    "Kit cuidados com barba":   {"preco": 120, "custo": 60},
    "Minoxidil":                {"preco": 90, "custo": 45},
    "Finalizador":              {"preco": 38, "custo": 17},
    "Toalha personalizada":     {"preco": 25, "custo": 10},
}


def telefone_df():
    return f"(61) 9{random.randint(8000, 9999)}-{random.randint(1000, 9999)}"


# ═══════════════════════════════════════════════════════════════
# 1. ATENDIMENTOS (últimos 90 dias, ~15-25 por dia útil)
# ═══════════════════════════════════════════════════════════════
def gerar_atendimentos():
    atendimentos = []
    hoje = datetime(2026, 4, 19)

    # Simula 90 dias de atendimento
    for dias_atras in range(90, 0, -1):
        data = hoje - timedelta(days=dias_atras)

        # Segunda a sábado (fechado domingo)
        if data.weekday() == 6:  # domingo
            continue

        # Mais movimento em sábado e sexta
        if data.weekday() == 5:  # sábado
            atendimentos_dia = random.randint(25, 40)
        elif data.weekday() == 4:  # sexta
            atendimentos_dia = random.randint(18, 28)
        else:
            atendimentos_dia = random.randint(12, 20)

        for _ in range(atendimentos_dia):
            hora = random.randint(9, 20)
            minuto = random.choice([0, 15, 30, 45])
            data_hora = data.replace(hour=hora, minute=minuto)

            cliente = random.choice(NOMES_CLIENTES)
            servico = random.choice(list(SERVICOS.keys()))
            preco_info = SERVICOS[servico]
            preco = random.randint(preco_info["preco_min"], preco_info["preco_max"])
            barbeiro = random.choice(BARBEIROS)

            # Alguns agendados (futuro), resto realizado
            if dias_atras <= 0:
                status = "Agendado"
            else:
                status = np.random.choice(
                    ["Realizado", "Cancelado", "Faltou"],
                    p=[0.90, 0.05, 0.05]
                )

            # Gorjeta (nem sempre)
            gorjeta = 0
            if status == "Realizado" and random.random() < 0.35:
                gorjeta = random.choice([5, 10, 10, 15, 20])

            atendimentos.append({
                "Data": data_hora.strftime("%Y-%m-%d %H:%M"),
                "Cliente": cliente,
                "Telefone": telefone_df(),
                "Servico": servico,
                "Barbeiro": barbeiro["nome"],
                "Comissao_Pct": barbeiro["comissao_pct"],
                "Valor": preco,
                "Gorjeta": gorjeta,
                "Comissao_Barbeiro": round(preco * barbeiro["comissao_pct"], 2),
                "Status": status,
                "Forma_Pagamento": np.random.choice(
                    ["PIX", "Cartão Débito", "Cartão Crédito", "Dinheiro"],
                    p=[0.50, 0.20, 0.20, 0.10]
                ),
            })

    # Adiciona alguns agendamentos futuros (próximos 7 dias)
    for dias_frente in range(1, 8):
        data = hoje + timedelta(days=dias_frente)
        if data.weekday() == 6:
            continue

        for _ in range(random.randint(3, 10)):
            hora = random.randint(9, 19)
            minuto = random.choice([0, 15, 30, 45])
            data_hora = data.replace(hour=hora, minute=minuto)
            cliente = random.choice(NOMES_CLIENTES)
            servico = random.choice(list(SERVICOS.keys()))
            preco_info = SERVICOS[servico]
            preco = random.randint(preco_info["preco_min"], preco_info["preco_max"])
            barbeiro = random.choice(BARBEIROS)

            atendimentos.append({
                "Data": data_hora.strftime("%Y-%m-%d %H:%M"),
                "Cliente": cliente,
                "Telefone": telefone_df(),
                "Servico": servico,
                "Barbeiro": barbeiro["nome"],
                "Comissao_Pct": barbeiro["comissao_pct"],
                "Valor": preco,
                "Gorjeta": 0,
                "Comissao_Barbeiro": round(preco * barbeiro["comissao_pct"], 2),
                "Status": "Agendado",
                "Forma_Pagamento": "",
            })

    df = pd.DataFrame(atendimentos)
    df = df.sort_values("Data", ascending=False).reset_index(drop=True)
    df.to_csv(f"{OUT_DIR}/barbearia_atendimentos.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ barbearia_atendimentos.csv ({len(df)} registros)")


# ═══════════════════════════════════════════════════════════════
# 2. VENDAS DE PRODUTOS (últimos 90 dias)
# ═══════════════════════════════════════════════════════════════
def gerar_vendas_produtos():
    vendas = []
    hoje = datetime(2026, 4, 19)

    for dias_atras in range(90, 0, -1):
        data = hoje - timedelta(days=dias_atras)
        if data.weekday() == 6:
            continue

        # 2-8 vendas de produto por dia
        qtd_vendas = random.randint(2, 8)
        for _ in range(qtd_vendas):
            produto = random.choice(list(PRODUTOS.keys()))
            info = PRODUTOS[produto]
            cliente = random.choice(NOMES_CLIENTES)
            quantidade = random.choice([1, 1, 1, 2])  # geralmente 1

            vendas.append({
                "Data": data.strftime("%Y-%m-%d"),
                "Cliente": cliente,
                "Produto": produto,
                "Quantidade": quantidade,
                "Preco_Unitario": info["preco"],
                "Custo_Unitario": info["custo"],
                "Receita_Total": info["preco"] * quantidade,
                "Lucro_Bruto": (info["preco"] - info["custo"]) * quantidade,
            })

    df = pd.DataFrame(vendas)
    df = df.sort_values("Data", ascending=False).reset_index(drop=True)
    df.to_csv(f"{OUT_DIR}/barbearia_produtos.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ barbearia_produtos.csv ({len(df)} registros)")


# ═══════════════════════════════════════════════════════════════
# 3. EVOLUÇÃO MENSAL
# ═══════════════════════════════════════════════════════════════
def gerar_evolucao():
    meses = []
    hoje = datetime(2026, 4, 19)

    for i in range(12, 0, -1):
        mes = hoje - timedelta(days=i * 30)
        # Tendência de crescimento
        base_atend = 350 + (12 - i) * 15
        base_receita = 19000 + (12 - i) * 900

        meses.append({
            "Mes": mes.strftime("%Y-%m"),
            "Atendimentos": base_atend + random.randint(-30, 40),
            "Receita_Servicos": base_receita + random.randint(-2000, 2500),
            "Receita_Produtos": random.randint(2200, 4500),
            "Clientes_Unicos": random.randint(180, 260),
            "Clientes_Novos": random.randint(25, 50),
        })

    pd.DataFrame(meses).to_csv(f"{OUT_DIR}/barbearia_evolucao.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ barbearia_evolucao.csv (12 meses)")


if __name__ == "__main__":
    print("Gerando dados da barbearia...\n")
    gerar_atendimentos()
    gerar_vendas_produtos()
    gerar_evolucao()
    print("\n✓ Dados da barbearia gerados!")
