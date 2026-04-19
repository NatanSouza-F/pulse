"""
Pulse — Demo Dashboard Premium
O pulso do seu negócio, no seu bolso.

Arquitetura:
  - Tela inicial: escolha do perfil
  - Dashboard específico por vertical (5-6 abas)
  - Mobile-first, interativo e com dados realistas
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Pulse • Demo",
    page_icon="💚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ⚙️ Substitua pelo seu número de WhatsApp (com DDD)
WHATSAPP = "5561999999999"

# Paleta de cores profissional
VERDE = "#10b981"
VERDE_CLARO = "#34d399"
VERDE_ESCURO = "#047857"
AZUL = "#3b82f6"
VERMELHO = "#ef4444"
AMBAR = "#f59e0b"
ROXO = "#8b5cf6"
CINZA = "#64748b"
FUNDO = "#f8fafc"

# ═══════════════════════════════════════════════════════════════
# CSS GLOBAL – ALTO CONTRASTE + ANIMAÇÃO
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #f8fafc; }
    header[data-testid="stHeader"] { background: transparent; height: 0; }
    .block-container { padding: 1rem !important; max-width: 480px !important; }
    h1, h2, h3, h4, p, span, div { color: #0f172a; }

    /* ANIMAÇÃO DE ÍCONES */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
        50% { transform: translateY(-8px) rotate(8deg); opacity: 1; }
        100% { transform: translateY(0px) rotate(0deg); opacity: 0.7; }
    }
    .icon-carousel {
        display: flex; justify-content: center; align-items: center;
        gap: 20px; margin-bottom: 8px; height: 50px; overflow: hidden;
    }
    .carousel-icon {
        font-size: 2.2rem; animation: float 4s ease-in-out infinite;
        display: inline-block; filter: drop-shadow(0 4px 6px rgba(16,185,129,0.15));
    }
    .carousel-icon:nth-child(1) { animation-delay: 0s; }
    .carousel-icon:nth-child(2) { animation-delay: 1.5s; }
    .carousel-icon:nth-child(3) { animation-delay: 3s; }

    /* KPI Cards */
    [data-testid="stMetric"] {
        background: #ffffff; border: none; border-radius: 20px;
        padding: 1rem 1rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    [data-testid="stMetricLabel"] {
        color: #0f172a !important; font-size: 0.7rem !important;
        font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: #047857 !important; font-size: 1.5rem !important; font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] { color: #0f172a !important; }

    /* Botões */
    .stButton button {
        background: #10b981; color: white; border: none; border-radius: 14px;
        padding: 0.7rem 1.2rem; font-weight: 600; font-size: 0.95rem; width: 100%;
        box-shadow: 0 2px 4px rgba(16,185,129,0.2);
    }
    .stButton button[kind="secondary"] {
        background: #ffffff; border: 1px solid #e2e8f0; color: #0f172a; box-shadow: none;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background: transparent; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px;
        padding: 0.45rem 0.7rem; font-weight: 500; font-size: 0.7rem;
        color: #0f172a !important; flex: 1 0 auto; text-align: center;
    }
    .stTabs [aria-selected="true"] {
        background: #10b981 !important; color: white !important; border-color: #10b981 !important;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border-radius: 16px !important; overflow: hidden; border: 1px solid #e2e8f0 !important;
    }
    div[data-testid="stDataFrame"] * { color: #0f172a !important; }

    /* Cards customizados */
    .perfil-card {
        background: #fff; border: 1px solid #e2e8f0; border-radius: 20px;
        padding: 1.5rem; margin-bottom: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .pulse-logo {
        font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(135deg, #047857 0%, #10b981 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin: 0;
    }
    .demo-badge {
        background: rgba(16,185,129,0.1); border: 1px solid #10b981;
        color: #047857; padding: 4px 10px; border-radius: 40px;
        font-size: 0.7rem; font-weight: 600;
    }
    .cta-whatsapp {
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white !important; padding: 14px 24px; border-radius: 60px;
        text-decoration: none; font-weight: 600; display: inline-block;
        box-shadow: 0 8px 20px rgba(37,211,102,0.3); margin: 12px 0;
    }
    .info-box {
        background: #ecfdf5; border-left: 3px solid #10b981;
        padding: 12px 16px; border-radius: 12px; margin: 12px 0;
        color: #064e3b !important;
    }
    .insight-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-radius: 16px; padding: 16px; margin: 16px 0;
        border: 1px solid #a7f3d0; color: #064e3b !important;
    }
    .alerta-item {
        background: #f8fafc; border-left: 4px solid #f59e0b; border-radius: 14px;
        padding: 12px 14px; margin-bottom: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        color: #0f172a !important;
    }
    .alerta-item.urgente { border-left-color: #ef4444; }
    .alerta-item.ok { border-left-color: #10b981; }
    .dash-header {
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 1rem; padding: 8px 0; border-bottom: 1px solid #e2e8f0;
    }
    .dash-title { font-size: 1.1rem; font-weight: 700; color: #0f172a; }
    .dash-subtitle { color: #475569 !important; }

    /* Gráficos */
    .js-plotly-plot {
        border-radius: 20px !important; overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    .plotly .xtick, .plotly .ytick, .plotly .legendtext, .plotly .gtitle {
        fill: #0f172a !important; font-weight: 500 !important;
    }
    .main-svg { background: transparent !important; }
</style>

<div class="icon-carousel">
    <span class="carousel-icon">📊</span>
    <span class="carousel-icon">💚</span>
    <span class="carousel-icon">🛡️</span>
    <span class="carousel-icon">💈</span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# ESTADO DA SESSÃO & FUNÇÕES AUXILIARES
# ═══════════════════════════════════════════════════════════════
if "perfil" not in st.session_state:
    st.session_state.perfil = None

def formatar_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_inteiro_br(valor):
    return f"{int(valor):,}".replace(",", ".")

def botao_voltar():
    if st.button("← Voltar para escolha de perfil", use_container_width=True, type="secondary"):
        st.session_state.perfil = None
        st.rerun()

def cta_whatsapp(texto_msg):
    msg_codificada = texto_msg.replace(" ", "%20").replace("\n", "%0A")
    link = f"https://wa.me/{WHATSAPP}?text={msg_codificada}"
    st.markdown(f"""
    <div style="text-align: center; margin: 16px 0;">
        <a href="{link}" target="_blank" class="cta-whatsapp">
            💬 &nbsp;Quero isso pra minha empresa
        </a>
    </div>
    <div style="text-align: center; color: #475569; font-size: 0.75rem;">
        Primeira conversa grátis • Sem compromisso
    </div>
    """, unsafe_allow_html=True)

def info_dados_ficticios():
    st.markdown("""
    <div class="info-box">
        <strong>💡 Demo com dados fictícios.</strong><br>
        Seus dados reais, assim, em 3 semanas.
    </div>
    """, unsafe_allow_html=True)

def layout_chart(altura=280, yaxis_opts=None):
    base = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(248,250,252,0.5)",
        "font": {"family": "Inter", "color": "#0f172a", "size": 11},
        "xaxis": {"gridcolor": "#e2e8f0", "tickfont": {"color": "#0f172a", "size": 10}},
        "yaxis": {"gridcolor": "#e2e8f0", "tickfont": {"color": "#0f172a", "size": 10}},
        "margin": {"t": 30, "b": 40, "l": 40, "r": 20},
        "height": altura,
        "hoverlabel": {"bgcolor": "white", "font": {"color": "#0f172a"}},
    }
    if yaxis_opts:
        base["yaxis"].update(yaxis_opts)
    return base

def metric_card(label, value, delta, sparkline_data):
    cols = st.columns([3, 1])
    with cols[0]:
        st.metric(label=label, value=value, delta=delta)
    with cols[1]:
        fig_spark = go.Figure(go.Scatter(
            y=sparkline_data, mode='lines', line=dict(color=VERDE, width=2),
            fill='tozeroy', fillcolor='rgba(16,185,129,0.15)'
        ))
        fig_spark.update_layout(
            margin=dict(l=0, r=0, t=5, b=0), height=50, width=80,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False), yaxis=dict(visible=False)
        )
        st.plotly_chart(fig_spark, use_container_width=False, config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════
# GERADORES DE DADOS (COM MAIS AGENDAMENTOS FUTUROS)
# ═══════════════════════════════════════════════════════════════
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

def gerar_dados_corretora(mes_ref="Jun", ano_ref="2026"):
    np.random.seed(42 + MESES.index(mes_ref))
    base_clientes = 200 + MESES.index(mes_ref) * 8
    clientes = [f"Cliente {i}" for i in range(1, base_clientes+1)]
    ramos = ["Auto", "Vida", "Residencial", "Empresarial", "Saúde"]
    seguradoras = ["Porto Seguro", "Bradesco", "SulAmérica", "Allianz", "Mapfre"]

    dados = []
    for cliente in clientes:
        status = np.random.choice(["Ativo", "Vencendo", "Cancelado"], p=[0.7, 0.2, 0.1])
        ramo = np.random.choice(ramos)
        premio = np.random.uniform(800, 8000)
        comissao_anual = premio * np.random.uniform(0.05, 0.20)
        dias = np.random.randint(-30, 120)
        dados.append({
            "Cliente": cliente, "Ramo": ramo, "Seguradora": np.random.choice(seguradoras),
            "Status": status, "Premio_Anual": round(premio,2),
            "Comissao_Anual": round(comissao_anual,2),
            "Comissao_Mensal": round(comissao_anual/12,2),
            "Dias_Para_Renovacao": dias
        })
    df = pd.DataFrame(dados)

    evolucao = []
    for i, mes in enumerate(MESES):
        comissao = 8000 * (1 + 0.03*i) * np.random.uniform(0.9,1.1)
        novos = int(12 + i*1.5 + np.random.randint(-3,5))
        cancel = int(5 + i*0.3 + np.random.randint(-2,3))
        evolucao.append({"Mes": mes, "Comissao_Total": round(comissao,2),
                         "Novos_Contratos": novos, "Cancelamentos": cancel})
    df_evo = pd.DataFrame(evolucao)
    return df, df_evo

def gerar_dados_contabil(mes_ref="Jun", ano_ref="2026"):
    np.random.seed(43 + MESES.index(mes_ref))
    empresas = [f"Empresa {i}" for i in range(1, 61)]
    regimes = ["Simples Nacional", "Lucro Presumido", "Lucro Real", "MEI"]
    dados = []
    for emp in empresas:
        regime = np.random.choice(regimes, p=[0.5,0.2,0.1,0.2])
        honorario = np.random.uniform(400, 3500)
        status = np.random.choice(["Entregue", "Pendente", "Atrasado"], p=[0.6,0.25,0.15])
        dias = np.random.randint(-5,20) if status != "Entregue" else np.random.randint(-30,0)
        dados.append({
            "Empresa": emp, "Regime_Tributario": regime,
            "Honorario_Mensal": round(honorario,2),
            "Status_Fechamento": status, "Dias_Para_Entrega": dias,
            "Contato": f"contato{emp[-2:]}@email.com"
        })
    df = pd.DataFrame(dados)

    prod = []
    for i, mes in enumerate(MESES):
        horas = 120 * (1 + 0.05*i) * np.random.uniform(0.9,1.1)
        receita = 12000 * (1 + 0.03*i) * np.random.uniform(0.95,1.05)
        prod.append({"Mes": mes, "Horas_Fechamento": round(horas,1), "Receita_Honorarios": round(receita,2)})
    df_prod = pd.DataFrame(prod)
    return df, df_prod

def gerar_dados_clinica(mes_ref="Jun", ano_ref="2026"):
    np.random.seed(44 + MESES.index(mes_ref))
    pacientes = [f"Paciente {i}" for i in range(1, 151)]
    procedimentos = ["Limpeza de Pele", "Botox", "Preenchimento", "Massagem", "Depilação a Laser", "Peeling"]
    profissionais = ["Dra. Ana", "Dra. Carla", "Dr. Paulo", "Dra. Fernanda"]
    dados = []
    hoje = datetime.now()
    for _ in range(400):  # Mais dados
        # 30% de chance de ser agendado para o futuro
        if np.random.rand() < 0.3:
            data = hoje + timedelta(days=np.random.randint(1, 30))
            status = "Agendado"
        else:
            data = hoje - timedelta(days=np.random.randint(0, 60))
            status = np.random.choice(["Realizado", "Cancelado"], p=[0.8, 0.2])
        valor = np.random.uniform(150, 1200)
        dados.append({
            "Data": data, "Paciente": np.random.choice(pacientes),
            "Procedimento": np.random.choice(procedimentos),
            "Profissional": np.random.choice(profissionais),
            "Valor": round(valor,2), "Status": status,
            "Forma_Pagamento": np.random.choice(["PIX","Cartão","Dinheiro"])
        })
    df = pd.DataFrame(dados)

    evo = []
    for i, mes in enumerate(MESES):
        rec = 28000 * (1 + 0.03*i) * np.random.uniform(0.9,1.1)
        ticket = rec / (130 + i*5)
        evo.append({"Mes": mes, "Receita": round(rec,2), "Ticket_Medio": round(ticket,2)})
    df_evo = pd.DataFrame(evo)
    return df, df_evo

def gerar_dados_barbearia(mes_ref="Jun", ano_ref="2026"):
    np.random.seed(45 + MESES.index(mes_ref))
    clientes = [f"Cliente {i}" for i in range(1, 201)]
    servicos = ["Corte", "Barba", "Sobrancelha", "Corte + Barba", "Hidratação"]
    barbeiros = ["João", "Pedro", "Lucas", "Mateus", "André"]
    dados = []
    hoje = datetime.now()
    for _ in range(600):  # Mais dados
        if np.random.rand() < 0.35:  # 35% agendados futuros
            data = hoje + timedelta(days=np.random.randint(1, 30))
            status = "Agendado"
        else:
            data = hoje - timedelta(days=np.random.randint(0, 90))
            status = np.random.choice(["Realizado", "Cancelado"], p=[0.85, 0.15])
        valor = np.random.uniform(35, 120)
        comissao_pct = 0.4 if np.random.choice(barbeiros) in ["João","Pedro"] else 0.35
        comissao = valor * comissao_pct
        gorjeta = np.random.choice([0,5,10,15], p=[0.5,0.3,0.15,0.05])
        dados.append({
            "Data": data, "Cliente": np.random.choice(clientes),
            "Servico": np.random.choice(servicos), "Barbeiro": np.random.choice(barbeiros),
            "Valor": round(valor,2), "Comissao_Barbeiro": round(comissao,2),
            "Gorjeta": gorjeta, "Status": status,
            "Telefone": f"1199999{np.random.randint(1000,9999)}"
        })
    df = pd.DataFrame(dados)

    produtos = ["Pomada", "Shampoo", "Óleo Barba", "Cera", "Perfume"]
    prod_data = []
    for _ in range(200):
        data = hoje - timedelta(days=np.random.randint(0,90))
        prod = np.random.choice(produtos)
        qtd = np.random.randint(1,4)
        preco = np.random.uniform(25,90)
        receita = qtd * preco
        lucro = receita * 0.45
        prod_data.append({
            "Data": data, "Produto": prod, "Quantidade": qtd,
            "Preco_Unitario": round(preco,2), "Receita_Total": round(receita,2),
            "Lucro_Bruto": round(lucro,2)
        })
    df_prod = pd.DataFrame(prod_data)

    evo = []
    for i, mes in enumerate(MESES):
        rec_serv = 18000 * (1 + 0.02*i) * np.random.uniform(0.9,1.1)
        rec_prod = 4000 * (1 + 0.03*i) * np.random.uniform(0.9,1.1)
        atend = int(120 + i*3)
        evo.append({"Mes": mes, "Receita_Servicos": round(rec_serv,2),
                   "Receita_Produtos": round(rec_prod,2), "Atendimentos": atend})
    df_evo = pd.DataFrame(evo)
    return df, df_prod, df_evo


# ═══════════════════════════════════════════════════════════════
# TELA INICIAL
# ═══════════════════════════════════════════════════════════════
def tela_inicial():
    st.markdown('<h1 class="pulse-logo">Pulse</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#475569;">O pulso do seu negócio, no seu bolso.</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align:center; color:#0f172a; font-size:0.92rem;">
        Escolha seu segmento para ver uma demonstração.<br>
        <span style="font-size:0.78rem; color:#64748b;">Dados fictícios, estrutura real.</span>
    </p>
    """, unsafe_allow_html=True)

    perfis = [
        ("🛡️", "Sou Corretora de Seguros", "Carteira, comissões, renovações e alertas.", "corretora"),
        ("📊", "Sou Escritório Contábil", "Gestão de carteira, fechamentos e produtividade.", "contabil"),
        ("💚", "Sou Clínica Estética", "Agenda, receita e performance dos profissionais.", "clinica"),
        ("💈", "Sou Barbearia", "Agenda, comissão dos barbeiros e produtos.", "barbearia")
    ]
    for icon, titulo, desc, perfil in perfis:
        st.markdown(f"""
        <div class="perfil-card">
            <div style="font-size:2.2rem;">{icon}</div>
            <div style="font-weight:700; font-size:1.05rem; color:#0f172a;">{titulo}</div>
            <div style="font-size:0.85rem; color:#475569;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Ver demo para {titulo.split()[-1]}", key=f"btn_{perfil}"):
            st.session_state.perfil = perfil
            st.rerun()
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-top:32px; padding-top:20px; border-top:1px solid #e2e8f0; color:#64748b; font-size:0.75rem;">
        Desenvolvido por <strong style="color:#059669;">Natan Souza</strong><br>
        Consultoria em Dados e Inteligência Comercial
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: CORRETORA (5 ABAS)
# ═══════════════════════════════════════════════════════════════
def dash_corretora():
    st.markdown("""
    <div class="dash-header">
        <div><div class="dash-title">🛡️ Pulse • Corretora</div><div class="dash-subtitle">Demo para Corretoras</div></div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mes = st.selectbox("Mês", MESES, index=5, key="cor_mes")
    with col2:
        ano = st.selectbox("Ano", ["2025", "2026"], index=1, key="cor_ano")
    df, df_evo = gerar_dados_corretora(mes, ano)

    info_dados_ficticios()
    st.markdown(f"""
    <div class="insight-box">
        💡 <strong>Insight de {mes}/{ano}:</strong> Sua taxa de renovação está 8% acima da média. O ticket médio subiu devido ao aumento de apólices de Vida.<br>
        <span style="font-size:0.8rem;">⚡ Ação: Foco em Auto — concorrência aumentou preços.</span>
    </div>
    """, unsafe_allow_html=True)

    ativos = df[df["Status"] == "Ativo"]
    comissao_mensal = ativos["Comissao_Mensal"].sum()
    renovacoes_30d = df[(df["Dias_Para_Renovacao"] >= 0) & (df["Dias_Para_Renovacao"] <= 30)]
    ticket = comissao_mensal / len(ativos) if len(ativos) > 0 else 0

    spark_comissao = df_evo["Comissao_Total"].tail(6).tolist()
    spark_ativos = [len(ativos) + i*2 for i in range(-3,3)]

    c1, c2 = st.columns(2)
    with c1:
        metric_card("CARTEIRA ATIVA", formatar_inteiro_br(len(ativos)), "+12", spark_ativos)
    with c2:
        metric_card("COMISSÃO / MÊS", formatar_brl(comissao_mensal), "+8%", spark_comissao)
    c3, c4 = st.columns(2)
    with c3:
        st.metric("VENCENDO EM 30d", len(renovacoes_30d))
    with c4:
        st.metric("TICKET MÉDIO", formatar_brl(ticket))

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.tabs([
        "📈 Evolução", "🔔 Alertas", "🎯 Mix", "📋 Carteira", "🏆 Top Clientes"
    ])

    with t1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_evo["Mes"], y=df_evo["Comissao_Total"],
                                 mode="lines+markers", line=dict(color=VERDE, width=3),
                                 fill="tozeroy", fillcolor="rgba(16,185,129,0.15)"))
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Novos", x=df_evo["Mes"], y=df_evo["Novos_Contratos"], marker_color=VERDE))
        fig2.add_trace(go.Bar(name="Cancelamentos", x=df_evo["Mes"], y=df_evo["Cancelamentos"], marker_color=VERMELHO))
        fig2.update_layout(**layout_chart(240))
        st.plotly_chart(fig2, use_container_width=True)

    with t2:
        urgentes = df[df["Dias_Para_Renovacao"].between(0,15)].sort_values("Dias_Para_Renovacao")
        if not urgentes.empty:
            for _, row in urgentes.head(8).iterrows():
                urgencia = "urgente" if row["Dias_Para_Renovacao"] <= 7 else ""
                st.markdown(f"""
                <div class="alerta-item {urgencia}">
                    <div style="display:flex; justify-content:space-between;">
                        <div><strong>{row['Cliente']}</strong><br><span style="font-size:0.78rem; color:#475569;">{row['Ramo']} • {row['Seguradora']}</span></div>
                        <div style="text-align:right;"><strong style="color:#ef4444;">{int(row['Dias_Para_Renovacao'])}d</strong><br><span style="font-size:0.78rem; color:#475569;">{formatar_brl(row['Premio_Anual'])}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Sem renovações urgentes.")

    with t3:
        mix = df[df["Status"]=="Ativo"].groupby("Ramo").size().reset_index(name="total")
        fig = px.pie(mix, values="total", names="Ramo", hole=0.5, color_discrete_sequence=[VERDE, AZUL, ROXO, AMBAR])
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(**layout_chart(330))
        st.plotly_chart(fig, use_container_width=True)

    with t4:
        busca = st.text_input("🔍 Buscar cliente", key="busca_cor")
        df_view = df.copy()
        if busca:
            df_view = df_view[df_view["Cliente"].str.contains(busca, case=False)]
        st.dataframe(df_view[["Cliente", "Ramo", "Seguradora", "Status", "Premio_Anual"]].head(20),
                     use_container_width=True, hide_index=True)

    with t5:
        top_clientes = ativos.groupby("Cliente")["Premio_Anual"].sum().sort_values(ascending=False).head(10)
        fig = go.Figure(go.Bar(x=top_clientes.values, y=top_clientes.index, orientation="h",
                               marker_color=VERDE, text=top_clientes.values, textposition='outside',
                               texttemplate='%{text:.2s}'))
        fig.update_layout(**layout_chart(340, yaxis_opts={"autorange": "reversed", "tickfont": {"color": "#0f172a", "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    cta_whatsapp("Oi Natan! Vi o demo do Pulse para corretoras e quero conversar.")
    botao_voltar()


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: CONTÁBIL (6 ABAS)
# ═══════════════════════════════════════════════════════════════
def dash_contabil():
    st.markdown("""
    <div class="dash-header">
        <div><div class="dash-title">📊 Pulse • Contábil</div><div class="dash-subtitle">Demo para Escritórios</div></div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mes = st.selectbox("Mês", MESES, index=5, key="cont_mes")
    with col2:
        ano = st.selectbox("Ano", ["2025", "2026"], index=1, key="cont_ano")
    df, df_prod = gerar_dados_contabil(mes, ano)

    info_dados_ficticios()
    st.markdown(f"""
    <div class="insight-box">
        💡 <strong>Insight de {mes}/{ano}:</strong> 82% das entregas dentro do prazo. Clientes do Simples com maior risco de atraso.
    </div>
    """, unsafe_allow_html=True)

    honorarios = df["Honorario_Mensal"].sum()
    entregues = df[df["Status_Fechamento"]=="Entregue"]
    atrasados = df[df["Status_Fechamento"]=="Atrasado"]
    spark_hon = df_prod["Receita_Honorarios"].tail(6).tolist()

    c1, c2 = st.columns(2)
    with c1:
        metric_card("EMPRESAS", len(df), "+2", [58,60,61,62,61,63])
    with c2:
        metric_card("HONORÁRIOS", formatar_brl(honorarios), "+5%", spark_hon)
    c3, c4 = st.columns(2)
    with c3:
        st.metric("ENTREGUES NO PRAZO", f"{(len(entregues)/len(df))*100:.0f}%")
    with c4:
        st.metric("EM ATRASO", len(atrasados))

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "📈 Produtividade", "⚠️ Atrasados", "📋 Carteira", "🥧 Regimes", "💰 Top Clientes", "📅 Obrigações"
    ])

    with t1:
        fig = go.Figure(go.Scatter(x=df_prod["Mes"], y=df_prod["Horas_Fechamento"],
                                   mode="lines+markers", line=dict(color=VERDE, width=3), fill="tozeroy"))
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        atrasados_df = df[df["Status_Fechamento"]=="Atrasado"]
        if not atrasados_df.empty:
            for _, row in atrasados_df.head(6).iterrows():
                st.markdown(f"""
                <div class="alerta-item urgente">
                    <strong>{row['Empresa']}</strong><br>
                    <span style="font-size:0.78rem; color:#475569;">{row['Regime_Tributario']} • {row['Dias_Para_Entrega']} dias de atraso</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum cliente em atraso.")

    with t3:
        busca = st.text_input("🔍 Buscar empresa", key="busca_cont")
        df_view = df.copy()
        if busca:
            df_view = df_view[df_view["Empresa"].str.contains(busca, case=False)]
        st.dataframe(df_view[["Empresa", "Regime_Tributario", "Status_Fechamento", "Honorario_Mensal"]],
                     use_container_width=True, hide_index=True)

    with t4:
        regime_counts = df["Regime_Tributario"].value_counts().reset_index()
        regime_counts.columns = ["Regime", "Quantidade"]
        fig = px.pie(regime_counts, values="Quantidade", names="Regime", hole=0.5,
                     color_discrete_sequence=[VERDE, AZUL, ROXO, AMBAR])
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)

    with t5:
        top_hon = df.groupby("Empresa")["Honorario_Mensal"].sum().sort_values(ascending=False).head(10)
        fig = go.Figure(go.Bar(x=top_hon.values, y=top_hon.index, orientation="h",
                               marker_color=VERDE, text=top_hon.values, textposition='outside',
                               texttemplate='%{text:.2s}'))
        fig.update_layout(**layout_chart(340, yaxis_opts={"autorange": "reversed", "tickfont": {"color": "#0f172a", "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)

    with t6:
        st.markdown("**📌 Próximas obrigações fiscais**")
        obrigacoes = pd.DataFrame({
            "Obrigação": ["DASN-SIMEI", "EFD-Contribuições", "DCTF", "DIRF", "ECD"],
            "Vencimento": ["31/05", "10/06", "15/06", "20/06", "30/06"],
            "Status": ["Pendente", "Pendente", "Pendente", "Pendente", "Pendente"]
        })
        st.dataframe(obrigacoes, use_container_width=True, hide_index=True)

    st.markdown("---")
    cta_whatsapp("Oi Natan! Vi o demo do Pulse para contabilidade.")
    botao_voltar()


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: CLÍNICA (6 ABAS) – AGENDA GARANTIDA
# ═══════════════════════════════════════════════════════════════
def dash_clinica():
    st.markdown("""
    <div class="dash-header">
        <div><div class="dash-title">💚 Pulse • Clínica</div><div class="dash-subtitle">Demo para Clínicas Estéticas</div></div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mes = st.selectbox("Mês", MESES, index=5, key="cli_mes")
    with col2:
        ano = st.selectbox("Ano", ["2025", "2026"], index=1, key="cli_ano")
    df, df_evo = gerar_dados_clinica(mes, ano)

    info_dados_ficticios()
    realizados = df[df["Status"]=="Realizado"]
    receita_mes = realizados["Valor"].sum()
    ticket = realizados["Valor"].mean()
    spark_rec = df_evo["Receita"].tail(6).tolist()

    c1, c2 = st.columns(2)
    with c1:
        metric_card("RECEITA / MÊS", formatar_brl(receita_mes), "+12%", spark_rec)
    with c2:
        st.metric("ATENDIMENTOS", len(realizados))
    c3, c4 = st.columns(2)
    with c3:
        st.metric("TICKET MÉDIO", formatar_brl(ticket))
    with c4:
        st.metric("AGENDADOS", len(df[df["Status"]=="Agendado"]))

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "📈 Receita", "⭐ Top Proced.", "📅 Agenda", "👩‍⚕️ Profissionais", "🔄 Fidelização", "💳 Pagamentos"
    ])

    with t1:
        fig = go.Figure(go.Bar(x=df_evo["Mes"], y=df_evo["Receita"], marker_color=VERDE))
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        top = realizados.groupby("Procedimento")["Valor"].sum().sort_values(ascending=True).tail(6)
        fig = go.Figure(go.Bar(y=top.index, x=top.values, orientation="h",
                               marker_color=VERDE, text=top.values, textposition='outside',
                               texttemplate='%{text:.2s}'))
        fig.update_layout(**layout_chart(320, yaxis_opts={"tickfont": {"color": "#0f172a", "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)

    with t3:
        hoje = datetime.now()
        agenda = df[(df["Status"]=="Agendado") & (df["Data"] >= hoje)].sort_values("Data").head(10)
        if not agenda.empty:
            for _, row in agenda.iterrows():
                st.markdown(f"""
                <div class="alerta-item ok">
                    <div style="display:flex; justify-content:space-between;">
                        <div><strong style="color:#0f172a;">{row['Paciente']}</strong><br><span style="font-size:0.78rem; color:#475569;">{row['Procedimento']} • {row['Profissional']}</span></div>
                        <div><strong style="color:#0f172a;">{row['Data'].strftime('%d/%m %H:%M')}</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum agendamento futuro no momento.")

    with t4:
        perf = realizados.groupby("Profissional")["Valor"].sum().reset_index()
        fig = px.bar(perf, x="Profissional", y="Valor", color="Profissional", text="Valor",
                     color_discrete_sequence=[VERDE]*4)
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)

    with t5:
        freq = realizados["Paciente"].value_counts().reset_index()
        freq.columns = ["Paciente", "Visitas"]
        fig = px.histogram(freq, x="Visitas", nbins=10, color_discrete_sequence=[VERDE])
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Clientes que voltam mais vezes")

    with t6:
        pgto = realizados["Forma_Pagamento"].value_counts().reset_index()
        pgto.columns = ["Forma", "Qtd"]
        fig = px.pie(pgto, values="Qtd", names="Forma", hole=0.5, color_discrete_sequence=[VERDE, AZUL, ROXO])
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    cta_whatsapp("Oi Natan! Vi o demo do Pulse para clínicas.")
    botao_voltar()


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: BARBEARIA (6 ABAS) – AGENDA GARANTIDA
# ═══════════════════════════════════════════════════════════════
def dash_barbearia():
    st.markdown("""
    <div class="dash-header">
        <div><div class="dash-title">💈 Pulse • Barbearia</div><div class="dash-subtitle">Demo para Barbearias</div></div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        mes = st.selectbox("Mês", MESES, index=5, key="bar_mes")
    with col2:
        ano = st.selectbox("Ano", ["2025", "2026"], index=1, key="bar_ano")
    df, df_prod, df_evo = gerar_dados_barbearia(mes, ano)

    info_dados_ficticios()
    hoje = datetime.now()
    realizados = df[df["Status"]=="Realizado"]
    mes_atual = realizados[realizados["Data"] >= hoje - timedelta(days=30)]
    receita_serv = mes_atual["Valor"].sum()
    receita_prod = df_prod[df_prod["Data"] >= hoje - timedelta(days=30)]["Receita_Total"].sum()
    receita_total = receita_serv + receita_prod
    spark_rec = df_evo["Receita_Servicos"].tail(6).tolist()

    c1, c2 = st.columns(2)
    with c1:
        metric_card("RECEITA TOTAL", formatar_brl(receita_total), "+15%", spark_rec)
    with c2:
        st.metric("ATENDIMENTOS", len(mes_atual))
    c3, c4 = st.columns(2)
    with c3:
        st.metric("TICKET MÉDIO", formatar_brl(mes_atual["Valor"].mean()))
    with c4:
        st.metric("AGENDADOS", len(df[df["Status"]=="Agendado"]))

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "💰 Comissões", "🛍️ Produtos", "📅 Agenda", "👥 Clientes", "📊 Ocupação", "🏆 Serviços"
    ])

    with t1:
        comissao = mes_atual.groupby("Barbeiro")["Comissao_Barbeiro"].sum().reset_index()
        fig = go.Figure(go.Bar(x=comissao["Comissao_Barbeiro"], y=comissao["Barbeiro"],
                               orientation="h", marker_color=VERDE,
                               text=comissao["Comissao_Barbeiro"], textposition='outside',
                               texttemplate='%{text:.2s}'))
        fig.update_layout(**layout_chart(260, yaxis_opts={"tickfont": {"color": "#0f172a", "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        top_prod = df_prod.groupby("Produto")["Receita_Total"].sum().sort_values(ascending=True).tail(5)
        fig = go.Figure(go.Bar(y=top_prod.index, x=top_prod.values, orientation="h",
                               marker_color=AZUL, text=top_prod.values, textposition='outside',
                               texttemplate='%{text:.2s}'))
        fig.update_layout(**layout_chart(260, yaxis_opts={"tickfont": {"color": "#0f172a", "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)

    with t3:
        agenda = df[(df["Status"]=="Agendado") & (df["Data"] >= hoje)].sort_values("Data").head(10)
        if not agenda.empty:
            for _, row in agenda.iterrows():
                st.markdown(f"""
                <div class="alerta-item ok">
                    <div style="display:flex; justify-content:space-between;">
                        <div><strong style="color:#0f172a;">{row['Cliente']}</strong><br><span style="font-size:0.78rem; color:#475569;">{row['Servico']} • {row['Barbeiro']}</span></div>
                        <div><strong style="color:#0f172a;">{row['Data'].strftime('%d/%m %H:%M')}</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum agendamento futuro no momento.")

    with t4:
        freq = realizados["Cliente"].value_counts().reset_index().head(10)
        freq.columns = ["Cliente", "Visitas"]
        fig = px.bar(freq, x="Visitas", y="Cliente", orientation="h", color_discrete_sequence=[VERDE])
        fig.update_layout(**layout_chart(320, yaxis_opts={"autorange": "reversed", "tickfont": {"color": "#0f172a", "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)

    with t5:
        horas = ["09h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h"]
        ocupacao = np.random.randint(40, 100, size=len(horas))
        fig = go.Figure(go.Scatter(x=horas, y=ocupacao, mode="lines+markers",
                                   fill="tozeroy", line=dict(color=VERDE, width=3)))
        fig.update_layout(**layout_chart(260, yaxis_opts={"title": "Ocupação (%)"}))
        st.plotly_chart(fig, use_container_width=True)

    with t6:
        serv = realizados.groupby("Servico")["Valor"].sum().sort_values(ascending=True).tail(6)
        fig = go.Figure(go.Bar(y=serv.index, x=serv.values, orientation="h",
                               marker_color=VERDE, text=serv.values, textposition='outside',
                               texttemplate='%{text:.2s}'))
        fig.update_layout(**layout_chart(320, yaxis_opts={"tickfont": {"color": "#0f172a", "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    cta_whatsapp("Oi Natan! Vi o demo do Pulse para barbearias.")
    botao_voltar()


# ═══════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════
if st.session_state.perfil is None:
    tela_inicial()
elif st.session_state.perfil == "corretora":
    dash_corretora()
elif st.session_state.perfil == "contabil":
    dash_contabil()
elif st.session_state.perfil == "clinica":
    dash_clinica()
elif st.session_state.perfil == "barbearia":
    dash_barbearia()
