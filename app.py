"""
Pulse — Demo Dashboard v6 (Cards 100% alinhados)
Todos os cards com altura fixa de 130px, mesmo em diferentes nichos.
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

pio.templates["pulse_dark"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, sans-serif", color=TEXTO, size=11),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,46,66,0.3)",
        colorway=[VERDE_NEON, AZUL_CLARO],
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
    /* Restante do CSS (carrossel, tabs, botões) mantido igual ao original */
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FUNÇÃO ÚNICA PARA CARD PADRÃO (altura fixa 130px)
# ═══════════════════════════════════════════════════════════════
def kpi_card(label, valor_atual, valor_anterior=None, formatter=None, icone="", tooltip=""):
    if formatter is None:
        formatter = lambda x: f"{int(x):,}".replace(",", ".") if isinstance(x, (int, float)) else str(x)
    # Formata valor atual
    valor_str = formatter(valor_atual)
    # Se não houver anterior, mostra só o valor
    if valor_anterior is None:
        badge = ""
        comp_str = ""
    else:
        delta, classe, seta = calcular_delta(valor_atual, valor_anterior)
        if delta is None:
            badge = '<span class="delta-badge delta-neutro">—</span>'
        else:
            badge = f'<span class="delta-badge {classe}">{seta} {formatar_pct(delta)}</span>'
        comp_str = f'<span style="color:#cbd5e1;">{formatter(valor_anterior)}</span> {badge}'
    tooltip_html = f'<span class="tooltip-icon" title="{tooltip}">?</span>' if tooltip else ""
    st.markdown(f"""
    <div class="card-padrao">
        <div class="card-label">{icone} {label} {tooltip_html}</div>
        <div class="card-valor">{valor_str}</div>
        <div class="card-footer">{f"vs anterior: {comp_str}" if comp_str else ""}</div>
    </div>
    """, unsafe_allow_html=True)

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

# ═══════════════════════════════════════════════════════════════
# DEMAIS FUNÇÕES (geração de dados, export, etc.) IGUAIS AO CÓDIGO ANTERIOR
# ═══════════════════════════════════════════════════════════════
# [Aqui você deve manter todas as funções auxiliares que já existiam:
#  gerar_dados_corretora, gerar_dados_contabil, gerar_dados_clinica, gerar_dados_barbearia,
#  seletor_periodo_comparacao, exportar_excel, exportar_pdf, bloco_export,
#  carrossel_animado, tela_inicial, etc. Vou omitir por brevidade,
#  mas elas são idênticas ao código anterior. O foco agora são os cards.]

# ═══════════════════════════════════════════════════════════════
# DASHBOARD CORRETORA (cards alinhados)
# ═══════════════════════════════════════════════════════════════
def dash_corretora():
    st.markdown('<div class="dash-header"><div><div class="dash-title">🛡️ Pulse • Corretora</div><div class="dash-subtitle">Demo para Corretoras de Seguros</div></div><span class="demo-badge">DEMO</span></div>', unsafe_allow_html=True)
    mes, ano, tipo_comp, mes_ant, ano_ant = seletor_periodo_comparacao("cor")
    periodo_label = f"{mes}/{ano}"
    with st.spinner("Carregando..."):
        df, df_evo = gerar_dados_corretora(mes, ano)
        if tipo_comp:
            df_ant, _ = gerar_dados_corretora(mes_ant, ano_ant)
        else:
            df_ant = None
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
    c1, c2 = st.columns(2)
    with c1:
        kpi_card("CARTEIRA ATIVA", len(ativos), ativos_ant, formatter=formatar_inteiro_br, icone="🛡️", tooltip="Clientes ativos")
    with c2:
        kpi_card("COMISSÃO / MÊS", comissao, comissao_ant, formatter=formatar_brl, icone="💰", tooltip="Comissão total")
    c3, c4 = st.columns(2)
    with c3:
        kpi_card("VENCENDO EM 30d", vencendo, None, formatter=formatar_inteiro_br, icone="⏰", tooltip="Apólices a vencer")
    with c4:
        kpi_card("TICKET MÉDIO", ticket, ticket_ant, formatter=formatar_brl, icone="🎫", tooltip="Comissão média por cliente")
    # ... resto do dashboard (tabs, etc.) igual ao original

# ═══════════════════════════════════════════════════════════════
# DASHBOARD CONTÁBIL (cards alinhados)
def dash_contabil():
    st.markdown('<div class="dash-header"><div><div class="dash-title">📊 Pulse • Contábil</div><div class="dash-subtitle">Demo para Escritórios</div></div><span class="demo-badge">DEMO</span></div>', unsafe_allow_html=True)
    mes, ano, tipo_comp, mes_ant, ano_ant = seletor_periodo_comparacao("cont")
    with st.spinner("Carregando..."):
        df, df_prod = gerar_dados_contabil(mes, ano)
        if tipo_comp:
            df_ant, _ = gerar_dados_contabil(mes_ant, ano_ant)
        else:
            df_ant = None
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
    c1, c2 = st.columns(2)
    with c1:
        kpi_card("EMPRESAS", len(df), empresas_ant, formatter=formatar_inteiro_br, icone="🏢", tooltip="Total na carteira")
    with c2:
        kpi_card("HONORÁRIOS", honorarios, honorarios_ant, formatter=formatar_brl, icone="📄", tooltip="Receita mensal")
    c3, c4 = st.columns(2)
    with c3:
        kpi_card("ENTREGUES NO PRAZO", f"{pct_prazo:.0f}%", None, formatter=lambda x: x, icone="✅", tooltip="% entregas no prazo")
    with c4:
        kpi_card("EM ATRASO", len(atrasados), None, formatter=formatar_inteiro_br, icone="⚠️", tooltip="Empresas atrasadas")
    # ... resto igual

# ═══════════════════════════════════════════════════════════════
# DASHBOARD CLÍNICA (cards alinhados)
def dash_clinica():
    st.markdown('<div class="dash-header"><div><div class="dash-title">💚 Pulse • Clínica</div><div class="dash-subtitle">Demo para Clínicas Estéticas</div></div><span class="demo-badge">DEMO</span></div>', unsafe_allow_html=True)
    mes, ano, tipo_comp, mes_ant, ano_ant = seletor_periodo_comparacao("cli")
    with st.spinner("Carregando..."):
        df, df_evo = gerar_dados_clinica(mes, ano)
        if tipo_comp:
            df_ant, _ = gerar_dados_clinica(mes_ant, ano_ant)
        else:
            df_ant = None
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
    c1, c2 = st.columns(2)
    with c1:
        kpi_card("RECEITA / MÊS", receita, receita_ant, formatter=formatar_brl, icone="💰", tooltip="Receita total")
    with c2:
        kpi_card("ATENDIMENTOS", len(realizados), None, formatter=formatar_inteiro_br, icone="👥", tooltip="Atendimentos realizados")
    c3, c4 = st.columns(2)
    with c3:
        kpi_card("TICKET MÉDIO", ticket, ticket_ant, formatter=formatar_brl, icone="🎫", tooltip="Valor médio por atendimento")
    with c4:
        kpi_card("AGENDADOS", agendados, None, formatter=formatar_inteiro_br, icone="📅", tooltip="Futuros agendamentos")
    # ... resto igual

# ═══════════════════════════════════════════════════════════════
# DASHBOARD BARBEARIA (cards alinhados)
def dash_barbearia():
    st.markdown('<div class="dash-header"><div><div class="dash-title">💈 Pulse • Barbearia</div><div class="dash-subtitle">Demo para Barbearias</div></div><span class="demo-badge">DEMO</span></div>', unsafe_allow_html=True)
    mes, ano, tipo_comp, mes_ant, ano_ant = seletor_periodo_comparacao("bar")
    with st.spinner("Carregando..."):
        df, df_prod, df_evo = gerar_dados_barbearia(mes, ano)
        if tipo_comp:
            df_ant, df_prod_ant, _ = gerar_dados_barbearia(mes_ant, ano_ant)
        else:
            df_ant = df_prod_ant = None
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
    c1, c2 = st.columns(2)
    with c1:
        kpi_card("RECEITA TOTAL", receita_total, receita_ant, formatter=formatar_brl, icone="💰", tooltip="Serviços + produtos")
    with c2:
        kpi_card("ATENDIMENTOS", len(mes_atual), None, formatter=formatar_inteiro_br, icone="✂️", tooltip="Atendimentos últimos 30d")
    c3, c4 = st.columns(2)
    with c3:
        kpi_card("TICKET MÉDIO", ticket, ticket_ant, formatter=formatar_brl, icone="🎫", tooltip="Valor médio por serviço")
    with c4:
        kpi_card("AGENDADOS", agendados, None, formatter=formatar_inteiro_br, icone="📅", tooltip="Agendamentos futuros")
    # ... resto igual

# ═══════════════════════════════════════════════════════════════
# ROUTER (mantido)
if st.session_state.get("perfil") is None:
    tela_inicial()
elif st.session_state.perfil == "corretora":
    dash_corretora()
elif st.session_state.perfil == "contabil":
    dash_contabil()
elif st.session_state.perfil == "clinica":
    dash_clinica()
elif st.session_state.perfil == "barbearia":
    dash_barbearia()
