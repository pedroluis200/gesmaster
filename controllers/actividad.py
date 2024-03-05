@auth.requires(auth.has_membership('Coordinador'))
def manage():
    actividades = db(db.actividad.id > 0).select()
    return dict(actividades=actividades)


@auth.requires(auth.has_membership('Coordinador'))
def crear():
    form = SQLFORM(db.actividad)

    if form.process(keepvalues=True).accepted:
        plugin_toastr_message_config('success', T(
            'Actividad creada correctamente'))    
        
        redirect(URL('manage'))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form)


@auth.requires(auth.has_membership('Coordinador'))
def editar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.actividad(request.args(0, cast=int)
                          ) or redirect(URL('manage'))
    
    db.actividad.id.readable = False

    form = SQLFORM(db.actividad, registro)

    if form.process(keepvalues=True).accepted:
        plugin_toastr_message_config('success', T(
            'Actividad editada correctamente'))        
        redirect(URL('manage'))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form)


@auth.requires(auth.has_membership('Coordinador'))
def eliminar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.actividad(request.args(0, cast=int)
                          ) or redirect(URL('manage'))

    db(db.actividad.id == registro.id).delete()

    plugin_toastr_message_config('success', T(
        'La actividad se ha eliminado correctamente'))

    redirect(URL("manage"))

    return dict()

