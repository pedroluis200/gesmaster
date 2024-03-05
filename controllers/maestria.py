@auth.requires_membership('Administrador')
def manage():
    maestrias = db(db.maestria.id > 0).select()
    return dict(maestrias=maestrias)


@auth.requires_membership('Administrador')
def crear():
    form = SQLFORM(db.maestria)

    if form.process().accepted:
        plugin_toastr_message_config('success', T(
            'La maestría se ha creado correctamente.'))
        redirect(URL('manage'))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form)


@auth.requires_membership('Administrador')
def editar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.maestria(request.args(0, cast=int)
                           ) or redirect(URL('manage'))

    form = SQLFORM(db.maestria, registro)

    if form.process().accepted:
        plugin_toastr_message_config('success', T(
            'La maestría se ha editado correctamente.'))
        redirect(URL('manage'))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form)


@auth.requires_membership('Administrador')
def eliminar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.maestria(request.args(0, cast=int)
                           ) or redirect(URL('manage'))

    usuario_coordinador = db(db.coordinador_maestria.id_maestria == registro.id).select()

    
    if usuario_coordinador:
        db((db.auth_user.id == usuario_coordinador.first().id_user)).delete()

    db(db.maestria.id == registro.id).delete()

    plugin_toastr_message_config('success', T(
        'La maestría se ha eliminado correctamente'))

    redirect(URL("manage"))

    return dict()
