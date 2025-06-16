# IPS - Procesador de Facturas

Aplicación para la gestión y procesamiento de facturas y soportes para regímenes subsidiado y contributivo.

## Estructura del Proyecto

```
APP_IPS/
├── app_ips.py                    # Archivo principal de la aplicación
├── app_ips_restore_point_1.py    # Punto de restauración (versión estable)
├── app_ips_restore_point_2.py    # Punto de restauración (verificación de facturas)
├── app_ips_restore_point_1.2.py   # Punto de restauración (verificación de facturas)
├── app_ips_restore_point_1.3.py   # Punto de restauración (corrección de números de contrato)
├── app_ips_restore_point_1.3.1.py # Punto de restauración (corrección de números de contrato)
├── app_ips_restore_point_1.3.2.py # Punto de restauración (corrección de números de contrato)
├── app_ips_restore_point_1.4.py   # Punto de restauración (empaquetado de soportes)
├── app_ips_restore_point_1.5.py   # Punto de restauración (empaquetado de facturas)
├── config.json                   # Archivo de configuración
├── SUBSIDIADO/                   # Directorio para régimen subsidiado
│   ├── FACTURAS/                # Facturas del régimen subsidiado
│   ├── SOPORTES/                # Soportes del régimen subsidiado
│   └── EMPAQUETADO/             # Archivos empaquetados del régimen subsidiado
└── CONTRIBUTIVO/                 # Directorio para régimen contributivo
    ├── FACTURAS/                # Facturas del régimen contributivo
    ├── SOPORTES/                # Soportes del régimen contributivo
    └── EMPAQUETADO/             # Archivos empaquetados del régimen contributivo
```

## Características Implementadas

### Versión Actual (Restore Point 1)
- **Configuración Inicial**
  - Ventana de configuración con campos para NIT, número de contrato y prefijo
  - Persistencia de configuración en archivo JSON
  - Validación de campos

- **Estructura de Directorios**
  - Creación automática de estructura de carpetas al inicio
  - Organización por régimen (Subsidiado y Contributivo)
  - Subdirectorios para Facturas, Soportes y Empaquetado
  - Visualización de estructura en ventana dedicada

- **Interfaz de Usuario**
  - Menú principal con opciones para cada régimen
  - Visualización de configuración actual
  - Consola integrada para mensajes del sistema
  - Diseño responsivo y centrado
  - Estilos personalizados para botones y elementos

## Requisitos

- Python 3.x
- tkinter (incluido en la instalación estándar de Python)
- Sistema operativo: Windows 10 o superior

## Instalación

1. Clonar o descargar el repositorio
2. Asegurarse de tener Python 3.x instalado
3. No se requieren dependencias adicionales

## Uso

1. Ejecutar el archivo principal:
   ```bash
   python app_ips.py
   ```

2. En la primera ejecución:
   - Se creará la estructura de directorios
   - Se mostrará la ventana de configuración inicial
   - Ingresar los datos requeridos (NIT, contrato, prefijo)

3. Funcionalidades disponibles:
   - Acceso a menús de régimen subsidiado y contributivo
   - Visualización de estructura de carpetas
   - Modificación de configuración
   - Consola integrada para mensajes del sistema

## Puntos de Restauración

### Restore Point 1.0
- Versión estable con estructura de carpetas
- Interfaz de usuario completa
- Sistema de configuración funcional
- Visualización de estructura de directorios

### Restore Point 1.1
- Todas las características del punto 1.0
- Mejoras en la interfaz de usuario
- Botones organizados en dos columnas
- Consola mejorada

### Restore Point 1.2
- Todas las características del punto 1.1
- Corrección del botón de verificación de facturas
- Implementación completa de la verificación de facturas
- Interfaz de tabla para resultados de verificación

### Restore Point 1.3
- Todas las características del punto 1.2
- Funcionalidad de corrección de números de contrato
  - Botón para corregir contratos en la ventana de resultados
  - Corrección automática de números de contrato en archivos XML
  - Actualización en tiempo real de la tabla de resultados
  - Resumen de correcciones realizadas
  - Registro de progreso en la consola

### Restore Point 1.3.1
- Todas las características del punto 1.3
- Mejoras en la gestión de rutas para el ejecutable
  - Soporte para ejecución como .exe y como script
  - Creación de carpetas en la ubicación correcta del ejecutable
  - Manejo mejorado de rutas absolutas y relativas

### Restore Point 1.3.2
- Todas las características del punto 1.3.1
- Mejoras en la corrección de números de contrato
- Mejor detección de casos que necesitan corrección
- Actualización correcta del estado en la interfaz
- Mejor manejo de mensajes y estados

### Restore Point 1.4
- Todas las características del punto 1.3.2
- Implementación de verificación de soportes
  - Verificación de archivos CRC, HEV, FEV y PDE
  - Agrupación por número de factura
  - Interfaz de tabla para resultados
- Implementación de empaquetado de soportes
  - Paquetes limitados a 50MB
  - Agrupación por facturas completas
  - Generación de manifiestos por paquete
  - Interfaz de progreso durante el empaquetado
  - Nombrado secuencial de paquetes

### Restore Point 1.5
- Todas las características del punto 1.4
- Implementación de empaquetado de facturas
  - Empaquetado basado en manifiestos de soportes
  - Mantiene la misma numeración que los paquetes de soportes
  - Incluye todos los archivos de las carpetas de facturas
  - Genera manifiestos para cada paquete de facturas
  - Interfaz de progreso durante el empaquetado
  - Manejo de errores y logging detallado

## Instrucciones de Restauración
Para restaurar a cualquiera de los puntos de restauración:
1. Hacer una copia de seguridad del archivo actual si es necesario
2. Copiar el contenido del archivo de restauración deseado a `app_ips.py`

## Próximas Características

- Procesamiento de soportes
- Empaquetado de archivos
- Reportes y estadísticas

## Notas de Desarrollo

- La aplicación utiliza tkinter para la interfaz gráfica
- Los datos de configuración se almacenan en formato JSON
- La estructura de carpetas se crea automáticamente al inicio
- Se implementa manejo de errores en operaciones críticas

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios que te gustaría hacer.

## Licencia

Este proyecto está bajo la Licencia MIT. 