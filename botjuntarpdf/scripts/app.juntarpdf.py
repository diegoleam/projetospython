import PyPDF2
import os
import time
import platform


def pode_excluir(arquivo):
    """Verifica se o arquivo pode ser excluído (se não estiver em uso)."""
    try:
        # Tenta abrir o arquivo no modo de escrita, se falhar, o arquivo está em uso
        with open(arquivo, 'a'):
            return True
    except IOError:
        return False


def abrir_pdf(pdf_path):
    """Abre o PDF gerado no visualizador de PDF padrão do sistema operacional."""
    sistema = platform.system()

    if sistema == "Windows":
        os.startfile(pdf_path)  # No Windows, abre o arquivo com o programa associado
    elif sistema == "Darwin":  # macOS
        os.system(f"open {pdf_path}")
    elif sistema == "Linux":
        os.system(f"xdg-open {pdf_path}")
    else:
        print(f"Não é possível abrir o PDF automaticamente no sistema {sistema}.")


# Criação do objeto de mesclagem
merger = PyPDF2.PdfMerger()

# Obtém o diretório onde o executável está localizado ou o diretório de trabalho atual
script_dir = os.path.dirname(os.path.abspath(__file__)) if hasattr(
    __builtins__, "__file__") else os.getcwd()

# Define os caminhos para as pastas "arquivos" e "pdfs_mesclados"
arquivos_dir = os.path.join(script_dir, "arquivos")
pdfs_mesclados_dir = os.path.join(script_dir, "pdfs_mesclados")

# Verifica se a pasta "arquivos" existe, caso contrário, cria
if not os.path.exists(arquivos_dir):
    print(f"A pasta 'arquivos' não foi encontrada. Criando a pasta {arquivos_dir}...")
    os.makedirs(arquivos_dir)

# Verifica se a pasta "pdfs_mesclados" existe, caso contrário, cria
if not os.path.exists(pdfs_mesclados_dir):
    print(f"A pasta 'pdfs_mesclados' não foi encontrada. Criando a pasta {pdfs_mesclados_dir}...")
    os.makedirs(pdfs_mesclados_dir)

# Lista os arquivos na pasta "arquivos"
lista_arquivos = os.listdir(arquivos_dir)
lista_arquivos.sort()

if not lista_arquivos:
    print("Não há arquivos PDF na pasta 'arquivos' para mesclar.")
else:
    # Confirmação antes de mesclar e excluir
    confirmacao = input(
        "Deseja mesclar os arquivos PDF na pasta 'arquivos' e excluí-los? (s/n): "
    )
    if confirmacao.lower() == "s":
        try:
            # Mescla os arquivos PDF
            for arquivo in lista_arquivos:
                if ".pdf" in arquivo:
                    merger.append(os.path.join(arquivos_dir, arquivo))

            # Salva o arquivo PDF final na pasta "pdfs_mesclados"
            output_pdf = os.path.join(pdfs_mesclados_dir, "PDF FINAL.pdf")
            merger.write(output_pdf)

            # Fechar o objeto PdfMerger para liberar os arquivos
            merger.close()

            print("PDF MESCLADO COM SUCESSO E SALVO EM:", output_pdf)

            # Abre o PDF gerado automaticamente
            abrir_pdf(output_pdf)

            # Exclui os arquivos PDF da pasta "arquivos"
            for arquivo in lista_arquivos:
                if ".pdf" in arquivo:
                    arquivo_completo = os.path.join(arquivos_dir, arquivo)

                    # Verifica se o arquivo pode ser excluído
                    while not pode_excluir(arquivo_completo):
                        print(f"O arquivo {arquivo} ainda está em uso. Tentando novamente...")
                        time.sleep(1)  # Aguarda um segundo antes de tentar novamente

                    # Exclui o arquivo
                    os.remove(arquivo_completo)
                    print(f"Arquivo {arquivo} excluído com sucesso.")

            print("Arquivos PDF originais excluídos.")

        except Exception as e:
            print(f"Ocorreu um erro durante a mesclagem ou exclusão: {e}")
    else:
        print("Operação cancelada.")
