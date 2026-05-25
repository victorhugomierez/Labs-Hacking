import os
import shutil

# Definimos el mapa de la arquitectura que creaste
DIRECTORIOS_MATRIZ = {
    "01-academic-unq": ["Algebra", "Resiliencia-operativa-CID", "Network-Fundamentals"],
    "02-automation-scripting": ["Custom Tooling Using Python", "Custom-Tooling-using-Burp", "transcribe_audio", "dollar-price", "Learn-Python"],
    "03-offensive-security": [
        "Attacking-ECB-Oracles", "Padding-Oracles", "CORS-SOP", "CSRF", "XSS", "WEBSOCKET", 
        "HTTP-REQUEST-SMUGGLING", "HTTP-2REQUEST-SMUGGLING", "HTTP-BROWSER-DESYNC", 
        "Inclusion-path-travelsal", "Insecure-Randomness", "Breaking Crypto the Simple Way", 
        "CVE-2022-26923", "Chaining Vulnerabilities", "Length-Extension-Attacks",
        "Multi-Stage-Web-Attack-XSS-to-Adm..."
    ],
    "04-ctf-wargames": ["BANDITO"],
    "05-environments-research": ["kali-Linux", "Learn-Linux", "security-research", "CI-SO-TECH"]
}

def organizar_laboratorio():
    ruta_raiz = os.getcwd()
    print(f"[*] Analizando directorio raíz: {ruta_raiz}\n")
    
    # Recorremos el mapa para verificar y mover lo que encuentre suelto
    for carpeta_destino, subcarpetas in DIRECTORIOS_MATRIZ.items():
        # Si por alguna razón borraste la carpeta principal, el script la recrea
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
            print(f"[+] Contenedor creado: {carpeta_destino}")
            
        for subcarpeta in subcarpetas:
            ruta_origen = os.path.join(ruta_raiz, subcarpeta)
            ruta_final = os.path.join(ruta_raiz, carpeta_destino, subcarpeta)
            
            # Si la carpeta está suelta en la raíz, se mueve
            if os.path.exists(ruta_origen) and os.path.isdir(ruta_origen):
                try:
                    shutil.move(ruta_origen, ruta_final)
                    print(f"[→] Movido con éxito: {subcarpeta} ──> {carpeta_destino}/")
                except Exception as e:
                    print(f"[❌] Error al mover {subcarpeta}: {e}")

    print("\n[+] Estructura normalizada y limpia.")

if __name__ == "__main__":
    organizar_laboratorio()