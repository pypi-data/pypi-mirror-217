from datetime import datetime

def formato_fecha(datetime_str,formato="%d/%m/%Y"):
    """
    Cambia el formato de un string dado a un formato dado y si no se da el formato requerido 
    lo cambia por defecto al formato: 
                formato="%d/%m/%Y"
    Args:
        - datetime_str (string): Un string de la fecha.
        - formato="%d/%m/%Y" (string): Un formato de la fecha

    Returns:
        string: La fecha en el formato requerido Ej: "20/06/2023"

    except:
        string: La fecha no es valida
    """
    try:
        date_time = datetime.strptime(datetime_str, '%Y-%m-%d')# convierto el estring en class datatime.datatime
        date_format = date_time.strftime(formato)# cambio el formato de la fecha
        return date_format
    except ValueError:
        return "La fecha no es valida"
