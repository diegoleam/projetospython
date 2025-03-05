import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# caminho da planilha

planilha = pd.read_excel("../planilhas/suap-login.xlsx")

# pesquisa os dados da planilha

for index, row in planilha.iterrows():
    usuario = row["Usuario"]
    senha = row["Senha"]


# abri o navegador
navegador = webdriver.Chrome()

# Abrir o site
navegador.get('https://suap.ifpb.edu.br/accounts/login/')

# Espera o campo usuário carregar
WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, 'id_username')))

# Preenche usuário e senha
navegador.find_element(By.ID, 'id_username').send_keys(usuario)
navegador.find_element(By.ID, 'id_password').send_keys(senha)

# Espera o botão e clica nele
botao = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[1]/form/div[4]/input')))
botao.click()

# Manter o navegador aberto até o usuário pressionar Enter
input("Pressione Enter para sair...")
