# Sistema de Gestión de Maestrías Universitarias

Este es un sistema de gestión diseñado para universidades que deseen administrar y gestionar sus programas de maestría de manera eficiente.

## Características principales

- **Gestión de programas de maestría:** Permite crear, editar y eliminar programas de maestría, incluyendo información detallada como nombre, descripción, requisitos de admisión, plan de estudios, etc.

- **Administración de estudiantes:** Facilita el registro y seguimiento de estudiantes matriculados en los programas de maestría, así como su información personal, académica y de contacto.

- **Gestión de profesores:** Permite gestionar el cuerpo docente asignado a cada programa de maestría, incluyendo información sobre su experiencia, áreas de especialización, horarios de clase, entre otros.

- **Control de inscripciones y matrículas:** Proporciona herramientas para administrar el proceso de inscripción y matrícula de los estudiantes en los diferentes programas de maestría.

- **Generación de informes:** Ofrece la capacidad de generar informes detallados sobre la matrícula, el progreso académico de los estudiantes, la disponibilidad de cursos, entre otros aspectos relevantes.

## Instalación

1. Clona este repositorio en tu máquina local utilizando el siguiente comando:

git clone <URL_del_repositorio>

markdown

Reemplaza `<URL_del_repositorio>` con la URL del repositorio.

2. Instala las dependencias necesarias ejecutando:

pip install -r requirements.txt

markdown


3. Configura el sistema de acuerdo a tus necesidades editando los archivos de configuración correspondientes.

4. Inicia el servidor ejecutando:

python manage.py runserver

markdown

El sistema estará disponible en la dirección local `http://localhost:8000`.

## Contribuir

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Realiza un fork del repositorio.
2. Crea una nueva rama para tus cambios (`git checkout -b feature/nombre-caracteristica`).
3. Realiza tus cambios y asegúrate de que las pruebas pasen.
4. Realiza un commit de tus cambios (`git commit -am 'Agrega nueva característica'`).
5. Sube tus cambios a tu fork (`git push origin feature/nombre-caracteristica`).
6. Crea un Pull Request en este repositorio.

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).