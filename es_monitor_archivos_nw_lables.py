import os
import hashlib
from datetime import datetime
import time
from pathlib import Path

class MonitorArchivos:
    def __init__(self, archivo_salida="monitor_archivos_labels.txt", intervalo_minimo_actualizacion=2):
        """
        Inicializa el monitor de archivos.

        Argumentos:
            archivo_salida (str): Nombre del archivo donde se combinará el código.
            intervalo_minimo_actualizacion (int): Tiempo mínimo (en segundos) entre actualizaciones.
        """
        self.hash_archivos = {}
        self.archivo_salida = archivo_salida
        self.ultima_actualizacion = 0
        self.intervalo_minimo_actualizacion = intervalo_minimo_actualizacion
        self.archivos_existentes = set()  # Seguimiento de archivos existentes

    def calcular_hash_archivo(self, ruta_archivo):
        """Calcula el hash MD5 del contenido del archivo."""
        try:
            with open(ruta_archivo, 'rb') as archivo:
                contenido = archivo.read()
                hasher = hashlib.md5()
                hasher.update(contenido)
                return hasher.hexdigest()
        except Exception as e:
            print(f"Error al leer el archivo {ruta_archivo}: {str(e)}")
            return None

    def archivo_ha_cambiado(self, ruta_archivo):
        """Verifica si un archivo ha cambiado comparando su contenido."""
        # Verificar si el archivo existe
        existe_archivo = os.path.exists(ruta_archivo)
        if not existe_archivo:
            return False

        hash_actual = self.calcular_hash_archivo(ruta_archivo)
        if hash_actual is None:
            return False

        if ruta_archivo not in self.hash_archivos:
            self.hash_archivos[ruta_archivo] = hash_actual
            return True

        if self.hash_archivos[ruta_archivo] != hash_actual:
            self.hash_archivos[ruta_archivo] = hash_actual
            return True

        return False

    def actualizar_archivo_combinado(self, archivos):
        """
        Actualiza el archivo combinado si ha pasado suficiente tiempo desde la última actualización.
        """
        tiempo_actual = time.time()
        tiempo_desde_ultima_actualizacion = tiempo_actual - self.ultima_actualizacion

        # Si no ha pasado suficiente tiempo desde la última actualización, no hacer nada
        if tiempo_desde_ultima_actualizacion < self.intervalo_minimo_actualizacion:
            print(f"Esperando {self.intervalo_minimo_actualizacion - tiempo_desde_ultima_actualizacion:.1f} segundos antes de la próxima actualización...")
            return

        self.ultima_actualizacion = tiempo_actual
        print(f"\nActualizando archivo combinado... ({datetime.now().strftime('%H:%M:%S')})")

        # Incluir solo los archivos que existen actualmente
        archivos_existentes = [f for f in archivos if os.path.exists(f)]
        archivos_unicos = list(dict.fromkeys(archivos_existentes))

        with open(self.archivo_salida, 'w', encoding='utf-8') as salida:
            salida.write(f"// Última actualización: {datetime.now()}\n")
            salida.write(f"// Total de archivos: {len(archivos_unicos)}\n\n")

            for ruta_archivo in archivos_unicos:
                try:
                    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                        contenido = archivo.read()
                        salida.write(f"\n// Archivo: {ruta_archivo}\n")
                        salida.write("/" + "=" * 79 + "\n\n")
                        salida.write(contenido)
                        salida.write("\n\n")
                except Exception as e:
                    print(f"Error al leer el archivo {ruta_archivo}: {str(e)}")

    def monitorear_archivos(self, archivos, intervalo_revision=10):
        """
        Monitorea archivos para detectar cambios.

        Argumentos:
            archivos (list): Lista de archivos a monitorear.
            intervalo_revision (int): Tiempo en segundos entre cada revisión de archivos.
        """
        # Eliminar duplicados de la lista de archivos
        archivos_unicos = list(dict.fromkeys(archivos))
        print(f"Iniciando monitoreo de {len(archivos_unicos)} archivos únicos...")
        print(f"Configuración:")
        print(f"- Intervalo de revisión: {intervalo_revision} segundos")
        print(f"- Tiempo mínimo entre actualizaciones: {self.intervalo_minimo_actualizacion} segundos")
        print(f"- Archivo de salida: {self.archivo_salida}")
        print("-" * 50)

        # Verificación inicial de archivos
        for ruta_archivo in archivos_unicos:
            if os.path.exists(ruta_archivo):
                self.archivos_existentes.add(ruta_archivo)
                self.calcular_hash_archivo(ruta_archivo)

        # Primera lectura de todos los archivos
        for ruta_archivo in archivos_unicos:
            self.calcular_hash_archivo(ruta_archivo)

        while True:
            cambios_detectados = False
            archivos_cambiados = []

            for ruta_archivo in archivos_unicos:
                if self.archivo_ha_cambiado(ruta_archivo):
                    print(f"Cambio detectado en: {os.path.basename(ruta_archivo)}")
                    cambios_detectados = True
                    if os.path.exists(ruta_archivo):
                        archivos_cambiados.append(ruta_archivo)

            if cambios_detectados:
                self.actualizar_archivo_combinado(archivos_unicos)
                print(f"Archivo combinado actualizado: {self.archivo_salida}")
                print(f"Conteo actual de archivos: {len(self.archivos_existentes)}")
                print("-" * 50)

            time.sleep(intervalo_revision)

# Lista completa de archivos a monitorear
archivos_a_monitorear = [
r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\audit\AuditAwareImpl.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\client\WebClientApiZpl.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\CorsConfig.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\CorsLoggingFilter.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\CurrentUser.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\JacksonConfig.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\SwaggerConfig.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\UserConfig.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\config\UserInterceptor.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\constants\RequestConstants.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\controller\RequestLabelsController.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\controller\RequestPrintController.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\response\ErrorResponseDto.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\ImagesDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\LabelsDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\PrintsDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\response\ResponseDto.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\dto\UserDTO.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\BaseEntity.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Images.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Labels.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Prints.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\entity\Templates.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\AuthorizationTokenException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\GlobalExceptionHandler.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\IntegrationZplException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\PrintException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\exception\ResourceNotFoundException.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\mapper\LabelsMapper.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\ImagesRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\LabelsRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\PrintsRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\repository\TemplatesRepository.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\Impl\PrintService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\Impl\RequestLabelsServiceImpl.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\Impl\UtilityService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\IPrintService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\IRequestLabelsService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\service\IUtilityService.java",
    r"C:\ProyectsSoftware\NIRSA\nw.servicio.solicitud\src\main\java\com\nirsa\solicitud\AccountsApplication.java"
]

if __name__ == "__main__":
    # Configuración personalizable
    INTERVALO_REVISION = 30  # Segundos entre cada revisión de archivos
    INTERVALO_MINIMO_ACTUALIZACION = 10  # Segundos mínimos entre actualizaciones del archivo combinado

    monitor = MonitorArchivos(intervalo_minimo_actualizacion=INTERVALO_MINIMO_ACTUALIZACION)
    try:
        monitor.monitorear_archivos(archivos_a_monitorear, intervalo_revision=INTERVALO_REVISION)
    except KeyboardInterrupt:
        print("\nMonitoreo finalizado.")
