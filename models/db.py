# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
import datetime
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    # SQLite
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])

    # MySQL
    # db = DAL('mysql://root:root@localhost/test?set_encoding=utf8mb4',
    #          pool_size=configuration.get('db.pool_size'),
    #          migrate_enabled=configuration.get('db.migrate'),
    #          check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=True, signature=False)

# My User configuration
auth.settings.controller = 'usuario'
auth.settings.login_url = URL('usuario', 'login')
auth.settings.login_next = URL('dashboard', 'index')
auth.settings.logout_next = URL('usuario', 'login')
auth.settings.on_failed_authorization = URL('usuario', 'no_autorizado')

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get(
    'smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(
        db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# add virtual field to auth_user
# -------------------------------------------------------------------------
db.auth_user.full_name = Field.Virtual(lambda row: ' '.join(
    [row.auth_user.first_name, row.auth_user.last_name]))

# -------------------------------------------------------------------------
# Settings
# -------------------------------------------------------------------------
db.define_table('settings',
                Field('centro', 'string'),
                Field('en_mantenimiento', 'boolean'),
                )

# Notifications
# -------------------------------------------------------------------------
db.define_table('notificacion',
                Field('titulo', 'string'),
                Field('descripcion', 'string'),
                Field('fecha', 'datetime', default=datetime.datetime.now()),
                Field('leido', 'boolean', default=False),
                Field('tipo', 'string'),
                Field('id_user', 'reference auth_user'),
                )

db.notificacion.tipo.requires = IS_IN_SET(
    ['success', 'info', 'warning', 'danger'])

db.notificacion.id_user.requires = IS_IN_DB(db, 'auth_user.id', '%(username)s')

# -------------------------------------------------------------------------
# Maestria
# -------------------------------------------------------------------------
db.define_table('maestria',
                Field('nombre', 'string', label='Maestría'),
                format='%(nombre)s'
                )

db.maestria.id.readable = False
db.maestria.nombre.requires = IS_NOT_EMPTY()
db.maestria.ediciones = Field.Virtual(lambda row: db(
    db.edicion.id_maestria == row.maestria.id).count())


# -------------------------------------------------------------------------
# Coordinador Maestria
# -------------------------------------------------------------------------
db.define_table('coordinador_maestria',
                Field('id_maestria', 'reference maestria'),
                Field('id_user', 'reference auth_user'),
                )

db.auth_user.maestria_usuario = Field.Virtual(lambda row: db(
    db.coordinador_maestria.id_user == row.auth_user.id).select().first())

# -------------------------------------------------------------------------
# Edicion
# -------------------------------------------------------------------------
db.define_table('edicion',
                Field('numero', 'integer', label='Número'),
                Field('limite_matricula', 'integer',
                      label='Límite de matrícula'),
                Field('creditos_minimos', 'integer', label='Créditos Mínimos'),
                Field('fecha_inicio', 'date',
                      widget=SQLFORM.widgets.string.widget),
                Field('fecha_fin', 'date', widget=SQLFORM.widgets.string.widget),
                Field('activa', 'boolean', default=True, writable=False,
                      readable=False, label='Activar edición'),
                Field('matricula_abierta', 'boolean',
                      default=True, label='Matrícula Abierta'),
                Field('id_maestria', 'reference maestria',
                      label='Maestría', writable=False),
                format='%(numero)s'
                )

db.edicion.matriculados = Field.Virtual(lambda row: db((db.admision.id_edicion == row.edicion.id) &
                                                       (db.admision.estado == 'Aprobado')).count()
                                        )

db.edicion.esta_llena = Field.Virtual(lambda row: db((db.admision.id_edicion == row.edicion.id) &
                                                     (db.admision.estado ==
                                                      'Aprobado')
                                                     ).count() == row.edicion.limite_matricula
                                      )

db.edicion.id.readable = False
db.edicion.numero.requires = [IS_NOT_EMPTY(), IS_INT_IN_RANGE(1, None)]
db.edicion.limite_matricula.requires = IS_INT_IN_RANGE(1)
db.edicion.creditos_minimos.requires = IS_INT_IN_RANGE(1)
db.edicion.fecha_inicio.requires = IS_DATE(format=T('%Y-%m-%d'))
db.edicion.fecha_fin.requires = IS_DATE(format=T('%Y-%m-%d'))
db.edicion.id_maestria.requires = IS_IN_DB(db, 'maestria.id', '%(nombre)s')


# -------------------------------------------------------------------------
# Edicion Actual
#
# La edición actual es la edición activa en el panel del coordinador.
# Es la instancia activa en el sistema, por tanto, todos los demás datos
# que dependen de esa edición, se encuentran visibles en la aplicación.
# -------------------------------------------------------------------------

db.define_table('edicion_actual',
                Field('id_edicion', 'reference edicion'),
                Field('id_user', 'reference auth_user')
                )

# -------------------------------------------------------------------------
# Admision
# -------------------------------------------------------------------------
db.define_table('admision',
                Field('nombre', 'string'),
                Field('apellido1', 'string'),
                Field('apellido2', 'string'),
                Field('ci', 'string'),
                Field('pasaporte', 'string'),
                Field('telefono', 'string', default='No definido'),
                Field('pais', 'string'),
                Field('sexo', 'string', default='No definido'),
                Field('correo', 'string'),
                Field('foto_ci_1', 'upload', uploadfield='foto_ci_1_data'),
                Field('foto_ci_1_data', 'blob'),
                Field('foto_ci_2', 'upload', uploadfield='foto_ci_2_data'),
                Field('foto_ci_2_data', 'blob'),

                Field('calle', 'string', default='No definido'),
                Field('apto', 'string', default='No definido'),
                Field('numero_residencia', 'string', default='No definido'),
                Field('entre_direccion', 'string', default='No definido'),
                Field('provincia_residencia', 'string'),
                Field('municipio_residencia', 'string'),

                Field('graduado_de', 'string'),
                Field('nombre_universidad', 'string', default='No definido'),
                Field('pais_universidad', 'string', default='No definido'),
                Field('fecha_graduado', 'date'),
                Field('numero_universidad', 'string', default='No definido'),
                Field('tomo', 'string', default='No definido'),
                Field('folio', 'string', default='No definido'),
                Field('foto_titulo', 'upload', uploadfield='foto_titulo_data'),
                Field('foto_titulo_data', 'blob'),

                Field('ocupacion', 'string'),
                Field('experiencia', 'integer'),
                Field('centro_laboral', 'string'),
                Field('forma_propiedad', 'string'),
                Field('calle_trabajo', 'string'),
                Field('numero_trabajo', 'string'),
                Field('entre_trabajo', 'string'),
                Field('provincia_trabajo', 'string', default='No definido'),
                Field('municipio_trabajo', 'string', default='No definido'),
                Field('telefono_trabajo', 'string', default='No definido'),
                Field('osde', 'string', default='No definido'),
                Field('organismo', 'string'),
                Field('cv', 'upload', uploadfield='cv_data'),
                Field('cv_data', 'blob'),
                Field('carta_sindicato', 'upload',
                      uploadfield='carta_sindicato_data'),
                Field('carta_sindicato_data', 'blob'),

                Field('estado', 'string', default='Pendiente'),
                Field('id_user', 'reference auth_user'),
                Field('id_edicion', 'reference edicion'),
                )

db.admision.estado.requires = IS_IN_SET(
    ['Aprobado', 'No aprobado', 'Pendiente', 'Baja'])
db.admision.id_user.requires = IS_IN_DB(db, 'auth_user.id', '%(username)s')
db.admision.id_edicion.requires = IS_IN_DB(db, 'edicion.id', '%(numero)s')

db.admision.creditos = Field.Virtual(lambda row: __get_creditos(row))


def __get_creditos(row):
    creditos = 0
    estudiante = row.admision

    calificaciones = db(db.calificacion.id_estudiante ==
                        estudiante.id).select()

    for c in calificaciones:
        if c.nota > 2:
            creditos += c.id_actividad_edicion.creditos

    return creditos


# -------------------------------------------------------------------------
# Bajas
# -------------------------------------------------------------------------
db.define_table('baja',
                Field('causa', 'text'),
                Field('id_admision', 'reference admision'),
                )

# -------------------------------------------------------------------------
# Tema de tesis
# -------------------------------------------------------------------------
db.define_table('tesis',
                Field('titulo', 'string', label='Título'),
                Field('documento', 'upload', uploadfield='documento_data'),
                Field('documento_data', 'blob'),
                Field('estado', 'string'),
                Field('tutor', 'reference auth_user'),
                Field('id_admision', 'reference admision'),
                )

db.tesis.titulo.requires = IS_NOT_EMPTY()
db.tesis.documento.requires = [IS_LENGTH(20971520, error_message="Debe tener una capacidad menor a 20 mb"),
                               IS_FILE(extension=['pdf', 'doc', 'docx'])]
db.tesis.estado.requires = IS_IN_SET(
    ['Aprobado', 'No aprobado', 'Pendiente'])

db.tesis.tutor.requires = IS_EMPTY_OR(IS_IN_DB(
    db((db.auth_user.id == db.auth_membership.user_id) &
       (db.auth_membership.group_id == db.auth_group.id) &
       (db.auth_group.role == 'Profesor')
       ),
    'auth_user.id', '%(first_name)s %(last_name)s')
)

db.tesis.estado.writable = False
db.tesis.tutor.writable = False
db.tesis.id_admision.readable = False
db.tesis.id_admision.writable = False

# -------------------------------------------------------------------------
# Actividad
# -------------------------------------------------------------------------
db.define_table('actividad',
                Field('nombre', 'string'),
                Field('tipo', 'string'),
                Field('optativo', 'boolean', default=False),
                )

db.actividad.nombre.requires = [
    IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'actividad.nombre')]
db.actividad.tipo.requires = IS_IN_SET(
    ['Lectiva', 'No lectiva'])

# -------------------------------------------------------------------------
# Actividad Edicion
# -------------------------------------------------------------------------
db.define_table('actividad_edicion',
                Field('id_actividad', 'reference actividad', label='Actividad'),
                Field('creditos', 'integer', label='Créditos'),
                Field('fecha_inicio', 'date',
                      widget=SQLFORM.widgets.string.widget),
                Field('fecha_fin', 'date', widget=SQLFORM.widgets.string.widget),
                Field('id_edicion', 'reference edicion'),
                Field('id_profesor', 'reference auth_user', label='Profesor'),
                )

db.actividad_edicion.creditos.requires = IS_INT_IN_RANGE(1, None)

db.actividad_edicion.fecha_inicio.requires = IS_DATE(format=T('%Y-%m-%d'))
db.actividad_edicion.fecha_fin.requires = IS_DATE(format=T('%Y-%m-%d'))

db.actividad_edicion.id_actividad.requires = IS_IN_DB(
    db, 'actividad.id', '%(nombre)s - %(tipo)s')

db.actividad_edicion.id_edicion.requires = IS_IN_DB(
    db, 'edicion.id', '%(numero)s')

db.actividad_edicion.id_profesor.requires = IS_IN_DB(
    db((db.auth_user.id == db.auth_membership.user_id) &
       (db.auth_membership.group_id == db.auth_group.id) &
       (db.auth_group.role == 'Profesor')
       ),
    'auth_user.id', '%(first_name)s %(last_name)s')


# -------------------------------------------------------------------------
# Calificacion
# -------------------------------------------------------------------------
db.define_table('calificacion',
                Field('nota', 'integer'),
                Field('tipo', 'string'),
                Field('id_actividad_edicion', 'reference actividad_edicion'),
                Field('id_estudiante', 'reference admision'),
                )

db.calificacion.nota.requires = IS_INT_IN_RANGE(0, None)
db.calificacion.tipo.requires = IS_IN_SET(
    ['Examen', 'Suficiencia', 'Convalidado'])
db.calificacion.id_actividad_edicion.requires = IS_IN_DB(
    db, 'actividad_edicion.id', '%(id)s')
db.calificacion.id_estudiante.requires = IS_IN_DB(
    db, 'admision.id', '%(nombre)s %(apellido1)s %(apellido2)s')


# -------------------------------------------------------------------------
# Acreditacion Profesor
# -------------------------------------------------------------------------
db.define_table('acreditacion_profesor',
                Field('creditos', 'integer', label='Créditos'),
                Field('evidencia', 'upload', uploadfield='evidencia_data'),
                Field('evidencia_data', 'blob'),
                Field('id_profesor', 'reference auth_user'),
                )

db.acreditacion_profesor.creditos.requires = IS_INT_IN_RANGE(1, None)
db.acreditacion_profesor.evidencia.requires = [IS_LENGTH(20971520, error_message="Debe tener una capacidad menor a 20 mb"),
                                               IS_FILE(extension=['pdf', 'doc', 'docx', 'jpg', 'png'])]

# Get creditos profesor
db.auth_user.total_creditos = Field.Virtual(lambda row: __get_creditos_profesor(row))

def  __get_creditos_profesor(row):
    creditos = 0

    sum = db.acreditacion_profesor.creditos.sum()

    creditos = db(db.acreditacion_profesor.id_profesor == row.auth_user.id).select(sum).first()[sum]

    return creditos or 0


# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
