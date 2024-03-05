def __cantidad_actividades(id_profesor):
    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()
    asignaturas = db((db.actividad_edicion.id_profesor == id_profesor) &
                     (db.actividad_edicion.id_edicion == edicion_actual.id_edicion))

    return asignaturas.count()


@auth.requires(auth.has_membership('Coordinador'))
def manage():
    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()
    profesores = db((db.actividad_edicion.id_profesor == db.auth_user.id) &
                    (db.actividad_edicion.id_edicion == edicion_actual.id_edicion)).select(groupby=db.auth_user.id)
    return dict(profesores=profesores, cantidad_actividades=__cantidad_actividades)


@auth.requires(auth.has_membership('Coordinador'))
def creditos():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    profesor = db.auth_user(request.args(0, cast=int)
                            ) or redirect(URL('dashboard', 'index'))
    creditos = db(db.acreditacion_profesor.id_profesor == profesor.id).select()
    return dict(creditos=creditos)


@auth.requires(auth.has_membership('Coordinador'))
def actividades():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    profesor = db.auth_user(request.args(0, cast=int)
                            ) or redirect(URL('dashboard', 'index'))

    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()

    actividades = db((db.actividad_edicion.id_profesor == profesor.id) &
                     (db.actividad_edicion.id_edicion == edicion_actual.id_edicion)).select()

    return dict(actividades=actividades, profesor=profesor)



@auth.requires(auth.has_membership('Coordinador'))
def eliminar_actividad():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.actividad(request.args(0, cast=int)
                          ) or redirect(URL('manage'))

    db(db.actividad.id == registro.id).delete()

    plugin_toastr_message_config('success', T(
        'La actividad se ha eliminado correctamente'))

    redirect(URL("actividades", args=request.vars['profesor']))

    return dict()