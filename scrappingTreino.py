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
    "id_despesas":[], 
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
            id_despesa = despesa.find_element(By.CLASS_NAME, "td_id_despesa").text
            data = despesa.find_element(By.CLASS_NAME, "td_data").text
            tipo = despesa.find_element(By.CLASS_NAME, "td_tipo").text
            setor = despesa.find_element(By.CLASS_NAME, "td_setor").text
            valor = despesa.find_element(By.CLASS_NAME, "td_valor").text
            fornecedor = despesa.find_element(By.CLASS_NAME, "td_fornecedor").text
            
            
            dic_despesas["id_despesas"].append(id_despesa)
            dic_despesas["data"].append(data)
            dic_despesas["tipo"].append(tipo)
            dic_despesas["setor"].append(setor )
            dic_despesas["valor"].append(valor)
            dic_despesas["fornecedor"].append(fornecedor)
           
            print(f"{id_despesa} - {data} - {tipo} - {setor} - {valor} - {fornecedor}")
        except Exception as e:
            print("Erro ao coletar dados", e)
            
        try:
            botao_orcamento = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, "//button[contains(text())='Orçamentos']"))
            )
            if botao_orcamento:
                driver.execute_script("arguments[0].click();", botao_orcamento)
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
            data = despesa.find_element(By.CLASS_NAME, "td_data").text
            tipo = despesa.find_element(By.CLASS_NAME, "td_tipo").text
            setor = despesa.find_element(By.CLASS_NAME, "td_setor").text
            valor = despesa.find_element(By.CLASS_NAME, "td_valor").text
            fornecedor = despesa.find_element(By.CLASS_NAME, "td_fornecedor").text
            
           
            print(f"{id_despesa} - {data} - {tipo} - {setor} - {valor} - {fornecedor}")
        except Exception as e:
            print("Erro ao coletar dados", e)
            
        
        
    



