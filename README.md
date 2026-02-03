Pollería App — Sistema Digital de Gestión de Pedidos para Negocio de Restauración
Resumen del proyecto

Pollería App es un sistema web de gestión de pedidos diseñado para digitalizar el flujo operativo de negocios de comida rápida, take away y restauración ligera.

El objetivo principal del proyecto es simular un entorno real de producción donde se separan claramente los roles de mostrador, cocina y pantalla de cliente, optimizando tiempos de servicio, visibilidad operativa y experiencia del usuario final.

Este proyecto está orientado a demostrar capacidades reales de diseño de sistemas, arquitectura backend, automatización de flujos y aplicaciones prácticas para negocio.

Problema que resuelve

Muchos pequeños negocios gestionan pedidos de forma manual, con errores frecuentes, desorganización y falta de visibilidad entre áreas.

Este sistema permite:

Centralizar pedidos en tiempo real

Reducir errores humanos

Mejorar coordinación entre mostrador y cocina

Mostrar pedidos listos automáticamente al cliente

Preparar el negocio para escalado digital

Funcionalidades clave

Creación y gestión de pedidos desde panel de mostrador

Visualización de pedidos activos en cocina

Pantalla pública de pedidos listos para clientes

Control de estados del pedido (pendiente, preparando, listo)

Actualización automática sin recarga manual

Interfaz adaptada a pantallas táctiles y tablets

Arquitectura preparada para red local o despliegue cloud

Arquitectura técnica
Backend

API REST desarrollada con FastAPI

Gestión centralizada del estado de pedidos

Arquitectura modular preparada para ampliación

Soporte para integración futura con base de datos y servicios externos

Frontend

Interfaz web ligera y rápida

Comunicación directa con backend

Actualización dinámica de datos

Diseño enfocado a operación real en cocina y mostrador

Flujo operativo

Mostrador crea el pedido

Cocina visualiza pedidos activos

Pedido cambia a estado listo

Pantalla pública muestra el pedido automáticamente

Este flujo replica el funcionamiento real de sistemas KDS (Kitchen Display System).

Stack tecnológico

Backend:

Python

FastAPI

Uvicorn

Frontend:

HTML5

CSS3

JavaScript

Otros:

Git

Arquitectura REST

Diseño orientado a procesos operativos

Instalación y ejecución local

Clonar repositorio:

git clone https://github.com/Jaume92/Polleria_app.git
cd Polleria_app


Crear entorno virtual:

python -m venv venv
source venv/bin/activate
venv\Scripts\activate


Instalar dependencias:

pip install -r requirements.txt


Ejecutar servidor:

uvicorn main:app --reload


Acceder a la aplicación:

http://127.0.0.1:8000

Aplicaciones reales del sistema

Este proyecto puede adaptarse directamente para:

TPV digital interno

Pantallas de cocina industriales

Pantallas públicas de pedidos

Sistemas de colas en restauración

Digitalización de procesos operativos

Integración con hardware (impresoras térmicas, tablets, kioskos)

Roadmap técnico (siguientes pasos)

Persistencia con base de datos (PostgreSQL / SQLite)

Autenticación y control de roles

Estadísticas de ventas y tiempos de preparación

Integración con impresora de tickets

Modo producción con despliegue cloud

Conversión a aplicación PWA para tablets

Autor

Jaume