from query_db import get_calificacion, get_edicion_actual


@auth.requires(auth.has_membership('Coordinador'))
def asignaturas():
    id_edicion = get_edicion_actual(db, auth)
    actividades = db(db.actividad_edicion.id_edicion == id_edicion).select()
    return dict(actividades=actividades)


@auth.requires(auth.has_membership('Coordinador'))
def calificaciones():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    edicion = get_edicion_actual(db, auth)

    actividad_edicion = db.actividad_edicion(request.args(0, cast=int)
                                             ) or redirect(URL('dashboard', 'index'))

    if edicion.id != actividad_edicion.id_edicion:
        redirect(URL('dashboard', 'index'))

    estudiantes = db(db.admision.id > 0).select()

    return dict(actividad_edicion=actividad_edicion, estudiantes=estudiantes, get_calificacion=get_calificacion)
