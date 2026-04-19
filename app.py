"""
Pulse — Demo Dashboard
O pulso do seu negócio, no seu bolso.

Arquitetura:
  - Tela inicial: escolha do perfil
  - Dashboard específico por vertical
  - Mobile-first
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

# WhatsApp do Natan (substituir pelo seu número real)
WHATSAPP = "5561999999999"

# Paleta refinada
VERDE = "#10b981"
VERDE_CLARO = "#34d399"
VERDE_ESCURO = "#047857"
AZUL = "#3b82f6"
VERMELHO = "#ef4444"
AMBAR = "#f59e0b"
ROXO = "#8b5cf6"
CINZA_TEXTO = "#64748b"
FUNDO = "#f8fafc"

# ═══════════════════════════════════════════════════════════════
# CSS GLOBAL — VISUAL APP MOBILE PREMIUM
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f8fafc;
    }

    header[data-testid="stHeader"] {
        background: transparent;
        height: 0;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 480px !important;
    }

    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif;
        color: #0f172a;
        letter-spacing: -0.02em;
    }

    /* ───── KPI Card ───── */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: none;
        border-radius: 20px;
        padding: 1rem 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.2s;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.1);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: #047857 !important;
        font-size: 1.55rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
    }

    /* ───── Botões ───── */
    .stButton button {
        background: #10b981;
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.7rem 1.2rem;
        font-weight: 600;
        font-size: 0.95rem;
        width: 100%;
        transition: all 0.2s;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
    }
    .stButton button:hover {
        background: #059669;
        transform: translateY(-1px);
        box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
    }

    .stButton button[kind="secondary"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        color: #0f172a;
        box-shadow: none;
    }

    /* ───── Tabs ───── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
        justify-content: space-between;
    }
    .stTabs [data-baseweb="tab"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.45rem 0.7rem;
        font-weight: 500;
        font-size: 0.78rem;
        color: #475569;
        flex: 1;
        text-align: center;
    }
    .stTabs [aria-selected="true"] {
        background: #10b981 !important;
        color: white !important;
        border-color: #10b981 !important;
    }

    /* ───── DataFrame limpo ───── */
    div[data-testid="stDataFrame"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        overflow: hidden;
    }
    div[data-testid="stDataFrame"] div {
        background: #ffffff !important;
        color: #0f172a !important;
    }
    div[data-testid="stDataFrame"] div[role="columnheader"] {
        background: #f8fafc !important;
        color: #475569 !important;
        font-weight: 600 !important;
    }

    /* ───── Splash Cards ───── */
    .perfil-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 14px;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .perfil-card:hover {
        border-color: #10b981;
        box-shadow: 0 12px 24px rgba(16, 185, 129, 0.12);
        transform: translateY(-2px);
    }
    .perfil-icon {
        font-size: 2.2rem;
        margin-bottom: 8px;
    }
    .perfil-titulo {
        font-weight: 700;
        font-size: 1.05rem;
        color: #0f172a;
        margin-bottom: 4px;
    }
    .perfil-desc {
        font-size: 0.85rem;
        color: #64748b;
        line-height: 1.4;
    }

    /* ───── Logo Pulse ───── */
    .pulse-logo {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #047857 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-align: center;
    }
    .pulse-slogan {
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 1.8rem;
        font-weight: 400;
    }

    .demo-badge {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #10b981;
        color: #047857;
        padding: 4px 10px;
        border-radius: 40px;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }

    .cta-whatsapp {
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white !important;
        padding: 14px 24px;
        border-radius: 60px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 8px 20px rgba(37, 211, 102, 0.3);
        margin: 12px 0;
    }

    .info-box {
        background: #ecfdf5;
        border-left: 3px solid #10b981;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 12px 0;
        font-size: 0.85rem;
        color: #064e3b;
    }

    .alerta-item {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #f59e0b;
        border-radius: 14px;
        padding: 12px 14px;
        margin-bottom: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .alerta-item.urgente {
        border-left-color: #ef4444;
    }
    .alerta-item.ok {
        border-left-color: #10b981;
    }

    .dash-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding: 8px 0;
        border-bottom: 1px solid #e2e8f0;
    }
    .dash-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
    }
    .dash-subtitle {
        font-size: 0.78rem;
        color: #64748b;
    }

    /* Gráficos com borda arredondada */
    .js-plotly-plot {
        border-radius: 20px !important;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# ESTADO DA SESSÃO
# ═══════════════════════════════════════════════════════════════
if "perfil" not in st.session_state:
    st.session_state.perfil = None

# ═══════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ═══════════════════════════════════════════════════════════════
def formatar_brl(valor):
    """Formata número em R$ brasileiro."""
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
    <div style="text-align: center; color: #94a3b8; font-size: 0.75rem;">
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

def layout_chart(altura=280):
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(248,250,252,0.5)",
        "font": {"family": "Inter", "color": "#0f172a", "size": 11},
        "xaxis": {
            "gridcolor": "#e2e8f0",
            "linecolor": "#cbd5e1",
            "tickfont": {"color": "#475569", "size": 10},
        },
        "yaxis": {
            "gridcolor": "#e2e8f0",
            "linecolor": "#cbd5e1",
            "tickfont": {"color": "#475569", "size": 10},
        },
        "margin": {"t": 30, "b": 40, "l": 40, "r": 20},
        "height": altura,
        "hoverlabel": {"bgcolor": "white", "font": {"color": "#0f172a"}},
    }

def metric_card(label, value, delta, sparkline_data):
    """Exibe um KPI com sparkline embutido."""
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
# GERADORES DE DADOS SINTÉTICOS (Substitui os CSVs)
# ═══════════════════════════════════════════════════════════════
def gerar_dados_corretora(mes_ref="Jun"):
    np.random.seed(42)
    meses_map = {"Jan":1, "Fev":2, "Mar":3, "Abr":4, "Mai":5, "Jun":6,
                 "Jul":7, "Ago":8, "Set":9, "Out":10, "Nov":11, "Dez":12}
    mes_num = meses_map.get(mes_ref, 6)
    base_clientes = 180 + mes_num * 10

    clientes = [f"Cliente {i}" for i in range(1, base_clientes+1)]
    ramos = ["Auto", "Vida", "Residencial", "Empresarial", "Saúde"]
    seguradoras = ["Porto Seguro", "Bradesco", "SulAmérica", "Allianz", "Mapfre"]
    status_opts = ["Ativo", "Vencendo", "Cancelado", "Pendente"]
    pesos_status = [0.7, 0.15, 0.1, 0.05]

    dados = []
    for i, cliente in enumerate(clientes):
        status = np.random.choice(status_opts, p=pesos_status)
        ramo = np.random.choice(ramos)
        premio = np.random.uniform(800, 8000) if ramo != "Vida" else np.random.uniform(200, 2000)
        comissao_anual = premio * np.random.uniform(0.05, 0.20)
        dias_renovacao = np.random.randint(-30, 120) if status == "Ativo" else np.random.randint(-10, 60)
        dados.append({
            "Cliente": cliente,
            "Ramo": ramo,
            "Seguradora": np.random.choice(seguradoras),
            "Status": status,
            "Premio_Anual": round(premio, 2),
            "Comissao_Anual": round(comissao_anual, 2),
            "Comissao_Mensal": round(comissao_anual / 12, 2),
            "Dias_Para_Renovacao": dias_renovacao
        })
    df = pd.DataFrame(dados)

    # Evolução
    meses_ano = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    evolucao = []
    comissao_base = 8000
    for i, mes in enumerate(meses_ano):
        sazonal = 1.0 + 0.2 * np.sin((i-3)*np.pi/6)  # pico em Mar/Set
        tendencia = 1.0 + i*0.03
        comissao = comissao_base * sazonal * tendencia * np.random.uniform(0.95, 1.05)
        novos = int(12 + i*1.5 + np.random.randint(-3,5))
        cancel = int(5 + i*0.3 + np.random.randint(-2,3))
        evolucao.append({
            "Mes": mes,
            "Comissao_Total": round(comissao, 2),
            "Novos_Contratos": novos,
            "Cancelamentos": cancel
        })
    df_evo = pd.DataFrame(evolucao)
    return df, df_evo

def gerar_dados_contabil():
    np.random.seed(43)
    empresas = [f"Empresa {i}" for i in range(1, 61)]
    regimes = ["Simples Nacional", "Lucro Presumido", "Lucro Real", "MEI"]
    status_fech = ["Entregue", "Pendente", "Atrasado"]
    pesos = [0.6, 0.25, 0.15]
    dados = []
    for emp in empresas:
        regime = np.random.choice(regimes, p=[0.5, 0.2, 0.1, 0.2])
        honorario = np.random.uniform(400, 3500)
        status = np.random.choice(status_fech, p=pesos)
        dias = np.random.randint(-5, 20) if status != "Entregue" else np.random.randint(-30, 0)
        dados.append({
            "Empresa": emp,
            "Regime_Tributario": regime,
            "Honorario_Mensal": round(honorario, 2),
            "Status_Fechamento": status,
            "Dias_Para_Entrega": dias,
            "Contato": f"contato{emp[-2:]}@email.com"
        })
    df = pd.DataFrame(dados)

    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    prod = []
    horas_base = 120
    for i, mes in enumerate(meses):
        horas = horas_base * (1 + 0.05*i) * np.random.uniform(0.9, 1.1)
        receita = 12000 * (1 + 0.03*i) * np.random.uniform(0.95, 1.05)
        prod.append({"Mes": mes, "Horas_Fechamento": round(horas, 1), "Receita_Honorarios": round(receita, 2)})
    df_prod = pd.DataFrame(prod)
    return df, df_prod

def gerar_dados_clinica():
    np.random.seed(44)
    pacientes = [f"Paciente {i}" for i in range(1, 151)]
    procedimentos = ["Limpeza de Pele", "Botox", "Preenchimento", "Massagem", "Depilação a Laser", "Peeling"]
    profissionais = ["Dra. Ana", "Dra. Carla", "Dr. Paulo", "Dra. Fernanda"]
    status_opts = ["Realizado", "Agendado", "Cancelado"]
    pesos = [0.7, 0.2, 0.1]

    dados = []
    hoje = datetime.now()
    for _ in range(300):
        data = hoje - timedelta(days=np.random.randint(0, 60))
        paciente = np.random.choice(pacientes)
        proc = np.random.choice(procedimentos)
        prof = np.random.choice(profissionais)
        valor = np.random.uniform(150, 1200)
        status = np.random.choice(status_opts, p=pesos)
        dados.append({
            "Data": data,
            "Paciente": paciente,
            "Procedimento": proc,
            "Profissional": prof,
            "Valor": round(valor, 2),
            "Status": status,
            "Forma_Pagamento": np.random.choice(["PIX", "Cartão", "Dinheiro"])
        })
    df = pd.DataFrame(dados)

    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    evo = []
    rec_base = 28000
    for i, mes in enumerate(meses):
        rec = rec_base * (1 + 0.03*i) * np.random.uniform(0.9, 1.1)
        ticket = rec / (130 + i*5)
        evo.append({"Mes": mes, "Receita": round(rec,2), "Ticket_Medio": round(ticket,2)})
    df_evo = pd.DataFrame(evo)
    return df, df_evo

def gerar_dados_barbearia():
    np.random.seed(45)
    clientes = [f"Cliente {i}" for i in range(1, 201)]
    servicos = ["Corte", "Barba", "Sobrancelha", "Corte + Barba", "Hidratação"]
    barbeiros = ["João", "Pedro", "Lucas", "Mateus", "André"]
    status_opts = ["Realizado", "Agendado", "Cancelado"]
    pesos = [0.75, 0.2, 0.05]

    dados = []
    hoje = datetime.now()
    for _ in range(500):
        data = hoje - timedelta(days=np.random.randint(0, 90))
        cliente = np.random.choice(clientes)
        serv = np.random.choice(servicos)
        barb = np.random.choice(barbeiros)
        valor = np.random.uniform(35, 120)
        comissao_pct = 0.4 if barb in ["João", "Pedro"] else 0.35
        comissao = valor * comissao_pct
        gorjeta = np.random.choice([0, 5, 10, 15], p=[0.5, 0.3, 0.15, 0.05])
        status = np.random.choice(status_opts, p=pesos)
        telefone = f"1199999{np.random.randint(1000,9999)}"
        dados.append({
            "Data": data,
            "Cliente": cliente,
            "Servico": serv,
            "Barbeiro": barb,
            "Valor": round(valor, 2),
            "Comissao_Barbeiro": round(comissao, 2),
            "Gorjeta": gorjeta,
            "Status": status,
            "Telefone": telefone
        })
    df = pd.DataFrame(dados)

    # Produtos
    produtos = ["Pomada", "Shampoo", "Óleo Barba", "Cera", "Perfume"]
    prod_data = []
    for _ in range(200):
        data = hoje - timedelta(days=np.random.randint(0, 90))
        prod = np.random.choice(produtos)
        qtd = np.random.randint(1, 4)
        preco_unit = np.random.uniform(25, 90)
        receita = qtd * preco_unit
        lucro = receita * 0.45
        prod_data.append({
            "Data": data,
            "Produto": prod,
            "Quantidade": qtd,
            "Preco_Unitario": round(preco_unit,2),
            "Receita_Total": round(receita,2),
            "Lucro_Bruto": round(lucro,2)
        })
    df_prod = pd.DataFrame(prod_data)

    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    evo = []
    rec_serv_base = 18000
    rec_prod_base = 4000
    for i, mes in enumerate(meses):
        rec_serv = rec_serv_base * (1 + 0.02*i) * np.random.uniform(0.9,1.1)
        rec_prod = rec_prod_base * (1 + 0.03*i) * np.random.uniform(0.9,1.1)
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
    st.markdown('<p class="pulse-slogan">O pulso do seu negócio, no seu bolso.</p>', unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align: center; color: #475569; font-size: 0.92rem; margin-bottom: 20px;">
        Escolha seu segmento para ver uma demonstração.<br>
        <span style="font-size: 0.78rem; color: #94a3b8;">Dados fictícios, estrutura real.</span>
    </p>
    """, unsafe_allow_html=True)

    perfis = [
        ("🛡️", "Sou Corretora de Seguros", "Carteira, comissões, renovações e alertas de vencimento.", "corretora"),
        ("📊", "Sou Escritório Contábil", "Gestão de carteira, fechamentos mensais e produtividade.", "contabil"),
        ("💚", "Sou Clínica Estética", "Agenda, procedimentos, receita e performance dos profissionais.", "clinica"),
        ("💈", "Sou Barbearia", "Agenda, comissão dos barbeiros, venda de produtos e clientes recorrentes.", "barbearia")
    ]

    for icon, titulo, desc, perfil in perfis:
        st.markdown(f"""
        <div class="perfil-card">
            <div class="perfil-icon">{icon}</div>
            <div class="perfil-titulo">{titulo}</div>
            <div class="perfil-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Ver demo para {titulo.split()[-1]}", key=f"btn_{perfil}"):
            st.session_state.perfil = perfil
            st.rerun()
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-top: 32px; padding-top: 20px;
                border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 0.75rem;">
        Desenvolvido por <strong style="color: #059669;">Natan Souza</strong><br>
        Consultoria em Dados e Inteligência Comercial
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: CORRETORA
# ═══════════════════════════════════════════════════════════════
def dash_corretora():
    st.markdown("""
    <div class="dash-header">
        <div>
            <div class="dash-title">🛡️ Pulse • Corretora</div>
            <div class="dash-subtitle">Demo para Corretoras de Seguros</div>
        </div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    # Filtro de período
    col1, col2 = st.columns(2)
    with col1:
        mes_selecionado = st.selectbox("Mês", ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"], index=5)
    with col2:
        ano_selecionado = st.selectbox("Ano", ["2025", "2026"], index=1)

    # Gerar dados baseados no mês (simula filtro real)
    df, df_evo = gerar_dados_corretora(mes_selecionado)

    info_dados_ficticios()

    # Insight contextual
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                border-radius: 16px; padding: 16px; margin: 16px 0; border: 1px solid #a7f3d0;">
        <span style="font-size: 1.2rem;">💡</span> 
        <strong style="font-size: 1rem; color: #064e3b;">Insight de {mes_selecionado}:</strong> 
        <span style="color: #047857;">
            Sua taxa de renovação está 8% acima da média. O ticket médio subiu devido ao aumento de apólices de Vida.
        </span>
        <div style="margin-top: 8px; font-size: 0.8rem; color: #065f46;">
            ⚡ Ação: Foco em Auto — concorrência aumentou preços. Oportunidade de cross-sell.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs com sparklines
    ativos = df[df["Status"] == "Ativo"]
    comissao_mensal = ativos["Comissao_Mensal"].sum()
    renovacoes_30d = df[(df["Dias_Para_Renovacao"] >= 0) & (df["Dias_Para_Renovacao"] <= 30)]
    ticket = comissao_mensal / len(ativos) if len(ativos) > 0 else 0

    # Dados para sparkline (últimos 6 meses da evolução)
    spark_comissao = df_evo["Comissao_Total"].tail(6).tolist()
    spark_ativos = [len(ativos) + i*2 for i in range(-3,3)]  # simulado

    c1, c2 = st.columns(2)
    with c1:
        metric_card("CARTEIRA ATIVA", formatar_inteiro_br(len(ativos)), "+12 vs mês ant.", spark_ativos)
    with c2:
        metric_card("COMISSÃO / MÊS", formatar_brl(comissao_mensal), "+8%", spark_comissao)

    c3, c4 = st.columns(2)
    with c3:
        st.metric("VENCENDO EM 30d", len(renovacoes_30d))
    with c4:
        st.metric("TICKET MÉDIO", formatar_brl(ticket))

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["📈 Evolução", "🔔 Alertas", "🎯 Mix", "📋 Carteira"])

    with t1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_evo["Mes"], y=df_evo["Comissao_Total"],
            mode="lines+markers", line=dict(color=VERDE, width=3),
            fill="tozeroy", fillcolor="rgba(16,185,129,0.15)",
        ))
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Novos", x=df_evo["Mes"], y=df_evo["Novos_Contratos"], marker_color=VERDE))
        fig2.add_trace(go.Bar(name="Cancelamentos", x=df_evo["Mes"], y=df_evo["Cancelamentos"], marker_color=VERMELHO))
        fig2.update_layout(**layout_chart(240), barmode="group")
        st.plotly_chart(fig2, use_container_width=True)

    with t2:
        urgentes = df[df["Dias_Para_Renovacao"].between(0, 15)].sort_values("Dias_Para_Renovacao")
        if not urgentes.empty:
            st.markdown("**Vencendo nos próximos 15 dias:**")
            for _, row in urgentes.head(8).iterrows():
                urgencia = "urgente" if row["Dias_Para_Renovacao"] <= 7 else ""
                st.markdown(f"""
                <div class="alerta-item {urgencia}">
                    <div style="display: flex; justify-content: space-between;">
                        <div><strong>{row['Cliente']}</strong><br><span style="font-size:0.78rem;">{row['Ramo']} • {row['Seguradora']}</span></div>
                        <div style="text-align:right;"><strong style="color:#ef4444;">{int(row['Dias_Para_Renovacao'])} dias</strong><br><span style="font-size:0.78rem;">{formatar_brl(row['Premio_Anual'])}</span></div>
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
        st.dataframe(df_view[["Cliente", "Ramo", "Seguradora", "Status"]].head(20), use_container_width=True, hide_index=True)

    st.markdown("---")
    cta_whatsapp("Oi Natan! Vi o demo do Pulse para corretoras e quero conversar.")
    botao_voltar()


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: CONTÁBIL
# ═══════════════════════════════════════════════════════════════
def dash_contabil():
    st.markdown("""
    <div class="dash-header">
        <div><div class="dash-title">📊 Pulse • Contábil</div><div class="dash-subtitle">Demo para Escritórios</div></div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    mes_selecionado = st.selectbox("Mês", ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"], index=5, key="mes_cont")
    df, df_prod = gerar_dados_contabil()
    info_dados_ficticios()

    # Insight
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border-radius:16px; padding:16px; margin:16px 0;">
        💡 <strong>Insight de {mes_selecionado}:</strong> 82% das entregas dentro do prazo. Clientes do Simples com maior risco de atraso.
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

    t1, t2, t3 = st.tabs(["📈 Produtividade", "⚠️ Atrasados", "📋 Carteira"])
    with t1:
        fig = go.Figure(go.Scatter(x=df_prod["Mes"], y=df_prod["Horas_Fechamento"], mode="lines+markers", line=dict(color=VERDE, width=3), fill="tozeroy"))
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        atrasados_df = df[df["Status_Fechamento"]=="Atrasado"]
        for _, row in atrasados_df.head(6).iterrows():
            st.markdown(f"""
            <div class="alerta-item urgente"><strong>{row['Empresa']}</strong><br><span style="font-size:0.78rem;">{row['Regime_Tributario']} • {row['Dias_Para_Entrega']} dias</span></div>
            """, unsafe_allow_html=True)

    with t3:
        st.dataframe(df[["Empresa", "Regime_Tributario", "Status_Fechamento"]], use_container_width=True, hide_index=True)

    cta_whatsapp("Oi Natan! Vi o demo do Pulse para contabilidade.")
    botao_voltar()


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: CLÍNICA
# ═══════════════════════════════════════════════════════════════
def dash_clinica():
    st.markdown("""
    <div class="dash-header">
        <div><div class="dash-title">💚 Pulse • Clínica</div><div class="dash-subtitle">Demo para Clínicas Estéticas</div></div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    df, df_evo = gerar_dados_clinica()
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

    t1, t2 = st.tabs(["📈 Receita", "⭐ Top Procedimentos"])
    with t1:
        fig = go.Figure(go.Bar(x=df_evo["Mes"], y=df_evo["Receita"], marker_color=VERDE))
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        top = realizados.groupby("Procedimento")["Valor"].sum().sort_values(ascending=True).tail(6)
        fig = go.Figure(go.Bar(y=top.index, x=top.values, orientation="h", marker_color=VERDE))
        fig.update_layout(**layout_chart(320))
        st.plotly_chart(fig, use_container_width=True)

    cta_whatsapp("Oi Natan! Vi o demo do Pulse para clínicas.")
    botao_voltar()


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: BARBEARIA
# ═══════════════════════════════════════════════════════════════
def dash_barbearia():
    st.markdown("""
    <div class="dash-header">
        <div><div class="dash-title">💈 Pulse • Barbearia</div><div class="dash-subtitle">Demo para Barbearias</div></div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    df, df_prod, df_evo = gerar_dados_barbearia()
    info_dados_ficticios()

    hoje = datetime.now()
    realizados = df[df["Status"]=="Realizado"]
    mes_atual = realizados[realizadoss["Data"] >= hoje - timedelta(days=30)]
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

    t1, t2 = st.tabs(["💰 Comissões", "🛍️ Produtos"])
    with t1:
        comissao_semana = mes_atual.groupby("Barbeiro")["Comissao_Barbeiro"].sum().reset_index()
        fig = go.Figure(go.Bar(x=comissao_semana["Comissao_Barbeiro"], y=comissao_semana["Barbeiro"], orientation="h", marker_color=VERDE))
        fig.update_layout(**layout_chart(260))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        top_prod = df_prod.groupby("Produto")["Receita_Total"].sum().sort_values(ascending=True).tail(5)
        fig = go.Figure(go.Bar(y=top_prod.index, x=top_prod.values, orientation="h", marker_color=AZUL))
        fig.update_layout(**layout_chart(260))
        st.plotly_chart(fig, use_container_width=True)

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
