import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Dados Câncer de Mama - ChatBot", page_icon=":bar_chart:", layout="wide")

st.title("📈🩺| Dados Câncer de Mama no Brasil em 2023")

#leitura do arquivo 
df = pd.read_excel(
    io="Dadoscancerdemama.xlsx",
    engine="openpyxl",
    sheet_name="Planilha1",
    usecols="A:D",
    nrows=34
)


st.dataframe(df)
st.markdown("Dados extraídos do Instituto Nacional de Câncer - INCA")

# Sidebar
st.sidebar.header("Filtre a região aqui:")

select_region = df.query('Regiões == "Região Norte" | Regiões == "Região Sul" | Regiões == "Região Nordeste" |  Regiões == "Região Sudeste" | Regiões == "Região Centro-Oeste" | Regiões == "Rio Grande do Norte"')

regiao = st.sidebar.multiselect(
    "Selecione a Região:",
    options= select_region['Regiões'].unique(),
    default= select_region['Regiões'].unique()
)

select_region = df.query('Regiões == @regiao')


# --MainPage--
st.title(":bar_chart: Câncer de Mama")
st.markdown("Taxas brutas e ajustadas de incidência por neoplasia maligna da mama, por 100 mil mulheres, estimadas para o ano de 2023, segundo Brasil, regiões e Unidades da Federação")

st.markdown("##")

mean_cases = round(select_region["Nº de casos"].mean(), 2)
taxa_b = round(select_region["Taxa bruta"].sum(), 2)
taxa_a = round(select_region["Taxa ajustada"].sum(), 2)

left_column, center_column, right_column = st.columns(3)

with left_column:
    st.subheader("Média de casos:")
    st.subheader(f"{mean_cases:,}")

with center_column:
    st.subheader("Total taxa bruta:")
    st.subheader(f"{taxa_b:,}")

with right_column:
    st.subheader("Total taxa ajustada:")
    st.subheader(f"{taxa_a:,}")

st.markdown("---")

# Calcular a média da idade por região
mean_age_by_region = (select_region.groupby(by=["Regiões"]).mean().round(0)[["Nº de casos"]].sort_values(by="Nº de casos"))

# Criação do gráfico diretamente do resultado do groupby
fig_sit = px.bar(
    mean_age_by_region, y=mean_age_by_region.index, x="Nº de casos",
    orientation="h",
    title="<b> Nº de casos de câncer de mama por região no Brasil</b>",
    color_discrete_sequence= ["#0083B8"] * len(mean_age_by_region),
    template="plotly_white",
    color="Nº de casos",

)


# Adicionar o chatbot
chatbot_code = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300&display=swap');

    h1{
    color: #ffff;
    font-size: 40px;
    font-family: 'Poppins', sans-serif;
    font-weight: 800;

    }

    .texto{
    width: 40%;
    color: #ffff;
    font-size: 18px;
    font-family: 'Poppins', sans-serif;
    }
</style>

<h1> FlorenceBot 🤖 </h1>
<p class="texto"> Com o propósito de ajudar mais pessoas a prevenirem-se contra a doença. Nossa missão é alcançar
o número máximo de pessoas para que tenham acesso à informação, detecção e prevenção do câncer de mama. 

Esperamos que após a análise e conversa com a FlorenceBot, você saia do site com mais conhecimento sobre a doença e que também 
consiga disseminar a informação para outras mulheres, juntos podemos ter um mundo mais conscientizado acerca dessa enfermidade. 
</p>

<script type="text/javascript"
    id="botcopy-embedder-d7lcfheammjct"
    class="botcopy-embedder-d7lcfheammjct" 
    data-botId="65552f94cf11360008493730"
>
    var s = document.createElement('script'); 
    s.type = 'text/javascript'; s.async = true; 
    s.src = 'https://widget.botcopy.com/js/injection.js'; 
    document.getElementById('botcopy-embedder-d7lcfheammjct').appendChild(s);
</script>
"""

# Incorporar o chatbot
components.html(chatbot_code, height=600)

# Mostrar o gráfico
st.plotly_chart(fig_sit)
