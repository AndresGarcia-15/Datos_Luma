import requests
import json
import sqlite3
import time
from datetime import datetime, timedelta

def obtener_ultima_fecha_db(db_file):
    """Obtiene la fecha más reciente de la tabla sunspot en la base de datos."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
       
        query = "SELECT MAX(date) FROM sunspot"
        cursor.execute(query)
        ultima_fecha = cursor.fetchone()[0]
        
        if not ultima_fecha:
            print("No se encontraron registros en la tabla sunspot.")
            
        
        print(f"Última fecha en la base de datos: {ultima_fecha}")
        
        
        if ' ' in ultima_fecha:
            ultima_fecha = ultima_fecha.split(' ')[0]
            
        
        fecha_dt = datetime.strptime(ultima_fecha, '%Y-%m-%d')
        fecha_siguiente = fecha_dt + timedelta(days=1)
        
        return fecha_siguiente.strftime('%Y-%m-%d')
    
    except sqlite3.Error as e:
        print(f"Error de SQLite: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def actualizar_datos_sunspot(db_file, max_llamadas=10):
    """Actualiza la tabla sunspot con datos desde la última fecha hasta hoy."""
   
    fecha_inicio = obtener_ultima_fecha_db(db_file)
    if not fecha_inicio:
        print("No se pudo determinar la fecha de inicio. Abortando.")
        return
    
    
    fecha_final = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Consultando datos desde {fecha_inicio} hasta {fecha_final}")
    
    
    base_url = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/daily-sunspot-number@datastro/records"
    
    
    limite_por_pagina = 100
    offset = 0
    todos_registros = []
    llamadas_realizadas = 0
    
    
    while llamadas_realizadas < max_llamadas:
        
        params = {
            'where': f"year_month_day >= '{fecha_inicio}' AND year_month_day <= '{fecha_final}'",
            'order_by': "year_month_day ASC",
            'limit': limite_por_pagina,
            'offset': offset
        }
        
        llamadas_realizadas += 1
        print(f"Realizando llamada {llamadas_realizadas}/{max_llamadas} (offset: {offset})")
        
        try:
           
            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                
                if llamadas_realizadas == 1:
                    with open('sunspot_data_response.json', 'w') as json_file:
                        json.dump(data, json_file, indent=4)
                
                
                if 'results' in data and data['results']:
                    nuevos_registros = data['results']
                    num_registros = len(nuevos_registros)
                    print(f"Se encontraron {num_registros} registros en esta página.")
                    
                    
                    todos_registros.extend(nuevos_registros)
                    
                    
                    if num_registros < limite_por_pagina:
                        print("No hay más datos disponibles.")
                        break
                    
                    
                    offset += limite_por_pagina
                    
                    
                    time.sleep(1)
                else:
                    print("No se encontraron registros en esta página.")
                    break
            else:
                print(f"Error en la consulta a la API: {response.status_code}")
                print(f"Respuesta: {response.text}")
                break
        
        except Exception as e:
            print(f"Error al procesar la solicitud: {e}")
            break
    
    
    if todos_registros:
        print(f"Total de registros encontrados: {len(todos_registros)}")
        insertar_en_db(db_file, todos_registros)
    else:
        print("No se encontraron nuevos datos para actualizar.")

def insertar_en_db(db_file, registros):
    """Inserta los nuevos registros en la tabla sunspot usando el mapeo correcto de columnas."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        
        if registros:
            print("Ejemplo de registro recibido:")
            print(registros[0])
        
       
        insert_query = """
        INSERT INTO sunspot (date, year, month, day, fractional_year, sunspot_number, std_dev, observations, definitive_indicator)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        
        data_tuples = []
        
        for registro in registros:
           
            fecha_str = registro['year_month_day']
            year = int(registro['column_1'])
            month = int(registro['column_2'])
            day = int(registro['column_3'])
            fractional_year = float(registro['column_4'])
            sunspot_number = int(float(registro['column_5'])) if registro['column_5'] is not None else 0
            std_dev = float(registro['column_6']) if registro['column_6'] is not None else 0
            observations = int(registro['column_7']) if registro['column_7'] is not None else 0
            definitive_indicator = int(registro['column_8']) if registro['column_8'] is not None else 0
            
            data_tuples.append((
                fecha_str,             
                year,                  
                month,                 
                day,                   
                fractional_year,      
                sunspot_number,        
                std_dev,               
                observations,         
                definitive_indicator   
            ))
            
            
            if len(data_tuples) == 1:
                print("Primer registro a insertar en DB:")
                print(data_tuples[0])
        
        
        cursor.executemany(insert_query, data_tuples)
        conn.commit()
        print(f"Se han insertado {len(data_tuples)} nuevos registros en la base de datos.")
        
    except sqlite3.Error as e:
        print(f"Error de SQLite al insertar datos: {e}")
    
    except Exception as e:
        print(f"Error al insertar datos: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    
    db_file = './DATA.db'
    actualizar_datos_sunspot(db_file, max_llamadas=10)