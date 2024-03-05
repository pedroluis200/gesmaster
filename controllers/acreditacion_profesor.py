@auth.requires(auth.has_membership('Profesor'))
def manage():
    creditos = db(db.acreditacion_profesor.id_profesor == auth.user.id).select()
    return dict(creditos=creditos)


@auth.requires(auth.has_membership('Profesor'))
def crear():
    db.acreditacion_profesor.id_profesor.writable = False
    form = SQLFORM(db.acreditacion_profesor)

    if form.validate():
        db.acreditacion_profesor.insert(id_profesor=auth.user.id, **form.vars)
        plugin_toastr_message_config('success', T(
        'La evidencia se añadió correctamente'))
        redirect(URL('manage'))
    elif form.errors:
        plugin_toastr_message_config('error', T(
        'Existen errores en el formulario'))

    return dict(form=form)


@auth.requires(auth.has_membership('Profesor'))
def editar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.acreditacion_profesor(request.args(0, cast=int)
                          ) or redirect(URL('manage'))

    db.acreditacion_profesor.id_profesor.writable = False
    db.acreditacion_profesor.id_profesor.readable = False
    db.acreditacion_profesor.id.readable = False
    
    form = SQLFORM(db.acreditacion_profesor, registro)
    if form.validate():
        if form.vars['evidencia']:
            db(db.acreditacion_profesor.id == registro.id).update(**form.vars)
        else:
            db(db.acreditacion_profesor.id == registro.id).update(creditos=form.vars.creditos)

        plugin_toastr_message_config('success', T(
        'La evidencia se actualizó correctamente'))
        redirect(URL('manage'))
    elif form.errors:
        plugin_toastr_message_config('error', T(
        'Existen errores en el formulario'))

    return dict(form=form, registro=registro)


@auth.requires_membership('Profesor')
def eliminar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.acreditacion_profesor(request.args(0, cast=int)
                          ) or redirect(URL('manage'))

    db(db.acreditacion_profesor.id == registro.id).delete()

    plugin_toastr_message_config('success', T(
        'El registro se ha eliminado correctamente'))

    redirect(URL("manage"))

    return dict()