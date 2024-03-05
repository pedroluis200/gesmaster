def get_centro(db):
    return db(db.settings.id > 0).select().first().centro

def get_edicion_actual(db, auth):
    return db(db.edicion_actual.id_user == auth.user.id).select().first()

def get_calificacion(db, id_actividad_edicion, id_estudiante):
    calificacion = db((db.calificacion.id_actividad_edicion == id_actividad_edicion) &
                      (db.calificacion.id_estudiante == id_estudiante)).select().first()
    return calificacion

def get_tesis(db, id_estudiante):
    tesis = db.tesis(id_admision=id_estudiante)
    return tesis
