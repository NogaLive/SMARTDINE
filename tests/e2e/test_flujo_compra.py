# tests/e2e/test_flujo_compra.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_realizar_pedido_web():
    # Configuración del navegador
    driver = webdriver.Chrome()
    driver.get("http://localhost:5173") # URL del Frontend React
    
    try:
        # 1. Agregar producto al carrito
        btn_agregar = driver.find_element(By.XPATH, "//button[contains(text(),'Agregar')]")
        btn_agregar.click()
        
        # 2. Verificar actualización del carrito
        total_text = driver.find_element(By.CLASS_NAME, "total").text
        assert "$15.5" in total_text
        
        # 3. Confirmar pedido
        driver.find_element(By.CLASS_NAME, "btn-pagar").click()
        
        # 4. Validar mensaje de éxito
        alerta = driver.find_element(By.CLASS_NAME, "alert")
        assert "¡Pedido enviado a cocina!" in alerta.text
        
    finally:
        driver.quit()