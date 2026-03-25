import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="TCO Avanzado y NPV", layout="wide")

# --- TRADUCCIONES ---
translations = {
    "es": {
        "title": "🚗 Simulador Financiero Multi-Vehículo",
        "subtitle": "Compara múltiples coches, analiza el impacto de la inflación y evalúa el Valor Actual Neto (NPV/VAN).",
        "global_config": "1. Configuración Global",
        "num_vehicles": "Número de vehículos a comparar",
        "years_ownership": "Años de posesión",
        "annual_km": "Kilómetros anuales",
        "macro_env": "2. Entorno Macroeconómico",
        "inflation": "Inflación anual estimada (%)",
        "discount_rate": "Tasa de descuento para VAN/NPV (%)",
        "discount_help": "*La tasa de descuento es lo que rentaría tu dinero si lo invirtieras en lugar de gastarlo en el coche.*",
        "vehicle": "Vehículo",
        "model_name": "Nombre del modelo",
        "base_price": "Precio base (€)",
        "operations": "**Operativa**",
        "consumption": "Consumo (kWh o L/100km)",
        "energy_cost": "Coste energía (€/kWh o €/L)",
        "base_maintenance": "Mantenimiento base (€)",
        "base_insurance": "Seguro base (€)",
        "depreciation": "Depreciación anual (%)",
        "financing": "**Financiación**",
        "type": "Tipo",
        "down_payment_pct": "Entrada (%)",
        "tin": "TIN (%)",
        "term_years": "Plazo (Años)",
        "monthly_fee": "Cuota mensual (€)",
        "initial_payment": "Aportación inicial (€)",
        "mant_ins_included": "Mantenimiento y seguro incluidos",
        "mant_ins_included_leasing": "Mantenimiento y seguro incl. (Leasing)",
        "residual_value": "Valor residual (€)",
        "year": "Año",
        "cash_flow": "📉 Flujo de Caja (Cash Flow)",
        "tco": "📈 Gasto Acumulado (TCO)",
        "cf_desc": "Entradas y salidas de dinero año a año. Nota cómo la inflación hace que las barras bajen un poco más cada año.",
        "cf_y_axis": "Flujo de Caja (€)",
        "tco_desc": "Evolución del dinero total desembolsado. La bajada en el último año representa la recuperación de dinero por la venta del vehículo. **El coche con la línea más baja al final es el más barato de mantener.**",
        "final_results": "💡 Resultados Finales",
        "resale_value": "Valor de reventa:",
        "financed_loan": "*(Vehículo Financiado a {} años)*",
        "financed_renting": "*(Vehículo de Renting)*",
        "financed_leasing": "*(Vehículo de Leasing)*",
        "npv_title": "VAN / Coste Presente Neto:",
        "npv_help": "Gasto total traído a valor de dinero de hoy.",
        "graph_analysis": "📊 Análisis Gráfico",
        "methodology_tab": "📚 Metodología Matemática"
    },
    "en": {
        "title": "🚗 Multi-Vehicle Financial Simulator",
        "subtitle": "Compare multiple cars, analyze inflation impact, and evaluate Net Present Value (NPV).",
        "global_config": "1. Global Configuration",
        "num_vehicles": "Number of vehicles to compare",
        "years_ownership": "Years of ownership",
        "annual_km": "Annual kilometers",
        "macro_env": "2. Macroeconomic Environment",
        "inflation": "Estimated annual inflation (%)",
        "discount_rate": "Discount rate for NPV (%)",
        "discount_help": "*The discount rate represents the return you could earn if you invested the money instead of spending it on the car.*",
        "vehicle": "Vehicle",
        "model_name": "Model name",
        "base_price": "Base price (€)",
        "operations": "**Operations**",
        "consumption": "Consumption (kWh or L/100km)",
        "energy_cost": "Energy cost (€/kWh or €/L)",
        "base_maintenance": "Base maintenance (€)",
        "base_insurance": "Base insurance (€)",
        "depreciation": "Annual depreciation (%)",
        "financing": "**Financing**",
        "type": "Type",
        "down_payment_pct": "Down payment (%)",
        "tin": "Interest Rate (TIN %)",
        "term_years": "Term (Years)",
        "monthly_fee": "Monthly fee (€)",
        "initial_payment": "Initial payment (€)",
        "mant_ins_included": "Maintenance and insurance included",
        "mant_ins_included_leasing": "Maintenance and ins. incl. (Leasing)",
        "residual_value": "Residual value (€)",
        "year": "Year",
        "cash_flow": "📉 Cash Flow",
        "tco": "📈 Cumulative Cost (TCO)",
        "cf_desc": "Year-by-year cash inflows and outflows. Notice how inflation pushes operational costs higher each year.",
        "cf_y_axis": "Cash Flow (€)",
        "tco_desc": "Evolution of total money spent. The drop in the final year represents money recovered from vehicle resale. **The car with the lowest line at the end is the cheapest to maintain.**",
        "final_results": "💡 Final Results",
        "resale_value": "Resale value:",
        "financed_loan": "*(Financed for {} years)*",
        "financed_renting": "*(Renting Vehicle)*",
        "financed_leasing": "*(Leasing Vehicle)*",
        "npv_title": "NPV / Net Present Cost:",
        "npv_help": "Total cost brought to today's money value.",
        "graph_analysis": "📊 Graphical Analysis",
        "methodology_tab": "📚 Mathematical Methodology"
    }
}

st.sidebar.image("Logo-IREC.jpg", use_column_width=True)
lang = st.sidebar.radio("Idioma / Language", options=["es", "en"], format_func=lambda x: "🇪🇸 Español" if x == "es" else "🇬🇧 English")
t = translations[lang]

st.sidebar.markdown("---")
st.sidebar.caption("👨‍💻 Desarrollado por: **Tomás Montes**")

st.title(t["title"])
st.write(t["subtitle"])

# --- BARRA LATERAL: PARÁMETROS GLOBALES ---
st.sidebar.header(t["global_config"])
num_vehiculos = st.sidebar.number_input(t["num_vehicles"], min_value=1, max_value=4, value=2)
anos_propiedad = st.sidebar.slider(t["years_ownership"], 1, 15, 5)
km_anuales = st.sidebar.number_input(t["annual_km"], value=15000, step=1000)

st.sidebar.markdown("---")
st.sidebar.header(t["macro_env"])
inflacion_anual = st.sidebar.number_input(t["inflation"], value=2.5, step=0.5) / 100
tasa_descuento = st.sidebar.number_input(t["discount_rate"], value=3.0, step=0.5) / 100
st.sidebar.write(t["discount_help"])

st.markdown("---")

# --- CREACIÓN DINÁMICA DE VEHÍCULOS ---
cols = st.columns(num_vehiculos)
vehiculos_data = []

# Valores por defecto para el primer par (R5 vs Clio) para que no tengas que teclear de cero
defaults = [
    {"nombre": "Renault 5 E-Tech", "precio": 26800, "energia": 15.0, "coste_u": 0.15, "mant": 200, "seg": 400, "dep": 12.0, "finan_tipo": "UPFRONT"},
    {"nombre": "Renault Clio TCe", "precio": 19000, "energia": 5.5, "coste_u": 1.60, "mant": 350, "seg": 450, "dep": 8.0, "finan_tipo": "UPFRONT"},
    {"nombre": "Coche 3", "precio": 25000, "energia": 14.0, "coste_u": 0.15, "mant": 250, "seg": 450, "dep": 10.0, "finan_tipo": "LOAN"},
    {"nombre": "Coche 4", "precio": 30000, "energia": 6.0, "coste_u": 1.60, "mant": 300, "seg": 500, "dep": 10.0, "finan_tipo": "LOAN"}
]

for i in range(num_vehiculos):
    with cols[i]:
        st.subheader(f"{t['vehicle']} {i+1}")
        d = defaults[i]
        
        nombre = st.text_input(t["model_name"], value=d["nombre"], key=f"nom_{i}")
        precio = st.number_input(t["base_price"], value=d["precio"], step=1000, key=f"pre_{i}")
        
        st.markdown(t["operations"])
        consumo = st.number_input(t["consumption"], value=d["energia"], step=0.5, key=f"con_{i}")
        coste_u = st.number_input(t["energy_cost"], value=d["coste_u"], step=0.01, key=f"cos_{i}")
        mant = st.number_input(t["base_maintenance"], value=d["mant"], step=50, key=f"man_{i}")
        seg = st.number_input(t["base_insurance"], value=d["seg"], step=50, key=f"seg_{i}")
        depreciacion = st.slider(t["depreciation"], 1.0, 30.0, d["dep"], step=0.5, key=f"dep_{i}") / 100
        
        st.markdown(t["financing"])
        opciones_fin = ["UPFRONT", "RENTING", "LEASING", "LOAN"]
        default_finan = d.get("finan_tipo", "UPFRONT")
        default_idx = opciones_fin.index(default_finan) if default_finan in opciones_fin else 0
        
        finan_tipo = st.selectbox(t["type"], options=opciones_fin, index=default_idx, key=f"fin_tipo_{i}")
        
        # Opciones por defecto
        entrada_pct = 1.0; interes = 0.0; plazo = 1
        cuota_mensual = 0.0; entrada_renting = 0.0; valor_residual = 0.0; seguro_mant_incluido = False
        
        if finan_tipo == "LOAN":
            entrada_pct = st.slider(t["down_payment_pct"], 0, 80, 20, key=f"ent_{i}") / 100
            interes = st.number_input(t["tin"], value=7.5, step=0.5, key=f"int_{i}") / 100
            plazo = st.slider(t["term_years"], 1, 10, 5, key=f"pla_{i}")
        elif finan_tipo == "RENTING":
            cuota_mensual = st.number_input(t["monthly_fee"], value=400.0, step=10.0, key=f"cuota_renting_{i}")
            entrada_renting = st.number_input(t["initial_payment"], value=0.0, step=500.0, key=f"ent_renting_{i}")
            seguro_mant_incluido = st.checkbox(t["mant_ins_included"], value=True, key=f"seg_mant_incl_{i}")
        elif finan_tipo == "LEASING":
            cuota_mensual = st.number_input(t["monthly_fee"], value=350.0, step=10.0, key=f"cuota_leasing_{i}")
            entrada_renting = st.number_input(t["initial_payment"], value=2000.0, step=500.0, key=f"ent_leasing_{i}")
            valor_residual = st.number_input(t["residual_value"], value=10000.0, step=1000.0, key=f"val_res_{i}")
            seguro_mant_incluido = st.checkbox(t["mant_ins_included_leasing"], value=False, key=f"seg_mant_leasing_{i}")
            
        vehiculos_data.append({
            "nombre": nombre, "precio": precio, "consumo": consumo, "coste_u": coste_u,
            "mant": mant, "seg": seg, "depreciacion": depreciacion,
            "finan_tipo": finan_tipo, "entrada_pct": entrada_pct, "interes": interes, "plazo": plazo,
            "cuota_mensual": cuota_mensual, "entrada_renting": entrada_renting, "valor_residual": valor_residual,
            "seguro_mant_incluido": seguro_mant_incluido
        })

# --- FUNCIONES MATEMÁTICAS ---
def calcular_cuota_anual(capital, tasa, años):
    if tasa == 0: return capital / años if años > 0 else 0
    tasa_m = tasa / 12
    meses = años * 12
    cuota_m = capital * (tasa_m / (1 - (1 + tasa_m) ** -meses))
    return cuota_m * 12

def capital_pendiente(capital, tasa, años_prestamo, años_transcurridos):
    if años_transcurridos >= años_prestamo: return 0
    if tasa == 0: return capital - (capital / años_prestamo) * años_transcurridos
    tasa_m = tasa / 12
    meses_tot = años_prestamo * 12
    meses_pag = años_transcurridos * 12
    cuota_m = capital * (tasa_m / (1 - (1 + tasa_m) ** -meses_tot))
    return cuota_m * ((1 - (1 + tasa_m) ** -(meses_tot - meses_pag)) / tasa_m)

# --- MOTORES DE CÁLCULO ---
flujos_anuales = []
npv_resultados = {}

for v in vehiculos_data:
    v["coste_energia_base"] = (km_anuales / 100) * v["consumo"] * v["coste_u"]
    v["reventa"] = v["precio"] * ((1 - v["depreciacion"]) ** anos_propiedad)
    
    npv_vehiculo = 0
    flujos_vehiculo = []
    
    cuota_anual_prestamo = 0
    cuota_anual_renting_leasing = 0
    
    if v["finan_tipo"] == "UPFRONT":
        v["entrada"] = v["precio"]
        v["prestamo"] = 0
    elif v["finan_tipo"] == "LOAN":
        v["entrada"] = v["precio"] * v["entrada_pct"]
        v["prestamo"] = v["precio"] - v["entrada"]
        cuota_anual_prestamo = calcular_cuota_anual(v["prestamo"], v["interes"], v["plazo"])
    elif v["finan_tipo"] in ["RENTING", "LEASING"]:
        v["entrada"] = v["entrada_renting"]
        v["prestamo"] = 0
        cuota_anual_renting_leasing = v["cuota_mensual"] * 12

    for ano in range(anos_propiedad + 1):
        if ano == 0:
            flujo_t = -v["entrada"]
        else:
            # Gastos operativos
            if v.get("seguro_mant_incluido", False):
                gasto_base = v["coste_energia_base"]
            else:
                gasto_base = v["coste_energia_base"] + v["mant"] + v["seg"]
                
            inflacion_factor = (1 + inflacion_anual) ** ano
            gasto_op_inflado = gasto_base * inflacion_factor
            
            pago_financiero = 0
            if v["finan_tipo"] == "LOAN" and ano <= v["plazo"]:
                pago_financiero = cuota_anual_prestamo
            elif v["finan_tipo"] in ["RENTING", "LEASING"]: 
                # Asumimos que el renting/leasing dura al menos los anos_propiedad
                pago_financiero = cuota_anual_renting_leasing
                
            flujo_t = -gasto_op_inflado - pago_financiero
            
            # Ajustes en el último año (reventa, deuda pendiente, valor residual)
            if ano == anos_propiedad:
                if v["finan_tipo"] in ["UPFRONT", "LOAN"]:
                    deuda_pend = capital_pendiente(v["prestamo"], v["interes"], v["plazo"], anos_propiedad) if v["finan_tipo"] == "LOAN" else 0
                    flujo_t += (v["reventa"] - deuda_pend)
                elif v["finan_tipo"] == "LEASING":
                    # En leasing se paga el valor residual para quedarse el coche, teniendo así el valor de reventa.
                    flujo_t += (v["reventa"] - v["valor_residual"])
                elif v["finan_tipo"] == "RENTING":
                    # El vehículo se devuelve al final del renting.
                    pass
                
        flujos_vehiculo.append(flujo_t)
        npv_vehiculo += flujo_t / ((1 + tasa_descuento) ** ano)
        
    v["flujos"] = flujos_vehiculo
    v["npv"] = npv_vehiculo

# --- PREPARAR DATOS PARA GRÁFICOS ---
# 1. Gráfico de Flujo de Caja
df_flujos = pd.DataFrame({t["year"]: [f"{t['year']} {i}" for i in range(anos_propiedad + 1)]}).set_index(t["year"])
for v in vehiculos_data:
    df_flujos[v["nombre"]] = v["flujos"]

# 2. Gráfico de TCO Acumulado (Para ver cómo se acumula el gasto)
# Invertimos el signo para que sea "Gasto acumulado" (positivo = más gasto)
df_acumulado = pd.DataFrame({t["year"]: [i for i in range(anos_propiedad + 1)]}).set_index(t["year"])
for v in vehiculos_data:
    # Hacemos suma acumulada de los flujos negativos
    df_acumulado[v["nombre"]] = np.cumsum([-f for f in v["flujos"]])

st.markdown("---")

# --- VISUALIZACIONES ---
st.header(t["graph_analysis"])
tab1, tab2, tab3 = st.tabs([t["cash_flow"], t["tco"], t["methodology_tab"]])

with tab1:
    st.write(t["cf_desc"])
    
    # Gráfico de barras agrupadas con Plotly
    fig_flujos = px.bar(df_flujos, barmode="group", labels={'value': t["cf_y_axis"], 'variable': t["vehicle"]})
    st.plotly_chart(fig_flujos, use_container_width=True)

with tab2:
    st.write(t["tco_desc"])
    st.line_chart(df_acumulado)

with tab3:
    if lang == "es":
        st.markdown("""
        ### 1. Actualización por Inflación
        A los gastos operativos base anuales (energía, mantenimiento, seguro) se les aplica una tasa de inflación compuesta. Esto modela que las cosas son más caras en el futuro:
        """)
        st.latex(r"\text{Gasto\_Inflado}_t = \text{Gasto\_Base} \times (1 + \text{inflación})^t")
        
        st.markdown("""
        ### 2. Valor Actual Neto (VAN / NPV)
        Para comparar una gran salida de dinero hoy frente a pequeños ahorros a lo largo de los años, descontamos los flujos de caja futuros a un valor presente utilizando una **tasa de descuento**. El VAN representa cuánto dinero de hoy te costará la posesión del vehículo a lo largo de todo el ciclo de vida:
        """)
        st.latex(r"\text{VAN} = \sum_{t=0}^{n} \frac{\text{Flujo\_Caja}_t}{(1 + \text{tasa\_descuento})^t}")
        
        st.markdown("""
        ### 3. Fórmulas de Financiación (Sistema Francés)
        Cuando seleccionas el formato "*Préstamo (LOAN)*", utilizamos el sistema de amortización francés para calcular cuotas fijas:
        """)
        st.latex(r"\text{Cuota\_Mensual} = \text{Capital} \times \frac{\text{TIN}/12}{1 - (1 + \text{TIN}/12)^{-(\text{Años} \times 12)}}")
        
        st.markdown("""
        Al final del periodo de análisis (año $n$), si decides vender el vehículo, primero liquidas la **deuda pendiente**, y la ganancia neta o saldo se imputa como flujo de caja en ese último año.
        """)
    else:
        st.markdown("""
        ### 1. Inflation Indexing
        Base operational expenses (energy, maintenance, insurance) are subject to compound inflation. This models the rising cost of living over time:
        """)
        st.latex(r"\text{Inflated\_Exp}_t = \text{Base\_Exp} \times (1 + \text{inflation})^t")
        
        st.markdown("""
        ### 2. Net Present Value (NPV / VAN)
        To compare a large cash output today versus smaller savings over 10 years, we discount future cash flows down to a present value using a **discount rate**. The NPV represents how much "money in today's terms" the vehicle cost will drain throughout its lifecycle:
        """)
        st.latex(r"\text{NPV} = \sum_{t=0}^{n} \frac{\text{Cash\_Flow}_t}{(1 + \text{discount\_rate})^t}")
        
        st.markdown("""
        ### 3. Constant Loan Formulas (French Amortization)
        When the "*LOAN*" format is selected, the generalized French amortization system translates your inputs to a fixed monthly quota:
        """)
        st.latex(r"\text{Monthly\_Fee} = \text{Principal} \times \frac{\text{TIN}/12}{1 - (1 + \text{TIN}/12)^{-(\text{Years} \times 12)}}")
        
        st.markdown("""
        At the end of the analysis period (year $n$), if you 'resale' the vehicle, you must first clear any **pending debt principal** and the resulting net liquidity is factored as a cash flow in that final year.
        """)

# --- RESULTADOS FINALES ---
st.markdown("---")
st.header(t["final_results"])

res_cols = st.columns(num_vehiculos)
for i, v in enumerate(vehiculos_data):
    with res_cols[i]:
        st.subheader(v["nombre"])
        st.write(f"**{t['resale_value']}** {v['reventa']:,.2f} €")
        
        # Si el NPV es negativo (que lo será, porque un coche es un gasto), mostramos su valor absoluto como "Coste Real"
        coste_presente = abs(v["npv"])
        
        if v["finan_tipo"] == "LOAN":
            st.write(t["financed_loan"].format(v['plazo']))
        elif v["finan_tipo"] == "RENTING":
            st.write(t["financed_renting"])
        elif v["finan_tipo"] == "LEASING":
            st.write(t["financed_leasing"])
            
        st.markdown(f"### {t['npv_title']}")
        st.markdown(f"### **{coste_presente:,.2f} €**")
        st.caption(t["npv_help"])