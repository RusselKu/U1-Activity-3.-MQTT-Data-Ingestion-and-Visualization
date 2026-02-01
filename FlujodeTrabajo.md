🏗️ 1. Data Architect

Objetivo: Establecer la infraestructura de almacenamiento y asegurar la integridad de los datos entrantes. 


Configuración de Base de Datos: Crear las tablas necesarias siguiendo estrictamente el esquema proporcionado. 


Tabla de Enteros: lake_raw_data_int con campos id, topic, payload, value (BIGINT) y ts. 


Tabla de Flotantes: lake_raw_data_float con campos idénticos, pero con value tipo DOUBLE PRECISION. 


Gestión de Flujo: Asegurar que el suscriptor MQTT pueda insertar datos sin latencia excesiva. 


Evidencia: Proveer capturas de pantalla de las tablas con datos ya insertados para el reporte. 

💻 2. Desarrolladoras (MQTT & Dashboard)

Objetivo: Implementar la lógica de comunicación, simulación de sensores y la interfaz de usuario. 

Sub-tarea A: Lógica MQTT (Paho)

Publicador: Crear un script que genere y publique valores aleatorios (enteros y flotantes) en tópicos distintos. 


Suscriptor: Implementar el cliente que escuche ambos tópicos y pase los datos al Data Architect para su inserción. 


Referencia: Utilizar obligatoriamente el código visto en clase como base. 

Sub-tarea B: Dashboard (Streamlit)

Visualización: Construir un dashboard en Streamlit que consuma los datos de la base de datos en tiempo real. 


Interfaz: Crear gráficas de series de tiempo que distingan claramente entre el flujo de enteros y el de flotantes. 

✍️ 3. Technical Documentation (LaTeX Master)

Objetivo: Compilar el reporte técnico final bajo estándares profesionales internacionales. 


Formato: Redactar el documento exclusivamente en LaTeX usando el formato IEEE. 

Contenido Obligatorio:


Diagrama de Arquitectura: Diseñar un esquema que muestre la conexión entre: Publicador → Broker → Suscriptor → Base de Datos → Dashboard. 


Explicación Técnica: Detallar las tecnologías usadas y cómo fluyen los datos a través de los componentes. 


Extensión: Asegurar un mínimo de 5 y un máximo de 6 páginas. 


Calidad: Revisar que el reporte cumpla con la rúbrica de "Comunicación Técnica". 

💡 Tips para el flujo de trabajo:
Sincronización: El Data Architect debe pasar las credenciales de la base de datos a las Desarrolladoras cuanto antes.


Iteración: Las Desarrolladoras deben entregar capturas de pantalla funcionales al LaTeX Master conforme avancen, no al final. 


Código Base: No intenten reinventar la rueda; partan del código de clase y extiéndanlo.