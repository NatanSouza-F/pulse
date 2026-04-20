"""
═══════════════════════════════════════════════════════════════════════════════
  PULSE — Demonstração Interativa de Soluções em Dados
  ──────────────────────────────────────────────────────────────────────────
  O pulso do seu negócio, no seu bolso.

  Versão:       v9 NASA
  Autor:        Natan Souza — Consultoria em Dados e Inteligência Comercial
  Contato:      contato@natansouza.com.br | WhatsApp (61) 99999-9999
  Atualizado:   2026

  ──────────────────────────────────────────────────────────────────────────
  ARQUITETURA
  ──────────────────────────────────────────────────────────────────────────
  1. Tela inicial         : Escolha de perfil + planos
  2. Dashboards (4)       : Corretora, Contábil, Clínica, Barbearia
  3. Visão do Gestor      : Consolidado executivo multi-nicho
  4. Página de Planos     : Tabela 3x3 com planos Básico/Intermediário/Avançado
  5. Engine de exports    : Excel (xlsxwriter) + PDF (reportlab)
  6. Filtros comparativos : MoM (mês anterior) e YoY (ano anterior)
═══════════════════════════════════════════════════════════════════════════════
"""

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  IMPORTS                                                              ║
# ╚═══════════════════════════════════════════════════════════════════════╝
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
from io import BytesIO


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURAÇÃO GLOBAL                                                  ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.set_page_config(
    page_title="Pulse • Demo",
    page_icon="💚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Contato
WHATSAPP = "5561999999999"


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  PALETA DE CORES — Design System Pulse                                ║
# ╚═══════════════════════════════════════════════════════════════════════╝
NAVY_DARK = "#0b1e2e"          # background principal
NAVY_MED = "#1a2e42"           # cards
NAVY_LIGHT = "#243b54"         # hover
VERDE_NEON = "#00ff88"         # accent / valores
VERDE = "#10b981"              # delta positivo
VERDE_AGUA = "#14b8a6"
VERDE_ESCURO = "#047857"
AZUL = "#3b82f6"
AZUL_CLARO = "#60a5fa"
VERMELHO = "#ef4444"           # delta negativo
AMBAR = "#f59e0b"              # atenção
ROXO = "#a855f7"
ROSA = "#ec4899"
TEXTO = "#f1f5f9"
TEXTO_MUTED = "#94a3b8"
BORDA = "#334155"


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  TEMPLATE PLOTLY — Identidade visual consistente                      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
pio.templates["pulse_dark"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, sans-serif", color=TEXTO, size=11),
        title=dict(font=dict(family="Inter, sans-serif", size=14, color=TEXTO)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,46,66,0.3)",
        colorway=[VERDE_NEON, AZUL_CLARO, ROXO, AMBAR, VERMELHO, ROSA, VERDE_AGUA],
    )
)
pio.templates.default = "pulse_dark"


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CONSTANTES                                                           ║
# ╚═══════════════════════════════════════════════════════════════════════╝
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  CSS GLOBAL — Estilo NASA                                             ║
# ╚═══════════════════════════════════════════════════════════════════════╝
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* ─────────── FONTE UNIFICADA ─────────── */
    *, html, body, [class*="css"], button, input, select, textarea,
    .stApp, .block-container, [data-testid], .js-plotly-plot, .plotly,
    .main-svg text, .stMarkdown, h1, h2, h3, h4, h5, h6, p, span, div, a, label {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ─────────── BACKGROUND ─────────── */
    .stApp {
        background:
            radial-gradient(ellipse at top, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at bottom, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
            #0b1e2e;
    }

    header[data-testid="stHeader"] { background: transparent; height: 0; }

    .block-container {
        max-width: 480px !important;
        padding: 3rem 1rem 1rem 1rem !important;
    }

    h1, h2, h3, h4, p, span, div, label { color: #f1f5f9; }

    /* ═══════════════════════════════════════════════════════════════
       CARROSSEL 3D ANIMADO — Estilo premium
       ═══════════════════════════════════════════════════════════════ */
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
        box-shadow:
            0 20px 40px rgba(0, 255, 136, 0.15),
            0 0 0 1px rgba(0, 255, 136, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        opacity: 0;
        animation: carousel-rotate 20s infinite ease-in-out;
    }
    .carousel-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
    }
    .carousel-card:nth-child(1) { animation-delay: 0s; }
    .carousel-card:nth-child(2) { animation-delay: 5s; }
    .carousel-card:nth-child(3) { animation-delay: 10s; }
    .carousel-card:nth-child(4) { animation-delay: 15s; }

    @keyframes carousel-rotate {
        0%, 100% { opacity: 0; transform: translateX(0) rotateY(90deg) scale(0.8); }
        5%       { opacity: 1; transform: translateX(0) rotateY(0deg) scale(1); }
        20%      { opacity: 1; transform: translateX(0) rotateY(0deg) scale(1); }
        25%      { opacity: 0; transform: translateX(-100%) rotateY(-90deg) scale(0.8); }
    }

    .carousel-icon { font-size: 1.8rem; line-height: 1; }
    .carousel-label {
        font-size: 0.65rem;
        font-weight: 700;
        color: #00ff88 !important;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    .carousel-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f1f5f9 !important;
        letter-spacing: -0.03em;
        line-height: 1;
        margin: 4px 0;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    .carousel-delta {
        font-size: 0.78rem;
        font-weight: 600;
        color: #00ff88 !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       KPI CARDS — Navy com glow
       ═══════════════════════════════════════════════════════════════ */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid rgba(0, 255, 136, 0.2) !important;
        border-radius: 16px;
        padding: 1rem;
        box-shadow:
            0 4px 12px -2px rgba(0, 0, 0, 0.3),
            0 0 0 1px rgba(0, 255, 136, 0.05);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        opacity: 0.7;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 255, 136, 0.4) !important;
        box-shadow:
            0 8px 20px -4px rgba(0, 0, 0, 0.4),
            0 0 30px rgba(0, 255, 136, 0.15);
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="stMetricValue"] {
        color: #00ff88 !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
    }
    [data-testid="stMetricDelta"] {
        font-weight: 600 !important;
        font-size: 0.78rem !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       BOTÕES
       ═══════════════════════════════════════════════════════════════ */
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
    .stButton button[kind="secondary"] {
        background: rgba(26, 46, 66, 0.6);
        border: 1px solid #334155;
        color: #f1f5f9;
        box-shadow: none;
    }
    .stButton button[kind="secondary"]:hover {
        background: #243b54;
        border-color: rgba(0, 255, 136, 0.3);
    }

    /* ═══════════════════════════════════════════════════════════════
       TABS
       ═══════════════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
        flex-wrap: wrap;
    }
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
        transition: all 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #243b54;
        color: #f1f5f9 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #10b981 0%, #00ff88 100%) !important;
        color: #0b1e2e !important;
        border-color: #00ff88 !important;
        box-shadow: 0 2px 12px rgba(0, 255, 136, 0.4);
        font-weight: 700 !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       INPUTS E SELECTS
       ═══════════════════════════════════════════════════════════════ */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: #1a2e42 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {
        border-color: rgba(0, 255, 136, 0.4) !important;
    }
    div[data-baseweb="select"] > div > div,
    div[data-baseweb="input"] > div > div,
    input, select { color: #f1f5f9 !important; }

    div[role="listbox"] { background: #1a2e42 !important; }
    div[role="option"] { color: #f1f5f9 !important; }
    div[role="option"]:hover { background: #243b54 !important; }

    .stSelectbox label, .stTextInput label, .stDateInput label {
        color: #94a3b8 !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       DATAFRAME
       ═══════════════════════════════════════════════════════════════ */
    div[data-testid="stDataFrame"] {
        border-radius: 14px !important;
        overflow: hidden;
        border: 1px solid #334155 !important;
        background: #1a2e42 !important;
    }
    div[data-testid="stDataFrame"] * {
        background: #1a2e42 !important;
        color: #f1f5f9 !important;
    }
    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: #243b54 !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       CARDS DE PERFIL
       ═══════════════════════════════════════════════════════════════ */
    .perfil-card {
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 1.3rem;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }
    .perfil-card:hover {
        border-color: rgba(0, 255, 136, 0.4);
        box-shadow: 0 8px 25px rgba(0, 255, 136, 0.12);
        transform: translateY(-1px);
    }
    .perfil-titulo { color: #f1f5f9 !important; font-weight: 700; }
    .perfil-desc { color: #94a3b8 !important; }

    /* ═══════════════════════════════════════════════════════════════
       LOGO
       ═══════════════════════════════════════════════════════════════ */
    .pulse-logo {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00ff88 0%, #14b8a6 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 0;
        letter-spacing: -0.04em;
        filter: drop-shadow(0 0 20px rgba(0, 255, 136, 0.3));
    }
    .pulse-slogan {
        text-align: center;
        color: #94a3b8 !important;
        font-weight: 500;
        margin-top: 4px;
    }

    /* ═══════════════════════════════════════════════════════════════
       BADGE DEMO
       ═══════════════════════════════════════════════════════════════ */
    .demo-badge {
        background: rgba(0, 255, 136, 0.12);
        border: 1px solid rgba(0, 255, 136, 0.4);
        color: #00ff88;
        padding: 4px 12px;
        border-radius: 40px;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    /* ═══════════════════════════════════════════════════════════════
       WHATSAPP CTA
       ═══════════════════════════════════════════════════════════════ */
    .cta-whatsapp {
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white !important;
        padding: 14px 28px;
        border-radius: 60px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 8px 20px rgba(37, 211, 102, 0.4);
        font-size: 0.95rem;
    }

    /* ═══════════════════════════════════════════════════════════════
       INFO / INSIGHTS
       ═══════════════════════════════════════════════════════════════ */
    .info-box {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.08) 0%, rgba(20, 184, 166, 0.05) 100%);
        border-left: 3px solid #00ff88;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 12px 0;
        color: #f1f5f9 !important;
    }
    .info-box strong { color: #00ff88 !important; }

    .insight-box {
        background: linear-gradient(135deg, rgba(26, 46, 66, 0.8) 0%, rgba(36, 59, 84, 0.6) 100%);
        border: 1px solid rgba(0, 255, 136, 0.25);
        border-radius: 14px;
        padding: 16px;
        margin: 16px 0;
        color: #f1f5f9 !important;
        position: relative;
        overflow: hidden;
    }
    .insight-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #00ff88, #14b8a6);
    }
    .insight-box strong { color: #00ff88 !important; }

    /* ═══════════════════════════════════════════════════════════════
       ALERTAS
       ═══════════════════════════════════════════════════════════════ */
    .alerta-item {
        background: #1a2e42;
        border: 1px solid #334155;
        border-left: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 8px;
        color: #f1f5f9 !important;
    }
    .alerta-item strong { color: #f1f5f9 !important; }
    .alerta-item span { color: #94a3b8 !important; }
    .alerta-item.urgente { border-left-color: #ef4444; }
    .alerta-item.ok { border-left-color: #00ff88; }

    /* ═══════════════════════════════════════════════════════════════
       HEADER DE DASHBOARD
       ═══════════════════════════════════════════════════════════════ */
    .dash-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding: 10px 0;
        border-bottom: 1px solid rgba(0, 255, 136, 0.15);
    }
    .dash-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: -0.02em;
    }
    .dash-subtitle {
        color: #94a3b8 !important;
        font-size: 0.78rem;
    }

    /* ═══════════════════════════════════════════════════════════════
       GRÁFICOS
       ═══════════════════════════════════════════════════════════════ */
    .js-plotly-plot {
        border-radius: 16px !important;
        overflow: hidden;
        background: #1a2e42;
        border: 1px solid #334155;
    }
    .main-svg { background: transparent !important; }

    /* ═══════════════════════════════════════════════════════════════
       DELTA BADGE (comparador)
       ═══════════════════════════════════════════════════════════════ */
    .delta-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 40px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-left: 6px;
    }
    .delta-up {
        background: rgba(0, 255, 136, 0.15);
        color: #00ff88;
        border: 1px solid rgba(0, 255, 136, 0.3);
    }
    .delta-down {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .delta-neutro {
        background: rgba(148, 163, 184, 0.15);
        color: #94a3b8;
        border: 1px solid rgba(148, 163, 184, 0.3);
    }

    /* ═══════════════════════════════════════════════════════════════
       EXPORT SECTION
       ═══════════════════════════════════════════════════════════════ */
    .export-section {
        background: linear-gradient(135deg, rgba(26, 46, 66, 0.6) 0%, rgba(36, 59, 84, 0.4) 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px;
        margin: 20px 0 12px 0;
    }
    .export-title {
        color: #00ff88;
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* ═══════════════════════════════════════════════════════════════
       PLANOS (NOVO - Tela de preços)
       ═══════════════════════════════════════════════════════════════ */
    .plano-card {
        background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 1.5rem 1.3rem;
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .plano-card:hover {
        transform: translateY(-3px);
        border-color: rgba(0, 255, 136, 0.4);
        box-shadow: 0 12px 30px rgba(0, 255, 136, 0.12);
    }
    .plano-card.destaque {
        border: 2px solid #00ff88;
        box-shadow: 0 8px 25px rgba(0, 255, 136, 0.2);
    }
    .plano-card.destaque::before {
        content: "RECOMENDADO";
        position: absolute;
        top: 12px;
        right: -35px;
        background: linear-gradient(135deg, #10b981, #00ff88);
        color: #0b1e2e;
        font-size: 0.6rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        padding: 4px 40px;
        transform: rotate(45deg);
    }
    .plano-tier {
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        color: #00ff88;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .plano-nome {
        font-size: 1.4rem;
        font-weight: 800;
        color: #f1f5f9;
        margin-bottom: 12px;
        letter-spacing: -0.02em;
    }
    .plano-preco {
        font-size: 2rem;
        font-weight: 900;
        color: #00ff88;
        letter-spacing: -0.03em;
        line-height: 1;
        margin: 8px 0 2px 0;
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
    }
    .plano-preco-sub {
        color: #94a3b8;
        font-size: 0.75rem;
        margin-bottom: 14px;
    }
    .plano-mensalidade {
        font-size: 0.95rem;
        font-weight: 700;
        color: #14b8a6;
        padding: 8px 12px;
        background: rgba(20, 184, 166, 0.1);
        border-radius: 8px;
        display: inline-block;
        margin-bottom: 14px;
    }
    .plano-features {
        list-style: none;
        padding: 0;
        margin: 0 0 16px 0;
    }
    .plano-features li {
        padding: 6px 0;
        color: #cbd5e1;
        font-size: 0.88rem;
        line-height: 1.4;
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }
    .plano-features li::before {
        content: "✓";
        color: #00ff88;
        font-weight: 900;
        flex-shrink: 0;
    }
    .plano-features li.indisponivel {
        color: #64748b;
        opacity: 0.5;
    }
    .plano-features li.indisponivel::before {
        content: "—";
        color: #64748b;
    }

    /* ═══════════════════════════════════════════════════════════════
       SCROLLBAR
       ═══════════════════════════════════════════════════════════════ */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0b1e2e; }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0, 255, 136, 0.3); }

    /* ═══════════════════════════════════════════════════════════════
       LOADING SPINNER
       ═══════════════════════════════════════════════════════════════ */
    .stSpinner > div {
        border-color: #00ff88 transparent transparent transparent !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       RESPONSIVO MOBILE
       ═══════════════════════════════════════════════════════════════ */
    @media (max-width: 480px) {
        .carousel-wrapper { height: 160px; }
        .carousel-card {
            width: 260px; height: 140px;
            margin-left: -130px; padding: 16px 20px;
        }
        .carousel-value { font-size: 1.9rem; }
        .pulse-logo { font-size: 2.5rem; }
        .plano-preco { font-size: 1.7rem; }
    }
</style>
""", unsafe_allow_html=True)


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  ESTADO DA SESSÃO                                                     ║
# ╚═══════════════════════════════════════════════════════════════════════╝
if "perfil" not in st.session_state:
    st.session_state.perfil = None

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  HELPERS DE FORMATAÇÃO                                                ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def formatar_brl(valor):
    """Formata valor monetário em R$ brasileiro (ex: R$ 1.234,56)."""
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"


def formatar_brl_compacto(valor):
    """R$ 187.543 → R$ 187k  |  R$ 1.250.000 → R$ 1,2M"""
    try:
        v = float(valor)
        if abs(v) >= 1_000_000:
            return f"R$ {v/1_000_000:.1f}M".replace(".", ",")
        elif abs(v) >= 1_000:
            return f"R$ {v/1_000:.0f}k"
        return f"R$ {v:.0f}"
    except (ValueError, TypeError):
        return "R$ 0"


def formatar_inteiro_br(valor):
    """Formata inteiro com separador de milhar (ex: 1.234)."""
    try:
        return f"{int(valor):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "0"


def formatar_pct(valor):
    """Formata percentual com sinal (ex: +12,5%)."""
    return f"{valor:+.1f}%".replace(".", ",")


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  ENGINE DE COMPARAÇÃO — MoM (mês anterior) / YoY (ano anterior)       ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def calcular_delta(atual, anterior):
    """Retorna (delta_pct, classe_css, seta) ou (None, 'delta-neutro', '—')."""
    if anterior == 0 or anterior is None:
        return None, "delta-neutro", "—"
    try:
        delta = ((atual - anterior) / anterior) * 100
        if delta > 0.5:
            return delta, "delta-up", "▲"
        elif delta < -0.5:
            return delta, "delta-down", "▼"
        return delta, "delta-neutro", "●"
    except (ValueError, TypeError):
        return None, "delta-neutro", "—"


def gerar_label_comparacao(mes_atual, ano_atual, tipo_comp):
    """Gera label legível do período anterior (ex: 'Mai/25')."""
    idx_atual = MESES.index(mes_atual)
    if tipo_comp == "MoM":
        if idx_atual == 0:
            mes_ant, ano_ant = "Dez", str(int(ano_atual) - 1)
        else:
            mes_ant, ano_ant = MESES[idx_atual - 1], ano_atual
        return f"{mes_ant}/{ano_ant[-2:]}"
    elif tipo_comp == "YoY":
        return f"{mes_atual}/{str(int(ano_atual) - 1)[-2:]}"
    return ""


def delta_badge_html(delta_pct, classe, seta):
    """Renderiza badge HTML com o delta."""
    if delta_pct is None:
        return f'<span class="delta-badge {classe}">— sem base</span>'
    return f'<span class="delta-badge {classe}">{seta} {formatar_pct(delta_pct)}</span>'


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  COMPONENTES UI                                                       ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def botao_voltar():
    """Botão padrão pra voltar à tela inicial."""
    if st.button("← Voltar para escolha de perfil", use_container_width=True, type="secondary"):
        st.session_state.perfil = None
        st.rerun()


def cta_whatsapp(texto_msg):
    """Botão de CTA grande pro WhatsApp com mensagem pré-preenchida."""
    msg = texto_msg.replace(" ", "%20").replace("\n", "%0A")
    link = f"https://wa.me/{WHATSAPP}?text={msg}"
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
    """Info box padrão informando que são dados de demo."""
    st.markdown("""
    <div class="info-box">
        <strong>💡 Demo com dados fictícios.</strong><br>
        Seus dados reais, assim, em até 3 semanas.
    </div>
    """, unsafe_allow_html=True)


def layout_chart(altura=280, yaxis_opts=None, showlegend=True):
    """Layout padrão pros gráficos Plotly."""
    base = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(26,46,66,0.3)",
        "font": {"family": "Inter, sans-serif", "color": TEXTO, "size": 11},
        "xaxis": {
            "gridcolor": "rgba(51, 65, 85, 0.4)",
            "linecolor": BORDA,
            "tickfont": {"family": "Inter, sans-serif", "color": TEXTO_MUTED, "size": 10},
        },
        "yaxis": {
            "gridcolor": "rgba(51, 65, 85, 0.4)",
            "linecolor": BORDA,
            "tickfont": {"family": "Inter, sans-serif", "color": TEXTO_MUTED, "size": 10},
        },
        "margin": {"t": 30, "b": 40, "l": 50, "r": 20},
        "height": altura,
        "hoverlabel": {
            "bgcolor": "#1a2e42",
            "font": {"family": "Inter, sans-serif", "color": TEXTO},
            "bordercolor": VERDE_NEON,
        },
        "legend": {"font": {"family": "Inter, sans-serif", "color": TEXTO, "size": 11}},
        "showlegend": showlegend,
    }
    if yaxis_opts:
        base["yaxis"].update(yaxis_opts)
    return base


def kpi_card(label, valor_atual, valor_anterior=None, formatter=None, label_comp="vs ant"):
    """
    KPI card customizado com comparador.
    Se valor_anterior for fornecido, mostra badge de delta.
    """
    if formatter is None:
        formatter = formatar_inteiro_br

    if valor_anterior is not None:
        delta, classe, seta = calcular_delta(valor_atual, valor_anterior)
        badge = delta_badge_html(delta, classe, seta)
        comp_line = f"""
        <div style="color: #94a3b8; font-size: 0.72rem; margin-top: 4px;">
            {label_comp}: <strong style="color: #cbd5e1;">{formatter(valor_anterior)}</strong>
            {badge}
        </div>
        """
    else:
        comp_line = ""

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a2e42 0%, #243b54 100%);
                border: 1px solid rgba(0, 255, 136, 0.2);
                border-radius: 16px; padding: 1rem;
                box-shadow: 0 4px 12px -2px rgba(0,0,0,0.3);
                position: relative; overflow: hidden; margin-bottom: 12px;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 2px;
                    background: linear-gradient(90deg, transparent, #00ff88, transparent);
                    opacity: 0.7;"></div>
        <div style="color: #94a3b8; font-size: 0.68rem; font-weight: 700;
                    text-transform: uppercase; letter-spacing: 0.08em;">{label}</div>
        <div style="color: #00ff88; font-size: 1.6rem; font-weight: 800;
                    letter-spacing: -0.02em; margin-top: 4px;
                    text-shadow: 0 0 15px rgba(0,255,136,0.3);">{formatter(valor_atual)}</div>
        {comp_line}
    </div>
    """, unsafe_allow_html=True)


def carrossel_animado():
    """Carrossel 3D animado com 4 KPIs giratórios (tela inicial)."""
    st.markdown("""
    <div class="carousel-wrapper">
        <div class="carousel-track">
            <div class="carousel-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="carousel-label">Carteira Ativa</span>
                    <span class="carousel-icon">🛡️</span>
                </div>
                <div>
                    <div class="carousel-value">2.431</div>
                    <div class="carousel-delta">▲ +12% vs mês anterior</div>
                </div>
            </div>
            <div class="carousel-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="carousel-label">Receita Mensal</span>
                    <span class="carousel-icon">💰</span>
                </div>
                <div>
                    <div class="carousel-value">R$ 187k</div>
                    <div class="carousel-delta">▲ +8,3% vs ano anterior</div>
                </div>
            </div>
            <div class="carousel-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="carousel-label">Taxa Retenção</span>
                    <span class="carousel-icon">🔄</span>
                </div>
                <div>
                    <div class="carousel-value">94,7%</div>
                    <div class="carousel-delta">▲ +2,1pp últimos 30d</div>
                </div>
            </div>
            <div class="carousel-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="carousel-label">NPS</span>
                    <span class="carousel-icon">⭐</span>
                </div>
                <div>
                    <div class="carousel-value">72</div>
                    <div class="carousel-delta">Zona de excelência</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  GERADORES DE DADOS — Dados fictícios realistas                       ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def gerar_dados_corretora(mes_ref="Jun", ano_ref="2026"):
    """Gera dados de carteira de corretora de seguros."""
    np.random.seed(42 + MESES.index(mes_ref) + int(ano_ref))
    base = 200 + MESES.index(mes_ref) * 8 + (int(ano_ref) - 2025) * 20
    clientes = [f"Cliente {i}" for i in range(1, base + 1)]
    ramos = ["Auto", "Vida", "Residencial", "Empresarial", "Saúde"]
    seguradoras = ["Porto Seguro", "Bradesco", "SulAmérica", "Allianz", "Mapfre"]

    dados = [{
        "Cliente": c,
        "Ramo": np.random.choice(ramos),
        "Seguradora": np.random.choice(seguradoras),
        "Status": np.random.choice(["Ativo", "Vencendo", "Cancelado"], p=[0.7, 0.2, 0.1]),
        "Premio_Anual": round(np.random.uniform(800, 8000), 2),
        "Comissao_Anual": round(np.random.uniform(100, 1500), 2),
        "Comissao_Mensal": round(np.random.uniform(10, 150), 2),
        "Dias_Para_Renovacao": np.random.randint(-30, 120),
    } for c in clientes]

    df = pd.DataFrame(dados)

    evolucao = [{
        "Mes": mes,
        "Comissao_Total": round(8000 * (1 + 0.03 * i) * np.random.uniform(0.9, 1.1), 2),
        "Novos_Contratos": int(12 + i * 1.5 + np.random.randint(-3, 5)),
        "Cancelamentos": int(5 + i * 0.3 + np.random.randint(-2, 3)),
    } for i, mes in enumerate(MESES)]

    return df, pd.DataFrame(evolucao)


def gerar_dados_contabil(mes_ref="Jun", ano_ref="2026"):
    """Gera dados de carteira de escritório contábil."""
    np.random.seed(43 + MESES.index(mes_ref) + int(ano_ref))
    base = 60 + (int(ano_ref) - 2025) * 10
    regimes = ["Simples Nacional", "Lucro Presumido", "Lucro Real", "MEI"]

    dados = [{
        "Empresa": f"Empresa {i}",
        "Regime_Tributario": np.random.choice(regimes, p=[0.5, 0.2, 0.1, 0.2]),
        "Honorario_Mensal": round(np.random.uniform(400, 3500), 2),
        "Status_Fechamento": np.random.choice(["Entregue", "Pendente", "Atrasado"], p=[0.6, 0.25, 0.15]),
        "Dias_Para_Entrega": np.random.randint(-5, 20),
    } for i in range(1, base + 1)]

    df = pd.DataFrame(dados)

    prod = [{
        "Mes": mes,
        "Horas_Fechamento": round(120 * (1 + 0.05 * i) * np.random.uniform(0.9, 1.1), 1),
        "Receita_Honorarios": round(12000 * (1 + 0.03 * i) * np.random.uniform(0.95, 1.05), 2),
    } for i, mes in enumerate(MESES)]

    return df, pd.DataFrame(prod)


def gerar_dados_clinica(mes_ref="Jun", ano_ref="2026"):
    """Gera dados de atendimentos de clínica estética."""
    np.random.seed(44 + MESES.index(mes_ref) + int(ano_ref))
    pacientes = [f"Paciente {i}" for i in range(1, 151)]
    procedimentos = ["Limpeza de Pele", "Botox", "Preenchimento", "Massagem",
                     "Depilação a Laser", "Peeling"]
    profissionais = ["Dra. Ana", "Dra. Carla", "Dr. Paulo", "Dra. Fernanda"]
    hoje = datetime.now()

    dados = []
    for _ in range(400):
        if np.random.rand() < 0.3:
            data = hoje + timedelta(days=np.random.randint(1, 30))
            status = "Agendado"
        else:
            data = hoje - timedelta(days=np.random.randint(0, 60))
            status = np.random.choice(["Realizado", "Cancelado"], p=[0.8, 0.2])

        dados.append({
            "Data": data,
            "Paciente": np.random.choice(pacientes),
            "Procedimento": np.random.choice(procedimentos),
            "Profissional": np.random.choice(profissionais),
            "Valor": round(np.random.uniform(150, 1200), 2),
            "Status": status,
            "Forma_Pagamento": np.random.choice(["PIX", "Cartão", "Dinheiro"]),
        })

    df = pd.DataFrame(dados)

    evo = [{
        "Mes": mes,
        "Receita": round(28000 * (1 + 0.03 * i) * np.random.uniform(0.9, 1.1), 2),
        "Ticket_Medio": round((28000 * (1 + 0.03 * i)) / (130 + i * 5), 2),
    } for i, mes in enumerate(MESES)]

    return df, pd.DataFrame(evo)


def gerar_dados_barbearia(mes_ref="Jun", ano_ref="2026"):
    """Gera dados de atendimentos + produtos de barbearia."""
    np.random.seed(45 + MESES.index(mes_ref) + int(ano_ref))
    clientes = [f"Cliente {i}" for i in range(1, 201)]
    servicos = ["Corte", "Barba", "Sobrancelha", "Corte + Barba", "Hidratação"]
    barbeiros = ["João", "Pedro", "Lucas", "Mateus", "André"]
    hoje = datetime.now()

    dados = []
    for _ in range(600):
        if np.random.rand() < 0.35:
            data = hoje + timedelta(days=np.random.randint(1, 30))
            status = "Agendado"
        else:
            data = hoje - timedelta(days=np.random.randint(0, 90))
            status = np.random.choice(["Realizado", "Cancelado"], p=[0.85, 0.15])

        barbeiro = np.random.choice(barbeiros)
        comissao_pct = 0.4 if barbeiro in ["João", "Pedro"] else 0.35
        valor = round(np.random.uniform(35, 120), 2)

        dados.append({
            "Data": data,
            "Cliente": np.random.choice(clientes),
            "Servico": np.random.choice(servicos),
            "Barbeiro": barbeiro,
            "Valor": valor,
            "Comissao_Barbeiro": round(valor * comissao_pct, 2),
            "Gorjeta": np.random.choice([0, 5, 10, 15], p=[0.5, 0.3, 0.15, 0.05]),
            "Status": status,
        })

    df = pd.DataFrame(dados)

    produtos = ["Pomada", "Shampoo", "Óleo Barba", "Cera", "Perfume"]
    prod_data = []
    for _ in range(200):
        preco = round(np.random.uniform(25, 90), 2)
        qtd = np.random.randint(1, 4)
        receita = preco * qtd
        prod_data.append({
            "Data": hoje - timedelta(days=np.random.randint(0, 90)),
            "Produto": np.random.choice(produtos),
            "Quantidade": qtd,
            "Preco_Unitario": preco,
            "Receita_Total": receita,
            "Lucro_Bruto": round(receita * 0.45, 2),
        })

    df_prod = pd.DataFrame(prod_data)

    evo = [{
        "Mes": mes,
        "Receita_Servicos": round(18000 * (1 + 0.02 * i) * np.random.uniform(0.9, 1.1), 2),
        "Receita_Produtos": round(4000 * (1 + 0.03 * i) * np.random.uniform(0.9, 1.1), 2),
        "Atendimentos": int(120 + i * 3),
    } for i, mes in enumerate(MESES)]

    return df, df_prod, pd.DataFrame(evo)


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  INSIGHTS AUTOMÁTICOS                                                 ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def gerar_insight_corretora(dados):
    """Insight contextual baseado em regras estatísticas."""
    ativos, vencendo = dados.get("ativos", 0), dados.get("vencendo", 0)
    comissao, comissao_ant = dados.get("comissao", 0), dados.get("comissao_ant", 0)

    partes = []
    if vencendo > 0:
        risco = (vencendo / max(ativos, 1)) * comissao
        partes.append(
            f"⚠️ <strong>{vencendo} apólices vencem em 30 dias</strong> — "
            f"aproximadamente {formatar_brl(risco)}/mês em risco."
        )
    if comissao_ant and comissao > comissao_ant:
        pct = ((comissao - comissao_ant) / comissao_ant) * 100
        partes.append(f"📈 Comissão cresceu <strong>{pct:.1f}%</strong> — tendência positiva sustentada.")
    return " ".join(partes) if partes else "✅ Operação estável. Foco em prospecção."


def gerar_insight_contabil(dados):
    total = dados.get("total", 0)
    atrasados, pct_prazo = dados.get("atrasados", 0), dados.get("pct_prazo", 0)

    partes = []
    if atrasados > 0:
        pct = (atrasados / max(total, 1)) * 100
        partes.append(
            f"⚠️ <strong>{atrasados} clientes em atraso</strong> ({pct:.1f}% da carteira)."
        )
    if pct_prazo >= 80:
        partes.append(f"✅ <strong>{pct_prazo:.0f}% das entregas no prazo</strong> — acima da média do setor (72%).")
    elif pct_prazo < 70:
        partes.append(f"🎯 Meta: 80%. Atual: {pct_prazo:.0f}%. Gap: {80 - pct_prazo:.0f}pp.")
    return " ".join(partes) if partes else "✅ Operação fluindo."


def gerar_insight_clinica(dados):
    receita, receita_ant = dados.get("receita", 0), dados.get("receita_ant", 0)
    ticket, agendados = dados.get("ticket", 0), dados.get("agendados", 0)

    partes = []
    if receita_ant and receita > receita_ant:
        pct = ((receita - receita_ant) / receita_ant) * 100
        partes.append(f"💚 Receita cresceu <strong>{pct:.1f}%</strong> vs período anterior.")
    if agendados > 0:
        partes.append(
            f"📅 <strong>{agendados} atendimentos agendados</strong> — "
            f"projeção de {formatar_brl(agendados * ticket)} em receita futura."
        )
    return " ".join(partes) if partes else "✅ Operação estável."


def gerar_insight_barbearia(dados):
    receita, receita_ant = dados.get("receita", 0), dados.get("receita_ant", 0)
    ticket, atend = dados.get("ticket", 0), dados.get("atendimentos", 0)

    partes = []
    if receita_ant and receita > receita_ant:
        pct = ((receita - receita_ant) / receita_ant) * 100
        partes.append(f"💚 Receita cresceu <strong>{pct:.1f}%</strong> vs período anterior.")
    if atend > 0:
        partes.append(f"✂️ Ticket médio de <strong>{formatar_brl(ticket)}</strong> em {atend} atendimentos.")
    return " ".join(partes) if partes else "✅ Barbearia fluindo bem."


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  SELETOR DE PERÍODO + COMPARAÇÃO                                      ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def seletor_periodo_comparacao(key_prefix):
    """Retorna (mes_atual, ano_atual, tipo_comp, mes_ant, ano_ant)."""
    col1, col2, col3 = st.columns([2, 2, 3])
    with col1:
        mes = st.selectbox("Mês", MESES, index=5, key=f"{key_prefix}_mes")
    with col2:
        ano = st.selectbox("Ano", ["2024", "2025", "2026"], index=2, key=f"{key_prefix}_ano")
    with col3:
        tipo_comp = st.selectbox(
            "Comparar com",
            ["Mês anterior", "Ano anterior", "Sem comparação"],
            index=0, key=f"{key_prefix}_comp"
        )

    idx = MESES.index(mes)
    mes_ant, ano_ant = None, None

    if tipo_comp == "Mês anterior":
        if idx == 0:
            mes_ant, ano_ant = "Dez", str(int(ano) - 1)
        else:
            mes_ant, ano_ant = MESES[idx - 1], ano
    elif tipo_comp == "Ano anterior":
        mes_ant, ano_ant = mes, str(int(ano) - 1)

    tipo_short = ("MoM" if tipo_comp == "Mês anterior"
                  else "YoY" if tipo_comp == "Ano anterior"
                  else None)
    return mes, ano, tipo_short, mes_ant, ano_ant


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  EXPORT EXCEL                                                         ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def exportar_excel(nome_base, dfs_dict, titulo_relatorio, periodo):
    """Gera arquivo Excel com capa Pulse + múltiplas abas formatadas."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        wb = writer.book

        # ───── Aba de capa ─────
        cover = wb.add_worksheet("Resumo")
        cover.set_column("A:A", 35)
        cover.set_column("B:B", 45)

        fmt_titulo = wb.add_format({
            "font_name": "Calibri", "font_size": 22, "bold": True,
            "font_color": "#00ff88", "bg_color": "#0b1e2e",
            "align": "center", "valign": "vcenter"
        })
        fmt_sub = wb.add_format({
            "font_name": "Calibri", "font_size": 12,
            "font_color": "#ffffff", "bg_color": "#1a2e42",
            "align": "center", "valign": "vcenter", "italic": True
        })
        fmt_label = wb.add_format({
            "font_name": "Calibri", "font_size": 11, "bold": True,
            "font_color": "#047857", "bg_color": "#ecfdf5",
            "border": 1, "border_color": "#10b981"
        })
        fmt_valor = wb.add_format({
            "font_name": "Calibri", "font_size": 11,
            "font_color": "#0f172a", "bg_color": "#ffffff",
            "border": 1, "border_color": "#10b981"
        })

        cover.set_row(1, 50)
        cover.merge_range("A2:B2", "PULSE", fmt_titulo)
        cover.set_row(2, 30)
        cover.merge_range("A3:B3", titulo_relatorio, fmt_sub)

        cover.write("A5", "Período", fmt_label)
        cover.write("B5", periodo, fmt_valor)
        cover.write("A6", "Gerado em", fmt_label)
        cover.write("B6", datetime.now().strftime("%d/%m/%Y %H:%M"), fmt_valor)
        cover.write("A7", "Tipo", fmt_label)
        cover.write("B7", "Demo com dados fictícios", fmt_valor)

        cover.merge_range("A9:B9",
            "Desenvolvido por Natan Souza — Consultoria em Dados e Inteligência Comercial",
            wb.add_format({"italic": True, "align": "center",
                           "font_color": "#64748b", "font_size": 10}))

        # ───── Formatos pras abas de dados ─────
        fmt_header = wb.add_format({
            "font_name": "Calibri", "font_size": 11, "bold": True,
            "font_color": "#ffffff", "bg_color": "#047857",
            "border": 1, "align": "center", "valign": "vcenter"
        })
        fmt_cell = wb.add_format({
            "font_name": "Calibri", "font_size": 10,
            "border": 1, "border_color": "#e2e8f0"
        })
        fmt_money = wb.add_format({
            "font_name": "Calibri", "font_size": 10,
            "border": 1, "border_color": "#e2e8f0",
            "num_format": 'R$ #,##0.00'
        })

        # ───── Abas de dados ─────
        for nome_aba, df in dfs_dict.items():
            df.to_excel(writer, sheet_name=nome_aba[:31], index=False, startrow=1)
            ws = writer.sheets[nome_aba[:31]]

            # Título da aba
            ws.merge_range(0, 0, 0, len(df.columns) - 1, nome_aba,
                wb.add_format({
                    "font_name": "Calibri", "font_size": 14, "bold": True,
                    "font_color": "#047857", "bg_color": "#ecfdf5",
                    "align": "center", "valign": "vcenter", "border": 1
                }))

            # Cabeçalhos
            for col_idx, col_name in enumerate(df.columns):
                ws.write(1, col_idx, col_name, fmt_header)
                ws.set_column(col_idx, col_idx, max(14, min(28, len(col_name) + 6)))

            # Dados
            for row_idx, row in df.iterrows():
                for col_idx, col_name in enumerate(df.columns):
                    val = row[col_name]
                    if any(k in col_name.lower() for k in ["valor", "premio", "comiss",
                                                           "honor", "receita", "lucro",
                                                           "ticket", "preco"]):
                        try:
                            ws.write_number(row_idx + 2, col_idx, float(val), fmt_money)
                        except (ValueError, TypeError):
                            ws.write(row_idx + 2, col_idx, str(val), fmt_cell)
                    else:
                        ws.write(row_idx + 2, col_idx,
                                str(val) if pd.isna(val) else val, fmt_cell)

    return output.getvalue()


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  EXPORT PDF EXECUTIVO                                                 ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def exportar_pdf(titulo_relatorio, periodo, kpis_dict, tabelas_dict, insights_list):
    """Gera PDF executivo com capa + KPIs + insights + tabelas."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                    TableStyle, PageBreak)
    from reportlab.lib.enums import TA_CENTER

    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4,
                             leftMargin=1.8*cm, rightMargin=1.8*cm,
                             topMargin=2*cm, bottomMargin=2*cm)

    s_titulo = ParagraphStyle("T", fontSize=36, textColor=colors.HexColor("#00ff88"),
                              fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4, leading=40)
    s_sub = ParagraphStyle("S", fontSize=12, textColor=colors.HexColor("#64748b"),
                           alignment=TA_CENTER, spaceAfter=20, leading=14)
    s_secao = ParagraphStyle("Sec", fontSize=14, textColor=colors.HexColor("#047857"),
                             fontName="Helvetica-Bold", spaceAfter=10, spaceBefore=16, leading=16)
    s_texto = ParagraphStyle("Tx", fontSize=10, textColor=colors.HexColor("#0f172a"),
                             leading=14, spaceAfter=8)
    s_ins = ParagraphStyle("In", fontSize=10, textColor=colors.HexColor("#064e3b"),
                           leading=14, spaceAfter=6, leftIndent=12)

    el = []

    # ───── Capa ─────
    el.append(Spacer(1, 3*cm))
    el.append(Paragraph("PULSE", s_titulo))
    el.append(Paragraph("O pulso do seu negócio, no seu bolso.", s_sub))
    el.append(Spacer(1, 1*cm))

    capa = [
        ["Relatório:", titulo_relatorio],
        ["Período:", periodo],
        ["Gerado em:", datetime.now().strftime("%d/%m/%Y %H:%M")],
        ["Tipo:", "Demo com dados fictícios"],
    ]
    t_capa = Table(capa, colWidths=[4*cm, 11*cm])
    t_capa.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#64748b")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#0f172a")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    el.append(t_capa)
    el.append(Spacer(1, 4*cm))
    el.append(Paragraph(
        "Desenvolvido por <b>Natan Souza</b><br/>Consultoria em Dados e Inteligência Comercial",
        ParagraphStyle("A", fontSize=10, textColor=colors.HexColor("#64748b"), alignment=TA_CENTER)
    ))
    el.append(PageBreak())

    # ───── KPIs ─────
    el.append(Paragraph("Indicadores principais", s_secao))
    kpi_data = [[k, v] for k, v in kpis_dict.items()]
    t_kpi = Table(kpi_data, colWidths=[8*cm, 8*cm])
    t_kpi.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (0, -1), 10),
        ("FONTSIZE", (1, 0), (1, -1), 14),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#64748b")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#047857")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    el.append(t_kpi)

    if insights_list:
        el.append(Paragraph("Insights automáticos", s_secao))
        for ins in insights_list:
            ins_clean = ins.replace("<strong>", "<b>").replace("</strong>", "</b>")
            el.append(Paragraph(f"• {ins_clean}", s_ins))
    el.append(PageBreak())

    # ───── Tabelas ─────
    for nome_tab, df in tabelas_dict.items():
        el.append(Paragraph(nome_tab, s_secao))
        if df is None or df.empty:
            el.append(Paragraph("Sem dados para o período.", s_texto))
            continue

        cols = list(df.columns)[:5]
        df_show = df[cols].head(20)
        data = [cols] + df_show.astype(str).values.tolist()
        larg_col = 17.4*cm / len(cols)
        tbl = Table(data, colWidths=[larg_col] * len(cols))
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#047857")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ]))
        el.append(tbl)
        el.append(Spacer(1, 0.5*cm))

    el.append(Spacer(1, 1*cm))
    el.append(Paragraph(
        "Relatório gerado pelo Pulse • Dados fictícios • © 2026 Natan Souza",
        ParagraphStyle("R", fontSize=8, textColor=colors.HexColor("#94a3b8"), alignment=TA_CENTER)
    ))

    doc.build(el)
    return output.getvalue()


def bloco_export(titulo, periodo, dfs_excel, kpis_dict, tabelas_pdf, insights_list):
    """Renderiza o bloco de export (Excel + PDF) no final do dashboard."""
    st.markdown("""
    <div class="export-section">
        <div class="export-title">📥 Exportar relatório</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        excel_bytes = exportar_excel("relatorio", dfs_excel, titulo, periodo)
        st.download_button(
            label="📊 Baixar Excel",
            data=excel_bytes,
            file_name=f"pulse_{titulo.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    with c2:
        pdf_bytes = exportar_pdf(titulo, periodo, kpis_dict, tabelas_pdf, insights_list)
        st.download_button(
            label="📄 Baixar PDF",
            data=pdf_bytes,
            file_name=f"pulse_{titulo.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  TELA INICIAL                                                         ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def tela_inicial():
    """Landing da aplicação: logo + carrossel + escolha de perfil + planos."""
    st.markdown('<h1 class="pulse-logo">Pulse</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="pulse-slogan">O pulso do seu negócio, no seu bolso.</p>',
        unsafe_allow_html=True
    )

    carrossel_animado()

    st.markdown("""
    <p style="text-align:center; color:#f1f5f9; font-size:0.92rem; font-weight:500; margin-top:4px;">
        Escolha seu segmento para ver a demonstração.<br>
        <span style="font-size:0.78rem; color:#94a3b8; font-weight:400;">
            Dados fictícios, estrutura real.
        </span>
    </p>
    """, unsafe_allow_html=True)

    # ───── Cards de perfil ─────
    perfis = [
        ("🛡️", "Sou Corretora de Seguros",
         "Carteira, comissões, renovações e alertas de vencimento.", "corretora"),
        ("📊", "Sou Escritório Contábil",
         "Gestão de carteira, fechamentos e produtividade.", "contabil"),
        ("💚", "Sou Clínica Estética",
         "Agenda, receita e performance dos profissionais.", "clinica"),
        ("💈", "Sou Barbearia",
         "Agenda, comissão dos barbeiros e produtos.", "barbearia")
    ]

    for icon, titulo, desc, perfil in perfis:
        st.markdown(f"""
        <div class="perfil-card">
            <div style="font-size:2rem;">{icon}</div>
            <div class="perfil-titulo" style="font-size:1.05rem; margin-top:4px;">{titulo}</div>
            <div class="perfil-desc" style="font-size:0.85rem; line-height:1.4;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Ver demo para {titulo.split()[-1]}", key=f"btn_{perfil}"):
            st.session_state.perfil = perfil
            st.rerun()

    # ───── Botão de planos ─────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="perfil-card" style="border: 2px solid rgba(0, 255, 136, 0.3);
                                     background: linear-gradient(135deg, rgba(0,255,136,0.05) 0%, rgba(20,184,166,0.05) 100%);">
        <div style="font-size:2rem;">💎</div>
        <div class="perfil-titulo" style="font-size:1.05rem; margin-top:4px;">Ver planos e investimento</div>
        <div class="perfil-desc" style="font-size:0.85rem; line-height:1.4;">
            Conheça os 3 tamanhos de projeto, o que cada um entrega e o investimento.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💎 Conhecer planos", key="btn_planos"):
        st.session_state.perfil = "planos"
        st.rerun()

    # ───── Rodapé ─────
    st.markdown("""
    <div style="text-align:center; margin-top:32px; padding-top:20px;
                border-top:1px solid rgba(0, 255, 136, 0.15);
                color:#94a3b8; font-size:0.75rem;">
        Desenvolvido por <strong style="color:#00ff88;">Natan Souza</strong><br>
        Consultoria em Dados e Inteligência Comercial
    </div>
    """, unsafe_allow_html=True)


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  TELA DE PLANOS — Tabela 3x3 com Básico / Intermediário / Avançado    ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def tela_planos():
    """Exibe os 3 planos com preços e features."""
    st.markdown("""
    <div class="dash-header">
        <div>
            <div class="dash-title">💎 Planos & Investimento</div>
            <div class="dash-subtitle">Escolha o tamanho ideal pro seu momento</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        💡 <strong>Como funciona:</strong> Você paga o valor da implementação uma única vez
        (projeto novo, feito sob medida) + mensalidade opcional para manutenção,
        suporte e evolução contínua. Sem fidelidade.
    </div>
    """, unsafe_allow_html=True)

    # ═══════ PLANO BÁSICO ═══════
    st.markdown("""
    <div class="plano-card">
        <div class="plano-tier">🥉 ENTRADA</div>
        <div class="plano-nome">Básico</div>
        <div class="plano-preco">R$ 1.500</div>
        <div class="plano-preco-sub">implementação única • 2 semanas de prazo</div>
        <div class="plano-mensalidade">+ R$ 250/mês (manutenção opcional)</div>
        <ul class="plano-features">
            <li>Dashboard web mobile-first</li>
            <li>Leitura de 1 fonte de dados (planilha ou Google Sheets)</li>
            <li>Até 3 indicadores principais (KPIs)</li>
            <li>Filtros básicos (período e busca)</li>
            <li>2 a 3 abas de visualização</li>
            <li>Link privado com senha</li>
            <li>Suporte por email em até 72h</li>
            <li class="indisponivel">Export Excel / PDF</li>
            <li class="indisponivel">Comparador de períodos</li>
            <li class="indisponivel">Alertas automáticos</li>
        </ul>
        <div style="padding: 10px; background: rgba(0,255,136,0.05); border-radius: 8px;
                    font-size: 0.8rem; color: #94a3b8; text-align: center;">
            <strong style="color: #00ff88;">Ideal para:</strong> primeiro projeto, validar conceito,
            sair do Excel puro.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📩 Quero o plano Básico", key="btn_plano_basico"):
        msg = ("Olá Natan! Tenho interesse no plano Básico do Pulse (R$ 1.500 "
               "+ R$ 250/mês). Podemos conversar?")
        link = f"https://wa.me/{WHATSAPP}?text={msg.replace(' ', '%20')}"
        st.markdown(f'<meta http-equiv="refresh" content="0;url={link}">',
                    unsafe_allow_html=True)

    # ═══════ PLANO INTERMEDIÁRIO ═══════
    st.markdown("""
    <div class="plano-card destaque">
        <div class="plano-tier">🥈 MAIS ESCOLHIDO</div>
        <div class="plano-nome">Intermediário</div>
        <div class="plano-preco">R$ 3.500</div>
        <div class="plano-preco-sub">implementação única • 4 semanas de prazo</div>
        <div class="plano-mensalidade">+ R$ 500/mês (manutenção recomendada)</div>
        <ul class="plano-features">
            <li>Tudo do plano Básico</li>
            <li>Leitura de até 3 fontes de dados integradas</li>
            <li>Até 6 indicadores principais (KPIs)</li>
            <li>Filtros combinados inteligentes</li>
            <li>Comparador de períodos (mês a mês e ano a ano)</li>
            <li>4 a 6 abas analíticas</li>
            <li>Export Excel / PDF completo com branding</li>
            <li>3 alertas automáticos configuráveis</li>
            <li>Integração com WhatsApp (link manual)</li>
            <li>Até 3 usuários simultâneos</li>
            <li>Reunião mensal de acompanhamento (1h)</li>
            <li>Suporte WhatsApp em até 48h</li>
        </ul>
        <div style="padding: 10px; background: rgba(0,255,136,0.1); border-radius: 8px;
                    font-size: 0.8rem; color: #f1f5f9; text-align: center;">
            <strong style="color: #00ff88;">Ideal para:</strong> empresas com 50-500 clientes,
            múltiplos processos para monitorar.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎯 Quero o plano Intermediário", key="btn_plano_inter"):
        msg = ("Olá Natan! Tenho interesse no plano Intermediário do Pulse (R$ 3.500 "
               "+ R$ 500/mês). Podemos conversar?")
        link = f"https://wa.me/{WHATSAPP}?text={msg.replace(' ', '%20')}"
        st.markdown(f'<meta http-equiv="refresh" content="0;url={link}">',
                    unsafe_allow_html=True)

    # ═══════ PLANO AVANÇADO ═══════
    st.markdown("""
    <div class="plano-card">
        <div class="plano-tier">🥇 PREMIUM</div>
        <div class="plano-nome">Avançado</div>
        <div class="plano-preco">R$ 6.500</div>
        <div class="plano-preco-sub">implementação única • 6 a 8 semanas de prazo</div>
        <div class="plano-mensalidade">+ R$ 1.200/mês (manutenção premium)</div>
        <ul class="plano-features">
            <li>Tudo do plano Intermediário</li>
            <li>Fontes de dados ilimitadas + banco próprio</li>
            <li>10+ indicadores customizados por área</li>
            <li>Filtros avançados com presets salvos</li>
            <li>7+ abas analíticas com drill-down</li>
            <li>Export PDF executivo com branding próprio</li>
            <li>Alertas ilimitados com envio automático via WhatsApp</li>
            <li>Automação completa de tarefas repetitivas</li>
            <li>Usuários ilimitados com níveis de permissão</li>
            <li>Conformidade LGPD (dados sensíveis protegidos)</li>
            <li>2 reuniões mensais + WhatsApp direto comigo</li>
            <li>1 nova feature por mês inclusa no contrato</li>
            <li>Suporte WhatsApp prioritário em até 24h</li>
        </ul>
        <div style="padding: 10px; background: rgba(0,255,136,0.05); border-radius: 8px;
                    font-size: 0.8rem; color: #94a3b8; text-align: center;">
            <strong style="color: #00ff88;">Ideal para:</strong> operações com 500+ clientes,
            múltiplas filiais ou dados sensíveis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Quero o plano Avançado", key="btn_plano_avanc"):
        msg = ("Olá Natan! Tenho interesse no plano Avançado do Pulse (R$ 6.500 "
               "+ R$ 1.200/mês). Podemos conversar?")
        link = f"https://wa.me/{WHATSAPP}?text={msg.replace(' ', '%20')}"
        st.markdown(f'<meta http-equiv="refresh" content="0;url={link}">',
                    unsafe_allow_html=True)

    # ═══════ Observações ═══════
    st.markdown("""
    <div class="insight-box" style="margin-top: 24px;">
        <strong>📋 Importante:</strong><br>
        <span style="font-size: 0.85rem; color: #cbd5e1;">
        • Diagnóstico inicial de 45min é sempre gratuito<br>
        • Todos os planos incluem entrega documentada<br>
        • Pagamento: 50% início + 50% entrega (ou 3x sem juros no pix)<br>
        • Manutenção mensal pode ser cancelada a qualquer momento<br>
        • Valores podem variar conforme complexidade específica do seu caso
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    cta_whatsapp(
        "Olá Natan! Vi os planos do Pulse e gostaria de entender qual faz "
        "mais sentido pra minha empresa. Podemos conversar?"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    botao_voltar()


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  DASHBOARD: CORRETORA                                                 ║
# ╚═══════════════════════════════════════════════════════════════════════╝
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

    mes, ano, tipo_comp, mes_ant, ano_ant = seletor_periodo_comparacao("cor")
    periodo_label = f"{mes}/{ano}"

    with st.spinner("Carregando dados..."):
        df, df_evo = gerar_dados_corretora(mes, ano)
        if tipo_comp:
            df_ant, df_evo_ant = gerar_dados_corretora(mes_ant, ano_ant)
        else:
            df_ant, df_evo_ant = None, None

    info_dados_ficticios()

    # ───── Métricas ─────
    ativos = df[df["Status"] == "Ativo"]
    comissao_mensal = ativos["Comissao_Mensal"].sum()
    vencendo_30d = len(df[(df["Dias_Para_Renovacao"] >= 0) &
                          (df["Dias_Para_Renovacao"] <= 30)])
    ticket = comissao_mensal / len(ativos) if len(ativos) > 0 else 0

    ativos_ant, comissao_ant, ticket_ant = 0, 0, 0
    if df_ant is not None:
        ativos_ant_df = df_ant[df_ant["Status"] == "Ativo"]
        ativos_ant = len(ativos_ant_df)
        comissao_ant = ativos_ant_df["Comissao_Mensal"].sum()
        ticket_ant = comissao_ant / ativos_ant if ativos_ant > 0 else 0

    insight = gerar_insight_corretora({
        "ativos": len(ativos), "vencendo": vencendo_30d,
        "comissao": comissao_mensal, "comissao_ant": comissao_ant,
    })

    st.markdown(f"""
    <div class="insight-box">
        💡 <strong>Insight de {periodo_label}</strong><br>
        {insight}
    </div>
    """, unsafe_allow_html=True)

    comp_label = gerar_label_comparacao(mes, ano, tipo_comp) if tipo_comp else "sem base"

    c1, c2 = st.columns(2)
    with c1:
        kpi_card("CARTEIRA ATIVA", len(ativos),
                 ativos_ant if tipo_comp else None,
                 formatter=formatar_inteiro_br, label_comp=f"vs {comp_label}")
    with c2:
        kpi_card("COMISSÃO / MÊS", comissao_mensal,
                 comissao_ant if tipo_comp else None,
                 formatter=formatar_brl, label_comp=f"vs {comp_label}")

    c3, c4 = st.columns(2)
    with c3:
        st.metric("VENCENDO EM 30d", vencendo_30d)
    with c4:
        kpi_card("TICKET MÉDIO", ticket,
                 ticket_ant if tipo_comp else None,
                 formatter=formatar_brl, label_comp=f"vs {comp_label}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ───── Tabs ─────
    t1, t2, t3, t4, t5 = st.tabs(["📈 Evolução", "🔔 Alertas", "🎯 Mix", "📋 Carteira", "🏆 Top"])

    with t1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_evo["Mes"], y=df_evo["Comissao_Total"],
            mode="lines+markers", name=ano,
            line=dict(color=VERDE_NEON, width=3),
            fill="tozeroy", fillcolor="rgba(0,255,136,0.15)"
        ))
        if df_evo_ant is not None and tipo_comp == "YoY":
            fig.add_trace(go.Scatter(
                x=df_evo_ant["Mes"], y=df_evo_ant["Comissao_Total"],
                mode="lines", name=ano_ant,
                line=dict(color=AZUL_CLARO, width=2, dash="dash"),
            ))
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Novos", x=df_evo["Mes"],
                              y=df_evo["Novos_Contratos"], marker_color=VERDE_NEON))
        fig2.add_trace(go.Bar(name="Cancelamentos", x=df_evo["Mes"],
                              y=df_evo["Cancelamentos"], marker_color=VERMELHO))
        fig2.update_layout(**layout_chart(240))
        st.plotly_chart(fig2, use_container_width=True)

    with t2:
        urgentes = df[df["Dias_Para_Renovacao"].between(0, 15)].sort_values("Dias_Para_Renovacao")
        if not urgentes.empty:
            for _, row in urgentes.head(8).iterrows():
                cls = "urgente" if row["Dias_Para_Renovacao"] <= 7 else ""
                st.markdown(f"""
                <div class="alerta-item {cls}">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <strong>{row['Cliente']}</strong><br>
                            <span style="font-size:0.78rem;">{row['Ramo']} • {row['Seguradora']}</span>
                        </div>
                        <div style="text-align:right;">
                            <strong style="color:#ef4444;">{int(row['Dias_Para_Renovacao'])}d</strong><br>
                            <span style="font-size:0.78rem;">{formatar_brl(row['Premio_Anual'])}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("✅ Sem renovações urgentes.")

    with t3:
        mix = df[df["Status"] == "Ativo"].groupby("Ramo").size().reset_index(name="total")
        fig = px.pie(mix, values="total", names="Ramo", hole=0.5,
                     color_discrete_sequence=[VERDE_NEON, AZUL_CLARO, ROXO, AMBAR, ROSA])
        fig.update_traces(textposition="inside", textinfo="percent+label",
                          textfont=dict(color="#0b1e2e", family="Inter", size=11))
        fig.update_layout(**layout_chart(330))
        st.plotly_chart(fig, use_container_width=True)

    with t4:
        busca = st.text_input("🔍 Buscar cliente", key="busca_cor")
        df_view = df.copy()
        if busca:
            df_view = df_view[df_view["Cliente"].str.contains(busca, case=False)]
        st.dataframe(
            df_view[["Cliente", "Ramo", "Seguradora", "Status", "Premio_Anual"]].head(20),
            use_container_width=True, hide_index=True
        )

    with t5:
        top = ativos.groupby("Cliente")["Premio_Anual"].sum().sort_values(ascending=False).head(10)
        fig = go.Figure(go.Bar(
            x=top.values, y=top.index, orientation="h",
            marker_color=VERDE_NEON, text=top.values, textposition='outside',
            texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)
        ))
        fig.update_layout(**layout_chart(340, yaxis_opts={
            "autorange": "reversed",
            "tickfont": {"family": "Inter", "color": TEXTO, "size": 10}
        }))
        st.plotly_chart(fig, use_container_width=True)

    # ───── Export ─────
    kpis_pdf = {
        "Carteira ativa": formatar_inteiro_br(len(ativos)),
        "Comissão mensal": formatar_brl(comissao_mensal),
        "Vencendo em 30 dias": str(vencendo_30d),
        "Ticket médio": formatar_brl(ticket),
    }
    tabelas = {
        "Carteira Ativa": ativos[["Cliente", "Ramo", "Seguradora", "Premio_Anual", "Comissao_Mensal"]],
        "Vencendo Proximos 30d": df[(df["Dias_Para_Renovacao"] >= 0) &
                                     (df["Dias_Para_Renovacao"] <= 30)][
            ["Cliente", "Ramo", "Seguradora", "Dias_Para_Renovacao", "Premio_Anual"]
        ],
        "Evolucao Mensal": df_evo,
    }
    bloco_export("Corretora de Seguros", periodo_label, tabelas, kpis_pdf, tabelas, [insight])

    st.markdown("---")
    cta_whatsapp(
        f"Oi Natan! Vi o demo do Pulse para corretoras (período {periodo_label}) "
        "e quero conversar."
    )
    botao_voltar()


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  DASHBOARD: CONTÁBIL                                                  ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def dash_contabil():
    st.markdown("""
    <div class="dash-header">
        <div>
            <div class="dash-title">📊 Pulse • Contábil</div>
            <div class="dash-subtitle">Demo para Escritórios de Contabilidade</div>
        </div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

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

    honorarios_ant, empresas_ant = 0, 0
    if df_ant is not None:
        honorarios_ant = df_ant["Honorario_Mensal"].sum()
        empresas_ant = len(df_ant)

    insight = gerar_insight_contabil({
        "total": len(df), "atrasados": len(atrasados), "pct_prazo": pct_prazo,
    })

    st.markdown(f"""
    <div class="insight-box">
        💡 <strong>Insight de {periodo_label}</strong><br>
        {insight}
    </div>
    """, unsafe_allow_html=True)

    comp_label = gerar_label_comparacao(mes, ano, tipo_comp) if tipo_comp else "sem base"

    c1, c2 = st.columns(2)
    with c1:
        kpi_card("EMPRESAS", len(df),
                 empresas_ant if tipo_comp else None,
                 formatter=formatar_inteiro_br, label_comp=f"vs {comp_label}")
    with c2:
        kpi_card("HONORÁRIOS", honorarios,
                 honorarios_ant if tipo_comp else None,
                 formatter=formatar_brl, label_comp=f"vs {comp_label}")

    c3, c4 = st.columns(2)
    with c3:
        st.metric("ENTREGUES NO PRAZO", f"{pct_prazo:.0f}%")
    with c4:
        st.metric("EM ATRASO", len(atrasados))

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "📈 Produtividade", "⚠️ Atrasados", "📋 Carteira", "🥧 Regimes", "💰 Top", "📅 Obrig."
    ])

    with t1:
        fig = go.Figure(go.Scatter(
            x=df_prod["Mes"], y=df_prod["Horas_Fechamento"],
            mode="lines+markers", line=dict(color=VERDE_NEON, width=3),
            fill="tozeroy", fillcolor="rgba(0,255,136,0.15)"
        ))
        if df_prod_ant is not None and tipo_comp == "YoY":
            fig.add_trace(go.Scatter(
                x=df_prod_ant["Mes"], y=df_prod_ant["Horas_Fechamento"],
                mode="lines", name=ano_ant,
                line=dict(color=AZUL_CLARO, width=2, dash="dash"),
            ))
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        atrasados_df = df[df["Status_Fechamento"] == "Atrasado"]
        if not atrasados_df.empty:
            for _, row in atrasados_df.head(6).iterrows():
                st.markdown(f"""
                <div class="alerta-item urgente">
                    <strong>{row['Empresa']}</strong><br>
                    <span style="font-size:0.78rem;">
                        {row['Regime_Tributario']} • {row['Dias_Para_Entrega']} dias de atraso
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("✅ Nenhum cliente em atraso.")

    with t3:
        busca = st.text_input("🔍 Buscar empresa", key="busca_cont")
        df_view = df.copy()
        if busca:
            df_view = df_view[df_view["Empresa"].str.contains(busca, case=False)]
        st.dataframe(
            df_view[["Empresa", "Regime_Tributario", "Status_Fechamento", "Honorario_Mensal"]],
            use_container_width=True, hide_index=True
        )

    with t4:
        regime_counts = df["Regime_Tributario"].value_counts().reset_index()
        regime_counts.columns = ["Regime", "Quantidade"]
        fig = px.pie(regime_counts, values="Quantidade", names="Regime", hole=0.5,
                     color_discrete_sequence=[VERDE_NEON, AZUL_CLARO, ROXO, AMBAR])
        fig.update_traces(textposition="inside", textinfo="percent+label",
                          textfont=dict(color="#0b1e2e", family="Inter", size=11))
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)

    with t5:
        top_hon = df.groupby("Empresa")["Honorario_Mensal"].sum().sort_values(ascending=False).head(10)
        fig = go.Figure(go.Bar(
            x=top_hon.values, y=top_hon.index, orientation="h",
            marker_color=VERDE_NEON, text=top_hon.values, textposition='outside',
            texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)
        ))
        fig.update_layout(**layout_chart(340, yaxis_opts={
            "autorange": "reversed",
            "tickfont": {"family": "Inter", "color": TEXTO, "size": 10}
        }))
        st.plotly_chart(fig, use_container_width=True)

    with t6:
        st.markdown("**📌 Próximas obrigações fiscais**")
        obrigacoes = pd.DataFrame({
            "Obrigação": ["DASN-SIMEI", "EFD-Contribuições", "DCTF", "DIRF", "ECD"],
            "Vencimento": ["31/05", "10/06", "15/06", "20/06", "30/06"],
            "Status": ["Pendente"] * 5
        })
        st.dataframe(obrigacoes, use_container_width=True, hide_index=True)

    kpis_pdf = {
        "Empresas na carteira": formatar_inteiro_br(len(df)),
        "Honorários mensais": formatar_brl(honorarios),
        "Entregues no prazo": f"{pct_prazo:.0f}%",
        "Clientes em atraso": str(len(atrasados)),
    }
    tabelas = {
        "Carteira Completa": df[["Empresa", "Regime_Tributario", "Status_Fechamento", "Honorario_Mensal"]],
        "Clientes em Atraso": df[df["Status_Fechamento"] == "Atrasado"][
            ["Empresa", "Regime_Tributario", "Dias_Para_Entrega"]
        ],
        "Produtividade Mensal": df_prod,
    }
    bloco_export("Contabilidade", periodo_label, tabelas, kpis_pdf, tabelas, [insight])

    st.markdown("---")
    cta_whatsapp(f"Oi Natan! Vi o demo do Pulse para contabilidade ({periodo_label}).")
    botao_voltar()


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  DASHBOARD: CLÍNICA                                                   ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def dash_clinica():
    st.markdown("""
    <div class="dash-header">
        <div>
            <div class="dash-title">💚 Pulse • Clínica</div>
            <div class="dash-subtitle">Demo para Clínicas Estéticas</div>
        </div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

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
    receita_mes = realizados["Valor"].sum()
    ticket = realizados["Valor"].mean() if not realizados.empty else 0
    agendados = len(df[df["Status"] == "Agendado"])

    receita_ant, ticket_ant = 0, 0
    if df_ant is not None:
        real_ant = df_ant[df_ant["Status"] == "Realizado"]
        receita_ant = real_ant["Valor"].sum()
        ticket_ant = real_ant["Valor"].mean() if not real_ant.empty else 0

    insight = gerar_insight_clinica({
        "receita": receita_mes, "receita_ant": receita_ant,
        "ticket": ticket, "agendados": agendados,
    })

    st.markdown(f"""
    <div class="insight-box">
        💡 <strong>Insight de {periodo_label}</strong><br>
        {insight}
    </div>
    """, unsafe_allow_html=True)

    comp_label = gerar_label_comparacao(mes, ano, tipo_comp) if tipo_comp else "sem base"

    c1, c2 = st.columns(2)
    with c1:
        kpi_card("RECEITA / MÊS", receita_mes,
                 receita_ant if tipo_comp else None,
                 formatter=formatar_brl, label_comp=f"vs {comp_label}")
    with c2:
        st.metric("ATENDIMENTOS", len(realizados))

    c3, c4 = st.columns(2)
    with c3:
        kpi_card("TICKET MÉDIO", ticket,
                 ticket_ant if tipo_comp else None,
                 formatter=formatar_brl, label_comp=f"vs {comp_label}")
    with c4:
        st.metric("AGENDADOS", agendados)

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "📈 Receita", "⭐ Top", "📅 Agenda", "👩‍⚕️ Prof.", "🔄 Fidelização", "💳 Pagto"
    ])

    with t1:
        fig = go.Figure(go.Bar(x=df_evo["Mes"], y=df_evo["Receita"],
                                marker_color=VERDE_NEON, name=ano))
        if df_evo_ant is not None and tipo_comp == "YoY":
            fig.add_trace(go.Scatter(
                x=df_evo_ant["Mes"], y=df_evo_ant["Receita"],
                mode="lines+markers", name=ano_ant,
                line=dict(color=AZUL_CLARO, width=2, dash="dash"),
            ))
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        top = realizados.groupby("Procedimento")["Valor"].sum().sort_values(ascending=True).tail(6)
        fig = go.Figure(go.Bar(
            y=top.index, x=top.values, orientation="h",
            marker_color=VERDE_NEON, text=top.values, textposition='outside',
            texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)
        ))
        fig.update_layout(**layout_chart(320, yaxis_opts={
            "tickfont": {"family": "Inter", "color": TEXTO, "size": 10}
        }))
        st.plotly_chart(fig, use_container_width=True)

    with t3:
        hoje = datetime.now()
        agenda = df[(df["Status"] == "Agendado") & (df["Data"] >= hoje)].sort_values("Data").head(10)
        if not agenda.empty:
            for _, row in agenda.iterrows():
                st.markdown(f"""
                <div class="alerta-item ok">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <strong>{row['Paciente']}</strong><br>
                            <span style="font-size:0.78rem;">
                                {row['Procedimento']} • {row['Profissional']}
                            </span>
                        </div>
                        <div><strong>{row['Data'].strftime('%d/%m %H:%M')}</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum agendamento futuro no momento.")

    with t4:
        perf = realizados.groupby("Profissional")["Valor"].sum().reset_index()
        fig = go.Figure(go.Bar(
            x=perf["Profissional"], y=perf["Valor"],
            marker_color=VERDE_NEON, text=perf["Valor"],
            texttemplate='R$ %{text:.2s}', textposition='outside',
            textfont=dict(color=TEXTO)
        ))
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
        fig = px.pie(pgto, values="Qtd", names="Forma", hole=0.5,
                     color_discrete_sequence=[VERDE_NEON, AZUL_CLARO, ROXO])
        fig.update_traces(textposition="inside", textinfo="percent+label",
                          textfont=dict(color="#0b1e2e", family="Inter", size=11))
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)

    kpis_pdf = {
        "Receita do período": formatar_brl(receita_mes),
        "Atendimentos realizados": str(len(realizados)),
        "Ticket médio": formatar_brl(ticket),
        "Agendamentos futuros": str(agendados),
    }
    df_export = realizados.copy()
    df_export["Data"] = df_export["Data"].dt.strftime("%d/%m/%Y %H:%M")
    tabelas = {
        "Atendimentos Realizados": df_export[
            ["Data", "Paciente", "Procedimento", "Profissional", "Valor"]
        ].head(100),
        "Evolucao Mensal": df_evo,
    }
    bloco_export("Clinica Estetica", periodo_label, tabelas, kpis_pdf, tabelas, [insight])

    st.markdown("---")
    cta_whatsapp(f"Oi Natan! Vi o demo do Pulse para clínicas ({periodo_label}).")
    botao_voltar()


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  DASHBOARD: BARBEARIA                                                 ║
# ╚═══════════════════════════════════════════════════════════════════════╝
def dash_barbearia():
    st.markdown("""
    <div class="dash-header">
        <div>
            <div class="dash-title">💈 Pulse • Barbearia</div>
            <div class="dash-subtitle">Demo para Barbearias</div>
        </div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

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

    receita_total_ant, ticket_ant = 0, 0
    if df_ant is not None:
        real_ant = df_ant[df_ant["Status"] == "Realizado"]
        mes_atual_ant = real_ant[real_ant["Data"] >= hoje - timedelta(days=30)]
        receita_serv_ant = mes_atual_ant["Valor"].sum()
        receita_prod_ant = df_prod_ant[
            df_prod_ant["Data"] >= hoje - timedelta(days=30)
        ]["Receita_Total"].sum()
        receita_total_ant = receita_serv_ant + receita_prod_ant
        ticket_ant = mes_atual_ant["Valor"].mean() if not mes_atual_ant.empty else 0

    insight = gerar_insight_barbearia({
        "receita": receita_total, "receita_ant": receita_total_ant,
        "ticket": ticket, "atendimentos": len(mes_atual),
    })

    st.markdown(f"""
    <div class="insight-box">
        💡 <strong>Insight de {periodo_label}</strong><br>
        {insight}
    </div>
    """, unsafe_allow_html=True)

    comp_label = gerar_label_comparacao(mes, ano, tipo_comp) if tipo_comp else "sem base"

    c1, c2 = st.columns(2)
    with c1:
        kpi_card("RECEITA TOTAL", receita_total,
                 receita_total_ant if tipo_comp else None,
                 formatter=formatar_brl, label_comp=f"vs {comp_label}")
    with c2:
        st.metric("ATENDIMENTOS", len(mes_atual))

    c3, c4 = st.columns(2)
    with c3:
        kpi_card("TICKET MÉDIO", ticket,
                 ticket_ant if tipo_comp else None,
                 formatter=formatar_brl, label_comp=f"vs {comp_label}")
    with c4:
        st.metric("AGENDADOS", agendados)

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "💰 Comissões", "🛍️ Produtos", "📅 Agenda", "👥 Clientes", "📊 Ocupação", "🏆 Serviços"
    ])

    with t1:
        comissao = mes_atual.groupby("Barbeiro")["Comissao_Barbeiro"].sum().reset_index()
        fig = go.Figure(go.Bar(
            x=comissao["Comissao_Barbeiro"], y=comissao["Barbeiro"],
            orientation="h", marker_color=VERDE_NEON,
            text=comissao["Comissao_Barbeiro"], textposition='outside',
            texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)
        ))
        fig.update_layout(**layout_chart(260, yaxis_opts={
            "tickfont": {"family": "Inter", "color": TEXTO, "size": 10}
        }))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        top_prod = df_prod.groupby("Produto")["Receita_Total"].sum().sort_values(ascending=True).tail(5)
        fig = go.Figure(go.Bar(
            y=top_prod.index, x=top_prod.values, orientation="h",
            marker_color=VERDE_NEON, text=top_prod.values, textposition='outside',
            texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)
        ))
        fig.update_layout(**layout_chart(260, yaxis_opts={
            "tickfont": {"family": "Inter", "color": TEXTO, "size": 10}
        }))
        st.plotly_chart(fig, use_container_width=True)

    with t3:
        agenda = df[(df["Status"] == "Agendado") & (df["Data"] >= hoje)].sort_values("Data").head(10)
        if not agenda.empty:
            for _, row in agenda.iterrows():
                st.markdown(f"""
                <div class="alerta-item ok">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <strong>{row['Cliente']}</strong><br>
                            <span style="font-size:0.78rem;">{row['Servico']} • {row['Barbeiro']}</span>
                        </div>
                        <div><strong>{row['Data'].strftime('%d/%m %H:%M')}</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum agendamento futuro no momento.")

    with t4:
        freq = realizados["Cliente"].value_counts().reset_index().head(10)
        freq.columns = ["Cliente", "Visitas"]
        fig = px.bar(freq, x="Visitas", y="Cliente", orientation="h",
                     color_discrete_sequence=[VERDE_NEON])
        fig.update_layout(**layout_chart(320, yaxis_opts={
            "autorange": "reversed",
            "tickfont": {"family": "Inter", "color": TEXTO, "size": 10}
        }))
        st.plotly_chart(fig, use_container_width=True)

    with t5:
        horas = ["09h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h"]
        np.random.seed(int(ano) + MESES.index(mes))
        ocupacao = np.random.randint(40, 100, size=len(horas))
        fig = go.Figure(go.Scatter(
            x=horas, y=ocupacao, mode="lines+markers",
            fill="tozeroy", line=dict(color=VERDE_NEON, width=3),
            fillcolor="rgba(0,255,136,0.2)"
        ))
        fig.update_layout(**layout_chart(260, yaxis_opts={"title": "Ocupação (%)"}))
        st.plotly_chart(fig, use_container_width=True)

    with t6:
        serv = realizados.groupby("Servico")["Valor"].sum().sort_values(ascending=True).tail(6)
        fig = go.Figure(go.Bar(
            y=serv.index, x=serv.values, orientation="h",
            marker_color=VERDE_NEON, text=serv.values, textposition='outside',
            texttemplate='R$ %{text:.2s}', textfont=dict(color=TEXTO)
        ))
        fig.update_layout(**layout_chart(320, yaxis_opts={
            "tickfont": {"family": "Inter", "color": TEXTO, "size": 10}
        }))
        st.plotly_chart(fig, use_container_width=True)

    kpis_pdf = {
        "Receita total": formatar_brl(receita_total),
        "Atendimentos": str(len(mes_atual)),
        "Ticket médio": formatar_brl(ticket),
        "Agendados": str(agendados),
    }
    df_export = realizados.copy()
    df_export["Data"] = df_export["Data"].dt.strftime("%d/%m/%Y %H:%M")
    tabelas = {
        "Atendimentos": df_export[
            ["Data", "Cliente", "Servico", "Barbeiro", "Valor", "Comissao_Barbeiro"]
        ].head(100),
        "Produtos Vendidos": df_prod[
            ["Data", "Produto", "Quantidade", "Receita_Total", "Lucro_Bruto"]
        ].head(100),
        "Evolucao Mensal": df_evo,
    }
    bloco_export("Barbearia", periodo_label, tabelas, kpis_pdf, tabelas, [insight])

    st.markdown("---")
    cta_whatsapp(f"Oi Natan! Vi o demo do Pulse para barbearias ({periodo_label}).")
    botao_voltar()


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  ROUTER PRINCIPAL                                                     ║
# ╚═══════════════════════════════════════════════════════════════════════╝
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
elif st.session_state.perfil == "planos":
    tela_planos()
