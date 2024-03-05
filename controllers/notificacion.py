@auth.requires_login()
def manage():
    notificaciones = db(db.notificacion.id_user == auth.user.id).select(
        orderby=~db.notificacion.fecha)

    db(db.notificacion.leido == False).update(leido=True)

    return dict(notificaciones=notificaciones)


@auth.requires_login()
def detalles():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.notificacion(request.args(0, cast=int)
                               ) or redirect(URL('manage'))

    registro.update_record(leido=True)

    return dict(n=registro)


@auth.requires_login()
def eliminar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.notificacion(request.args(0, cast=int)
                               ) or redirect(URL('manage'))

    db(db.notificacion.id == registro.id).delete()

    plugin_toastr_message_config('success', T(
        'La notificación se ha eliminado correctamente'))

    redirect(URL("manage"))

    return dict()


@auth.requires_login()
def eliminar_todas():
    db(db.notificacion.id_user == auth.user.id).delete()

    plugin_toastr_message_config('success', T(
        'Todas las notificaciones se han eliminado correctamente'))

    redirect(URL("manage"))

    return dict()
