def parse_prediction(prediction):
    result = []

    for servicio in prediction['servicios']['item']:
        indexes = []
        for key in servicio.keys():
            if key.startswith('distanciabus'):
                index = key.replace('distanciabus', '')
                if index.isdigit():
                    indexes.append(int(index))
        
        indexes.sort()
        
        for i in indexes:
            distancia = servicio.get(f'distanciabus{i}')
            prediccion = servicio.get(f'horaprediccionbus{i}')
            result.append({
                'servicio': servicio['servicio'],
                'distancia': distancia,
                'prediccion': prediccion
            })
    return result


def parse_prediction_for_reply(parsed_prediction):
    formated = []
    for bus in parsed_prediction:
        distancia = f"{bus['distancia']}m" if bus["distancia"] else "💤"
        prediccion = f"({bus['prediccion']})" if bus["prediccion"]  else "💤"
        servicio = bus["servicio"]
        formated.append(f"🚍 {servicio} {distancia} {prediccion}")
    sep = [15*"➖"]
    return "\n".join(sep + formated + sep)
