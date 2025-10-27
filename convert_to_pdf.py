#!/usr/bin/env python3
"""
Script para convertir infografia_mlops.html a PDF usando Playwright
"""
from playwright.sync_api import sync_playwright
import os
import time

# Rutas de archivos
html_file = 'infografia_mlops.html'
pdf_file = 'infografia_mlops.pdf'

# Verificar que el archivo HTML existe
if not os.path.exists(html_file):
    print(f"Error: No se encuentra el archivo {html_file}")
    exit(1)

print(f"Convirtiendo {html_file} a PDF usando Playwright...")

# Obtener la ruta absoluta del archivo HTML
html_path = os.path.abspath(html_file)
file_url = f"file:///{html_path.replace(os.sep, '/')}"

print(f"URL del archivo: {file_url}")

with sync_playwright() as p:
    # Iniciar navegador
    browser = p.chromium.launch()
    page = browser.new_page()

    # Cargar el HTML
    page.goto(file_url)

    # Esperar a que la página cargue completamente
    page.wait_for_load_state("networkidle")
    time.sleep(2)  # Tiempo adicional para asegurar que todo esté renderizado

    # Obtener la altura total del contenido
    total_height = page.evaluate("document.body.scrollHeight")

    # Convertir a PDF con tamaño personalizado para una sola página continua
    page.pdf(
        path=pdf_file,
        width='210mm',  # Ancho A4
        height=f'{total_height}px',  # Altura dinámica basada en el contenido
        print_background=True,
        margin={
            'top': '0mm',
            'right': '0mm',
            'bottom': '0mm',
            'left': '0mm'
        },
        prefer_css_page_size=False,
        display_header_footer=False
    )

    browser.close()

print(f"[OK] PDF generado exitosamente: {pdf_file}")
print(f"  Tamano del archivo: {os.path.getsize(pdf_file) / 1024:.2f} KB")
