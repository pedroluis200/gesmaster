import query_db

@auth.requires_membership('Coordinador')
def manage():
    coordinador = db.auth_user(auth.user.id)
    ediciones = db(db.edicion.id_maestria ==
                   coordinador.maestria_usuario.id_maestria).select()
    return dict(ediciones=ediciones)


@auth.requires(auth.has_membership('Coordinador'))
def detalles():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    edicion = db.edicion(request.args(0, cast=int)
                         ) or redirect(URL('dashboard', 'index'))

    return dict(edicion=edicion)

###################################################################
# Las funciones a continuación son privadas
# y se usan en los controladores crear, editar y cambiar_matricula
###################################################################


def __close_all_matriculas():
    usuario = db.auth_user(auth.user.id)
    maestria = usuario.maestria_usuario.id_maestria

    db((db.edicion.id_maestria == maestria) & (
        db.edicion.matricula_abierta == True)).update(matricula_abierta=False)


def __create_edicion(form):
    if form.vars.matricula_abierta:
        __close_all_matriculas()

    coordinador = db(db.coordinador_maestria.id_user ==
                     auth.user.id).select().first()
    id_edicion = db.edicion.insert(
        id_maestria=coordinador.id_maestria, **form.vars)

    if not db(db.edicion_actual.id_user == coordinador.id_user).select():
        db.edicion_actual.insert(
            id_edicion=id_edicion, id_user=coordinador.id_user)

    plugin_toastr_message_config('success', T(
        'La edición se ha creado correctamente.'))

    redirect(URL('manage'))


def __edit_edicion(form, registro):
    if form.vars.matricula_abierta:
        __close_all_matriculas()
    
    registro.update_record(**form.vars)

    plugin_toastr_message_config('success', T(
        'La edición se ha editado correctamente.'))

    redirect(URL('manage'))



def __throw_error():
    return plugin_toastr_message_config('error', T(
        'Existen errores en el formulario'))

###################################################

@auth.requires_membership('Coordinador')
def crear():
    form = SQLFORM(db.edicion)
    usuario = db.auth_user(auth.user.id)

    if form.validate(keepvalues=True):
        date1 = form.vars.fecha_inicio
        date2 = form.vars.fecha_fin

        if date1 < date2:
            maestria = usuario.maestria_usuario.id_maestria

            # Verificar que no exista una edicion de esta maestria
            # con el mismo numero
            if db((db.edicion.id_maestria == maestria.id) & (db.edicion.numero == form.vars.numero)).select():
                form.errors.numero = 'Este número se encuentra registrado'
                __throw_error()
            else:
                __create_edicion(form)
        else:
            form.errors.fecha_fin = 'La fecha final debe ser mayor a la inicial'
            __throw_error()
    elif form.errors:
        __throw_error()

    return dict(form=form)


@auth.requires_membership('Coordinador')
def editar():
    if not request.args(0):
        redirect(URL('manage'))
    
    edicion_actual = query_db.get_edicion_actual(db, auth)

    registro = db.edicion(request.args(0, cast=int)
                          ) or redirect(URL('manage'))

    if registro.esta_llena:
        db.edicion.matricula_abierta.writable = False

    form = SQLFORM(db.edicion, registro)

    if form.validate(keepvalues=True):
        date1 = form.vars.fecha_inicio
        date2 = form.vars.fecha_fin

        if date1 < date2:
            # Verificar que no exista una edicion de esta maestria
            # con el mismo numero
            if db((db.edicion.id_maestria == registro.id_maestria) &
                  (db.edicion.numero == form.vars.numero) &
                  (db.edicion.numero != registro.numero)).select():
                form.errors.numero = 'Este número se encuentra registrado'
                __throw_error()
            else:
                __edit_edicion(form, registro)
        else:
            form.errors.fecha_fin = 'La fecha final debe ser mayor a la inicial'
            __throw_error()
    elif form.errors:
        __throw_error()

    return dict(form=form, registro=registro, edicion_actual=edicion_actual)


@auth.requires_membership('Coordinador')
def eliminar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.edicion(request.args(0, cast=int)
                          ) or redirect(URL('manage'))

    db(db.edicion.id == registro.id).delete()

    # En caso de que esta sea la edicion activa en la vista de la aplicacion
    # seleccionar la que le sigue

    ediciones = db(db.edicion.id_maestria == registro.id_maestria).select()

    if not db(db.edicion_actual.id_user == auth.user.id).select() and ediciones:
        db.edicion_actual.insert(
            id_edicion=ediciones.first().id, id_user=auth.user.id)

    plugin_toastr_message_config('success', T(
        'La edición se ha eliminado correctamente'))

    redirect(URL("manage"))

    return dict()


@auth.requires_membership('Coordinador')
def activar_edicion():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.edicion(request.args(0, cast=int)
                          ) or redirect(URL('manage'))

    registro.update_record(activa=True)

    plugin_toastr_message_config('success', T(
        'La edición se ha activado correctamente'))
    redirect(URL('manage'))
    return dict()


@auth.requires_membership('Coordinador')
def archivar_edicion():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.edicion(request.args(0, cast=int)
                          ) or redirect(URL('manage'))

    registro.update_record(activa=False, matricula_abierta=False)

    plugin_toastr_message_config('success', T(
        'La edición se ha archivado correctamente'))
    redirect(URL('manage'))
    return dict()


@auth.requires_membership('Coordinador')
def cambiar_matricula():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.edicion(request.args(0, cast=int)
                          ) or redirect(URL('manage'))
    
    if registro.esta_llena:
        redirect(URL('manage'))

    if registro.matricula_abierta:
        plugin_toastr_message_config('success', T(
            'La matrícula se ha cerrado correctamente'))
    else:
        __close_all_matriculas()
        plugin_toastr_message_config('success', T(
            'La matrícula se abrió correctamente'))

    registro.update_record(matricula_abierta=not registro.matricula_abierta)

    redirect(URL('manage'))
    return dict()


def no_edicion():
    return dict()
