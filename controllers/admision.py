import datetime


def __verificar_admision_enviada():
    # Verificar si ya se envio la admision
    admision_enviada = db(db.admision.id_user == auth.user.id).select()

    if admision_enviada:
        redirect(URL('admision_enviada'))


@auth.requires(auth.has_membership('Coordinador'))
def manage():
    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()
    admisiones = db(db.admision.id_edicion == edicion_actual.id_edicion).select(
        orderby=~db.admision.estado)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def detalles():
    if not request.args(0):
        redirect(URL('default', 'index'))

    admision = db.admision(request.args(0, cast=int)
                           ) or redirect(URL('dashboard', 'index'))

    if auth.has_membership('Estudiante') and auth.user.id != admision.id_user:
        redirect(URL('usuario', 'no_autorizado'))

    return dict(admision=admision)


@auth.requires(auth.has_membership('Coordinador') or auth.has_membership('Estudiante'))
def reporte_admision():
    if not request.args(0):
        redirect(URL('default', 'index'))

    admision = db.admision(request.args(0, cast=int)
                           ) or redirect(URL('dashboard', 'index'))

    if auth.has_membership('Estudiante') and auth.user.id != admision.id_user:
        redirect(URL('usuario', 'no_autorizado'))

    centro = db(db.settings.id > 0).select().first().centro

    return dict(admision=admision, centro=centro)


@auth.requires(auth.has_membership('Estudiante'))
def detalles_envio():
    admision = db(db.admision.id_user == auth.user.id).select().first()

    if admision:
        if auth.has_membership('Estudiante') and auth.user.id != admision.id_user:
            redirect(URL('usuario', 'no_autorizado'))

    return dict(admision=admision)


@auth.requires(auth.has_membership('Coordinador'))
def modificar_solicitud():
    if not request.args(0):
        redirect(URL('default', 'index'))

    admision = db.admision(request.args(0, cast=int)
                           ) or redirect(URL('dashboard', 'index'))

    field = [Field('estado', 'string', default=admision.estado, requires=IS_IN_SET(
        ['Aprobado', 'No aprobado', 'Pendiente']))]

    form = SQLFORM.factory(*field)

    if form.validate(keepvalues=True):
        if form.vars.estado == 'Aprobado':
            notificacion = {
                'titulo': 'Solicitud aprobada',
                'descripcion': 'Su solicitud de admisión para matricular a la maestría fue aprobada.',
                'tipo': 'success',

            }

            notificacion['id_user'] = admision.id_user
            db.notificacion.insert(**notificacion)

        elif form.vars.estado == 'No aprobado':
            notificacion = {
                'titulo': 'Solicitud denegada',
                'descripcion': 'Su solicitud de admisión fue denegada por los coordinadores.',
                'tipo': 'danger',
            }

            notificacion['id_user'] = admision.id_user
            db.notificacion.insert(**notificacion)

        if not form.errors:
            admision.update_record(estado=form.vars.estado)
            plugin_toastr_message_config('success', T(
                'La solicitud se modificó correctamente'))
            redirect(URL('detalles', args=admision.id))

    elif form.errors:
        plugin_toastr_message_config('error', T(
            'El formulario contiene errores'))

    return dict(form=form)


@auth.requires(auth.has_membership('Coordinador'))
def eliminar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.admision(request.args(0, cast=int)
                           ) or redirect(URL('manage'))
    x = registro.id

    db(db.admision.id == x).delete()
    plugin_toastr_message_config('success', T(
        'Admisión eliminada correctamente'))

    redirect(URL("manage"))
    return dict()


@auth.requires_membership('Estudiante')
def seleccionar_maestria():
    __verificar_admision_enviada()

    maestrias = db((db.edicion.id_maestria == db.maestria.id) &
                   (db.edicion.matricula_abierta == True)).select()

    maestrias = maestrias.find(lambda row: row.edicion.esta_llena == False)

    if not maestrias:
        redirect(URL('dashboard', 'index'))

    options = [OPTION(m.maestria.nombre, _value=m.maestria.id)
               for m in maestrias]

    form = FORM('Seleccione una maestría:',
                SELECT(options, _name='maestria', _class='form-control'),
                INPUT(_type='submit', _value='Enviar', _class='btn btn-primary mt-4'))

    if form.accepts(request, session):
        redirect(URL('crear_admision', args=form.vars.maestria))

    return dict(form=form, maestrias=maestrias)


@auth.requires_membership('Estudiante')
def crear_admision():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    registro = db.maestria(request.args(0, cast=int)
                           ) or redirect(URL('dashboard', 'index'))

    __verificar_admision_enviada()

    edicion = db((db.edicion.id_maestria == registro.id) &
                 (db.edicion.matricula_abierta == True)).select().first()

    return dict(edicion=edicion)


@request.restful()
def api_crear():
    response.view = 'generic.json'

    def POST(*args, **vars):
        if not request.env.request_method == 'POST':
            raise HTTP(403)

        if vars['fecha_graduado']:
            fecha_graduado = vars['fecha_graduado'].split('/')
            fecha_graduado = datetime.date(int(fecha_graduado[2]), int(
                fecha_graduado[1]), int(fecha_graduado[0]))
            vars['fecha_graduado'] = fecha_graduado

        id_user = auth.user.id

        vars['id_user'] = id_user

        if 'foto_ci_1' in vars:
            vars['foto_ci_1_data'] = vars['foto_ci_1'].value

        if 'foto_ci_2' in vars:
            vars['foto_ci_2_data'] = vars['foto_ci_2'].value

        if 'foto_titulo' in vars:
            vars['foto_titulo_data'] = vars['foto_titulo'].value

        if 'cv' in vars:
            vars['cv_data'] = vars['cv'].value

        if 'carta_sindicato' in vars:
            vars['carta_sindicato_data'] = vars['carta_sindicato'].value

        admision_id = db.admision.insert(**vars)

        # Enviar notificación al coordinador
        admision = db.admision(admision_id)
        coordinadores = db(db.coordinador_maestria.id_maestria ==
                           admision.id_edicion.id_maestria).select()

        nombre_maestria = admision.id_edicion.id_maestria.nombre
        edicion_numero = admision.id_edicion.numero

        notificacion = {
            'titulo': 'Nueva admisión enviada',
            'descripcion': f'El usuario {auth.user.username} ha enviado una solicitud de admisión para matricular en edición #{edicion_numero} de la maestría {nombre_maestria}.',
            'tipo': 'info',

        }

        for c in coordinadores:
            notificacion['id_user'] = c.id_user
            db.notificacion.insert(**notificacion)

        return dict(result=admision_id)

    return locals()


@auth.requires(auth.has_membership('Coordinador'))
def editar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.admision(request.args(0, cast=int)
                           ) or redirect(URL('manage'))

    return dict(registro=registro)


@request.restful()
def api_editar():
    response.view = 'generic.json'

    def GET(*args, **vars):
        admision = db.admision(args[0])
        return dict(admision=admision)

    def POST(*args, **vars):
        if not request.env.request_method == 'POST':
            raise HTTP(403)

        if vars['fecha_graduado']:
            fecha_graduado = vars['fecha_graduado'].split('/')
            fecha_graduado = datetime.date(int(fecha_graduado[2]), int(
                fecha_graduado[1]), int(fecha_graduado[0]))
            vars['fecha_graduado'] = fecha_graduado

        if auth.has_membership('Estudiante'):
            vars['estado'] = 'Pendiente'

        if 'foto_ci_1' in vars:
            vars['foto_ci_1_data'] = vars['foto_ci_1'].value

        if 'foto_ci_2' in vars:
            vars['foto_ci_2_data'] = vars['foto_ci_2'].value

        if 'foto_titulo' in vars:
            vars['foto_titulo_data'] = vars['foto_titulo'].value

        if 'cv' in vars:
            vars['cv_data'] = vars['cv'].value

        if 'carta_sindicato' in vars:
            vars['carta_sindicato_data'] = vars['carta_sindicato'].value

        db(db.admision.id == vars['id_admision']).update(**vars)

        return dict(result='admision_id')

    return locals()


@ auth.requires_membership('Estudiante')
def admision_enviada():
    return dict()


@ auth.requires(auth.has_membership('Coordinador') or auth.has_membership('Estudiante'))
def admision_editada():
    if auth.has_membership('Coordinador'):
        plugin_toastr_message_config('success', T(
            'Admisión editada correctamente'))
        redirect(URL('manage'))
    else:
        plugin_toastr_message_config('success', T(
            'Admisión enviada correctamente'))
        redirect(URL('detalles_envio'))
    return dict()
