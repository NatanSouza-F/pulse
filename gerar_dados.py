"""
Gera dados fictícios mas realistas para o Pulse Demo.
Rodar UMA vez: python gerar_dados.py
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
# NOMES BRASILEIROS REALISTAS
# ═══════════════════════════════════════════════════════════════
NOMES = [
    "Carlos Silva", "Ana Beatriz Oliveira", "João Pedro Santos", "Maria Fernanda Costa",
    "Rafael Almeida", "Juliana Ribeiro", "Bruno Ferreira", "Patrícia Souza",
    "Gabriel Lima", "Camila Rodrigues", "Lucas Martins", "Renata Carvalho",
    "Thiago Pereira", "Amanda Barbosa", "Leonardo Gomes", "Fernanda Dias",
    "André Nascimento", "Beatriz Moreira", "Eduardo Cardoso", "Luana Azevedo",
    "Matheus Rocha", "Isabela Cunha", "Daniel Freitas", "Larissa Pinto",
    "Rodrigo Teixeira", "Priscila Araújo", "Felipe Correia", "Tatiana Mendes",
    "Vinícius Ramos", "Mariana Castro", "Gustavo Fonseca", "Bruna Viana",
    "Henrique Campos", "Natália Monteiro", "Alexandre Batista", "Vanessa Moura",
    "Raphael Nunes", "Letícia Siqueira", "Fábio Duarte", "Carolina Xavier",
    "Marcelo Costa", "Débora Pires", "Ricardo Brito", "Simone Machado",
    "Paulo Henrique", "Aline Coelho", "Sérgio Lopes", "Cristiane Reis",
    "Otávio Guimarães", "Rebeca Farias"
]

EMPRESAS_SUFIXOS = ["Ltda", "ME", "Eireli", "S/A"]
EMPRESAS_PRIMEIRO = ["Imóveis", "Comércio", "Serviços", "Tecnologia", "Engenharia",
                    "Construções", "Distribuidora", "Transportes", "Consultoria",
                    "Indústria", "Logística", "Papelaria", "Mercado", "Farmácia"]
EMPRESAS_NOMES = ["Brasilia", "Central", "Real", "Prime", "Forte", "Sol", "Nova",
                 "Alpha", "Modelo", "Global", "União", "Capital", "Mega", "Gold"]


def cnpj_valido():
    """Gera CNPJ aleatório (não necessariamente válido, mas formato correto)"""
    n = [random.randint(0, 9) for _ in range(8)]
    return f"{n[0]}{n[1]}.{n[2]}{n[3]}{n[4]}.{n[5]}{n[6]}{n[7]}/0001-{random.randint(10, 99)}"


def telefone_brasiliense():
    return f"(61) 9{random.randint(8000, 9999)}-{random.randint(1000, 9999)}"


# ═══════════════════════════════════════════════════════════════
# 1. DADOS PARA CORRETORA DE SEGUROS
# ═══════════════════════════════════════════════════════════════
def gerar_corretora():
    clientes = []
    seguradoras = ["Porto Seguro", "Bradesco Seguros", "Tokio Marine", 
                   "SulAmérica", "HDI Seguros", "Allianz", "Mapfre", "Zurich"]
    ramos = ["Auto", "Residencial", "Vida", "Empresarial", "Viagem", "Saúde"]
    status_opcoes = ["Ativo", "Ativo", "Ativo", "Ativo", "Vencendo", "Cancelado"]

    hoje = datetime(2026, 4, 19)

    for i in range(200):
        nome = random.choice(NOMES)
        ramo = random.choice(ramos)
        seguradora = random.choice(seguradoras)

        # Prêmios realistas por ramo
        premio_ranges = {
            "Auto": (1200, 5500), "Residencial": (400, 2200),
            "Vida": (600, 3500), "Empresarial": (3000, 18000),
            "Viagem": (150, 900), "Saúde": (2400, 12000)
        }
        premio_anual = random.randint(*premio_ranges[ramo])
        comissao_pct = random.uniform(0.10, 0.22)
        comissao = round(premio_anual * comissao_pct, 2)

        data_inicio = hoje - timedelta(days=random.randint(30, 900))
        data_renovacao = data_inicio + timedelta(days=365)
        dias_pra_renovacao = (data_renovacao - hoje).days

        # Status baseado em dias pra renovação
        if dias_pra_renovacao < 0:
            status = "Cancelado" if random.random() > 0.3 else "Vencido"
        elif dias_pra_renovacao < 30:
            status = "Vencendo"
        else:
            status = "Ativo"

        clientes.append({
            "Cliente": nome,
            "Telefone": telefone_brasiliense(),
            "Seguradora": seguradora,
            "Ramo": ramo,
            "Premio_Anual": premio_anual,
            "Comissao_Mensal": round(comissao / 12, 2),
            "Comissao_Anual": comissao,
            "Data_Inicio": data_inicio.strftime("%Y-%m-%d"),
            "Data_Renovacao": data_renovacao.strftime("%Y-%m-%d"),
            "Dias_Para_Renovacao": dias_pra_renovacao,
            "Status": status,
        })

    df = pd.DataFrame(clientes)
    df.to_csv(f"{OUT_DIR}/corretora_carteira.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ corretora_carteira.csv ({len(df)} registros)")

    # Tendência de comissão mensal (últimos 12 meses)
    meses = []
    for i in range(12, 0, -1):
        mes = hoje - timedelta(days=i * 30)
        base = 38000 + random.randint(-5000, 8000)
        crescimento = i * 500  # tendência de crescimento
        meses.append({
            "Mes": mes.strftime("%Y-%m"),
            "Comissao_Total": base + crescimento,
            "Novos_Contratos": random.randint(8, 22),
            "Cancelamentos": random.randint(1, 6),
        })
    pd.DataFrame(meses).to_csv(f"{OUT_DIR}/corretora_evolucao.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ corretora_evolucao.csv")


# ═══════════════════════════════════════════════════════════════
# 2. DADOS PARA ESCRITÓRIO CONTÁBIL
# ═══════════════════════════════════════════════════════════════
def gerar_contabilidade():
    regimes = ["Simples Nacional", "Lucro Presumido", "Lucro Real", "MEI"]
    regimes_peso = [0.55, 0.25, 0.08, 0.12]
    segmentos = ["Comércio varejista", "Serviços", "Construção civil",
                 "Tecnologia", "Indústria", "Transporte", "Saúde"]

    clientes = []
    hoje = datetime(2026, 4, 19)

    for i in range(32):
        primeiro = random.choice(EMPRESAS_PRIMEIRO)
        meio = random.choice(EMPRESAS_NOMES)
        sufixo = random.choice(EMPRESAS_SUFIXOS)
        nome_empresa = f"{primeiro} {meio} {sufixo}"

        regime = np.random.choice(regimes, p=regimes_peso)
        segmento = random.choice(segmentos)

        faturamento_ranges = {
            "MEI": (3000, 8000), "Simples Nacional": (15000, 180000),
            "Lucro Presumido": (100000, 500000), "Lucro Real": (300000, 2000000)
        }
        faturamento = random.randint(*faturamento_ranges[regime])

        # Status mensal aleatório: pendente, entregue, atrasado
        status = np.random.choice(
            ["Entregue", "Pendente", "Atrasado"],
            p=[0.68, 0.22, 0.10]
        )

        clientes.append({
            "Empresa": nome_empresa,
            "CNPJ": cnpj_valido(),
            "Regime_Tributario": regime,
            "Segmento": segmento,
            "Faturamento_Mensal": faturamento,
            "Honorario_Mensal": random.randint(400, 2500),
            "Cliente_Desde": (hoje - timedelta(days=random.randint(60, 2000))).strftime("%Y-%m"),
            "Status_Fechamento": status,
            "Dias_Para_Entrega": random.randint(0, 20),
            "Contato": random.choice(NOMES),
            "Telefone": telefone_brasiliense(),
        })

    df = pd.DataFrame(clientes)
    df.to_csv(f"{OUT_DIR}/contabil_clientes.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ contabil_clientes.csv ({len(df)} registros)")

    # Produtividade mensal
    meses = []
    for i in range(12, 0, -1):
        mes = hoje - timedelta(days=i * 30)
        horas_fech = 120 - (i * 3)  # tendência de redução (ganho de produtividade)
        meses.append({
            "Mes": mes.strftime("%Y-%m"),
            "Horas_Fechamento": max(40, horas_fech + random.randint(-10, 10)),
            "Empresas_Entregues_Prazo": random.randint(24, 32),
            "Receita_Honorarios": random.randint(38000, 55000),
        })
    pd.DataFrame(meses).to_csv(f"{OUT_DIR}/contabil_produtividade.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ contabil_produtividade.csv")


# ═══════════════════════════════════════════════════════════════
# 3. DADOS PARA CLÍNICA ESTÉTICA
# ═══════════════════════════════════════════════════════════════
def gerar_clinica():
    procedimentos_map = {
        "Limpeza de Pele": (120, 200),
        "Botox": (800, 1800),
        "Preenchimento Labial": (1200, 2500),
        "Harmonização Facial": (2500, 5000),
        "Drenagem Linfática": (150, 280),
        "Massagem Modeladora": (120, 220),
        "Criolipólise": (600, 1200),
        "Peeling Químico": (300, 600),
        "Depilação a Laser": (200, 450),
        "Microagulhamento": (350, 700),
    }

    profissionais = [
        "Dra. Patrícia Lima", "Dr. Rafael Souza", 
        "Dra. Juliana Costa", "Bruna (Esteticista)", "Marina (Esteticista)"
    ]

    atendimentos = []
    hoje = datetime(2026, 4, 19)

    for i in range(450):  # atendimentos dos últimos 90 dias
        nome = random.choice(NOMES)
        proc = random.choice(list(procedimentos_map.keys()))
        preco = random.randint(*procedimentos_map[proc])
        data = hoje - timedelta(days=random.randint(0, 90),
                                hours=random.randint(0, 23),
                                minutes=random.choice([0, 30]))
        profissional = random.choice(profissionais)

        # Alguns pacientes retornam (identifica recorrência)
        status = np.random.choice(
            ["Realizado", "Agendado", "Cancelado", "Faltou"],
            p=[0.75, 0.15, 0.05, 0.05]
        )

        atendimentos.append({
            "Data": data.strftime("%Y-%m-%d %H:%M"),
            "Paciente": nome,
            "Telefone": telefone_brasiliense(),
            "Procedimento": proc,
            "Profissional": profissional,
            "Valor": preco,
            "Status": status,
            "Forma_Pagamento": random.choice(["PIX", "Cartão Crédito", "Cartão Débito", "Dinheiro"]),
        })

    df = pd.DataFrame(atendimentos)
    df = df.sort_values("Data", ascending=False).reset_index(drop=True)
    df.to_csv(f"{OUT_DIR}/clinica_atendimentos.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ clinica_atendimentos.csv ({len(df)} registros)")

    # Evolução mensal
    meses = []
    for i in range(12, 0, -1):
        mes = hoje - timedelta(days=i * 30)
        meses.append({
            "Mes": mes.strftime("%Y-%m"),
            "Atendimentos": random.randint(120, 180),
            "Receita": random.randint(48000, 78000),
            "Ticket_Medio": random.randint(350, 520),
            "Pacientes_Novos": random.randint(18, 35),
        })
    pd.DataFrame(meses).to_csv(f"{OUT_DIR}/clinica_evolucao.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ clinica_evolucao.csv")


# ═══════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Gerando dados fictícios realistas...\n")

    print("[1/4] Corretora de Seguros")
    gerar_corretora()

    print("\n[2/4] Escritório Contábil")
    gerar_contabilidade()

    print("\n[3/4] Clínica Estética")
    gerar_clinica()

    print("\n[4/4] Barbearia")
    # Importa e roda o script da barbearia
    import subprocess
    subprocess.run(["python3", "gerar_barbearia.py"], check=False)

    print("\n✓ Todos os CSVs gerados em ./dados/")
