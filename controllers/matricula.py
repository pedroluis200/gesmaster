from query_db import get_edicion_actual


@auth.requires(auth.has_membership('Coordinador'))
def manage():
    edicion_actual = get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def bajas():
    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()
    admisiones = db((db.admision.id_edicion == edicion_actual.id_edicion) &
                    (db.admision.estado == 'Baja') &
                    (db.admision.id == db.baja.id_admision)
                    ).select()
    return dict(admisiones=admisiones, edicion_actual=edicion_actual)


@auth.requires(auth.has_membership('Coordinador'))
def dar_baja():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.admision(request.args(0, cast=int)
                           ) or redirect(URL('manage'))

    form = SQLFORM.factory(Field('causa', 'text', requires=IS_NOT_EMPTY()))

    if form.validate():
        registro.update_record(estado='Baja')

        db.baja.insert(causa=form.vars.causa, id_admision=registro.id)

        plugin_toastr_message_config('success', T(
            'El estudiante ha sido dado de baja correctamente'))

        redirect(URL("manage"))

    notificacion = {
        'titulo': 'Baja del curso',
        'descripcion': f'Fue dado de baja de la maestría.',
        'tipo': 'danger',
        'id_user': registro.id_user
    }

    db.notificacion.insert(**notificacion)

    return dict(form=form)


@auth.requires(auth.has_membership('Coordinador'))
def activar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.admision(request.args(0, cast=int)
                           ) or redirect(URL('manage'))

    if registro.id_edicion.esta_llena:
        redirect(URL('bajas'))
        plugin_toastr_message_config('error', T(
            'No se puede activar este estudiante. La matrícula está llena'))

    registro.update_record(estado='Aprobado')

    db(db.baja.id_admision == registro.id).delete()

    plugin_toastr_message_config('success', T(
        'El estudiante ha sido activado correctamente'))

    notificacion = {
        'titulo': 'Se ha activado su matrícula',
        'descripcion': f'Su matrícula ha vuelto a estar activa en la maestría. Bienvenido de nuevo!!',
        'tipo': 'success',
        'id_user': registro.id_user
    }

    db.notificacion.insert(**notificacion)

    redirect(URL("bajas"))
    return dict()
