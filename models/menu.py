# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    ('Label', T('Menú')),
    (T('Inicio'), request.controller == 'dashboard',
     'home', URL('dashboard', 'index')),
    # (T('Entidad'), False, 'envelope', '#', [
    #     (T('Design'), False, URL('admin', 'default', 'design')),
    # ])
]

# Estudiante
if auth.has_membership('Estudiante'):
    response.menu += [
        (T('Datos de admisión'),  request.controller ==
         'admision', 'file-text', URL('admision', 'detalles_envio')),
        (T('Tema de tesis'),  request.controller ==
         'tesis', 'crosshairs', URL('tesis', 'detalles_evaluacion')),
        (T('Calificaciones'), request.controller == 'calificacion_estudiante',
         'file', URL('calificacion_estudiante', 'calificaciones')),
    ]


# Profesor
if auth.has_membership('Profesor'):
    response.menu += [
        (T('Calificar'),  request.controller ==
         'calificacion_profesor', 'pencil-square-o', URL('calificacion_profesor', 'select_maestria')),
        (T('Acreditación'),  request.controller ==
         'acreditacion_profesor', 'star', URL('acreditacion_profesor', 'manage')),
        (T('Tutoría'),  request.controller ==
         'tesis', 'book', URL('tesis', 'tutoria')),
    ]


# Coordinador & Administrador
if auth.has_membership('Administrador') or auth.has_membership('Coordinador'):
    pass


# Coordinador
if auth.has_membership('Coordinador'):
    response.menu += [
        ('Label', T('Edición de maestría')),
        (T('Ediciones'), request.controller == 'edicion',
         'table', URL('edicion', 'manage')),
        ('Label', T('Estudiantes')),
        (T('Estudiantes'), request.controller == 'admision', 'group', '#', [
            (T('Admisiones'), False, 'file', URL('admision', 'manage')),
            (T('Matrícula'), False, 'pencil-square-o', URL('matricula', 'manage')),
            (T('Bajas'), False, 'minus-circle', URL('matricula', 'bajas')),
        ]),
        (T('Calificaciones'), request.controller == 'calificacion',
         'file-text', URL('calificacion', 'asignaturas')),
        (T('Temas de tesis'),  request.controller == 'tesis', 'book', '#', [
            (T('Aprobados'), False, 'check-square',
             URL('tesis', 'temas_aprobados')),
            (T('Pendientes'), False, 'clock-o',
             URL('tesis', 'temas_pendientes')),
        ]),
        ('Label', T('Profesores')),
        (T('Profesores'), request.controller == 'profesor',
         'users', URL('profesor', 'manage')),
        (T('Actividades'),  request.controller == 'actividad' or request.controller == 'actividad_edicion',
         'list-alt', '#', [
            (T('Nomenclador'), False, 'edit',
             URL('actividad', 'manage')),
            (T('Edición actual'), False, 'calendar-alt',
             URL('actividad_edicion', 'manage')),
        ]),
        ('Label', T('Reportes')),
        (T('Dictámenes'), request.controller == 'dictamen', 'files-o', '#', [
            (T('Solicitud de matrícula (PG-01)'), False, 'user',
             URL('dictamen', 'dictamen_solicitud_admision')),
            (T('Admisión (PG-02)'), False, 'file-text',
             URL('dictamen', 'dictamen_admision')),
            (T('Certificación de calificaciones (PG-03)'), False, 'edit',
             URL('dictamen', 'dictamen_certificacion_calificaciones')),
            (T('Créditos no lectivos (PG-04)'), False, 'th-list',
             URL('dictamen', 'dictamen_no_lectivos')),
            (T('Evaluaciones de suficiencia (PG-05)'), False, 'star',
             URL('dictamen', 'dictamen_suficiencia')),
            (T('Convalidaciones (PG-06)'), False, 'check-circle',
             URL('dictamen', 'dictamen_convalidacion')),
            (T('Bajas (PG-07)'), False, 'minus-circle',
             URL('dictamen', 'generar_bajas')),
            (T('Temas de tesis (PG-08)'), False, 'book',
             URL('dictamen', 'dictamen_tesis')),
            (T('Acta de defensa (PG-09)'), False, 'file',
             URL('dictamen', 'generar_acta_defensa')),
            (T('Cierre de expediente (PG-10)'), False, 'archive',
             URL('dictamen', 'dictamen_cierre_expediente')),
            (T('Actividades del programa (PG-11)'), False, 'list-alt',
             URL('dictamen', 'generar_actividades')),
            (T('Matrícula oficial (PG-12)'), False, 'users',
             URL('dictamen', 'generar_matricula_oficial')),
            (T('Calendario oficial (PG-13)'), False, 'calendar',
             URL('dictamen', 'generar_calendario_oficial')),
            (T('Evaluación de actividades (PG-14)'), False, 'pencil-square',
             URL('dictamen', 'dictamen_evaluacion_actividades')),
            (T('Nombramiento del tribunal (PG-15)'), False, 'legal',
             URL('dictamen', 'dictamen_tribunal')),
            (T('Otorgamiento de títulos o certificados (PG-16)'), False, 'file-text',
             URL('dictamen', 'generar_otorgamiento')),
            (T('Graduados de la edición (PG-17)'), False, 'trophy',
             URL('dictamen', 'generar_graduados')),
            (T('Cierre de la edición (PG-18)'), False, 'flag-checkered',
             URL('dictamen', 'generar_cierre_edicion')),
            (T('Dictamen del consejo científico (PG-19)'), False, 'briefcase',
             URL('dictamen', 'generar_dictamen_consejo')),
            (T('Certificado del curso (PG-20)'), False, 'clipboard',
             URL('dictamen', 'dictamen_certificado')),
        ]),
        ('Label', T('Configuración')),
        (T('Configuración'), request.function == 'coordinador_configuracion',
         'gear', URL('settings', 'coordinador_configuracion')),
        (T('Mantenimiento'), request.function == 'sistema_mantenimiento',
         'lock', URL('settings', 'sistema_mantenimiento')),
    ]


# Administrador
if auth.has_membership('Administrador'):
    response.menu += [
        (T('Maestrías'), request.controller == 'maestria',
         'trophy', URL('maestria', 'manage')),
        ('Label', T('Seguridad')),
        (T('Mantenimiento'), request.function == 'sistema_mantenimiento',
         'lock', URL('settings', 'sistema_mantenimiento')),
        (T('Configuración'), request.function == 'administrador_configuracion',
         'gear', URL('settings', 'administrador_configuracion')),
        (T('Usuarios'), request.controller ==
         'usuario', 'user', URL('usuario', 'manage')),
    ]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------
