def login():
    form = SQLFORM.factory(
        Field('username', requires=IS_NOT_EMPTY()),
        Field('password', 'password', requires=[IS_NOT_EMPTY(), CRYPT()]),
    )

    if form.process(hideerror=True).accepted:
        username = form.vars.username
        password = form.vars.password
        user = auth.login_bare(username, password)

        if user:
            edicion_actual = db(db.edicion.activa == True).select().first()

            if not edicion_actual:
                plugin_toastr_message_config('success', T(
                    'No hay ediciones activas'))
            else:
                plugin_toastr_message_config('success', T(
                    'Bienvenido al sistema'))

            redirect(auth.settings.login_next)
        else:
            form.errors.credenciales = T('Credenciales incorrectas')
            plugin_toastr_message_config('error', T(
                'Usuario y/o Contraseña incorrectos'))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form)


def register():
    usuarios = db(db.auth_user.id > 0)
    require_username = [IS_NOT_EMPTY(), IS_NOT_IN_DB(
        usuarios, "auth_user.username"), IS_LENGTH(20)]
    require_email = [IS_NOT_EMPTY(), IS_EMAIL(
    ), IS_NOT_IN_DB(usuarios, "auth_user.email")]

    form = SQLFORM.factory(Field("first_name", label=T("Nombre(s)"), requires=IS_NOT_EMPTY()),
                           Field("last_name", label=T("Apellidos"),
                                 requires=IS_NOT_EMPTY()),
                           Field("username", label=T(
                               "Nombre de usuario"), requires=require_username),
                           Field("email", label=T("Correo electrónico"),
                                 requires=require_email),
                           Field("password", "password", label=T(
                               "Contraseña"), requires=[IS_NOT_EMPTY(), CRYPT()]),
                           Field("repeat", "password", label=T("Repetir contraseña"), requires=[
                               IS_EQUAL_TO(request.vars.password)]),

                           )

    if form.process(hideerror=True).accepted:
        user_id = db.auth_user.insert(**form.vars)
        group_id = db(db.auth_group.role == "Estudiante").select().first().id
        db.auth_membership.insert(
            user_id=user_id, group_id=group_id)
        plugin_toastr_message_config('success', T(
            'El registro se realizó correctamente'))
        redirect(URL("usuario", "login"))

    elif form.errors:
        plugin_toastr_message_config('error', T(
            'El formulario contiene errores'))

    return dict(form=form)


@auth.requires_login()
def logout():
    # Cierra la sesión del usuario dado
    auth.logout()
    return dict()


@auth.requires_login()
def perfil():
    usuario = db.auth_user(auth.user.id
                           ) or redirect(URL('usuario', 'login'))

    rol = db(db.auth_membership.user_id ==
             usuario.id).select().first().group_id.role

    form = SQLFORM.factory(Field("password", "password", label=T("Nueva Contraseña"), requires=[IS_NOT_EMPTY(), CRYPT()]),
                           Field("repeat", "password", label=T("Repetir contraseña"), requires=[
                               IS_EQUAL_TO(request.vars.password)]),
                           )

    if form.process(hideerror=True).accepted:
        db(db.auth_user.id == usuario.id).update(**form.vars)
        plugin_toastr_message_config('success', T(
            'Contraseña actualizada correctamente'))
        redirect(URL("perfil", args=usuario.id))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'El formulario contiene errores'))

    return dict(usuario=usuario, rol=rol, form=form)


@auth.requires_membership('Administrador')
def manage():
    usuarios = db((db.auth_user.id != auth.user.id) & (
        db.auth_user.username != "admin") &
        (db.auth_membership.user_id == db.auth_user.id)).select(db.auth_user.ALL, db.auth_membership.ALL)
    return dict(usuarios=usuarios)


@auth.requires(auth.has_membership('Administrador') or auth.has_membership('Coordinador'))
def detalles():
    if not request.args(0):
        redirect(URL('default', 'index'))

    usuario = db.auth_user(request.args(0, cast=int)
                           ) or redirect(URL('index'))

    rol = db(db.auth_membership.user_id ==
             usuario.id).select().first().group_id.role

    return dict(usuario=usuario, rol=rol)


@auth.requires_membership('Administrador')
def crear():
    usuarios = db(db.auth_user.id > 0)
    require_username = [IS_NOT_EMPTY(), IS_NOT_IN_DB(
        usuarios, "auth_user.username"), IS_LENGTH(20)]
    require_email = [IS_NOT_EMPTY(), IS_EMAIL(
    ), IS_NOT_IN_DB(usuarios, "auth_user.email")]

    form = SQLFORM.factory(Field("first_name", label=T("Nombre(s)"), requires=IS_NOT_EMPTY()),
                           Field("last_name", label=T("Apellidos"),
                                 requires=IS_NOT_EMPTY()),
                           Field("username", label=T(
                               "Nombre de usuario"), requires=require_username),
                           Field("email", label=T("Correo electrónico"),
                                 requires=require_email),
                           Field("password", "password", label=T(
                               "Contraseña"), requires=[IS_NOT_EMPTY(), CRYPT()]),
                           Field("repeat", "password", label=T("Repetir contraseña"), requires=[
                               IS_EQUAL_TO(request.vars.password)]),
                           Field("rol", "reference auth_group", label=T("Rol de usuario"),
                                 requires=IS_IN_DB(db, 'auth_group.id', '%(role)s', zero=T('Seleccionar rol'))),
                           Field("maestria", "reference maestria", label=T("Asociar Maestría"),
                                 requires=IS_EMPTY_OR(IS_IN_DB(db, 'maestria.id', '%(nombre)s', zero=T('Seleccionar maestría'))
                                                      )
                                 ),
                           )

    if form.validate(keepvalues=True):
        if form.vars.rol == 2 and not form.vars.maestria:
            form.errors.maestria = 'Seleccione una maestría'
            plugin_toastr_message_config('error', T(
                'El formulario contiene errores'))
        else:
            user_id = db.auth_user.insert(**form.vars)
            db.auth_membership.insert(
                user_id=user_id, group_id=form.vars.rol)

            if form.vars.rol == 2:
                db.coordinador_maestria.insert(
                    id_maestria=form.vars.maestria, id_user=user_id)

            plugin_toastr_message_config('success', T(
                'Usuario creado correctamente'))
            redirect(URL("usuario", "manage"))

    elif form.errors:
        plugin_toastr_message_config('error', T(
            'El formulario contiene errores'))

    return dict(form=form)


@auth.requires_membership("Administrador")
def editar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.auth_user(request.args(0, cast=int)
                            ) or redirect(URL('manage'))

    usuarios = db(db.auth_user.id != registro.id)
    require_username = [IS_NOT_EMPTY(), IS_NOT_IN_DB(
        usuarios, "auth_user.username"), IS_LENGTH(20)]
    require_email = [IS_NOT_EMPTY(), IS_EMAIL(
    ), IS_NOT_IN_DB(usuarios, "auth_user.email")]

    rol_id = db(db.auth_membership.user_id ==
                registro.id).select().first().group_id.id

    maestria = db(db.coordinador_maestria.id_user ==
                  registro.id).select()

    form = SQLFORM.factory(Field("first_name", label=T("Nombre(s)"), default=registro.first_name,
                                 requires=IS_NOT_EMPTY()),
                           Field("last_name", label=T(
                               "Apellidos"), default=registro.last_name, requires=IS_NOT_EMPTY()),
                           Field("username", label=T(
                               "Nombre de usuario"), default=registro.username, requires=require_username),
                           Field("email", label=T("Correo electrónico"),
                                 default=registro.email, requires=require_email),
                           Field("rol", "reference auth_group", label=T("Rol de usuario"),
                                 default=rol_id, requires=IS_IN_DB(db, 'auth_group.id', '%(role)s',
                                                                   zero=T('Seleccionar rol'))),
                           Field("maestria", "reference maestria", label=T("Asociar Maestría"),
                                 default=maestria.first().id_maestria if maestria else None,
                                 requires=IS_EMPTY_OR(IS_IN_DB(db, 'maestria.id', '%(nombre)s', zero=T('Seleccionar maestría'))
                                                      )
                                 ),
                           )

    if form.validate(keepvalues=True):
        if form.vars.rol == 2 and not form.vars.maestria:
            form.errors.maestria = 'Seleccione una maestría'
            plugin_toastr_message_config('error', T(
                'El formulario contiene errores'))
        else:
            db(db.auth_user.id == registro.id).update(**form.vars)
            db(db.auth_membership.user_id == registro.id).update(
                group_id=form.vars.rol)

            if form.vars.rol == 2:
                if db(db.coordinador_maestria.id_user == registro.id).select():
                    db(db.coordinador_maestria.id_user == registro.id).update(
                        id_maestria=form.vars.maestria)
                else:
                    db.coordinador_maestria.insert(
                        id_maestria=form.vars.maestria, id_user=registro.id)

            else:
                db(db.coordinador_maestria.id_user == registro.id).delete()

            plugin_toastr_message_config('success', T(
                'Usuario actualizado correctamente'))
            redirect(URL("detalles", args=registro.id))
    elif form.errors:
        plugin_toastr_message_config('error', T(
            'El formulario contiene errores'))

    return dict(form=form, registro=registro)


@auth.requires_membership("Administrador")
def eliminar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.auth_user(request.args(0, cast=int)
                            ) or redirect(URL('manage'))
    x = registro.id

    if not registro.username == "admin":
        db(db.auth_user.id == x).delete()
        plugin_toastr_message_config('success', T(
            'Usuario eliminado correctamente'))

    redirect(URL("manage"))
    return dict()


@auth.requires_membership("Administrador")
def cambiar_clave():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    registro = db.auth_user(request.args(0, cast=int)
                            ) or redirect(URL('manage'))

    form = SQLFORM.factory(Field("password", "password", label=T("Nueva Contraseña"), requires=[IS_NOT_EMPTY(), CRYPT()]),
                           Field("repeat", "password", label=T("Repetir contraseña"), requires=[
                               IS_EQUAL_TO(request.vars.password)]),
                           )

    if form.process(hideerror=True).accepted:
        db(db.auth_user.id == registro.id).update(**form.vars)
        plugin_toastr_message_config('success', T(
            'Contraseña actualizada correctamente'))
        redirect(URL("detalles", args=registro.id))

    elif form.errors:
        plugin_toastr_message_config('error', T(
            'El formulario contiene errores'))

    return dict(form=form, registro=registro)


@auth.requires_login()
def no_autorizado():
    return locals()
