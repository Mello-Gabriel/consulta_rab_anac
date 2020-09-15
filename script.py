### Importando a biblioteca pandas e a associando à sigla pd.
import pandas as pd

# ### Extraindo tabelas com matrículas de aeronaves:
# - [Frota da Gol do Wikipédia](https://pt.wikipedia.org/wiki/Frota_de_aeronaves_da_Gol_Linhas_A%C3%A9reas_Inteligentes)

importacao=pd.read_html('https://pt.wikipedia.org/wiki/Frota_de_aeronaves_da_Gol_Linhas_A%C3%A9reas_Inteligentes')
# As tabelas são incoporadas a uma lista de DataFrames.

# ### Selecionando as tabelas que serão utilizadas.

importacao=importacao[2:5]
# Somente as tabelas 2, 3 e 4 serão utilizads.

# ### Unificando as tabelas e criando uma lista com os prefixos das aeronaves.

aeronaves=pd.concat(importacao, ignore_index=True)
#Agrupa todas as tabelas extraidas para o DataFrame aeronaves.
aeronaves=list(aeronaves['Prefixo'][0:140]) 
#Cria a lista com os prefixos válidos, para isso extrai a coluna 'Prefixo' e linhas 0 a 139.

# ### Realizando a consulta no RAB e salvando as informações em um dicionário.
# É realizado ajuste do index para que não existam nomes duplicados. Depois é realizada a transposição das tabelas de linhas para colunas.

rab={}
for aeronave in aeronaves:
    rab[aeronave]=pd.read_html(f'https://sistemas.anac.gov.br/aeronaves/cons_rab_resposta.asp?textMarca={aeronave}')[0]
    #O read_html retorna uma lista de dataframes, precisamos somente do primeiro, por isso selecionamos o item [0] da lista.
    rab[aeronave]=rab[aeronave].set_index(0)
    #Seleciona a primeira coluna como index.
    rab[aeronave].index = rab[aeronave].index.where(~rab[aeronave].index.duplicated(), rab[aeronave].index + '1')
    #Identifica valores de index repetidos e edita o segundo valor.
    rab[aeronave]=rab[aeronave].transpose()
    #Transpoe a tabela.

# ### Unificando as tabelas importadas e associando a chave do dicionário ao índex da tabela.

indice=list(rab.keys())
tabela=pd.concat(rab, keys=indice).droplevel(1)
tabela.to_excel('./output/consulta.xls') # Exportação para excel - para auxliar a vizualização dos dados e buscar por falhas.

# ### Apresentando a tabela criada.

print(tabela.head(5))

# Verificando características da tabela, como o tipo de dados em cada coluna.

tabela.info()

# Verificando o tipo de dados para cada linha da coluna 'Peso Máximo de Decolagem:'

tabela['Peso Máximo de Decolagem:'].apply(type)

# 

tabela['Peso Máximo de Decolagem:']=tabela['Peso Máximo de Decolagem:'].replace(['-','Kg'],'',regex=True).astype('float')
tabela['Peso Máximo de Decolagem:'].apply(type)

# 

tabela.info()

