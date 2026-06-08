import random

def coletar():
    """Simula a leitura de parâmetros do satélite EnviroSat."""
    return {
        "temperatura_sensor_termico": round(random.uniform(15.0, 45.0), 2),  
        "energia_bateria": round(random.uniform(10.0, 100.0), 2),          
        "buffer_imagens": random.randint(0, 50),                             
        "precisao_geolocalizacao": round(random.uniform(0.5, 12.0), 2)       
    }