# Modulo para controlar o navegador web
from selenium import webdriver

# localizador de elementos
from selenium.webdriver.common.by import By

# serviço para configurar o caminho de executavel chromedriver
from selenium.webdriver.chrome.service import Service

# classe que permite executar ações avanças(o mover do mouse, clique/arrastar)
from selenium.webdriver.common.action_chains import ActionChains

# classe que espera de forma explicita até que uma condição seja satisfeita
from selenium.webdriver.support.ui import WebDriverWait

# condições esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import pandas as pd

import time

# uso de tratamento de exceção
from selenium.common.exceptions import TimeoutException


chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"

service = Service(chrome_driver_path) 
options = webdriver.ChromeOptions() 
options.add_argument("--disable-gpu") 
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=service, options=options)

url_base = "https://masander.github.io/AlimenticiaLTDA-financeiro/"
driver.get(url_base)
time.sleep(5) 

dic_despesas = {
    "data":[],
    "tipo":[],
    "setor":[],
    "valor":[],
    "fornecedor":[],
    }

dic_orcamento = {
    "setor":[], 
    "mes":[],
    "ano":[],
    "valor_previsto":[],
    "valor_realizado":[],
    }


while True:
    try:
        WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located((By.XPATH, "//tr[contains(@style, \"border-bottom: 1px solid rgb(221, 221, 221)\")]")))
    except TimeoutException:
        print("Tempo de espera excedido!")
        
    despesas = driver.find_elements(By.XPATH, "//tr[contains(@style, \"border-bottom: 1px solid rgb(221, 221, 221)\")]")
    
    for despesa in despesas:
        try:
            data = despesa.find_element(By.CLASS_NAME, "td_data").text.strip()
            tipo = despesa.find_element(By.CLASS_NAME, "td_tipo").text.strip()
            setor = despesa.find_element(By.CLASS_NAME, "td_setor").text.strip()
            valor = despesa.find_element(By.CLASS_NAME, "td_valor").text.strip()
            fornecedor = despesa.find_element(By.CLASS_NAME, "td_fornecedor").text.strip()
            
                 
            dic_despesas["data"].append(data)
            dic_despesas["tipo"].append(tipo)
            dic_despesas["setor"].append(setor )
            dic_despesas["valor"].append(valor)
            dic_despesas["fornecedor"].append(fornecedor)
           
            print(f"{data} - {tipo} - {setor} - {valor} - {fornecedor}")
        except Exception as e:
            print("Erro ao coletar dados", e)
            
    try:
        botao_orcamento = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Orçamentos')]")))
        if botao_orcamento:
            driver.execute_script("arguments[0].click();", botao_orcamento)
            print("clicadp")
            time.sleep(5)
    except Exception:
            print("Error")
            
        
    try:
        WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located((By.XPATH, "//tr[contains(@style, \"border-bottom: 1px solid rgb(221, 221, 221)\")]")))
    except TimeoutException:
        print("Tempo de espera excedido!")
        
    orcamentos = driver.find_elements(By.XPATH, "//tr[contains(@style, \"border-bottom: 1px solid rgb(221, 221, 221)\")]")
    
    for orcamento in orcamentos:
        try:
            setor = orcamento.find_element(By.CLASS_NAME, "td_setor").text.strip()
            mes = orcamento.find_element(By.CLASS_NAME, "td_mes").text.strip()
            ano = orcamento.find_element(By.CLASS_NAME, "td_ano").text.strip()
            valor_previsto = orcamento.find_element(By.CLASS_NAME, "td_valor_previsto").text.strip()
            valor_realizado = orcamento.find_element(By.CLASS_NAME, "td_valor_realizado").text.strip()
            
            dic_orcamento["setor"].append(setor)
            dic_orcamento["mes"].append(mes)
            dic_orcamento["ano"].append(ano)
            dic_orcamento["valor_previsto"].append(valor_previsto)
            dic_orcamento["valor_realizado"].append(valor_realizado)
            
           
            print(f"{setor} - {mes} - {ano} - {valor_previsto} - {valor_realizado}")
        except Exception as e:
            print("Erro ao coletar dados", e)
    break

driver.quit()

df_despesas = pd.DataFrame(dic_despesas)
print(f"Arquivo 'Despesas' salvo com sucesso {len(df_despesas)} amazenados")
df_despesas.to_excel("Despesas.xlsx", index=False)

df_orcamento = pd.DataFrame(dic_orcamento)
print(f"Arquivo 'orcamento' salvo com sucesso {len(df_orcamento)} amazenados")
df_orcamento.to_excel("Orcamento.xlsx", index=False)

            
        
        
    



