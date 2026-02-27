import json
from datetime import datetime, timedelta
from src.conexion_db import ConexionDB

class AuthDAO:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_usuario(self, username, passphrase):
        conn = self.db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios_voz (username, passphrase_text) VALUES (%s, %s) RETURNING id",
                (username, passphrase)
            )
            user_id = cursor.fetchone()[0]
            
            log_exito = {"status": "OK", "confianza": 0.98, "latencia": "1.2s"}
            cursor.execute(
                "INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)",
                (user_id, json.dumps(log_exito))
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            cursor.close()

    def obtener_usuario(self, username):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, passphrase_text, intentos_fallidos, bloqueado_hasta FROM usuarios_voz WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def registrar_intento_fallido(self, user_id, frase_intentada, intentos_actuales):
        conn = self.db.conectar()
        cursor = conn.cursor()
        nuevos_intentos = intentos_actuales + 1
        restantes = max(0, 3 - nuevos_intentos)
        
        bloqueo_query = ""
        if restantes == 0:
            bloqueado_hasta = datetime.now() + timedelta(minutes=15)
            cursor.execute("UPDATE usuarios_voz SET intentos_fallidos = %s, bloqueado_hasta = %s WHERE id = %s", (nuevos_intentos, bloqueado_hasta, user_id))
        else:
            cursor.execute("UPDATE usuarios_voz SET intentos_fallidos = %s WHERE id = %s", (nuevos_intentos, user_id))

        log_fallo = {"status": "FAIL", "frase_intentada": frase_intentada, "intentos_restantes": restantes} 
        cursor.execute("INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)", (user_id, json.dumps(log_fallo)))
        
        conn.commit()
        cursor.close()
        return restantes

    def registrar_acceso_exitoso(self, user_id, confianza, latencia):
        conn = self.db.conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios_voz SET intentos_fallidos = 0, bloqueado_hasta = NULL WHERE id = %s", (user_id,))
        
        log_exito = {"status": "OK", "confianza": confianza, "latencia": latencia}
        cursor.execute("INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)", (user_id, json.dumps(log_exito)))
        
        conn.commit()
        cursor.close()

    def registrar_error_tecnico(self, username, motivo):
        user = self.obtener_usuario(username)
        if user:
            conn = self.db.conectar()
            cursor = conn.cursor()
            log_error = {"status": "ERROR", "motivo": motivo, "hardware_db": 85} 
            cursor.execute("INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)", (user[0], json.dumps(log_error)))
            conn.commit()
            cursor.close()

    def obtener_auditoria_critica(self):
        conn = self.db.conectar()
        cursor = conn.cursor()
        query = """
        SELECT u.username, l.resultado_json->>'status' 
        FROM log_accesos_voz l 
        JOIN usuarios_voz u ON l.usuario_id = u.id 
        WHERE l.resultado_json->>'status' = 'FAIL' 
        OR (l.resultado_json->>'confianza')::float < 0.6;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados