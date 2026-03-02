import streamlit as st
import pandas as pd
from databricks import sql

# --- 1. Configurações da Página ---
st.set_page_config(page_title="Canada Tech Hubs Weather", page_icon="🍁", layout="wide")

st.title("🍁 Monitoramento Climático - Polos Tech do Canadá")
st.markdown("Dashboard interativo alimentado em tempo real pela Camada Gold no Databricks.")

# --- 2. Suas Credenciais do Databricks ---
DATABRICKS_SERVER_HOSTNAME = "dbc-38fc862a-bf7b.cloud.databricks.com"
DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/a3efbc0f7c7f3d0c"

# --- 3. Conexão com o Banco de Dados ---
# DICA: Usamos o @st.cache_data para não ficar batendo no banco de dados 
# toda vez que o usuário clicar num botão. Isso economiza dinheiro da empresa!

@st.cache_data(ttl=600)

def puxar_dados_gold():
  try: 
# Abrindo a porta do Databricks
        connection = sql.connect(
            server_hostname="dbc-38fc862a-bf7b.cloud.databricks.com",
            http_path="/sql/1.0/warehouses/a3efbc0f7c7f3d0c",
            auth_path="databricks-oauth"
        )
        
        # O SQL puro brilhando no Python: pegando os dados da nossa tabela
        query = "SELECT * FROM default.gold_latest_weather"
        
        # O Pandas transforma o resultado do SQL direto em uma tabela visual
        df = pd.read_sql(query, connection)
        connection.close()
        return df
      
  except Exception as e:
        st.error(f"Erro ao conectar no Databricks: {e}")
        return pd.DataFrame()

# --- 4. Construindo a Interface ---
# Executa a função que criamos acima
df_gold = puxar_dados_gold()


# Se a tabela não estiver vazia, montamos os gráficos
if not df_gold.empty:
    st.subheader("📍 Panorama Atual")
    
    # Criamos colunas dinâmicas (uma para cada cidade)
    colunas = st.columns(len(df_gold))
    
    for index, row in df_gold.iterrows():
        with colunas[index]:
            st.metric(
                label=row['city_name'],
                value=f"{row['temperature_c']} °C",
                delta=row['weather_condition'] # Mostra se está chovendo, nublado, etc.
            )
            
    st.divider() # Linha de separação visual
    
    # Criamos duas colunas grandes para os gráficos
    grafico1, grafico2 = st.columns(2)
    
    with grafico1:
        st.subheader("📊 Comparativo de Temperatura (°C)")
        # Preparando os dados e gerando gráfico de barras
        dados_temp = df_gold.set_index('city_name')['temperature_c']
        st.bar_chart(dados_temp)
        
    with grafico2:
        st.subheader("💨 Velocidade do Vento (m/s)")
        dados_vento = df_gold.set_index('city_name')['wind_speed_m_s']
        st.bar_chart(dados_vento)

    st.divider()
    
    # Mostrando a tabela crua no final para auditoria
    st.subheader("Tabela de Dados Analíticos (Camada Gold)")
    st.dataframe(df_gold, use_container_width=True)
    
else:
    st.warning("Nenhum dado encontrado. Verifique se a Camada Gold foi gerada no Databricks!")