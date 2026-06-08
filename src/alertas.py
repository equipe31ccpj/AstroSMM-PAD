def avaliar(dados):
    """Avalia os thresholds de segurança usando lógica condicional Python."""
    alertas = []
    
    if dados["temperatura_sensor_termico"] > 40.0:
        alertas.append({
            "parametro": "temperatura_sensor_termico",
            "status": "CRÍTICO",
            "mensagem": f"Superaquecimento detectado: {dados['temperatura_sensor_termico']}°C."
        })
        
    if dados["energia_bateria"] < 20.0:
        alertas.append({
            "parametro": "energia_bateria",
            "status": "CRÍTICO",
            "mensagem": f"Bateria em nível crítico de sobrevivência: {dados['energia_bateria']}%."
        })
        
    if dados["precisao_geolocalizacao"] > 10.0:
        alertas.append({
            "parametro": "precisao_geolocalizacao",
            "status": "ATENÇÃO",
            "mensagem": f"Desvio orbital suspeito. Margem de erro: {dados['precisao_geolocalizacao']}m."
        })
        
    return alertas