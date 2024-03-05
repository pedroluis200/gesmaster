@auth.requires(auth.has_membership('Estudiante'))
def detalles_evaluacion():
    record = db((db.admision.id_user == auth.user.id) &
                (db.tesis.id_admision == db.admision.id)
                ).select().first()
    return dict(tesis=record.tesis if record else None)


@auth.requires(auth.has_membership('Estudiante'))
def enviar_evaluacion():
    tesis = db((db.admision.id_user == auth.user.id) &
               (db.tesis.id_admision == db.admision.id)
               ).select().first()

    admision = db(db.admision.id_user == auth.user.id).select().first()

    if tesis:
        redirect(URL('detalles_evaluacion'))

    if not admision:
        redirect(URL('dashboard', 'index'))

    form = SQLFORM(db.tesis)

    if form.validate():
        db.tesis.insert(estado="Pendiente",
                        documento_data=request.vars.documento.value,
                        id_admision=admision.id,
                        **form.vars
                        )

        plugin_toastr_message_config('success', T(
            'Los datos se han enviado correctamente'))

        # Enviar notificación al coordinador
        coordinadores = db(db.coordinador_maestria.id_maestria ==
                           admision.id_edicion.id_maestria).select()

        nombre_maestria = admision.id_edicion.id_maestria.nombre
        edicion_numero = admision.id_edicion.numero

        estudiante = f'Este usuario está matriculado en la edición #{edicion_numero} de la maestría {nombre_maestria}.'
        notificacion = {
            'titulo': 'Nuevo tema de tesis pendiente de aprobación',
            'descripcion': f'El usuario {auth.user.username} le ha enviado el tema de su investigación. {estudiante}',
            'tipo': 'info',
        }

        for c in coordinadores:
            notificacion['id_user'] = c.id_user
            db.notificacion.insert(**notificacion)

        redirect(URL("detalles_evaluacion"))

    elif form.errors:
        plugin_toastr_message_config('error', T(
            'El formulario contiene errores'))

    return dict(form=form)


@auth.requires(auth.has_membership('Estudiante'))
def volver_enviar_evaluacion():
    admision = db(db.admision.id_user == auth.user.id).select().first()

    if not admision:
        redirect(URL('dashboard', 'index'))

    form = SQLFORM(db.tesis)

    if form.validate():
        db(db.tesis.id_admision == admision.id).delete()

        db.tesis.insert(estado="Pendiente",
                        documento_data=request.vars.documento.value,
                        id_admision=admision.id,
                        **form.vars
                        )

        plugin_toastr_message_config('success', T(
            'Los datos se han enviado correctamente'))

        # Enviar notificación al coordinador
        coordinadores = db((db.auth_user.id == db.auth_membership.user_id) & (
            db.auth_membership.group_id == db.auth_group.id) & (db.auth_group.role == 'Coordinador')).select()

        nombre_maestria = admision.id_edicion.id_maestria.nombre
        edicion_numero = admision.id_edicion.numero

        estudiante = f'Este usuario está matriculado en la edición #{edicion_numero} de la maestría {nombre_maestria}.'

        notificacion = {
            'titulo': 'Nuevo tema de tesis pendiente de aprobación',
            'descripcion': f'El usuario {auth.user.username} le ha enviado el tema de su investigación. {estudiante}',
            'tipo': 'info',
        }

        for c in coordinadores:
            notificacion['id_user'] = c.auth_user.id
            db.notificacion.insert(**notificacion)

        redirect(URL("detalles_evaluacion"))

    elif form.errors:
        plugin_toastr_message_config('error', T(
            'El formulario contiene errores'))

    return dict(form=form)


@auth.requires(auth.has_membership('Coordinador'))
def asignar_tutor():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    tesis = db.tesis(request.args(0, cast=int)
                     ) or redirect(URL('dashboard', 'index'))

    requires = IS_EMPTY_OR(IS_IN_DB(
        db((db.auth_user.id == db.auth_membership.user_id) &
           (db.auth_membership.group_id == db.auth_group.id) &
            (db.auth_group.role == 'Profesor')
           ),
        'auth_user.id', '%(first_name)s %(last_name)s')
    )

    form = SQLFORM.factory(
        Field('tutor', 'reference auth_user', default=tesis.tutor, requires=requires))

    if form.validate():
        tesis.update_record(**form.vars)

        user_tutor = db.auth_user(tesis.tutor)

        if user_tutor:
            tutor = user_tutor.first_name + ' ' + user_tutor.last_name

            notificacion = {
                'titulo': 'Se le ha asignado un tutor',
                'descripcion': f'El comité organizador de la maestría le ha asignado el tutor {tutor}.',
                'tipo': 'info',
                'id_user': tesis.id_admision.id_user
            }

            db.notificacion.insert(**notificacion)

            plugin_toastr_message_config('success', T(
                'El tutor fue asignado correctamente'))
        else:
            plugin_toastr_message_config('success', T(
                'No se asignó ningún tutor'))

        redirect(URL("detalles", args=tesis.id))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'El formulario contiene errores'))

    return dict(form=form)


@auth.requires(auth.has_membership('Coordinador'))
def temas_aprobados():
    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()
    aprobados = db((db.admision.id_edicion == edicion_actual.id_edicion) &
                   (db.admision.id == db.tesis.id_admision) &
                   (db.tesis.estado == 'Aprobado')
                   ).select()
    return dict(aprobados=aprobados)


@auth.requires(auth.has_membership('Coordinador'))
def temas_pendientes():
    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()
    pendientes = db((db.admision.id_edicion == edicion_actual.id_edicion) &
                    (db.admision.id == db.tesis.id_admision) &
                    (db.tesis.estado == 'Pendiente')
                    ).select()
    return dict(pendientes=pendientes)


@auth.requires(auth.has_membership('Coordinador'))
def modificar_estado():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    tesis = db.tesis(request.args(0, cast=int)
                     ) or redirect(URL('dashboard', 'index'))

    form = SQLFORM.factory(Field('estado', 'string', default=tesis.estado, requires=IS_IN_SET(
        ['Aprobado', 'No aprobado', 'Pendiente'])))

    if form.validate(keepvalues=True):
        estado = tesis.estado

        tesis.update_record(**form.vars)

        plugin_toastr_message_config('success', T(
            'El estado se ha cambiado correctamente'))

        if form.vars.estado == 'No aprobado':
            notificacion = {
                'titulo': 'Tema de tesis rechazado',
                'descripcion': 'Su tema de tesis fue rechazado por el comité académico de la maestría.',
                'tipo': 'danger',
            }

            notificacion['id_user'] = tesis.id_admision.id_user
            db.notificacion.insert(**notificacion)

        if estado == 'Aprobado':
            notificacion = {
                'titulo': 'Tema de tesis aprobado',
                'descripcion': 'Su tema de tesis fue aprobado por el comité académico de la maestría.',
                'tipo': 'success',
            }

            notificacion['id_user'] = tesis.id_admision.id_user
            db.notificacion.insert(**notificacion)

        redirect(URL("detalles", args=tesis.id))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form, tesis=tesis)


@auth.requires(auth.has_membership('Coordinador') or auth.has_membership('Profesor'))
def detalles():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    tesis = db.tesis(request.args(0, cast=int)
                     ) or redirect(URL('dashboard', 'index'))

    return dict(tesis=tesis)


@auth.requires(auth.has_membership('Coordinador'))
def eliminar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.tesis(request.args(0, cast=int)
                        ) or redirect(URL('manage'))
    x = registro.id

    db(db.tesis.id == x).delete()
    plugin_toastr_message_config('success', T(
        'Tema de tesis eliminado correctamente'))

    if registro.estado == 'Pendiente':
        redirect(URL("temas_pendientes"))
    else:
        redirect(URL("temas_aprobados"))

    return dict()


@auth.requires(auth.has_membership('Profesor'))
def tutoria():
    listado = db((db.tesis.tutor == auth.user.id) &
               (db.tesis.id_admision == db.admision.id) &
               (db.admision.id_edicion == db.edicion.id) &
               (db.edicion.activa == True)).select()

    return dict(listado=listado)
