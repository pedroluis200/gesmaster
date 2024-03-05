@auth.requires(auth.has_membership('Administrador') or auth.has_membership('Coordinador'))
def sistema_mantenimiento():
    settings = db(db.settings.id > 0).select().first()
    mantenimiento = settings.en_mantenimiento
    return dict(mantenimiento=mantenimiento)


@auth.requires(auth.has_membership('Administrador') or auth.has_membership('Coordinador'))
def cambiar_mantenimiento():
    settings = db(db.settings.id > 0).select().first()
    mantenimiento = settings.en_mantenimiento
    settings.update_record(en_mantenimiento=not mantenimiento)

    if not mantenimiento:
        plugin_toastr_message_config('success', T(
            'El sistema está en mantenimiento'))
    else:
        plugin_toastr_message_config('success', T(
            'El sistema está activo'))

    redirect(URL('dashboard', 'index'))
    return dict()


@auth.requires_login()
def en_mantenimiento():
    return dict()


@auth.requires_membership('Coordinador')
def coordinador_configuracion():
    usuario = db.auth_user(auth.user.id)
    requires = IS_IN_DB(db(db.edicion.id_maestria ==
                        usuario.maestria_usuario.id_maestria), 'edicion.id', '%(numero)s')

    form = SQLFORM.factory(
        Field('edicion', 'reference edicion',
              label='Edición de Maestría',
              default=db.edicion_actual(id_user=usuario.id).id_edicion,
              requires=requires),
    )

    if form.validate(keepvalues=True):
        db(db.edicion_actual.id_user == usuario.id).update(id_edicion=form.vars.edicion)
        plugin_toastr_message_config('success', T(
            'La configuración se ha guardado correctamente.'))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form)


@auth.requires_membership('Administrador')
def administrador_configuracion():
    centro = db.settings(db.settings.id > 0).centro

    form = SQLFORM.factory(
        Field('centro', 'string',
              label='Nombre del centro',
              default=centro,
              requires=IS_NOT_EMPTY()),
    )

    if form.validate(keepvalues=True):
        db(db.settings.id > 0).update(centro=form.vars.centro)
        plugin_toastr_message_config('success', T(
            'La configuración se ha guardado correctamente.'))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form)
