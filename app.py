"""
Pulse — Demo Dashboard v6 (Cards 100% alinhados)
Todos os cards com altura fixa de 130px, mesmo em diferentes nichos.
Gráficos de pizza sem labels internos (apenas legenda).
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
from io import BytesIO

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title="Pulse • Demo", page_icon="💚", layout="centered", initial_sidebar_state="collapsed")
WHATSAPP = "5561999999999"

# Cores
NAVY_DARK = "#0b1e2e"
NAVY_MED = "#1a2e42"
VERDE_NEON = "#00ff88"
TEXTO = "#f1f5f9"
TEXTO_MUTED = "#94a3b8"
VERMELHO = "#ef4444"
AZUL_CLARO = "#60a5fa"
ROXO = "#a855f7"
AMBAR = "#f59e0b"
ROSA = "#ec4899"
VERDE_AGUA = "#14b8a6"

pio.templates["pulse_dark"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, sans-serif", color=TEXTO, size=11),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,46,66,0.3)",
        colorway=[VERDE_NEON, AZUL_CLARO, ROXO, AMBAR, VERMELHO, ROSA, VERDE_AGUA],
    )
)
pio.templates.default = "pulse_dark"

MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

# ═══════════════════════════════════════════════════════════════
# CSS GLOBAL (cards com altura fixa)
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp {
        background: radial-gradient(ellipse at top, rgba(16,185,129,0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom, rgba(59,130,246,0.05) 0%, transparent 50%),
                    #0b1e2e;
    }
    .block-container { max-width: 480px !important; padding: 1rem !important; }

    /* Card padrão com altura fixa de 130px */
    .card-padrao {
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid rgba(0,255,136,0.2);
        border-radius: 16px;
        padding: 0.9rem 1rem;
        box-shadow: 0 4px 12px -2px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card-padrao::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        opacity: 0.7;
    }
    .card-padrao:hover {
        transform: translateY(-2px);
        border-color: rgba(0,255,136,0.4);
        box-shadow: 0 8px 20px -4px rgba(0,0,0,0.4), 0 0 30px rgba(0,255,136,0.15);
    }
    .card-label {
        color: #94a3b8;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .card-valor {
        color: #00ff88;
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        text-shadow: 0 0 15px rgba(0,255,136,0.3);
        line-height: 1.2;
    }
    .card-footer {
        color: #94a3b8;
        font-size: 0.72rem;
        margin-top: 4px;
    }
    .delta-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 40px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-left: 6px;
    }
    .delta-up { background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.3); }
    .delta-down { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
    .delta-neutro { background: rgba(148,163,184,0.15); color: #94a3b8; border: 1px solid rgba(148,163,184,0.3); }
    .tooltip-icon {
        display: inline-block;
        width: 14px; height: 14px;
        border-radius: 50%;
        background: rgba(0,255,136,0.15);
        color: #00ff88;
        text-align: center;
        font-size: 10px;
        line-height: 14px;
        cursor: help;
        margin-left: 4px;
        border: 1px solid rgba(0,255,136,0.3);
    }
    /* Força colunas com mesma altura */
    .stColumn > div { height: 100%; }
    /* Carrossel e outros elementos mantidos */
    .carousel-wrapper {
        position: relative;
        width: 100%;
        height: 180px;
        margin: 16px 0 24px 0;
        perspective: 1200px;
        overflow: hidden;
    }
    .carousel-track {
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
    }
    .carousel-card {
        position: absolute;
        top: 0;
        left: 50%;
        width: 280px;
        height: 160px;
        margin-left: -140px;
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 20px;
        padding: 20px 24px;
        box-shadow: 0 20px 40px rgba(0, 255, 136, 0.15), 0 0 0 1px rgba(0, 255, 136, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        opacity: 0;
        animation: carousel-rotate 20s infinite ease-in-out;
    }
    .carousel-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
    }
    .carousel-card:nth-child(1) { animation-delay: 0s; }
    .carousel-card:nth-child(2) { animation-delay: 5s; }
    .carousel-card:nth-child(3) { animation-delay: 10s; }
    .carousel-card:nth-child(4) { animation-delay: 15s; }
    @keyframes carousel-rotate {
        0%, 100% { opacity: 0; transform: translateX(0) rotateY(90deg) scale(0.8); }
        5% { opacity: 1; transform: translateX(0) rotateY(0deg) scale(1); }
        20% { opacity: 1; transform: translateX(0) rotateY(0deg) scale(1); }
        25% { opacity: 0; transform: translateX(-100%) rotateY(-90deg) scale(0.8); }
    }
    .carousel-label { font-size: 0.65rem; font-weight: 700; color: #00ff88 !important; letter-spacing: 0.12em; text-transform: uppercase; }
    .carousel-value { font-size: 2.2rem; font-weight: 800; color: #f1f5f9 !important; letter-spacing: -0.03em; line-height: 1; margin: 4px 0; text-shadow: 0 0 20px rgba(0, 255, 136, 0.3); }
    .carousel-delta { font-size: 0.78rem; font-weight: 600; color: #00ff88 !important; }
    .stButton button, .stDownloadButton button {
        background: linear-gradient(135deg, #10b981 0%, #00ff88 100%);
        color: #0b1e2e;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.2rem;
        font-weight: 700;
        font-size: 0.95rem;
        width: 100%;
        box-shadow: 0 4px 12px rgba(0, 255, 136, 0.25);
        transition: all 0.2s ease;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(0, 255, 136, 0.4);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background: transparent; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] {
        background: #1a2e42;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 0.5rem 0.7rem;
        font-weight: 500;
        font-size: 0.72rem;
        color: #94a3b8 !important;
        flex: 1 0 auto;
        text-align: center;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #10b981 0%, #00ff88 100%) !important;
        color: #0b1e2e !important;
        border-color: #00ff88 !important;
        font-weight: 700 !important;
    }
    .perfil-card {
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 1.3rem;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }
    .perfil-card:hover { border-color: rgba(0, 255, 136, 0.4); box-shadow: 0 8px 25px rgba(0, 255, 136, 0.12); transform: translateY(-1px); }
    .pulse-logo {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00ff88 0%, #14b8a6 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        filter: drop-shadow(0 0 20px rgba(0, 255, 136, 0.3));
    }
    .demo-badge {
        background: rgba(0, 255, 136, 0.12);
        border: 1px solid rgba(0, 255, 136, 0.4);
        color: #00ff88;
        padding: 4px 12px;
        border-radius: 40px;
        font-size: 0.68rem;
        font-weight: 700;
    }
    .insight-box {
        background: linear-gradient(135deg, rgba(26, 46, 66, 0.8) 0%, rgba(36, 59, 84, 0.6) 100%);
        border: 1px solid rgba(0, 255, 136, 0.25);
        border-radius: 14px;
        padding: 16px;
        margin: 16px 0;
        position: relative;
        overflow: hidden;
    }
    .insight-box::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #00ff88, #14b8a6);
    }
    .insight-box strong { color: #00ff88 !important; }
    .info-box {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.08) 0%, rgba(20, 184, 166, 0.05) 100%);
        border-left: 3px solid #00ff88;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 12px 0;
    }
    .alerta-item {
        background: #1a2e42;
        border: 1px solid #334155;
        border-left: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }
    .alerta-item.urgente { border-left-color: #ef4444; }
    .alerta-item.ok { border-left-color: #00ff88; }
    .cta-whatsapp {
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white !important;
        padding: 14px 28px;
        border-radius: 60px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 8px 20px rgba(37, 211, 102, 0.4);
    }
    .dash-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(0, 255, 136, 0.15);
    }
    .dash-title { font-size: 1.15rem; font-weight: 700; }
    .dash-subtitle { color: #94a3b8 !important; font-size: 0.78rem; }
    .export-section {
        background: linear-gradient(135deg, rgba(26, 46, 66, 0.6) 0%, rgba(36, 59, 84, 0.4) 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px;
        margin: 20px 0 12px 0;
    }
    .export-title { color: #00ff88; font-weight: 700; font-size: 0.9rem; margin-bottom: 10px; }
    @media (max-width: 480px) {
        .carousel-wrapper { height: 160px; }
        .carousel-card { width: 260px; height: 140px; margin-left: -130px; padding: 16px 20px; }
        .card-padrao { height: 110px; }
        .card-valor { font-size: 1.3rem; }
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# FUNÇÕES DE FORMATAÇÃO E UTILITÁRIOS
# ═══════════════════════════════════════════════════════════════
def formatar_brl(valor):
    try:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def formatar_inteiro_br(valor):
    try:
        return f"{int(valor):,}".replace(",", ".")
    except:
        return "0"

def formatar_pct(valor):
    return f"{valor:+.1f}%".replace(".", ",")

def calcular_delta(atual, anterior):
    if anterior == 0 or anterior is None:
        return None, "delta-neutro", "—"
    delta = ((atual - anterior) / anterior) * 100
    if delta > 0.5:
        return delta, "delta-up", "▲"
    elif delta < -0.5:
        return delta, "delta-down", "▼"
    else:
        return delta, "delta-neutro", "●"

def gerar_label_comparacao(mes_atual, ano_atual, tipo_comp):
    idx = MESES.index(mes_atual)
    if tipo_comp == "MoM":
        if idx == 0:
            mes_ant = "Dez"
            ano_ant = str(int(ano_atual) - 1)
        else:
            mes_ant = MESES[idx - 1]
            ano_ant = ano_atual
        return f"{mes_ant}/{ano_ant[-2:]}"
    elif tipo_comp == "YoY":
        ano_ant = str(int(ano_atual) - 1)
        return f"{mes_atual}/{ano_ant[-2:]}"
    return ""

# ═══════════════════════════════════════════════════════════════
# CARD PADRÃO (altura fixa 130px)
# ═══════════════════════════════════════════════════════════════
def kpi_card(label, valor_atual, valor_anterior=None, formatter=None, icone="", tooltip=""):
    if formatter is None:
        formatter = lambda x: f"{int(x):,}".replace(",", ".") if isinstance(x, (int, float)) else str(x)
    valor_str = formatter(valor_atual)
    if valor_anterior is None:
        comp_html = ""
    else:
        delta, classe, seta = calcular_delta(valor_atual, valor_anterior)
        if delta is None:
            badge = '<span class="delta-badge delta-neutro">—</span>'
        else:
            badge = f'<span class="delta-badge {classe}">{seta} {formatar_pct(delta)}</span>'
        comp_html = f'<span style="color:#cbd5e1;">{formatter(valor_anterior)}</span> {badge}'
    tooltip_html = f'<span class="tooltip-icon" title="{tooltip}">?</span>' if tooltip else ""
    st.markdown(f"""
    <div class="card-padrao">
        <div class="card-label">{icone} {label} {tooltip_html}</div>
        <div class="card-valor">{valor_str}</div>
        <div class="card-footer">vs anterior: {comp_html}</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# LAYOUT DE GRÁFICOS
# ═══════════════════════════════════════════════════════════════
def layout_chart(altura=280, yaxis_opts=None, showlegend=True):
    base = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(26,46,66,0.3)",
        "font": {"family": "Inter, sans-serif", "color": TEXTO, "size": 11},
        "xaxis": {"gridcolor": "rgba(51, 65, 85, 0.4)", "linecolor": "#334155", "tickfont": {"color": TEXTO_MUTED, "size": 10}},
        "yaxis": {"gridcolor": "rgba(51, 65, 85, 0.4)", "linecolor": "#334155", "tickfont": {"color": TEXTO_MUTED, "size": 10}},
        "margin": {"t": 30, "b": 40, "l": 50, "r": 20},
        "height": altura,
        "hoverlabel": {"bgcolor": "#1a2e42", "font": {"color": TEXTO}, "bordercolor": VERDE_NEON},
        "legend": {"font": {"color": TEXTO, "size": 11}},
        "showlegend": showlegend,
    }
    if yaxis_opts:
        base["yaxis"].update(yaxis_opts)
    return base

# ═══════════════════════════════════════════════════════════════
# CARROSSEL
# ═══════════════════════════════════════════════════════════════
def carrossel_animado():
    st.markdown("""
    <div class="carousel-wrapper">
        <div class="carousel-track">
            <div class="carousel-card">
                <div style="display: flex; justify-content: space-between;">
                    <span class="carousel-label">Carteira Ativa</span>
                    <span class="carousel-icon">🛡️</span>
                </div>
                <div><div class="carousel-value">2.431</div><div class="carousel-delta">▲ +12% vs mês anterior</div></div>
            </div>
            <div class="carousel-card">
                <div style="display: flex; justify-content: space-between;">
                    <span class="carousel-label">Receita Mensal</span>
                    <span class="carousel-icon">💰</span>
                </div>
                <div><div class="carousel-value">R$ 187k</div><div class="carousel-delta">▲ +8,3% vs ano anterior</div></div>
            </div>
            <div class="carousel-card">
                <div style="display: flex; justify-content: space-between;">
                    <span class="carousel-label">Taxa Retenção</span>
                    <span class="carousel-icon">🔄</span>
                </div>
                <div><div class="carousel-value">94,7%</div><div class="carousel-delta">▲ +2,1pp últimos 30d</div></div>
            </div>
            <div class="carousel-card">
                <div style="display: flex; justify-content: space-between;">
                    <span class="carousel-label">NPS</span>
                    <span class="carousel-icon">⭐</span>
                </div>
                <div><div class="carousel-value">72</div><div class="carousel-delta">Zona de excelência</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# GERADORES DE DADOS
# ═══════════════════════════════════════════════════════════════
def gerar_dados_corretora(mes_ref="Jun", ano_ref="2026"):
    np.random.seed(42 + MESES.index(mes_ref) + int(ano_ref))
    base_clientes = 200 + MESES.index(mes_ref) * 8 + (int(ano_ref) - 2025) * 20
    clientes = [f"Cliente {i}" for i in range(1, base_clientes + 1)]
    ramos = ["Auto", "Vida", "Residencial", "Empresarial", "Saúde"]
    seguradoras = ["Porto Seguro", "Bradesco", "SulAmérica", "Allianz", "Mapfre"]
    dados = []
    for cliente in clientes:
        status = np.random.choice(["Ativo", "Vencendo", "Cancelado"], p=[0.7, 0.2, 0.1])
        ramo = np.random.choice(ramos)
        premio = np.random.uniform(800, 8000)
        comissao_anual = premio * np.random.uniform(0.05, 0.20)
        dias = np.random.randint(-30, 120)
        dados.append({"Cliente": cliente, "Ramo": ramo, "Seguradora": np.random.choice(seguradoras),
                      "Status": status, "Premio_Anual": round(premio, 2),
                      "Comissao_Anual": round(comissao_anual, 2),
                      "Comissao_Mensal": round(comissao_anual / 12, 2),
                      "Dias_Para_Renovacao": dias})
    df = pd.DataFrame(dados)
    evolucao = []
    for i, mes in enumerate(MESES):
        comissao = 8000 * (1 + 0.03 * i) * np.random.uniform(0.9, 1.1)
        novos = int(12 + i * 1.5 + np.random.randint(-3, 5))
        cancel = int(5 + i * 0.3 + np.random.randint(-2, 3))
        evolucao.append({"Mes": mes, "Comissao_Total": round(comissao, 2),
                         "Novos_Contratos": novos, "Cancelamentos": cancel})
    df_evo = pd.DataFrame(evolucao)
    return df, df_evo

def gerar_dados_contabil(mes_ref="Jun", ano_ref="2026"):
    np.random.seed(43 + MESES.index(mes_ref) + int(ano_ref))
    base = 60 + (int(ano_ref) - 2025) * 10
    empresas = [f"Empresa {i}" for i in range(1, base + 1)]
    regimes = ["Simples Nacional", "Lucro Presumido", "Lucro Real", "MEI"]
    dados = []
    for emp in empresas:
        regime = np.random.choice(regimes, p=[0.5, 0.2, 0.1, 0.2])
        honorario = np.random.uniform(400, 3500)
        status = np.random.choice(["Entregue", "Pendente", "Atrasado"], p=[0.6, 0.25, 0.15])
        dias = np.random.randint(-5, 20) if status != "Entregue" else np.random.randint(-30, 0)
        dados.append({"Empresa": emp, "Regime_Tributario": regime, "Honorario_Mensal": round(honorario, 2),
                      "Status_Fechamento": status, "Dias_Para_Entrega": dias})
    df = pd.DataFrame(dados)
    prod = []
    for i, mes in enumerate(MESES):
        horas = 120 * (1 + 0.05 * i) * np.random.uniform(0.9, 1.1)
        receita = 12000 * (1 + 0.03 * i) * np.random.uniform(0.95, 1.05)
        prod.append({"Mes": mes, "Horas_Fechamento": round(horas, 1), "Receita_Honorarios": round(receita, 2)})
    df_prod = pd.DataFrame(prod)
    return df, df_prod

def gerar_dados_clinica(mes_ref="Jun", ano_ref="2026"):
    np.random.seed(44 + MESES.index(mes_ref) + int(ano_ref))
    pacientes = [f"Paciente {i}" for i in range(1, 151)]
    procedimentos = ["Limpeza de Pele", "Botox", "Preenchimento", "Massagem", "Depilação a Laser", "Peeling"]
    profissionais = ["Dra. Ana", "Dra. Carla", "Dr. Paulo", "Dra. Fernanda"]
    dados = []
    hoje = datetime.now()
    for _ in range(400):
        if np.random.rand() < 0.3:
            data = hoje + timedelta(days=np.random.randint(1, 30))
            status = "Agendado"
        else:
            data = hoje - timedelta(days=np.random.randint(0, 60))
            status = np.random.choice(["Realizado", "Cancelado"], p=[0.8, 0.2])
        valor = np.random.uniform(150, 1200)
        dados.append({"Data": data, "Paciente": np.random.choice(pacientes), "Procedimento": np.random.choice(procedimentos),
                      "Profissional": np.random.choice(profissionais), "Valor": round(valor, 2), "Status": status,
                      "Forma_Pagamento": np.random.choice(["PIX", "Cartão", "Dinheiro"])})
    df = pd.DataFrame(dados)
    evo = []
    for i, mes in enumerate(MESES):
        rec = 28000 * (1 + 0.03 * i) * np.random.uniform(0.9, 1.1)
        ticket = rec / (130 + i * 5)
        evo.append({"Mes": mes, "Receita": round(rec, 2), "Ticket_Medio": round(ticket, 2)})
    df_evo = pd.DataFrame(evo)
    return df, df_evo

def gerar_dados_barbearia(mes_ref="Jun", ano_ref="2026"):
    np.random.seed(45 + MESES.index(mes_ref) + int(ano_ref))
    clientes = [f"Cliente {i}" for i in range(1, 201)]
    servicos = ["Corte", "Barba", "Sobrancelha", "Corte + Barba", "Hidratação"]
    barbeiros = ["João", "Pedro", "Lucas", "Mateus", "André"]
    dados = []
    hoje = datetime.now()
    for _ in range(600):
        if np.random.rand() < 0.35:
            data = hoje + timedelta(days=np.random.randint(1, 30))
            status = "Agendado"
        else:
            data = hoje - timedelta(days=np.random.randint(0, 90))
            status = np.random.choice(["Realizado", "Cancelado"], p=[0.85, 0.15])
        valor = np.random.uniform(35, 120)
        barbeiro = np.random.choice(barbeiros)
        comissao_pct = 0.4 if barbeiro in ["João", "Pedro"] else 0.35
        comissao = valor * comissao_pct
        gorjeta = np.random.choice([0, 5, 10, 15], p=[0.5, 0.3, 0.15, 0.05])
        dados.append({"Data": data, "Cliente": np.random.choice(clientes), "Servico": np.random.choice(servicos),
                      "Barbeiro": barbeiro, "Valor": round(valor, 2), "Comissao_Barbeiro": round(comissao, 2),
                      "Gorjeta": gorjeta, "Status": status})
    df = pd.DataFrame(dados)
    produtos = ["Pomada", "Shampoo", "Óleo Barba", "Cera", "Perfume"]
    prod_data = []
    for _ in range(200):
        data = hoje - timedelta(days=np.random.randint(0, 90))
        prod = np.random.choice(produtos)
        qtd = np.random.randint(1, 4)
        preco = np.random.uniform(25, 90)
        receita = qtd * preco
        lucro = receita * 0.45
        prod_data.append({"Data": data, "Produto": prod, "Quantidade": qtd, "Preco_Unitario": round(preco, 2),
                          "Receita_Total": round(receita, 2), "Lucro_Bruto": round(lucro, 2)})
    df_prod = pd.DataFrame(prod_data)
    evo = []
    for i, mes in enumerate(MESES):
        rec_serv = 18000 * (1 + 0.02 * i) * np.random.uniform(0.9, 1.1)
        rec_prod = 4000 * (1 + 0.03 * i) * np.random.uniform(0.9, 1.1)
        atend = int(120 + i * 3)
        evo.append({"Mes": mes, "Receita_Servicos": round(rec_serv, 2),
                    "Receita_Produtos": round(rec_prod, 2), "Atendimentos": atend})
    df_evo = pd.DataFrame(evo)
    return df, df_prod, df_evo

# ═══════════════════════════════════════════════════════════════
# INSIGHTS AUTOMÁTICOS
# ═══════════════════════════════════════════════════════════════
def gerar_insight_corretora(dados):
    ativos = dados.get("ativos", 0)
    vencendo = dados.get("vencendo", 0)
    comissao = dados.get("comissao", 0)
    comissao_ant = dados.get("comissao_ant", 0)
    insights = []
    if vencendo > 0:
        receita_em_risco = (vencendo / max(ativos, 1)) * comissao
        insights.append(f"⚠️ <strong>{vencendo} apólices vencem em 30 dias</strong> — aproximadamente {formatar_brl(receita_em_risco)}/mês em risco.")
    if comissao_ant and comissao > comissao_ant:
        pct = ((comissao - comissao_ant) / comissao_ant) * 100
        insights.append(f"📈 Comissão cresceu <strong>{pct:.1f}%</strong> vs período anterior. Tendência positiva sustentada.")
    if not insights:
        insights.append("✅ Operação estável no período. Foco em prospecção.")
    return " ".join(insights)

def gerar_insight_contabil(dados):
    total = dados.get("total", 0)
    atrasados = dados.get("atrasados", 0)
    pct_prazo = dados.get("pct_prazo", 0)
    insights = []
    if atrasados > 0:
        pct_atraso = (atrasados / max(total, 1)) * 100
        insights.append(f"⚠️ <strong>{atrasados} clientes em atraso</strong> ({pct_atraso:.1f}% da carteira). Revisar processo de coleta de documentos.")
    if pct_prazo >= 80:
        insights.append(f"✅ <strong>{pct_prazo:.0f}% das entregas no prazo</strong> — acima da média do setor (72%).")
    elif pct_prazo < 70:
        insights.append(f"🎯 Meta de entregas no prazo: 80%. Atual: {pct_prazo:.0f}%. Gap: {80 - pct_prazo:.0f}pp.")
    return " ".join(insights) if insights else "✅ Operação fluindo."

def gerar_insight_clinica(dados):
    receita = dados.get("receita", 0)
    receita_ant = dados.get("receita_ant", 0)
    ticket = dados.get("ticket", 0)
    agendados = dados.get("agendados", 0)
    insights = []
    if receita_ant and receita > receita_ant:
        pct = ((receita - receita_ant) / receita_ant) * 100
        insights.append(f"💚 Receita cresceu <strong>{pct:.1f}%</strong> vs período anterior. Mantendo tendência saudável.")
    if agendados > 0:
        insights.append(f"📅 <strong>{agendados} atendimentos agendados</strong> — projeção de {formatar_brl(agendados * ticket)} em receita futura.")
    return " ".join(insights) if insights else "✅ Operação estável."

def gerar_insight_barbearia(dados):
    receita = dados.get("receita", 0)
    receita_ant = dados.get("receita_ant", 0)
    ticket = dados.get("ticket", 0)
    atendimentos = dados.get("atendimentos", 0)
    insights = []
    if receita_ant and receita > receita_ant:
        pct = ((receita - receita_ant) / receita_ant) * 100
        insights.append(f"💚 Receita cresceu <strong>{pct:.1f}%</strong> vs período anterior.")
    if atendimentos > 0:
        insights.append(f"✂️ Ticket médio de <strong>{formatar_brl(ticket)}</strong> em {atendimentos} atendimentos.")
    return " ".join(insights) if insights else "✅ Barbearia fluindo bem."

# ═══════════════════════════════════════════════════════════════
# SELETOR DE PERÍODO
# ═══════════════════════════════════════════════════════════════
def seletor_periodo_comparacao(key_prefix):
    col1, col2, col3 = st.columns([2, 2, 3])
    with col1:
        mes = st.selectbox("Mês", MESES, index=5, key=f"{key_prefix}_mes")
    with col2:
        ano = st.selectbox("Ano", ["2024", "2025", "2026"], index=2, key=f"{key_prefix}_ano")
    with col3:
        tipo_comp = st.selectbox("Comparar com", ["Mês anterior", "Ano anterior", "Sem comparação"], index=0, key=f"{key_prefix}_comp")
    idx = MESES.index(mes)
    mes_ant, ano_ant = None, None
    if tipo_comp == "Mês anterior":
        if idx == 0:
            mes_ant = "Dez"
            ano_ant = str(int(ano) - 1)
        else:
            mes_ant = MESES[idx - 1]
            ano_ant = ano
    elif tipo_comp == "Ano anterior":
        mes_ant = mes
        ano_ant = str(int(ano) - 1)
    tipo_short = "MoM" if tipo_comp == "Mês anterior" else ("YoY" if tipo_comp == "Ano anterior" else None)
    return mes, ano, tipo_short, mes_ant, ano_ant

# ═══════════════════════════════════════════════════════════════
# EXPORT (Excel e PDF)
# ═══════════════════════════════════════════════════════════════
def exportar_excel(nome_base, dfs_dict, titulo_relatorio, periodo):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook = writer.book
        cover = workbook.add_worksheet("Resumo")
        cover.set_column("A:A", 35)
        cover.set_column("B:B", 45)
        fmt_titulo = workbook.add_format({"font_name": "Calibri", "font_size": 22, "bold": True, "font_color": "#00ff88", "bg_color": "#0b1e2e", "align": "center", "valign": "vcenter"})
        fmt_subtitulo = workbook.add_format({"font_name": "Calibri", "font_size": 12, "font_color": "#ffffff", "bg_color": "#1a2e42", "align": "center", "valign": "vcenter", "italic": True})
        fmt_label = workbook.add_format({"font_name": "Calibri", "font_size": 11, "bold": True, "font_color": "#047857", "bg_color": "#ecfdf5", "border": 1, "border_color": "#10b981"})
        fmt_valor = workbook.add_format({"font_name": "Calibri", "font_size": 11, "font_color": "#0f172a", "bg_color": "#ffffff", "border": 1, "border_color": "#10b981"})
        cover.set_row(1, 50)
        cover.merge_range("A2:B2", "PULSE", fmt_titulo)
        cover.set_row(2, 30)
        cover.merge_range("A3:B3", titulo_relatorio, fmt_subtitulo)
        cover.write("A5", "Período", fmt_label)
        cover.write("B5", periodo, fmt_valor)
        cover.write("A6", "Gerado em", fmt_label)
        cover.write("B6", datetime.now().strftime("%d/%m/%Y %H:%M"), fmt_valor)
        cover.write("A7", "Tipo", fmt_label)
        cover.write("B7", "Demo com dados fictícios", fmt_valor)
        cover.merge_range("A9:B9", "Desenvolvido por Natan Souza — Consultoria em Dados e Inteligência Comercial",
                          workbook.add_format({"italic": True, "align": "center", "font_color": "#64748b", "font_size": 10}))
        fmt_header = workbook.add_format({"font_name": "Calibri", "font_size": 11, "bold": True, "font_color": "#ffffff", "bg_color": "#047857", "border": 1, "align": "center"})
        fmt_cell = workbook.add_format({"font_name": "Calibri", "font_size": 10, "border": 1, "border_color": "#e2e8f0"})
        fmt_money = workbook.add_format({"font_name": "Calibri", "font_size": 10, "border": 1, "border_color": "#e2e8f0", "num_format": 'R$ #,##0.00'})
        for nome_aba, df in dfs_dict.items():
            df.to_excel(writer, sheet_name=nome_aba[:31], index=False, startrow=1)
            ws = writer.sheets[nome_aba[:31]]
            ws.merge_range(0, 0, 0, len(df.columns)-1, nome_aba,
                          workbook.add_format({"font_name": "Calibri", "font_size": 14, "bold": True, "font_color": "#047857", "bg_color": "#ecfdf5", "align": "center", "border": 1}))
            for col_idx, col_name in enumerate(df.columns):
                ws.write(1, col_idx, col_name, fmt_header)
                ws.set_column(col_idx, col_idx, max(14, min(28, len(col_name)+6)))
            for row_idx, row in df.iterrows():
                for col_idx, col_name in enumerate(df.columns):
                    val = row[col_name]
                    if any(k in col_name.lower() for k in ["valor", "premio", "comiss", "honor", "receita", "lucro", "ticket", "preco"]):
                        try:
                            ws.write_number(row_idx+2, col_idx, float(val), fmt_money)
                        except:
                            ws.write(row_idx+2, col_idx, str(val), fmt_cell)
                    else:
                        ws.write(row_idx+2, col_idx, str(val) if pd.isna(val) else val, fmt_cell)
    return output.getvalue()

def exportar_pdf(titulo_relatorio, periodo, kpis_dict, tabelas_dict, insights_list):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.enums import TA_CENTER
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4, leftMargin=1.8*cm, rightMargin=1.8*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    s_titulo = ParagraphStyle("TituloPulse", fontSize=36, textColor=colors.HexColor("#00ff88"), fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4, leading=40)
    s_subtitulo = ParagraphStyle("SubPulse", fontSize=12, textColor=colors.HexColor("#64748b"), alignment=TA_CENTER, spaceAfter=20, leading=14)
    s_secao = ParagraphStyle("Secao", fontSize=14, textColor=colors.HexColor("#047857"), fontName="Helvetica-Bold", spaceAfter=10, spaceBefore=16, leading=16)
    s_texto = ParagraphStyle("Texto", fontSize=10, textColor=colors.HexColor("#0f172a"), leading=14, spaceAfter=8)
    s_insight = ParagraphStyle("Insight", fontSize=10, textColor=colors.HexColor("#064e3b"), leading=14, spaceAfter=6, leftIndent=12)
    elementos = []
    elementos.append(Spacer(1, 3*cm))
    elementos.append(Paragraph("PULSE", s_titulo))
    elementos.append(Paragraph("O pulso do seu negócio, no seu bolso.", s_subtitulo))
    elementos.append(Spacer(1, 1*cm))
    capa_data = [["Relatório:", titulo_relatorio], ["Período:", periodo], ["Gerado em:", datetime.now().strftime("%d/%m/%Y %H:%M")], ["Tipo:", "Demo com dados fictícios"]]
    t_capa = Table(capa_data, colWidths=[4*cm, 11*cm])
    t_capa.setStyle(TableStyle([("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"), ("FONTNAME", (1,0), (1,-1), "Helvetica"), ("FONTSIZE", (0,0), (-1,-1), 11), ("TEXTCOLOR", (0,0), (0,-1), colors.HexColor("#64748b")), ("TEXTCOLOR", (1,0), (1,-1), colors.HexColor("#0f172a")), ("BOTTOMPADDING", (0,0), (-1,-1), 10), ("TOPPADDING", (0,0), (-1,-1), 10), ("LINEBELOW", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0"))]))
    elementos.append(t_capa)
    elementos.append(Spacer(1, 4*cm))
    elementos.append(Paragraph("Desenvolvido por <b>Natan Souza</b><br/>Consultoria em Dados e Inteligência Comercial", ParagraphStyle("Assinatura", fontSize=10, textColor=colors.HexColor("#64748b"), alignment=TA_CENTER)))
    elementos.append(PageBreak())
    elementos.append(Paragraph("Indicadores principais", s_secao))
    kpi_data = [[k, v] for k, v in kpis_dict.items()]
    t_kpi = Table(kpi_data, colWidths=[8*cm, 8*cm])
    t_kpi.setStyle(TableStyle([("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"), ("FONTNAME", (1,0), (1,-1), "Helvetica-Bold"), ("FONTSIZE", (0,0), (0,-1), 10), ("FONTSIZE", (1,0), (1,-1), 14), ("TEXTCOLOR", (0,0), (0,-1), colors.HexColor("#64748b")), ("TEXTCOLOR", (1,0), (1,-1), colors.HexColor("#047857")), ("BOTTOMPADDING", (0,0), (-1,-1), 12), ("TOPPADDING", (0,0), (-1,-1), 12), ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")), ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")), ("INNERGRID", (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0"))]))
    elementos.append(t_kpi)
    if insights_list:
        elementos.append(Paragraph("Insights automáticos", s_secao))
        for ins in insights_list:
            ins_clean = ins.replace("<strong>", "<b>").replace("</strong>", "</b>")
            elementos.append(Paragraph(f"• {ins_clean}", s_insight))
    elementos.append(PageBreak())
    for nome_tab, df in tabelas_dict.items():
        elementos.append(Paragraph(nome_tab, s_secao))
        if df is None or df.empty:
            elementos.append(Paragraph("Sem dados para o período.", s_texto))
            continue
        cols = list(df.columns)[:5]
        df_show = df[cols].head(20)
        data = [cols] + df_show.astype(str).values.tolist()
        larg_col = 17.4*cm / len(cols)
        tbl = Table(data, colWidths=[larg_col]*len(cols))
        tbl.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#047857")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,0), 8), ("TOPPADDING", (0,0), (-1,0), 8), ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#e2e8f0")), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]), ("FONTNAME", (0,1), (-1,-1), "Helvetica")]))
        elementos.append(tbl)
        elementos.append(Spacer(1, 0.5*cm))
    elementos.append(Spacer(1, 1*cm))
    elementos.append(Paragraph("Relatório gerado pelo Pulse • Dados fictícios • © 2026 Natan Souza", ParagraphStyle("Rodape", fontSize=8, textColor=colors.HexColor("#94a3b8"), alignment=TA_CENTER)))
    doc.build(elementos)
    return output.getvalue()

def bloco_export(titulo_relatorio, periodo, dfs_excel, kpis_dict, tabelas_pdf, insights_list):
    st.markdown('<div class="export-section"><div class="export-title">📥 Exportar relatório</div></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        excel_bytes = exportar_excel("relatorio", dfs_excel, titulo_relatorio, periodo)
        st.download_button(label="📊 Baixar Excel", data=excel_bytes, file_name=f"pulse_{titulo_relatorio.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with c2:
        pdf_bytes = exportar_pdf(titulo_relatorio, periodo, kpis_dict, tabelas_pdf, insights_list)
        st.download_button(label="📄 Baixar PDF", data=pdf_bytes, file_name=f"pulse_{titulo_relatorio.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", mime="application/pdf", use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TELA INICIAL
# ═══════════════════════════════════════════════════════════════
def tela_inicial():
    st.markdown('<h1 class="pulse-logo">Pulse</h1>', unsafe_allow_html=True)
    st.markdown('<p class="pulse-slogan">O pulso do seu negócio, no seu bolso.</p>', unsafe_allow_html=True)
    carrossel_animado()
    st.markdown('<p style="text-align:center; color:#f1f5f9; font-size:0.92rem;">Escolha seu segmento para ver a demonstração.<br><span style="font-size:0.78rem; color:#94a3b8;">Dados fictícios, estrutura real.</span></p>', unsafe_allow_html=True)
    perfis = [
        ("🛡️", "Sou Corretora de Seguros", "Carteira, comissões, renovações e alertas de vencimento.", "corretora"),
        ("📊", "Sou Escritório Contábil", "Gestão de carteira, fechamentos e produtividade.", "contabil"),
        ("💚", "Sou Clínica Estética", "Agenda, receita e performance dos profissionais.", "clinica"),
        ("💈", "Sou Barbearia", "Agenda, comissão dos barbeiros e produtos.", "barbearia")
    ]
    for icon, titulo, desc, perfil in perfis:
        st.markdown(f'<div class="perfil-card"><div style="font-size:2rem;">{icon}</div><div class="perfil-titulo" style="font-size:1.05rem;">{titulo}</div><div class="perfil-desc" style="font-size:0.85rem;">{desc}</div></div>', unsafe_allow_html=True)
        if st.button(f"Ver demo para {titulo.split()[-1]}", key=f"btn_{perfil}"):
            st.session_state.perfil = perfil
            st.rerun()
    st.markdown('<div style="text-align:center; margin-top:32px; border-top:1px solid rgba(0,255,136,0.15); padding-top:20px; color:#94a3b8; font-size:0.75rem;">Desenvolvido por <strong style="color:#00ff88;">Natan Souza</strong><br>Consultoria em Dados e Inteligência Comercial</div>', unsafe_allow_html=True)

def info_dados_ficticios():
    st.markdown('<div class="info-box"><strong>💡 Demo com dados fictícios.</strong><br>Seus dados reais, assim, em 3 semanas.</div>', unsafe_allow_html=True)

def botao_voltar():
    if st.button("← Voltar para escolha de perfil", use_container_width=True, type="secondary"):
        st.session_state.perfil = None
        st.rerun()

def cta_whatsapp(texto_msg):
    msg_codificada = texto_msg.replace(" ", "%20").replace("\n", "%0A")
    link = f"https://wa.me/{WHATSAPP}?text={msg_codificada}"
    st.markdown(f'<div style="text-align: center; margin: 16px 0;"><a href="{link}" target="_blank" class="cta-whatsapp">💬 &nbsp;Quero isso pra minha empresa</a></div><div style="text-align: center; color: #94a3b8; font-size: 0.75rem;">Primeira conversa grátis • Sem compromisso</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# DASHBOARD CORRETORA
# ═══════════════════════════════════════════════════════════════
def dash_corretora():
    st.markdown('<div class="dash-header"><div><div class="dash-title">🛡️ Pulse • Corretora</div><div class="dash-subtitle">Demo para Corretoras de Seguros</div></div><span class="demo-badge">DEMO</span></div>', unsafe_allow_html=True)
    mes, ano, tipo_comp, mes_ant, ano_ant = seletor_periodo_comparacao("cor")
    periodo_label = f"{mes}/{ano}"
    with st.spinner("Carregando dados..."):
        df, df_evo = gerar_dados_corretora(mes, ano)
        if tipo_comp:
            df_ant, df_evo_ant = gerar_dados_corretora(mes_ant, ano_ant)
        else:
            df_ant, df_evo_ant = None, None
    info_dados_ficticios()
    ativos = df[df["Status"] == "Ativo"]
    comissao = ativos["Comissao_Mensal"].sum()
    vencendo = len(df[(df["Dias_Para_Renovacao"] >= 0) & (df["Dias_Para_Renovacao"] <= 30)])
    ticket = comissao / len(ativos) if len(ativos) > 0 else 0
    ativos_ant = comissao_ant = ticket_ant = 0
    if df_ant is not None:
        ativos_ant_df = df_ant[df_ant["Status"] == "Ativo"]
        ativos_ant = len(ativos_ant_df)
        comissao_ant = ativos_ant_df["Comissao_Mensal"].sum()
        ticket_ant = comissao_ant / ativos_ant if ativos_ant > 0 else 0
    insight = gerar_insight_corretora({"ativos": len(ativos), "vencendo": vencendo, "comissao": comissao, "comissao_ant": comissao_ant})
    st.markdown(f'<div class="insight-box">💡 <strong>Insight de {mes}/{ano}</strong><br>{insight}</div>', unsafe_allow_html=True)
    comp_label = gerar_label_comparacao(mes, ano, tipo_comp) if tipo_comp else ""
    c1, c2 = st.columns(2)
    with c1:
        kpi_card("CARTEIRA ATIVA", len(ativos), ativos_ant, formatter=formatar_inteiro_br, icone="🛡️", tooltip="Clientes ativos")
    with c2:
        kpi_card("COMISSÃO / MÊS", comissao, comissao_ant, formatter=formatar_brl, icone="💰", tooltip="Comissão total do mês")
    c3, c4 = st.columns(2)
    with c3:
        kpi_card("VENCENDO EM 30d", vencendo, None, formatter=formatar_inteiro_br, icone="⏰", tooltip="Apólices a vencer em 30 dias")
    with c4:
        kpi_card("TICKET MÉDIO", ticket, ticket_ant, formatter=formatar_brl, icone="🎫", tooltip="Comissão média por cliente ativo")
    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2, t3, t4, t5 = st.tabs(["📈 Evolução", "🔔 Alertas", "🎯 Mix", "📋 Carteira", "🏆 Top"])
    with t1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_evo["Mes"], y=df_evo["Comissao_Total"], mode="lines+markers", name=ano, line=dict(color=VERDE_NEON, width=3), fill="tozeroy", fillcolor="rgba(0,255,136,0.15)"))
        if df_evo_ant is not None and tipo_comp == "YoY":
            fig.add_trace(go.Scatter(x=df_evo_ant["Mes"], y=df_evo_ant["Comissao_Total"], mode="lines", name=ano_ant, line=dict(color=AZUL_CLARO, width=2, dash="dash")))
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Novos", x=df_evo["Mes"], y=df_evo["Novos_Contratos"], marker_color=VERDE_NEON))
        fig2.add_trace(go.Bar(name="Cancelamentos", x=df_evo["Mes"], y=df_evo["Cancelamentos"], marker_color=VERMELHO))
        fig2.update_layout(**layout_chart(240))
        st.plotly_chart(fig2, use_container_width=True)
    with t2:
        urgentes = df[df["Dias_Para_Renovacao"].between(0, 15)].sort_values("Dias_Para_Renovacao")
        if not urgentes.empty:
            for _, row in urgentes.head(8).iterrows():
                urgencia = "urgente" if row["Dias_Para_Renovacao"] <= 7 else ""
                st.markdown(f'<div class="alerta-item {urgencia}"><div style="display:flex; justify-content:space-between;"><div><strong>{row["Cliente"]}</strong><br><span style="font-size:0.78rem;">{row["Ramo"]} • {row["Seguradora"]}</span></div><div style="text-align:right;"><strong style="color:#ef4444;">{int(row["Dias_Para_Renovacao"])}d</strong><br><span style="font-size:0.78rem;">{formatar_brl(row["Premio_Anual"])}</span></div></div></div>', unsafe_allow_html=True)
        else:
            st.info("✅ Sem renovações urgentes.")
    with t3:
        mix = df[df["Status"] == "Ativo"].groupby("Ramo").size().reset_index(name="total")
        fig = px.pie(mix, values="total", names="Ramo", hole=0.5, color_discrete_sequence=[VERDE_NEON, AZUL_CLARO, ROXO, AMBAR, ROSA])
        fig.update_traces(textposition="inside", textinfo="percent", textfont=dict(color="#0b1e2e", family="Inter", size=11))
        fig.update_layout(**layout_chart(330))
        st.plotly_chart(fig, use_container_width=True)
    with t4:
        busca = st.text_input("🔍 Buscar cliente", key="busca_cor")
        df_view = df.copy()
        if busca:
            df_view = df_view[df_view["Cliente"].str.contains(busca, case=False)]
        st.dataframe(df_view[["Cliente", "Ramo", "Seguradora", "Status", "Premio_Anual"]].head(20), use_container_width=True, hide_index=True)
    with t5:
        top_clientes = ativos.groupby("Cliente")["Premio_Anual"].sum().sort_values(ascending=False).head(10)
        fig = go.Figure(go.Bar(x=top_clientes.values, y=top_clientes.index, orientation="h", marker_color=VERDE_NEON, text=top_clientes.values, textposition='outside', texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)))
        fig.update_layout(**layout_chart(340, yaxis_opts={"autorange": "reversed", "tickfont": {"color": TEXTO, "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)
    kpis_pdf = {"Carteira ativa": formatar_inteiro_br(len(ativos)), "Comissão mensal": formatar_brl(comissao), "Vencendo em 30 dias": str(vencendo), "Ticket médio": formatar_brl(ticket)}
    tabelas_export = {"Carteira Ativa": ativos[["Cliente", "Ramo", "Seguradora", "Premio_Anual", "Comissao_Mensal"]], "Vencendo Proximos 30d": df[(df["Dias_Para_Renovacao"] >= 0) & (df["Dias_Para_Renovacao"] <= 30)][["Cliente", "Ramo", "Seguradora", "Dias_Para_Renovacao", "Premio_Anual"]], "Evolucao Mensal": df_evo}
    bloco_export("Corretora de Seguros", periodo_label, tabelas_export, kpis_pdf, tabelas_export, [insight])
    st.markdown("---")
    cta_whatsapp(f"Oi Natan! Vi o demo do Pulse para corretoras (período {periodo_label}) e quero conversar.")
    botao_voltar()

# ═══════════════════════════════════════════════════════════════
# DASHBOARD CONTÁBIL
# ═══════════════════════════════════════════════════════════════
def dash_contabil():
    st.markdown('<div class="dash-header"><div><div class="dash-title">📊 Pulse • Contábil</div><div class="dash-subtitle">Demo para Escritórios de Contabilidade</div></div><span class="demo-badge">DEMO</span></div>', unsafe_allow_html=True)
    mes, ano, tipo_comp, mes_ant, ano_ant = seletor_periodo_comparacao("cont")
    periodo_label = f"{mes}/{ano}"
    with st.spinner("Carregando dados..."):
        df, df_prod = gerar_dados_contabil(mes, ano)
        if tipo_comp:
            df_ant, df_prod_ant = gerar_dados_contabil(mes_ant, ano_ant)
        else:
            df_ant, df_prod_ant = None, None
    info_dados_ficticios()
    honorarios = df["Honorario_Mensal"].sum()
    entregues = df[df["Status_Fechamento"] == "Entregue"]
    atrasados = df[df["Status_Fechamento"] == "Atrasado"]
    pct_prazo = (len(entregues) / len(df)) * 100 if len(df) > 0 else 0
    honorarios_ant = empresas_ant = 0
    if df_ant is not None:
        honorarios_ant = df_ant["Honorario_Mensal"].sum()
        empresas_ant = len(df_ant)
    insight = gerar_insight_contabil({"total": len(df), "atrasados": len(atrasados), "pct_prazo": pct_prazo})
    st.markdown(f'<div class="insight-box">💡 <strong>Insight de {mes}/{ano}</strong><br>{insight}</div>', unsafe_allow_html=True)
    comp_label = gerar_label_comparacao(mes, ano, tipo_comp) if tipo_comp else ""
    c1, c2 = st.columns(2)
    with c1:
        kpi_card("EMPRESAS", len(df), empresas_ant, formatter=formatar_inteiro_br, icone="🏢", tooltip="Total de empresas na carteira")
    with c2:
        kpi_card("HONORÁRIOS", honorarios, honorarios_ant, formatter=formatar_brl, icone="📄", tooltip="Soma dos honorários mensais")
    c3, c4 = st.columns(2)
    with c3:
        kpi_card("ENTREGUES NO PRAZO", f"{pct_prazo:.0f}%", None, formatter=lambda x: x, icone="✅", tooltip="Percentual de entregas no prazo")
    with c4:
        kpi_card("EM ATRASO", len(atrasados), None, formatter=formatar_inteiro_br, icone="⚠️", tooltip="Empresas com fechamento atrasado")
    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2, t3, t4, t5, t6 = st.tabs(["📈 Produtividade", "⚠️ Atrasados", "📋 Carteira", "🥧 Regimes", "💰 Top", "📅 Obrig."])
    with t1:
        fig = go.Figure(go.Scatter(x=df_prod["Mes"], y=df_prod["Horas_Fechamento"], mode="lines+markers", line=dict(color=VERDE_NEON, width=3), fill="tozeroy", fillcolor="rgba(0,255,136,0.15)"))
        if df_prod_ant is not None and tipo_comp == "YoY":
            fig.add_trace(go.Scatter(x=df_prod_ant["Mes"], y=df_prod_ant["Horas_Fechamento"], mode="lines", name=ano_ant, line=dict(color=AZUL_CLARO, width=2, dash="dash")))
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)
    with t2:
        atrasados_df = df[df["Status_Fechamento"] == "Atrasado"]
        if not atrasados_df.empty:
            for _, row in atrasados_df.head(6).iterrows():
                st.markdown(f'<div class="alerta-item urgente"><strong>{row["Empresa"]}</strong><br><span style="font-size:0.78rem;">{row["Regime_Tributario"]} • {row["Dias_Para_Entrega"]} dias de atraso</span></div>', unsafe_allow_html=True)
        else:
            st.info("✅ Nenhum cliente em atraso.")
    with t3:
        busca = st.text_input("🔍 Buscar empresa", key="busca_cont")
        df_view = df.copy()
        if busca:
            df_view = df_view[df_view["Empresa"].str.contains(busca, case=False)]
        st.dataframe(df_view[["Empresa", "Regime_Tributario", "Status_Fechamento", "Honorario_Mensal"]], use_container_width=True, hide_index=True)
    with t4:
        regime_counts = df["Regime_Tributario"].value_counts().reset_index()
        regime_counts.columns = ["Regime", "Quantidade"]
        fig = px.pie(regime_counts, values="Quantidade", names="Regime", hole=0.5, color_discrete_sequence=[VERDE_NEON, AZUL_CLARO, ROXO, AMBAR])
        fig.update_traces(textposition="inside", textinfo="percent", textfont=dict(color="#0b1e2e", family="Inter", size=11))
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)
    with t5:
        top_hon = df.groupby("Empresa")["Honorario_Mensal"].sum().sort_values(ascending=False).head(10)
        fig = go.Figure(go.Bar(x=top_hon.values, y=top_hon.index, orientation="h", marker_color=VERDE_NEON, text=top_hon.values, textposition='outside', texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)))
        fig.update_layout(**layout_chart(340, yaxis_opts={"autorange": "reversed", "tickfont": {"color": TEXTO, "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)
    with t6:
        st.markdown("**📌 Próximas obrigações fiscais**")
        obrigacoes = pd.DataFrame({"Obrigação": ["DASN-SIMEI", "EFD-Contribuições", "DCTF", "DIRF", "ECD"], "Vencimento": ["31/05", "10/06", "15/06", "20/06", "30/06"], "Status": ["Pendente", "Pendente", "Pendente", "Pendente", "Pendente"]})
        st.dataframe(obrigacoes, use_container_width=True, hide_index=True)
    kpis_pdf = {"Empresas na carteira": formatar_inteiro_br(len(df)), "Honorários mensais": formatar_brl(honorarios), "Entregues no prazo": f"{pct_prazo:.0f}%", "Clientes em atraso": str(len(atrasados))}
    tabelas_export = {"Carteira Completa": df[["Empresa", "Regime_Tributario", "Status_Fechamento", "Honorario_Mensal"]], "Clientes em Atraso": df[df["Status_Fechamento"] == "Atrasado"][["Empresa", "Regime_Tributario", "Dias_Para_Entrega"]], "Produtividade Mensal": df_prod}
    bloco_export("Contabilidade", periodo_label, tabelas_export, kpis_pdf, tabelas_export, [insight])
    st.markdown("---")
    cta_whatsapp(f"Oi Natan! Vi o demo do Pulse para contabilidade (período {periodo_label}) e quero conversar.")
    botao_voltar()

# ═══════════════════════════════════════════════════════════════
# DASHBOARD CLÍNICA
# ═══════════════════════════════════════════════════════════════
def dash_clinica():
    st.markdown('<div class="dash-header"><div><div class="dash-title">💚 Pulse • Clínica</div><div class="dash-subtitle">Demo para Clínicas Estéticas</div></div><span class="demo-badge">DEMO</span></div>', unsafe_allow_html=True)
    mes, ano, tipo_comp, mes_ant, ano_ant = seletor_periodo_comparacao("cli")
    periodo_label = f"{mes}/{ano}"
    with st.spinner("Carregando dados..."):
        df, df_evo = gerar_dados_clinica(mes, ano)
        if tipo_comp:
            df_ant, df_evo_ant = gerar_dados_clinica(mes_ant, ano_ant)
        else:
            df_ant, df_evo_ant = None, None
    info_dados_ficticios()
    realizados = df[df["Status"] == "Realizado"]
    receita = realizados["Valor"].sum()
    ticket = realizados["Valor"].mean() if not realizados.empty else 0
    agendados = len(df[df["Status"] == "Agendado"])
    receita_ant = ticket_ant = 0
    if df_ant is not None:
        real_ant = df_ant[df_ant["Status"] == "Realizado"]
        receita_ant = real_ant["Valor"].sum()
        ticket_ant = real_ant["Valor"].mean() if not real_ant.empty else 0
    insight = gerar_insight_clinica({"receita": receita, "receita_ant": receita_ant, "ticket": ticket, "agendados": agendados})
    st.markdown(f'<div class="insight-box">💡 <strong>Insight de {mes}/{ano}</strong><br>{insight}</div>', unsafe_allow_html=True)
    comp_label = gerar_label_comparacao(mes, ano, tipo_comp) if tipo_comp else ""
    c1, c2 = st.columns(2)
    with c1:
        kpi_card("RECEITA / MÊS", receita, receita_ant, formatter=formatar_brl, icone="💰", tooltip="Receita total do mês")
    with c2:
        kpi_card("ATENDIMENTOS", len(realizados), None, formatter=formatar_inteiro_br, icone="👥", tooltip="Atendimentos realizados no período")
    c3, c4 = st.columns(2)
    with c3:
        kpi_card("TICKET MÉDIO", ticket, ticket_ant, formatter=formatar_brl, icone="🎫", tooltip="Valor médio por atendimento")
    with c4:
        kpi_card("AGENDADOS", agendados, None, formatter=formatar_inteiro_br, icone="📅", tooltip="Atendimentos agendados futuramente")
    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2, t3, t4, t5, t6 = st.tabs(["📈 Receita", "⭐ Top", "📅 Agenda", "👩‍⚕️ Prof.", "🔄 Fidelização", "💳 Pagto"])
    with t1:
        fig = go.Figure(go.Bar(x=df_evo["Mes"], y=df_evo["Receita"], marker_color=VERDE_NEON, name=ano))
        if df_evo_ant is not None and tipo_comp == "YoY":
            fig.add_trace(go.Scatter(x=df_evo_ant["Mes"], y=df_evo_ant["Receita"], mode="lines+markers", name=ano_ant, line=dict(color=AZUL_CLARO, width=2, dash="dash")))
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)
    with t2:
        top = realizados.groupby("Procedimento")["Valor"].sum().sort_values(ascending=True).tail(6)
        fig = go.Figure(go.Bar(y=top.index, x=top.values, orientation="h", marker_color=VERDE_NEON, text=top.values, textposition='outside', texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)))
        fig.update_layout(**layout_chart(320, yaxis_opts={"tickfont": {"color": TEXTO, "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)
    with t3:
        hoje = datetime.now()
        agenda = df[(df["Status"] == "Agendado") & (df["Data"] >= hoje)].sort_values("Data").head(10)
        if not agenda.empty:
            for _, row in agenda.iterrows():
                st.markdown(f'<div class="alerta-item ok"><div style="display:flex; justify-content:space-between;"><div><strong>{row["Paciente"]}</strong><br><span style="font-size:0.78rem;">{row["Procedimento"]} • {row["Profissional"]}</span></div><div><strong>{row["Data"].strftime("%d/%m %H:%M")}</strong></div></div></div>', unsafe_allow_html=True)
        else:
            st.info("Nenhum agendamento futuro no momento.")
    with t4:
        perf = realizados.groupby("Profissional")["Valor"].sum().reset_index()
        fig = go.Figure(go.Bar(x=perf["Profissional"], y=perf["Valor"], marker_color=VERDE_NEON, text=perf["Valor"], texttemplate='R$ %{text:.2s}', textposition='outside', textfont=dict(color=TEXTO)))
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)
    with t5:
        freq = realizados["Paciente"].value_counts().reset_index()
        freq.columns = ["Paciente", "Visitas"]
        fig = px.histogram(freq, x="Visitas", nbins=10, color_discrete_sequence=[VERDE_NEON])
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)
    with t6:
        pgto = realizados["Forma_Pagamento"].value_counts().reset_index()
        pgto.columns = ["Forma", "Qtd"]
        fig = px.pie(pgto, values="Qtd", names="Forma", hole=0.5, color_discrete_sequence=[VERDE_NEON, AZUL_CLARO, ROXO])
        fig.update_traces(textposition="inside", textinfo="percent", textfont=dict(color="#0b1e2e", family="Inter", size=11))
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)
    kpis_pdf = {"Receita do período": formatar_brl(receita), "Atendimentos realizados": str(len(realizados)), "Ticket médio": formatar_brl(ticket), "Agendamentos futuros": str(agendados)}
    df_export = realizados.copy()
    df_export["Data"] = df_export["Data"].dt.strftime("%d/%m/%Y %H:%M")
    tabelas_export = {"Atendimentos Realizados": df_export[["Data", "Paciente", "Procedimento", "Profissional", "Valor"]].head(100), "Evolucao Mensal": df_evo}
    bloco_export("Clinica Estetica", periodo_label, tabelas_export, kpis_pdf, tabelas_export, [insight])
    st.markdown("---")
    cta_whatsapp(f"Oi Natan! Vi o demo do Pulse para clínicas (período {periodo_label}) e quero conversar.")
    botao_voltar()

# ═══════════════════════════════════════════════════════════════
# DASHBOARD BARBEARIA
# ═══════════════════════════════════════════════════════════════
def dash_barbearia():
    st.markdown('<div class="dash-header"><div><div class="dash-title">💈 Pulse • Barbearia</div><div class="dash-subtitle">Demo para Barbearias</div></div><span class="demo-badge">DEMO</span></div>', unsafe_allow_html=True)
    mes, ano, tipo_comp, mes_ant, ano_ant = seletor_periodo_comparacao("bar")
    periodo_label = f"{mes}/{ano}"
    with st.spinner("Carregando dados..."):
        df, df_prod, df_evo = gerar_dados_barbearia(mes, ano)
        if tipo_comp:
            df_ant, df_prod_ant, df_evo_ant = gerar_dados_barbearia(mes_ant, ano_ant)
        else:
            df_ant, df_prod_ant, df_evo_ant = None, None, None
    info_dados_ficticios()
    hoje = datetime.now()
    realizados = df[df["Status"] == "Realizado"]
    mes_atual = realizados[realizados["Data"] >= hoje - timedelta(days=30)]
    receita_serv = mes_atual["Valor"].sum()
    receita_prod = df_prod[df_prod["Data"] >= hoje - timedelta(days=30)]["Receita_Total"].sum()
    receita_total = receita_serv + receita_prod
    ticket = mes_atual["Valor"].mean() if not mes_atual.empty else 0
    agendados = len(df[df["Status"] == "Agendado"])
    receita_ant = ticket_ant = 0
    if df_ant is not None:
        real_ant = df_ant[df_ant["Status"] == "Realizado"]
        mes_ant_atual = real_ant[real_ant["Data"] >= hoje - timedelta(days=30)]
        receita_serv_ant = mes_ant_atual["Valor"].sum()
        receita_prod_ant = df_prod_ant[df_prod_ant["Data"] >= hoje - timedelta(days=30)]["Receita_Total"].sum()
        receita_ant = receita_serv_ant + receita_prod_ant
        ticket_ant = mes_ant_atual["Valor"].mean() if not mes_ant_atual.empty else 0
    insight = gerar_insight_barbearia({"receita": receita_total, "receita_ant": receita_ant, "ticket": ticket, "atendimentos": len(mes_atual)})
    st.markdown(f'<div class="insight-box">💡 <strong>Insight de {mes}/{ano}</strong><br>{insight}</div>', unsafe_allow_html=True)
    comp_label = gerar_label_comparacao(mes, ano, tipo_comp) if tipo_comp else ""
    c1, c2 = st.columns(2)
    with c1:
        kpi_card("RECEITA TOTAL", receita_total, receita_ant, formatter=formatar_brl, icone="💰", tooltip="Receita total (serviços + produtos)")
    with c2:
        kpi_card("ATENDIMENTOS", len(mes_atual), None, formatter=formatar_inteiro_br, icone="✂️", tooltip="Atendimentos realizados nos últimos 30 dias")
    c3, c4 = st.columns(2)
    with c3:
        kpi_card("TICKET MÉDIO", ticket, ticket_ant, formatter=formatar_brl, icone="🎫", tooltip="Valor médio por serviço")
    with c4:
        kpi_card("AGENDADOS", agendados, None, formatter=formatar_inteiro_br, icone="📅", tooltip="Atendimentos agendados futuramente")
    st.markdown("<br>", unsafe_allow_html=True)
    t1, t2, t3, t4, t5, t6 = st.tabs(["💰 Comissões", "🛍️ Produtos", "📅 Agenda", "👥 Clientes", "📊 Ocupação", "🏆 Serviços"])
    with t1:
        comissao = mes_atual.groupby("Barbeiro")["Comissao_Barbeiro"].sum().reset_index()
        fig = go.Figure(go.Bar(x=comissao["Comissao_Barbeiro"], y=comissao["Barbeiro"], orientation="h", marker_color=VERDE_NEON, text=comissao["Comissao_Barbeiro"], textposition='outside', texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)))
        fig.update_layout(**layout_chart(260, yaxis_opts={"tickfont": {"color": TEXTO, "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)
    with t2:
        top_prod = df_prod.groupby("Produto")["Receita_Total"].sum().sort_values(ascending=True).tail(5)
        fig = go.Figure(go.Bar(y=top_prod.index, x=top_prod.values, orientation="h", marker_color=VERDE_NEON, text=top_prod.values, textposition='outside', texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)))
        fig.update_layout(**layout_chart(260, yaxis_opts={"tickfont": {"color": TEXTO, "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)
    with t3:
        agenda = df[(df["Status"] == "Agendado") & (df["Data"] >= hoje)].sort_values("Data").head(10)
        if not agenda.empty:
            for _, row in agenda.iterrows():
                st.markdown(f'<div class="alerta-item ok"><div style="display:flex; justify-content:space-between;"><div><strong>{row["Cliente"]}</strong><br><span style="font-size:0.78rem;">{row["Servico"]} • {row["Barbeiro"]}</span></div><div><strong>{row["Data"].strftime("%d/%m %H:%M")}</strong></div></div></div>', unsafe_allow_html=True)
        else:
            st.info("Nenhum agendamento futuro no momento.")
    with t4:
        freq = realizados["Cliente"].value_counts().reset_index().head(10)
        freq.columns = ["Cliente", "Visitas"]
        fig = px.bar(freq, x="Visitas", y="Cliente", orientation="h", color_discrete_sequence=[VERDE_NEON])
        fig.update_layout(**layout_chart(320, yaxis_opts={"autorange": "reversed", "tickfont": {"color": TEXTO, "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)
    with t5:
        horas = ["09h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h"]
        np.random.seed(int(ano) + MESES.index(mes))
        ocupacao = np.random.randint(40, 100, size=len(horas))
        fig = go.Figure(go.Scatter(x=horas, y=ocupacao, mode="lines+markers", fill="tozeroy", line=dict(color=VERDE_NEON, width=3), fillcolor="rgba(0,255,136,0.2)"))
        fig.update_layout(**layout_chart(260, yaxis_opts={"title": "Ocupação (%)"}))
        st.plotly_chart(fig, use_container_width=True)
    with t6:
        serv = realizados.groupby("Servico")["Valor"].sum().sort_values(ascending=True).tail(6)
        fig = go.Figure(go.Bar(y=serv.index, x=serv.values, orientation="h", marker_color=VERDE_NEON, text=serv.values, textposition='outside', texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)))
        fig.update_layout(**layout_chart(320, yaxis_opts={"tickfont": {"color": TEXTO, "size": 10}}))
        st.plotly_chart(fig, use_container_width=True)
    kpis_pdf = {"Receita total": formatar_brl(receita_total), "Atendimentos": str(len(mes_atual)), "Ticket médio": formatar_brl(ticket), "Agendados": str(agendados)}
    df_export = realizados.copy()
    df_export["Data"] = df_export["Data"].dt.strftime("%d/%m/%Y %H:%M")
    tabelas_export = {"Atendimentos": df_export[["Data", "Cliente", "Servico", "Barbeiro", "Valor", "Comissao_Barbeiro"]].head(100), "Produtos Vendidos": df_prod[["Data", "Produto", "Quantidade", "Receita_Total", "Lucro_Bruto"]].head(100), "Evolucao Mensal": df_evo}
    bloco_export("Barbearia", periodo_label, tabelas_export, kpis_pdf, tabelas_export, [insight])
    st.markdown("---")
    cta_whatsapp(f"Oi Natan! Vi o demo do Pulse para barbearias (período {periodo_label}) e quero conversar.")
    botao_voltar()

# ═══════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════
if "perfil" not in st.session_state:
    st.session_state.perfil = None

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
