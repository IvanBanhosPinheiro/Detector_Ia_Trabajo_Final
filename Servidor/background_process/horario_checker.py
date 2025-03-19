"""
Calcula el tiempo hasta la próxima comprobación necesaria de horarios.

Determina cuándo debe ocurrir la próxima comprobación de horarios basándose en:
1. El fin del horario activo actual (si existe)
2. El inicio del próximo horario programado

Utiliza un mecanismo de espera inteligente que:
- Selecciona el tiempo más corto entre los eventos relevantes
- Permite ser despertado manualmente cuando hay cambios en la configuración
- Establece un tiempo predeterminado si no hay horarios programados

Returns:
    None: La función no retorna valores, pero hace que el hilo
            espere hasta el próximo tiempo relevante

Side Effects:
    - Pone al hilo en estado de espera hasta el tiempo calculado
    - Imprime información de depuración sobre la próxima comprobación

Note:
    La función asume que los horarios no se superponen en un mismo día
"""
from datetime import datetime, timedelta
import threading, time
from models.models import Horario, Usuario
from routes.capturas.capturas_control import get_estado_sistema, set_capture_status

class HorarioChecker(threading.Thread):
    """
    Hilo de verificación de horarios para el modo automático.
    
    Esta clase implementa un hilo que verifica periódicamente los horarios
    configurados y activa/desactiva las capturas en consecuencia.
    
    Hereda de threading.Thread y se ejecuta como un daemon, terminando
    automáticamente cuando el programa principal finaliza.
    
    Attributes:
        app: Instancia de la aplicación Flask
        running (bool): Indica si el hilo debe continuar ejecutándose
        wakeup_event (Event): Evento para controlar el ciclo de espera
        
    Note:
        El hilo utiliza el contexto de aplicación Flask para acceder 
        a la base de datos y otras funciones de la aplicación.
    """
    def __init__(self, app):
        """
        Inicializa el hilo de verificación de horarios.
        
        Args:
            app: Instancia de la aplicación Flask
            
        Note:
            El hilo se configura como daemon para que termine
            automáticamente cuando finaliza el programa principal.
        """
        super().__init__()
        self.app = app
        self.daemon = True  # El hilo se cerrará cuando el programa principal termine
        self.running = True
        self.wakeup_event = threading.Event()  # Evento para despertar al hilo
        print("Hilo de comprobación de horarios iniciado")

    def run(self):
        """
        Punto de entrada principal del hilo.
        
        Implementa el bucle principal que verifica horarios periódicamente.
        Espera 5 segundos iniciales para permitir que la aplicación se inicialice
        completamente, y luego alterna entre verificar horarios y calcular 
        el tiempo de espera hasta la próxima verificación necesaria.
        
        Side Effects:
            - Modifica el estado del sistema de capturas
            - Imprime información de depuración
            
        Note:
            Captura excepciones para evitar que el hilo termine inesperadamente
        """
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
        """
        Comprueba qué profesor debe estar activo según el horario actual.
        
        Verifica si el momento actual coincide con algún horario programado.
        Si encuentra un horario activo, activa las capturas para el profesor
        correspondiente. Si no, desactiva las capturas.
        
        Process:
            1. Verifica si el modo automático está activado
            2. Obtiene el día y hora actual
            3. Busca un horario que coincida con el momento actual
            4. Activa/desactiva las capturas según corresponda
            
        Side Effects:
            - Llama a set_capture_status() para modificar el estado del sistema
            - Imprime información de depuración
            
        Note:
            Solo tiene efecto si el sistema está en modo automático
        """
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
        """
        Calcula el tiempo hasta la próxima comprobación necesaria de horarios.
        
        Determina cuándo debe ocurrir la próxima comprobación de horarios basándose en:
        1. El fin del horario activo actual (si existe)
        2. El inicio del próximo horario programado
        
        Utiliza un mecanismo de espera inteligente que:
        - Selecciona el tiempo más corto entre los eventos relevantes
        - Permite ser despertado manualmente cuando hay cambios en la configuración
        - Establece un tiempo predeterminado si no hay horarios programados
        
        Returns:
            None: La función no retorna valores, pero hace que el hilo
                espere hasta el próximo tiempo relevante
        
        Side Effects:
            - Pone al hilo en estado de espera hasta el tiempo calculado
            - Imprime información de depuración sobre la próxima comprobación
        
        Note:
            La función asume que los horarios no se superponen en un mismo día
        """
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
        """
        Detiene el hilo de comprobación.
        
        Establece la bandera 'running' a False, lo que hará que el bucle
        principal termine en su próxima iteración.
        
        Note:
            No termina inmediatamente el hilo, sino que permite que
            termine de forma controlada en su próxima iteración
        """
        self.running = False

    def despertar(self):
        """
        Despierta al hilo para forzar una comprobación inmediata.
        
        Activa el evento de despertar, lo que interrumpe cualquier espera
        en curso y fuerza al hilo a realizar una comprobación de horarios.
        
        Side Effects:
            - Activa self.wakeup_event
            - Imprime mensaje de depuración
            
        Note:
            Útil cuando se cambia la configuración de horarios o
            se alterna manualmente entre modo automático y manual
        """
        print("Despertando hilo de comprobación de horarios...")
        self.wakeup_event.set()