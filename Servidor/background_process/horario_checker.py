from datetime import datetime, timedelta
import threading, time
from models.models import Horario, Usuario
from routes.capturas.capturas_control import get_estado_sistema, set_capture_status

class HorarioChecker(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.daemon = True  # El hilo se cerrará cuando el programa principal termine
        self.running = True
        self.wakeup_event = threading.Event()  # Evento para despertar al hilo
        print("Hilo de comprobación de horarios iniciado")

    def run(self):
        time.sleep(5)  # Esperar a que la aplicación esté lista
        while self.running:
            with self.app.app_context():
                try:
                    self.comprobar_horarios()
                except Exception as e:
                    print(f"Error al comprobar horarios: {e}")
                
                # Calcular tiempo hasta la próxima comprobación
                self.esperar_siguiente()

    def comprobar_horarios(self):
        """Comprueba qué profesor debe estar activo según el horario actual"""
        estado = get_estado_sistema()
        
        if not estado['modo_automatico']:
            print("Modo automático desactivado")
            return

        ahora = datetime.now()
        dia_actual = ahora.weekday()
        hora_actual = ahora.time()
        
        print(f"Comprobando horarios: Día {dia_actual} (Lunes=0), Hora {hora_actual.strftime('%H:%M')}")

        # Buscar horario activo para el momento actual
        horario_activo = Horario.query.filter_by(dia=dia_actual).filter(
            Horario.hora_inicio <= hora_actual,
            Horario.hora_fin >= hora_actual
        ).first()

        if horario_activo:
            # Activar profesor según horario
            nuevo_profesor = horario_activo.id_usuario
            
            # Solo actualizar si hay cambio de profesor
            if nuevo_profesor != estado['user_id']:
                usuario = Usuario.query.get(nuevo_profesor)
                set_capture_status(True, nuevo_profesor)
                print(f"Activando capturas para {usuario.nombre}")
                print(f"Horario: {horario_activo.hora_inicio.strftime('%H:%M')} - {horario_activo.hora_fin.strftime('%H:%M')}")
            else:
                usuario = Usuario.query.get(estado['user_id'])
                print(f"Profesor {usuario.nombre if usuario else 'desconocido'} ya activo")
                
            # Verificar si estamos cerca del final del horario
            tiempo_restante = datetime.combine(ahora.date(), horario_activo.hora_fin) - ahora
            if tiempo_restante.total_seconds() < 60:  # Si falta menos de 1 minuto
                set_capture_status(False, None)
                print(f"Desactivando capturas por fin de horario de {usuario.nombre}")
        else:
            print("No se encontró horario activo para el momento actual")
            if estado['enabled']:
                set_capture_status(False, None)
                print("Desactivando capturas")

    def esperar_siguiente(self):
        """Calcula el tiempo hasta la próxima comprobación necesaria"""
        ahora = datetime.now()
        dia_actual = ahora.weekday()
        hora_actual = ahora.time()

        # Verificar si hay un horario activo actual
        horario_actual = Horario.query.filter_by(dia=dia_actual).filter(
            Horario.hora_inicio <= hora_actual,
            Horario.hora_fin >= hora_actual
        ).first()

        # Buscar próximo horario (hoy o en días siguientes)
        proximo_horario = None
        dias_busqueda = 7  # Buscar en la próxima semana
        
        for dias_offset in range(dias_busqueda):
            dia_busqueda = (dia_actual + dias_offset) % 7
            horarios_dia = Horario.query.filter_by(dia=dia_busqueda).order_by(Horario.hora_inicio).all()
            
            for horario in horarios_dia:
                if dias_offset == 0:  # Hoy
                    if horario.hora_inicio > hora_actual:
                        proximo_horario = horario
                        break
                else:  # Otros días
                    proximo_horario = horario
                    break
            
            if proximo_horario:
                break

        # Calcular tiempos de espera
        tiempo_espera = None

        if horario_actual:
            # Calcular tiempo hasta el final del horario actual
            fin_actual = datetime.combine(ahora.date(), horario_actual.hora_fin)
            tiempo_hasta_fin = (fin_actual - ahora).total_seconds()
            tiempo_espera = tiempo_hasta_fin

        if proximo_horario:
            # Calcular tiempo hasta el próximo horario
            dias_espera = (proximo_horario.dia - dia_actual) % 7
            proxima_fecha = datetime.combine(
                ahora.date() + timedelta(days=dias_espera),
                proximo_horario.hora_inicio
            )
            tiempo_hasta_siguiente = (proxima_fecha - ahora).total_seconds()
            
            # Usar el tiempo más corto entre fin actual y próximo inicio
            if tiempo_espera is None or tiempo_hasta_siguiente < tiempo_espera:
                tiempo_espera = tiempo_hasta_siguiente

        if tiempo_espera is not None:
            print(f"Próxima comprobación en {tiempo_espera/3600:.2f} horas")
            # Esperar hasta el tiempo calculado o hasta que nos despierten
            self.wakeup_event.wait(timeout=max(1, tiempo_espera))
            self.wakeup_event.clear()  # Resetear el evento
        else:
            # Si no hay horarios, esperar 1 hora
            print("No hay horarios futuros, esperando 1 hora")
            self.wakeup_event.wait(timeout=3600)
            self.wakeup_event.clear()  # Resetear el evento

    def stop(self):
        """Detiene el hilo de comprobación"""
        self.running = False

    def despertar(self):
        """Despierta al hilo para forzar una comprobación"""
        print("Despertando hilo de comprobación de horarios...")
        self.wakeup_event.set()