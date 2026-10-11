# =============================================================================
# SITIA-PYME · Micro App v1.0
# Recorrido estándar de 8 componentes
# USACH · ASIQUINTA · FONDEF IDeA I+D 2027
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json

st.set_page_config(
    page_title="SITIA-PYME · Micro App",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white; padding: 30px; border-radius: 12px;
        margin-bottom: 25px;
    }
    .main-header h1 { margin: 0; font-size: 2.2em; }
    .main-header p { margin: 8px 0 0 0; opacity: 0.9; }
    .kpi-card {
        background: white; padding: 20px; border-radius: 10px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 5px 0;
    }
    .kpi-card.rojo { border-color: #dc2626; }
    .kpi-card.amarillo { border-color: #f59e0b; }
    .kpi-card.verde { border-color: #10b981; }
    .kpi-label { font-size: 0.8em; color: #64748b; text-transform: uppercase; }
    .kpi-value { font-size: 2em; font-weight: bold; color: #1e3a8a; margin: 8px 0; }
    .kpi-card.rojo .kpi-value { color: #dc2626; }
    .kpi-card.amarillo .kpi-value { color: #f59e0b; }
    .kpi-card.verde .kpi-value { color: #10b981; }
</style>
""", unsafe_allow_html=True)


BENCHMARK_SECTORIAL = {
    "C": {"nombre": "Manufactura", "empresas_2024": 1374,
          "ventas_qn": 13409.20, "ventas_meta": 31114.18, "brecha_ventas": 1.320,
          "empleo_qn": 6.34, "empleo_meta": 7.32, "brecha_empleo": 0.154,
          "prioridad": "Productividad · costos · automatización · B2B · financiamiento"},
    "G": {"nombre": "Comercio", "empresas_2024": 3225,
          "ventas_qn": 8624.10, "ventas_meta": 17494.41, "brecha_ventas": 1.029,
          "empleo_qn": 2.70, "empleo_meta": 2.79, "brecha_empleo": 0.032,
          "prioridad": "CRM · e-commerce · inventario · pricing · fidelización"},
    "F": {"nombre": "Construcción", "empresas_2024": 624,
          "ventas_qn": 4464.85, "ventas_meta": 7104.82, "brecha_ventas": 0.591,
          "empleo_qn": 6.11, "empleo_meta": 9.53, "brecha_empleo": 0.558,
          "prioridad": "Caja · costos · cartera · planificación · capital humano"},
}


def generador_ideas():
    st.markdown("## 💡 Generador de Ideas")
    st.markdown("Genera ideas de intervención basadas en datos reales.")
    col1, col2 = st.columns([1, 2])
    with col1:
        sector = st.selectbox("Sector", ["Manufactura", "Comercio", "Construcción"], key="ideas_sector")
        tipo_idea = st.selectbox("Tipo", ["Intervención sectorial", "Propuesta de valor", "Programa piloto"], key="ideas_tipo")
        contexto = st.text_area("Contexto", value="Quinta Normal, brecha crítica, 84% sin KPIs", height=80, key="ideas_contexto")
        generar = st.button("✨ Generar ideas", type="primary", use_container_width=True)
    with col2:
        if generar:
            with st.spinner("Generando..."):
                time.sleep(0.8)
                ideas = [
                    {"titulo": "Clínica de productividad lean",
                     "descripcion": "Programa de 12 semanas para redefinir procesos y estandarizar operaciones.",
                     "impacto": "Reducción 15-25% en costos operativos",
                     "complejidad": "Media",
                     "kpi": "Ventas/empresa",
                     "brecha": "Escala y productividad"},
                    {"titulo": "Plataforma B2B de encadenamiento",
                     "descripcion": "Marketplace digital que conecta pymes con compradores industriales.",
                     "impacto": "Acceso a nuevos mercados; +20-40% en ventas",
                     "complejidad": "Alta",
                     "kpi": "Ventas/empresa",
                     "brecha": "Acceso a mercados"},
                    {"titulo": "Fondo de capital de trabajo",
                     "descripcion": "Fondo concursable con garantía estatal para capital de trabajo.",
                     "impacto": "Desbloqueo de inversión; +15% productividad",
                     "complejidad": "Media",
                     "kpi": "Inversión por empresa",
                     "brecha": "Financiamiento"},
                ]
                for i, idea in enumerate(ideas, 1):
                    with st.expander(f"💡 Idea {i}: {idea['titulo']}", expanded=(i == 1)):
                        st.markdown(f"**Descripción:** {idea['descripcion']}")
                        st.markdown(f"**Impacto:** {idea['impacto']}")
                        st.markdown(f"**Complejidad:** {idea['complejidad']}")
                        st.markdown(f"**KPI:** `{idea['kpi']}`")
                        st.markdown(f"**Brecha:** {idea['brecha']}")
        else:
            st.info("👈 Configura y presiona Generar ideas.")


def tu_primer_mvp():
    st.markdown("## 🛠️ Tu Primer MVP")
    st.markdown("Diagnostica una pyme y genera una recomendación priorizada.")
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.form("form_diagnostico"):
            nombre = st.text_input("Nombre", "Mi PyME SpA")
            sector = st.selectbox("Sector", ["Manufactura", "Comercio", "Construcción"])
            empleados = st.number_input("N° empleados", 1, 250, 10)
            ventas_uf = st.number_input("Ventas anuales (UF)", 100, 100000, 5000)
            tiene_kpis = st.checkbox("¿Tiene KPIs?", value=False)
            nivel_procesos = st.slider("Nivel de procesos (1-5)", 1, 5, 2)
            submitted = st.form_submit_button("🔍 Diagnosticar", type="primary", use_container_width=True)
    with col2:
        if submitted:
            codigo = {"Manufactura": "C", "Comercio": "G", "Construcción": "F"}[sector]
            b = BENCHMARK_SECTORIAL[codigo]
            brecha_ventas = max(0, (b["ventas_meta"] - ventas_uf) / ventas_uf) if ventas_uf > 0 else 0
            score_kpis = 0 if tiene_kpis else 30
            score_procesos = (5 - nivel_procesos) * 10
            score_ventas = min(40, brecha_ventas * 20)
            score_total = min(100, score_kpis + score_procesos + score_ventas)
            if score_total >= 60:
                nivel_riesgo, color = "ALTO", "rojo"
            elif score_total >= 30:
                nivel_riesgo, color = "MEDIO", "amarillo"
            else:
                nivel_riesgo, color = "BAJO", "verde"
            st.markdown("### 📊 Resultado")
            st.markdown(
                f'<div class="kpi-card {color}">'
                f'<div class="kpi-label">Score</div>'
                f'<div class="kpi-value">{score_total:.0f}/100</div>'
                f'<strong>RIESGO {nivel_riesgo}</strong></div>',
                unsafe_allow_html=True,
            )
            m1, m2, m3 = st.columns(3)
            m1.metric("Brecha ventas", f"+{brecha_ventas*100:.0f}%")
            m2.metric("Nivel procesos", f"{nivel_procesos}/5")
            m3.metric("KPIs", "Sí" if tiene_kpis else "No")
            st.markdown("### 🎯 Ruta de intervención")
            for i, accion in enumerate(b["prioridad"].split(" · "), 1):
                st.markdown(f"**{i}.** {accion}")
        else:
            st.info("👈 Completa el formulario.")


def kit_de_marca():
    st.markdown("## 🎨 Kit de Marca")
    colores = {
        "Azul primario": "#1e3a8a", "Azul secundario": "#3b82f6",
        "Rojo alerta": "#dc2626", "Amarillo precaución": "#f59e0b",
        "Verde éxito": "#10b981", "Gris fondo": "#f5f7fa",
    }
    cols = st.columns(3)
    for i, (nombre, hex_code) in enumerate(colores.items()):
        with cols[i % 3]:
            txt = "#2c3e50" if hex_code in ["#f5f7fa"] else "white"
            st.markdown(
                f'<div style="background:{hex_code}; padding:30px; border-radius:8px;'
                f'margin:5px 0; text-align:center;">'
                f'<p style="color:{txt}; font-weight:bold; margin:0;">{nombre}</p>'
                f'<p style="color:{txt}; font-size:0.85em; margin:5px 0 0 0;">{hex_code}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
    st.markdown("### ✍️ Tipografía")
    st.markdown("- Títulos: Inter Bold")
    st.markdown("- Cuerpo: Inter Regular")
    st.markdown("- Mono: JetBrains Mono")


def generador_landing():
    st.markdown("## 🖼️ Generador de Landing")
    titulo = st.text_input("Título", "SITIA-PYME · Inteligencia Territorial para tu PyME")
    subtitulo = st.text_input("Subtítulo", "Diagnóstico, recomendación y seguimiento")
    cta = st.text_input("CTA", "Solicita tu diagnóstico gratuito")
    st.markdown("### 👁️ Preview")
    st.markdown(
        f'<div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6);'
        f'color: white; padding: 60px 40px; border-radius: 15px;'
        f'text-align: center; margin: 20px 0;">'
        f'<h1>{titulo}</h1><p>{subtitulo}</p>'
        f'<a href="#" style="background: white; color: #1e3a8a; padding: 15px 40px;'
        f'border-radius: 30px; text-decoration: none; font-weight: bold;">{cta}</a>'
        f'</div>',
        unsafe_allow_html=True,
    )


def generador_anuncios():
    st.markdown("## 📢 Generador de Anuncios")
    col1, col2 = st.columns([1, 1])
    with col1:
        plataforma = st.selectbox("Plataforma", ["LinkedIn", "Instagram", "Facebook", "Google Ads"])
        generar = st.button("✨ Generar", type="primary", use_container_width=True)
    with col2:
        if generar:
            anuncios = [
                {"headline": "¿Tu PyME pierde ventas sin saber por qué?",
                 "body": "En Quinta Normal, las ventas por empresa cayeron 47.5% desde 2019. Diagnóstico gratuito.",
                 "cta": "Solicita tu diagnóstico →",
                 "hashtags": "#PyME #QuintaNormal #SITIA"},
                {"headline": "Tu PyME no necesita más apoyo genérico",
                 "body": "Usamos datos reales para recomendarte exactamente qué hacer en tu sector.",
                 "cta": "Descubre tu ruta →",
                 "hashtags": "#PyMEChile #Datos"},
                {"headline": "Cierra tu brecha de ventas con una ruta clara",
                 "body": "SITIA-PYME ayuda a empresas a cerrar su brecha principal.",
                 "cta": "Únete →",
                 "hashtags": "#USACH #ASIQUINTA"},
            ]
            for i, ad in enumerate(anuncios, 1):
                with st.expander(f"📢 Variante {i}", expanded=(i == 1)):
                    st.markdown(f"**Headline:** {ad['headline']}")
                    st.markdown(f"**Body:** {ad['body']}")
                    st.markdown(f"**CTA:** `{ad['cta']}`")
                    st.markdown(f"**Hashtags:** {ad['hashtags']}")
        else:
            st.info("👈 Configura y presiona Generar.")


def generador_emails():
    st.markdown("## 📧 Generador de Emails")
    tipo = st.selectbox("Tipo", ["Prospección (3)", "Onboarding (4)", "Seguimiento (3)"])
    if st.button("✨ Generar secuencia", type="primary"):
        emails = [
            {"dia": "Día 0", "asunto": "¿Sabes cuál es tu brecha?",
             "cuerpo": "Hola [Nombre],\n\nNuestro diagnóstico gratuito identifica tu brecha.\n\n[Link]"},
            {"dia": "Día 3", "asunto": "Caso real: 40% cerrado en 90 días",
             "cuerpo": "Hola [Nombre],\n\nUna PyME cerró el 40% de su brecha.\n\n[Caso]"},
            {"dia": "Día 7", "asunto": "Última oportunidad",
             "cuerpo": "Hola [Nombre],\n\nEl programa cierra postulaciones.\n\n[Postular]"},
        ]
        for i, email in enumerate(emails, 1):
            with st.expander(f"📧 Email {i}: {email['asunto']}", expanded=(i == 1)):
                st.markdown(f"**Asunto:** {email['asunto']}")
                st.markdown(f"**Día:** {email['dia']}")
                st.markdown("---")
                st.markdown(email["cuerpo"])


def ventas_diarias():
    st.markdown("## 📈 Ventas Diarias")
    if "ventas_historial" not in st.session_state:
        hoy = datetime.now()
        np.random.seed(42)
        ejemplo = []
        for i in range(30):
            fecha = hoy - timedelta(days=29 - i)
            v = int(np.random.randint(0, 5))
            ejemplo.append({
                "fecha": fecha.strftime("%Y-%m-%d"),
                "diagnosticos": v,
                "meta": 3,
                "cumplimiento": v / 3 * 100,
            })
        st.session_state.ventas_historial = pd.DataFrame(ejemplo)
    with st.form("form_ventas"):
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha_input = st.date_input("Fecha", datetime.now())
        with col2:
            cantidad = st.number_input("Diagnósticos", 0, 50, 3)
        with col3:
            meta = st.number_input("Meta", 1, 50, 3)
        submitted = st.form_submit_button("💾 Registrar", type="primary", use_container_width=True)
    if submitted:
        nuevo = {
            "fecha": fecha_input.strftime("%Y-%m-%d"),
            "diagnosticos": cantidad,
            "meta": meta,
            "cumplimiento": cantidad / meta * 100,
        }
        df = st.session_state.ventas_historial
        df = df[df["fecha"] != nuevo["fecha"]]
        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        st.session_state.ventas_historial = df.sort_values("fecha").reset_index(drop=True)
        st.success("✅ Registrado")
        st.rerun()
    df = st.session_state.ventas_historial
    df["fecha_dt"] = pd.to_datetime(df["fecha"])
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Hoy", int(df.tail(1)["diagnosticos"].iloc[0]))
    with col2:
        st.metric("Últimos 7d", int(df.tail(7)["diagnosticos"].sum()))
    with col3:
        st.metric("Últimos 30d", int(df.tail(30)["diagnosticos"].sum()))
    with col4:
        cumpl = df.tail(30)["diagnosticos"].sum() / df.tail(30)["meta"].sum() * 100
        st.metric("Cumplimiento", f"{cumpl:.0f}%")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["fecha_dt"], y=df["diagnosticos"], name="Diagnósticos", marker_color="#3b82f6"))
    fig.add_trace(go.Scatter(x=df["fecha_dt"], y=df["meta"], name="Meta",
                              line=dict(color="#dc2626", dash="dash", width=2)))
    fig.update_layout(title="Diagnósticos diarios vs meta", height=400, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)


def panel_ventas():
    st.markdown("## 📊 Panel de Ventas")
    pipeline = pd.DataFrame({
        "Etapa": ["Prospectos", "Contactados", "Diagnóstico", "Propuesta", "Cerrados"],
        "Cantidad": [250, 180, 120, 65, 42],
        "Tasa conversión": [100.0, 72.0, 48.0, 26.0, 16.8],
    })
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Prospectos", "250", delta="+45")
    with col2:
        st.metric("Diagnósticos", "120", delta="+28")
    with col3:
        st.metric("Conversión", "16.8%", delta="+2.3 pp")
    with col4:
        st.metric("MRR", "$2.1M CLP", delta="+18%")
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure(go.Funnel(y=pipeline["Etapa"], x=pipeline["Cantidad"],
                                    textinfo="value+percent initial"))
        fig.update_layout(title="Funnel", height=400)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = go.Figure(go.Bar(x=pipeline["Etapa"], y=pipeline["Tasa conversión"],
                                text=[f"{v}%" for v in pipeline["Tasa conversión"]],
                                textposition="outside"))
        fig.update_layout(title="Conversión", yaxis_title="%", height=400)
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(pipeline, use_container_width=True, hide_index=True)


def main():
    st.markdown(
        '<div class="main-header">'
        '<h1>🏭 SITIA-PYME · Micro App</h1>'
        '<p>Sistema Inteligente Territorial de Alerta Temprana e Intervención</p>'
        '<p style="font-size: 0.9em; opacity: 0.8;">USACH · ASIQUINTA · FONDEF IDeA I+D 2027</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("## 🧭 Recorrido estándar")
    opciones = {
        "💡 1) Generador de Ideas": generador_ideas,
        "🛠️ 2) Tu primer MVP": tu_primer_mvp,
        "🎨 3) Kit de Marca": kit_de_marca,
        "🖼️ 4) Generador de Landing": generador_landing,
        "📢 5) Generador de Anuncios": generador_anuncios,
        "📧 6) Generador de Emails": generador_emails,
        "📈 7) Ventas diarias": ventas_diarias,
        "📊 8) Panel de ventas": panel_ventas,
    }
    seleccion = st.sidebar.radio("Módulo", list(opciones.keys()), label_visibility="collapsed")
    opciones[seleccion]()
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #94a3b8; padding: 20px;">'
        '<p><strong>SITIA-PYME v1.0</strong> · USACH · ASIQUINTA</p></div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
