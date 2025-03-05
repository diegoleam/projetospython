import pandas as pd
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --------------------------------------------
# 1. CONFIGURAÇÃO DO LOG PARA REGISTRAR ERROS E SUCESSOS
# --------------------------------------------

# Define o diretório onde os logs serão armazenados
log_dir = "../logs"
os.makedirs(log_dir, exist_ok=True)  # Cria a pasta "logs" caso ela não exista

# Define o caminho do arquivo de log
log_file = os.path.join(log_dir, "suap_login.log")

# Configura o sistema de logging (registro de logs)
logging.basicConfig(
    filename=log_file,  # Arquivo onde os logs serão armazenados
    level=logging.INFO,  # Nível de log (INFO para registrar sucessos e erros)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato das mensagens de log
    datefmt="%d-%m-%Y %H:%M" # Adicionando o formato da data e hora
)

# --------------------------------------------
# 2. VERIFICAR SE A PLANILHA EXISTE E CARREGAR DADOS
# --------------------------------------------

# Caminho onde a planilha está armazenada
planilha_path = "../planilhas/suap-login.xlsx"

# Verifica se o arquivo da planilha existe antes de tentar abri-lo
if not os.path.exists(planilha_path):
    logging.error("ERRO: Planilha não encontrada no caminho: %s", planilha_path)
    print("ERRO: Planilha não encontrada. Verifique o caminho e tente novamente.")
else:
    try:
        # Carrega os dados da planilha para um DataFrame do pandas
        planilha = pd.read_excel(planilha_path)

        # Verifica se a planilha está vazia
        if planilha.empty:
            logging.error("ERRO: A planilha está vazia.")
            print("ERRO: A planilha está vazia. Adicione dados e tente novamente.")
        else:
            # Captura apenas o primeiro usuário da planilha (se houver vários, apenas o primeiro será utilizado)

            usuario = str(planilha.loc[0, "Usuario"])
            senha = str(planilha.loc[0, "Senha"])

            # --------------------------------------------
            # 3. INICIAR O NAVEGADOR E REALIZAR O LOGIN
            # --------------------------------------------

            # Abre o navegador Chrome
            navegador = webdriver.Chrome()

            # Acessa a página de login do SUAP
            navegador.get('https://suap.ifpb.edu.br/accounts/login/')

            # Aguarda até que o campo de usuário esteja disponível na página
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, 'id_username')))

            # Preenche o campo de usuário com o valor obtido na planilha
            navegador.find_element(By.ID, 'id_username').send_keys(usuario)

            # Preenche o campo de senha com o valor obtido na planilha
            navegador.find_element(By.ID, 'id_password').send_keys(senha)

            # Aguarda até que o botão de login esteja disponível e clica nele
            botao = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[1]/form/div[4]/input')))
            botao.click()

            # Registra o sucesso do login nos logs
            logging.info("Login bem-sucedido para o usuário: %s", usuario)
            print("Login realizado com sucesso!")

            # --------------------------------------------
            # 4. MANTER O NAVEGADOR ABERTO ATÉ QUE O USUÁRIO PRESSIONE ENTER
            # --------------------------------------------

            input("Pressione Enter para sair...")

    except Exception as e:
        # Caso ocorra algum erro durante a execução, ele será registrado no log e exibido ao usuário
        logging.error("ERRO durante a execução: %s", str(e))
        print(f"ERRO: Ocorreu um erro durante a execução. Veja o log em {log_file} para mais detalhes.")
