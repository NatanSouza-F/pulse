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
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Pulse • Demo",
    page_icon="💚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# WhatsApp do Natan (substituir depois)
WHATSAPP = "5561999999999"

# Paleta
VERDE = "#00ff88"
VERDE_ESCURO = "#059669"
AZUL = "#3b82f6"
VERMELHO = "#ef4444"
AMBAR = "#f59e0b"
ROXO = "#8b5cf6"
CINZA_TEXTO = "#64748b"
FUNDO = "#f8fafc"


# ═══════════════════════════════════════════════════════════════
# CSS GLOBAL — VISUAL APP MOBILE
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
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: #059669 !important;
        font-size: 1.55rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
    }

    /* ───── Botões ───── */
    .stButton button {
        background: #00ff88;
        color: #0b1e2e;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.2rem;
        font-weight: 600;
        font-size: 0.95rem;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background: #00cc6a;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,255,136,0.3);
    }

    /* Botão secundário */
    .stButton button[kind="secondary"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        color: #0f172a;
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
        background: #00ff88 !important;
        color: #0b1e2e !important;
        border-color: #00ff88 !important;
    }

    /* ───── DataFrame limpo ───── */
    div[data-testid="stDataFrame"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
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
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 14px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .perfil-card:hover {
        border-color: #00ff88;
        box-shadow: 0 8px 20px rgba(0,255,136,0.12);
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
        background: linear-gradient(135deg, #059669 0%, #00ff88 100%);
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

    /* Badge demo */
    .demo-badge {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid #00ff88;
        color: #059669;
        padding: 4px 10px;
        border-radius: 40px;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }

    /* CTA fixo embaixo (mobile) */
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

    /* Info card destacado */
    .info-box {
        background: #ecfdf5;
        border-left: 3px solid #059669;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 12px 0;
        font-size: 0.85rem;
        color: #064e3b;
    }

    /* Cards de alertas */
    .alerta-item {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }
    .alerta-item.urgente {
        border-left-color: #ef4444;
    }
    .alerta-item.ok {
        border-left-color: #10b981;
    }

    /* Header interno do dashboard */
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
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# ESTADO DA SESSÃO
# ═══════════════════════════════════════════════════════════════
if "perfil" not in st.session_state:
    st.session_state.perfil = None


# ═══════════════════════════════════════════════════════════════
# LAYOUT DE GRÁFICOS
# ═══════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════
# HELPERS
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


# ═══════════════════════════════════════════════════════════════
# TELA INICIAL — ESCOLHA DE PERFIL
# ═══════════════════════════════════════════════════════════════
def tela_inicial():
    st.markdown('<h1 class="pulse-logo">Pulse</h1>', unsafe_allow_html=True)
    st.markdown('<p class="pulse-slogan">O pulso do seu negócio, no seu bolso.</p>',
                unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align: center; color: #475569; font-size: 0.92rem; margin-bottom: 20px;">
        Escolha seu segmento para ver uma demonstração.<br>
        <span style="font-size: 0.78rem; color: #94a3b8;">Dados fictícios, estrutura real.</span>
    </p>
    """, unsafe_allow_html=True)

    # Card 1 - Corretora
    st.markdown("""
    <div class="perfil-card">
        <div class="perfil-icon">🛡️</div>
        <div class="perfil-titulo">Sou Corretora de Seguros</div>
        <div class="perfil-desc">
            Carteira, comissões, renovações e alertas de vencimento.
            Ideal para corretoras com 100+ clientes.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ver demo para Corretora", key="btn_corretora"):
        st.session_state.perfil = "corretora"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # Card 2 - Contábil
    st.markdown("""
    <div class="perfil-card">
        <div class="perfil-icon">📊</div>
        <div class="perfil-titulo">Sou Escritório Contábil</div>
        <div class="perfil-desc">
            Gestão de carteira, fechamentos mensais, produtividade
            e indicadores financeiros dos clientes.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ver demo para Contabilidade", key="btn_contabil"):
        st.session_state.perfil = "contabil"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # Card 3 - Clínica
    st.markdown("""
    <div class="perfil-card">
        <div class="perfil-icon">💚</div>
        <div class="perfil-titulo">Sou Clínica Estética</div>
        <div class="perfil-desc">
            Agenda, procedimentos, receita, pacientes recorrentes
            e performance dos profissionais.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ver demo para Clínica", key="btn_clinica"):
        st.session_state.perfil = "clinica"
        st.rerun()

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # Card 4 - Barbearia
    st.markdown("""
    <div class="perfil-card">
        <div class="perfil-icon">💈</div>
        <div class="perfil-titulo">Sou Barbearia</div>
        <div class="perfil-desc">
            Agenda, comissão dos barbeiros, venda de produtos
            e clientes recorrentes. Chega de anotar no caderno.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ver demo para Barbearia", key="btn_barbearia"):
        st.session_state.perfil = "barbearia"
        st.rerun()

    # Rodapé
    st.markdown("""
    <div style="text-align: center; margin-top: 32px; padding-top: 20px;
                border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 0.75rem;">
        Desenvolvido por <strong style="color: #059669;">Natan Souza</strong><br>
        Consultoria em Dados e Inteligência Comercial
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: CORRETORA DE SEGUROS
# ═══════════════════════════════════════════════════════════════
def dash_corretora():
    df = pd.read_csv("dados/corretora_carteira.csv")
    df_evo = pd.read_csv("dados/corretora_evolucao.csv")

    # Header
    st.markdown("""
    <div class="dash-header">
        <div>
            <div class="dash-title">🛡️ Pulse • Corretora</div>
            <div class="dash-subtitle">Demo para Corretoras de Seguros</div>
        </div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    info_dados_ficticios()

    # ═══════ KPIs ═══════
    ativos = df[df["Status"] == "Ativo"]
    vencendo = df[df["Status"] == "Vencendo"]
    comissao_mensal = ativos["Comissao_Mensal"].sum()
    renovacoes_30d = df[(df["Dias_Para_Renovacao"] >= 0) & (df["Dias_Para_Renovacao"] <= 30)]

    c1, c2 = st.columns(2)
    with c1:
        st.metric("CARTEIRA ATIVA", formatar_inteiro_br(len(ativos)),
                  f"+{len(df[df['Status'] != 'Cancelado']) - len(ativos)}")
    with c2:
        st.metric("COMISSÃO / MÊS", formatar_brl(comissao_mensal))

    c3, c4 = st.columns(2)
    with c3:
        st.metric("VENCENDO EM 30d", len(renovacoes_30d))
    with c4:
        ticket = comissao_mensal / len(ativos) if len(ativos) > 0 else 0
        st.metric("TICKET MÉDIO", formatar_brl(ticket))

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════ Tabs ═══════
    t1, t2, t3, t4 = st.tabs(["📈 Evolução", "🔔 Alertas", "🎯 Mix", "📋 Carteira"])

    with t1:
        st.markdown("#### Comissão mensal (12 meses)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_evo["Mes"],
            y=df_evo["Comissao_Total"],
            mode="lines+markers",
            line=dict(color=VERDE, width=3),
            fill="tozeroy",
            fillcolor="rgba(0,255,136,0.15)",
            marker=dict(size=7, color=VERDE_ESCURO),
        ))
        fig.update_layout(**layout_chart(280))
        fig.update_yaxes(title="R$")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Movimento de contratos")
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Novos", x=df_evo["Mes"], y=df_evo["Novos_Contratos"],
                             marker_color=VERDE))
        fig.add_trace(go.Bar(name="Cancelamentos", x=df_evo["Mes"],
                             y=df_evo["Cancelamentos"], marker_color=VERMELHO))
        fig.update_layout(**layout_chart(240), barmode="group",
                          legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        st.markdown("#### 🔔 Precisa da sua atenção")

        urgentes = df[df["Dias_Para_Renovacao"].between(0, 15)].sort_values("Dias_Para_Renovacao")
        if not urgentes.empty:
            st.markdown("**Vencendo nos próximos 15 dias:**")
            for _, row in urgentes.head(8).iterrows():
                urgencia = "urgente" if row["Dias_Para_Renovacao"] <= 7 else ""
                st.markdown(f"""
                <div class="alerta-item {urgencia}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{row['Cliente']}</strong><br>
                            <span style="font-size: 0.78rem; color: #64748b;">
                                {row['Ramo']} • {row['Seguradora']}
                            </span>
                        </div>
                        <div style="text-align: right;">
                            <strong style="color: #ef4444;">{int(row['Dias_Para_Renovacao'])} dias</strong><br>
                            <span style="font-size: 0.78rem; color: #64748b;">
                                {formatar_brl(row['Premio_Anual'])}
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Sem renovações urgentes agora.")

    with t3:
        st.markdown("#### Mix de ramos")
        mix_ramo = df[df["Status"] == "Ativo"].groupby("Ramo").size().reset_index(name="total")
        fig = px.pie(mix_ramo, values="total", names="Ramo",
                     color_discrete_sequence=[VERDE, AZUL, ROXO, AMBAR, VERMELHO, "#ec4899"],
                     hole=0.5)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(**layout_chart(330), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Top 5 Seguradoras (por comissão)")
        top_seg = (df[df["Status"] == "Ativo"]
                   .groupby("Seguradora")["Comissao_Anual"]
                   .sum()
                   .sort_values(ascending=True)
                   .tail(5))
        fig = go.Figure(go.Bar(
            x=top_seg.values,
            y=top_seg.index,
            orientation="h",
            marker_color=VERDE,
            text=[formatar_brl(v) for v in top_seg.values],
            textposition="outside",
        ))
        fig.update_layout(**layout_chart(260))
        st.plotly_chart(fig, use_container_width=True)

    with t4:
        st.markdown("#### Carteira completa")
        busca = st.text_input("🔍 Buscar cliente", placeholder="Digite o nome...", key="busca_cor")

        df_view = df.copy()
        if busca:
            df_view = df_view[df_view["Cliente"].str.contains(busca, case=False, na=False)]

        df_view["Prêmio"] = df_view["Premio_Anual"].apply(formatar_brl)
        df_view["Comissão"] = df_view["Comissao_Mensal"].apply(formatar_brl)

        st.dataframe(
            df_view[["Cliente", "Ramo", "Seguradora", "Status", "Prêmio", "Comissão"]].head(50),
            use_container_width=True, hide_index=True, height=400,
        )

    st.markdown("---")
    cta_whatsapp(
        "Oi Natan! Vi o demo do Pulse para corretoras e quero conversar sobre "
        "implementar isso na minha corretora."
    )
    st.markdown("<br>", unsafe_allow_html=True)
    botao_voltar()


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: ESCRITÓRIO CONTÁBIL
# ═══════════════════════════════════════════════════════════════
def dash_contabil():
    df = pd.read_csv("dados/contabil_clientes.csv")
    df_prod = pd.read_csv("dados/contabil_produtividade.csv")

    st.markdown("""
    <div class="dash-header">
        <div>
            <div class="dash-title">📊 Pulse • Contábil</div>
            <div class="dash-subtitle">Demo para Escritórios de Contabilidade</div>
        </div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    info_dados_ficticios()

    # KPIs
    honorarios = df["Honorario_Mensal"].sum()
    entregues = df[df["Status_Fechamento"] == "Entregue"]
    atrasados = df[df["Status_Fechamento"] == "Atrasado"]

    c1, c2 = st.columns(2)
    with c1:
        st.metric("EMPRESAS NA CARTEIRA", len(df))
    with c2:
        st.metric("HONORÁRIOS / MÊS", formatar_brl(honorarios))

    c3, c4 = st.columns(2)
    with c3:
        taxa_prazo = (len(entregues) / len(df)) * 100 if len(df) > 0 else 0
        st.metric("ENTREGUES NO PRAZO", f"{taxa_prazo:.0f}%")
    with c4:
        st.metric("EM ATRASO", len(atrasados),
                  delta="-2 vs mês anterior", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["📈 Produtividade", "⚠️ Atrasados", "📁 Regime", "📋 Carteira"])

    with t1:
        st.markdown("#### Horas dedicadas a fechamento (12 meses)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_prod["Mes"],
            y=df_prod["Horas_Fechamento"],
            mode="lines+markers",
            line=dict(color=VERDE_ESCURO, width=3),
            fill="tozeroy",
            fillcolor="rgba(5,150,105,0.12)",
            marker=dict(size=7),
        ))
        fig.update_layout(**layout_chart(280))
        fig.update_yaxes(title="Horas")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Receita de honorários")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_prod["Mes"],
            y=df_prod["Receita_Honorarios"],
            marker_color=VERDE,
            text=[formatar_brl(v)[:-3] for v in df_prod["Receita_Honorarios"]],
            textposition="outside",
        ))
        fig.update_layout(**layout_chart(280))
        fig.update_yaxes(title="R$")
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        st.markdown("#### 📋 Status dos fechamentos deste mês")

        pendentes = df[df["Status_Fechamento"] == "Pendente"].sort_values("Dias_Para_Entrega")
        atrasados_df = df[df["Status_Fechamento"] == "Atrasado"].sort_values("Dias_Para_Entrega")

        if not atrasados_df.empty:
            st.markdown("**🔴 Atrasados:**")
            for _, row in atrasados_df.iterrows():
                st.markdown(f"""
                <div class="alerta-item urgente">
                    <strong>{row['Empresa']}</strong><br>
                    <span style="font-size: 0.78rem; color: #64748b;">
                        {row['Regime_Tributario']} • {row['Contato']}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        if not pendentes.empty:
            st.markdown("**🟡 Pendentes:**")
            for _, row in pendentes.head(8).iterrows():
                st.markdown(f"""
                <div class="alerta-item">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <strong>{row['Empresa']}</strong><br>
                            <span style="font-size: 0.78rem; color: #64748b;">
                                {row['Regime_Tributario']}
                            </span>
                        </div>
                        <div style="text-align: right;">
                            <strong style="color: #f59e0b;">{int(row['Dias_Para_Entrega'])}d</strong>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with t3:
        st.markdown("#### Regime tributário")
        mix_reg = df.groupby("Regime_Tributario").size().reset_index(name="total")
        fig = px.pie(mix_reg, values="total", names="Regime_Tributario",
                     color_discrete_sequence=[VERDE, AZUL, ROXO, AMBAR], hole=0.55)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(**layout_chart(340), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Honorários por regime")
        hon_reg = df.groupby("Regime_Tributario")["Honorario_Mensal"].sum().reset_index()
        fig = go.Figure(go.Bar(
            x=hon_reg["Regime_Tributario"],
            y=hon_reg["Honorario_Mensal"],
            marker_color=VERDE,
            text=[formatar_brl(v) for v in hon_reg["Honorario_Mensal"]],
            textposition="outside",
        ))
        fig.update_layout(**layout_chart(260))
        st.plotly_chart(fig, use_container_width=True)

    with t4:
        busca = st.text_input("🔍 Buscar empresa", placeholder="Digite...", key="busca_cont")
        df_view = df.copy()
        if busca:
            df_view = df_view[df_view["Empresa"].str.contains(busca, case=False, na=False)]
        df_view["Honorário"] = df_view["Honorario_Mensal"].apply(formatar_brl)
        st.dataframe(
            df_view[["Empresa", "Regime_Tributario", "Status_Fechamento", "Honorário"]],
            use_container_width=True, hide_index=True, height=400,
        )

    st.markdown("---")
    cta_whatsapp(
        "Oi Natan! Vi o demo do Pulse para contabilidade e quero conversar "
        "sobre automatizar o fechamento no meu escritório."
    )
    st.markdown("<br>", unsafe_allow_html=True)
    botao_voltar()


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: CLÍNICA ESTÉTICA
# ═══════════════════════════════════════════════════════════════
def dash_clinica():
    df = pd.read_csv("dados/clinica_atendimentos.csv")
    df["Data"] = pd.to_datetime(df["Data"])
    df_evo = pd.read_csv("dados/clinica_evolucao.csv")

    st.markdown("""
    <div class="dash-header">
        <div>
            <div class="dash-title">💚 Pulse • Clínica</div>
            <div class="dash-subtitle">Demo para Clínicas Estéticas</div>
        </div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    info_dados_ficticios()

    realizados = df[df["Status"] == "Realizado"]
    hoje = pd.Timestamp("2026-04-19")
    mes_atual = realizados[realizados["Data"] >= hoje - pd.Timedelta(days=30)]
    receita_mes = mes_atual["Valor"].sum()
    ticket_medio = mes_atual["Valor"].mean() if not mes_atual.empty else 0

    c1, c2 = st.columns(2)
    with c1:
        st.metric("RECEITA / MÊS", formatar_brl(receita_mes))
    with c2:
        st.metric("ATENDIMENTOS", len(mes_atual),
                  delta=f"+{len(mes_atual) - 135}")

    c3, c4 = st.columns(2)
    with c3:
        st.metric("TICKET MÉDIO", formatar_brl(ticket_medio))
    with c4:
        agendados = df[df["Status"] == "Agendado"]
        st.metric("AGENDADOS", len(agendados))

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["📈 Receita", "⭐ Top", "👤 Pacientes", "📅 Agenda"])

    with t1:
        st.markdown("#### Receita dos últimos 12 meses")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_evo["Mes"],
            y=df_evo["Receita"],
            marker_color=VERDE,
            text=[formatar_brl(v)[:-3] for v in df_evo["Receita"]],
            textposition="outside",
        ))
        fig.update_layout(**layout_chart(300))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Ticket médio (evolução)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_evo["Mes"],
            y=df_evo["Ticket_Medio"],
            mode="lines+markers",
            line=dict(color=VERDE_ESCURO, width=3),
            marker=dict(size=8),
        ))
        fig.update_layout(**layout_chart(260))
        fig.update_yaxes(title="R$")
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        st.markdown("#### 🏆 Procedimentos mais rentáveis")
        top_proc = (realizados.groupby("Procedimento")["Valor"]
                    .sum().sort_values(ascending=True).tail(8))
        fig = go.Figure(go.Bar(
            x=top_proc.values,
            y=top_proc.index,
            orientation="h",
            marker_color=VERDE,
            text=[formatar_brl(v) for v in top_proc.values],
            textposition="outside",
        ))
        fig.update_layout(**layout_chart(360))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 👥 Performance por profissional")
        perf = (realizados.groupby("Profissional")
                .agg(atendimentos=("Valor", "count"), receita=("Valor", "sum"))
                .sort_values("receita", ascending=False))
        perf["receita_fmt"] = perf["receita"].apply(formatar_brl)
        perf = perf[["atendimentos", "receita_fmt"]].rename(
            columns={"atendimentos": "Atendimentos", "receita_fmt": "Receita"}
        )
        st.dataframe(perf, use_container_width=True)

    with t3:
        st.markdown("#### 🌟 Pacientes mais frequentes")
        top_pac = (realizados.groupby("Paciente")
                   .agg(visitas=("Valor", "count"), total=("Valor", "sum"))
                   .sort_values("visitas", ascending=False).head(10))
        top_pac["Total gasto"] = top_pac["total"].apply(formatar_brl)
        top_pac = top_pac[["visitas", "Total gasto"]].rename(columns={"visitas": "Visitas"})
        st.dataframe(top_pac, use_container_width=True)

        st.markdown("#### 💳 Formas de pagamento")
        pagto = realizados.groupby("Forma_Pagamento")["Valor"].sum().reset_index()
        fig = px.pie(pagto, values="Valor", names="Forma_Pagamento",
                     color_discrete_sequence=[VERDE, AZUL, ROXO, AMBAR], hole=0.5)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(**layout_chart(320), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with t4:
        st.markdown("#### 📅 Próximos atendimentos")
        proximos = (df[df["Status"] == "Agendado"]
                    .sort_values("Data")
                    .head(15))

        for _, row in proximos.iterrows():
            data_fmt = row["Data"].strftime("%d/%m às %H:%M")
            st.markdown(f"""
            <div class="alerta-item ok">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <strong>{row['Paciente']}</strong><br>
                        <span style="font-size: 0.78rem; color: #64748b;">
                            {row['Procedimento']} • {row['Profissional']}
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <strong style="color: #059669;">{data_fmt}</strong><br>
                        <span style="font-size: 0.78rem; color: #64748b;">
                            {formatar_brl(row['Valor'])}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    cta_whatsapp(
        "Oi Natan! Vi o demo do Pulse para clínicas e quero conversar "
        "sobre implementar isso na minha clínica."
    )
    st.markdown("<br>", unsafe_allow_html=True)
    botao_voltar()


# ═══════════════════════════════════════════════════════════════
# DASHBOARD: BARBEARIA
# ═══════════════════════════════════════════════════════════════
def dash_barbearia():
    df = pd.read_csv("dados/barbearia_atendimentos.csv")
    df["Data"] = pd.to_datetime(df["Data"])
    df_prod = pd.read_csv("dados/barbearia_produtos.csv")
    df_prod["Data"] = pd.to_datetime(df_prod["Data"])
    df_evo = pd.read_csv("dados/barbearia_evolucao.csv")

    st.markdown("""
    <div class="dash-header">
        <div>
            <div class="dash-title">💈 Pulse • Barbearia</div>
            <div class="dash-subtitle">Demo para Barbearias</div>
        </div>
        <span class="demo-badge">DEMO</span>
    </div>
    """, unsafe_allow_html=True)

    info_dados_ficticios()

    # ═══════ KPIs ═══════
    hoje = pd.Timestamp("2026-04-19")
    realizados = df[df["Status"] == "Realizado"]
    mes_atual = realizados[realizados["Data"] >= hoje - pd.Timedelta(days=30)]
    semana_atual = realizados[realizados["Data"] >= hoje - pd.Timedelta(days=7)]

    receita_mes_servicos = mes_atual["Valor"].sum()
    receita_mes_produtos = df_prod[df_prod["Data"] >= hoje - pd.Timedelta(days=30)]["Receita_Total"].sum()
    receita_total_mes = receita_mes_servicos + receita_mes_produtos

    c1, c2 = st.columns(2)
    with c1:
        st.metric("RECEITA / MÊS", formatar_brl(receita_total_mes),
                  delta="serviços + produtos")
    with c2:
        st.metric("ATENDIMENTOS", len(mes_atual),
                  delta=f"+{len(mes_atual) - 340}")

    c3, c4 = st.columns(2)
    with c3:
        ticket = mes_atual["Valor"].mean() if not mes_atual.empty else 0
        st.metric("TICKET MÉDIO", formatar_brl(ticket))
    with c4:
        agendados_futuros = df[(df["Status"] == "Agendado") & (df["Data"] > hoje)]
        st.metric("AGENDAMENTOS", len(agendados_futuros),
                  delta="próximos 7 dias")

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════ Tabs ═══════
    t1, t2, t3, t4, t5 = st.tabs(["💰 Comissões", "📈 Evolução", "🛍️ Produtos", "👥 Clientes", "📅 Agenda"])

    # ─── Tab 1: COMISSÕES (dor #1 da barbearia) ───
    with t1:
        st.markdown("#### 💰 Comissão da semana atual")
        st.caption("O barbeiro recebe todo sábado. Quanto pagar pra cada um?")

        # Filtra semana atual
        inicio_semana = hoje - pd.Timedelta(days=7)
        semana_real = df[
            (df["Status"] == "Realizado") &
            (df["Data"] >= inicio_semana) &
            (df["Data"] <= hoje)
        ]

        comissoes = (semana_real
                     .groupby("Barbeiro")
                     .agg(atendimentos=("Valor", "count"),
                          receita=("Valor", "sum"),
                          comissao=("Comissao_Barbeiro", "sum"),
                          gorjetas=("Gorjeta", "sum"))
                     .reset_index()
                     .sort_values("receita", ascending=False))

        for _, row in comissoes.iterrows():
            total_receber = row["comissao"] + row["gorjetas"]
            st.markdown(f"""
            <div class="alerta-item ok">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <strong style="font-size: 1.05rem;">{row['Barbeiro']}</strong><br>
                        <span style="font-size: 0.78rem; color: #64748b;">
                            {int(row['atendimentos'])} atendimentos • Receita: {formatar_brl(row['receita'])}
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <strong style="color: #059669; font-size: 1.1rem;">
                            {formatar_brl(total_receber)}
                        </strong><br>
                        <span style="font-size: 0.72rem; color: #64748b;">
                            Comissão: {formatar_brl(row['comissao'])}<br>
                            Gorjetas: {formatar_brl(row['gorjetas'])}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Comparativo mensal por barbeiro")
        comissoes_mes = (mes_atual
                        .groupby("Barbeiro")["Comissao_Barbeiro"]
                        .sum()
                        .reset_index()
                        .sort_values("Comissao_Barbeiro", ascending=True))

        fig = go.Figure(go.Bar(
            y=comissoes_mes["Barbeiro"],
            x=comissoes_mes["Comissao_Barbeiro"],
            orientation="h",
            marker_color=VERDE,
            text=[formatar_brl(v) for v in comissoes_mes["Comissao_Barbeiro"]],
            textposition="outside",
        ))
        fig.update_layout(**layout_chart(260))
        st.plotly_chart(fig, use_container_width=True)

    # ─── Tab 2: EVOLUÇÃO ───
    with t2:
        st.markdown("#### Receita mensal (serviços + produtos)")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Serviços",
            x=df_evo["Mes"],
            y=df_evo["Receita_Servicos"],
            marker_color=VERDE,
        ))
        fig.add_trace(go.Bar(
            name="Produtos",
            x=df_evo["Mes"],
            y=df_evo["Receita_Produtos"],
            marker_color=AZUL,
        ))
        fig.update_layout(**layout_chart(300), barmode="stack",
                          legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Atendimentos por mês")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_evo["Mes"],
            y=df_evo["Atendimentos"],
            mode="lines+markers",
            line=dict(color=VERDE_ESCURO, width=3),
            fill="tozeroy",
            fillcolor="rgba(5,150,105,0.12)",
            marker=dict(size=8),
        ))
        fig.update_layout(**layout_chart(260))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 🌟 Serviços mais populares")
        top_serv = (realizados.groupby("Servico")
                    .agg(qtd=("Valor", "count"), receita=("Valor", "sum"))
                    .sort_values("receita", ascending=True)
                    .tail(6))
        fig = go.Figure(go.Bar(
            y=top_serv.index,
            x=top_serv["receita"],
            orientation="h",
            marker_color=VERDE,
            text=[formatar_brl(v) for v in top_serv["receita"]],
            textposition="outside",
        ))
        fig.update_layout(**layout_chart(320))
        st.plotly_chart(fig, use_container_width=True)

    # ─── Tab 3: PRODUTOS (loja) ───
    with t3:
        st.markdown("#### 🛍️ Vendas da loja (mês)")
        prod_mes = df_prod[df_prod["Data"] >= hoje - pd.Timedelta(days=30)]

        c1, c2 = st.columns(2)
        with c1:
            st.metric("RECEITA PRODUTOS", formatar_brl(prod_mes["Receita_Total"].sum()))
        with c2:
            lucro = prod_mes["Lucro_Bruto"].sum()
            st.metric("LUCRO BRUTO", formatar_brl(lucro))

        st.markdown("#### 🏆 Top 5 produtos mais vendidos")
        top_prod = (prod_mes.groupby("Produto")
                    .agg(qtd=("Quantidade", "sum"),
                         receita=("Receita_Total", "sum"),
                         lucro=("Lucro_Bruto", "sum"))
                    .sort_values("receita", ascending=True)
                    .tail(5))

        fig = go.Figure(go.Bar(
            y=top_prod.index,
            x=top_prod["receita"],
            orientation="h",
            marker_color=AZUL,
            text=[formatar_brl(v) for v in top_prod["receita"]],
            textposition="outside",
        ))
        fig.update_layout(**layout_chart(280))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 💸 Margem por produto")
        prod_margem = (prod_mes.groupby("Produto")
                       .agg(receita=("Receita_Total", "sum"),
                            lucro=("Lucro_Bruto", "sum"))
                       .reset_index())
        prod_margem["margem_pct"] = (prod_margem["lucro"] / prod_margem["receita"] * 100).round(1)
        prod_margem["Receita"] = prod_margem["receita"].apply(formatar_brl)
        prod_margem["Lucro"] = prod_margem["lucro"].apply(formatar_brl)
        prod_margem["Margem"] = prod_margem["margem_pct"].apply(lambda x: f"{x}%")

        st.dataframe(
            prod_margem[["Produto", "Receita", "Lucro", "Margem"]],
            use_container_width=True, hide_index=True,
        )

    # ─── Tab 4: CLIENTES (retenção / clientes sumidos) ───
    with t4:
        st.markdown("#### 🌟 Clientes mais frequentes")

        top_clientes = (realizados.groupby("Cliente")
                        .agg(visitas=("Valor", "count"),
                             total=("Valor", "sum"),
                             ultima_visita=("Data", "max"))
                        .sort_values("visitas", ascending=False)
                        .head(10))
        top_clientes["Última visita"] = top_clientes["ultima_visita"].dt.strftime("%d/%m/%Y")
        top_clientes["Total gasto"] = top_clientes["total"].apply(formatar_brl)

        st.dataframe(
            top_clientes[["visitas", "Total gasto", "Última visita"]].rename(
                columns={"visitas": "Visitas"}
            ),
            use_container_width=True,
        )

        st.markdown("#### 🚨 Clientes sumidos")
        st.caption("Não vêm há mais de 30 dias — hora de mandar mensagem.")

        ultima_visita = (realizados.groupby("Cliente")
                         .agg(ultima=("Data", "max"),
                              visitas_totais=("Valor", "count"),
                              gasto=("Valor", "sum"),
                              telefone=("Telefone", "first")))
        ultima_visita["dias_sem_vir"] = (hoje - ultima_visita["ultima"]).dt.days

        # Clientes frequentes (2+ visitas) que sumiram
        sumidos = ultima_visita[
            (ultima_visita["dias_sem_vir"] > 30) &
            (ultima_visita["visitas_totais"] >= 2)
        ].sort_values("dias_sem_vir", ascending=False).head(8)

        for cliente, row in sumidos.iterrows():
            urgencia = "urgente" if row["dias_sem_vir"] > 60 else ""
            # Link whatsapp pra trazer o cliente de volta
            msg = f"Oi {cliente.split()[0]}, tá sumido! Bora marcar um corte essa semana? Tá com horário pra você."
            wa_link = f"https://wa.me/{row['telefone'].replace('(','').replace(')','').replace('-','').replace(' ','')}?text={msg.replace(' ', '%20')}"

            st.markdown(f"""
            <div class="alerta-item {urgencia}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{cliente}</strong><br>
                        <span style="font-size: 0.78rem; color: #64748b;">
                            {int(row['visitas_totais'])} visitas • {formatar_brl(row['gasto'])} gastos
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <strong style="color: #ef4444;">{int(row['dias_sem_vir'])}d</strong><br>
                        <a href="{wa_link}" target="_blank"
                           style="font-size: 0.72rem; color: #059669; text-decoration: none; font-weight: 600;">
                            💬 Chamar
                        </a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ─── Tab 5: AGENDA ───
    with t5:
        st.markdown("#### 📅 Próximos agendamentos")

        proximos = (df[df["Status"] == "Agendado"]
                    .sort_values("Data")
                    .head(20))

        for _, row in proximos.iterrows():
            data_fmt = row["Data"].strftime("%d/%m às %H:%M")
            st.markdown(f"""
            <div class="alerta-item ok">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <strong>{row['Cliente']}</strong><br>
                        <span style="font-size: 0.78rem; color: #64748b;">
                            {row['Servico']} • {row['Barbeiro']}
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <strong style="color: #059669;">{data_fmt}</strong><br>
                        <span style="font-size: 0.78rem; color: #64748b;">
                            {formatar_brl(row['Valor'])}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    cta_whatsapp(
        "Oi Natan! Vi o demo do Pulse para barbearias e quero conversar "
        "sobre organizar a minha barbearia."
    )
    st.markdown("<br>", unsafe_allow_html=True)
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
