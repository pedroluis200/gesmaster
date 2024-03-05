from query_db import get_calificacion


@auth.requires_membership('Estudiante')
def calificaciones():
    estudiante = db.admision(id_user=auth.user.id) or redirect(
        URL('dashboard', 'index'))

    actividades_edicion = db(
        db.actividad_edicion.id_edicion == estudiante.id_edicion).select()

    return dict(estudiante=estudiante, actividades_edicion=actividades_edicion, get_calificacion=get_calificacion)
