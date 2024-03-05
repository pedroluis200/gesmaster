from datetime import timedelta


@auth.requires_login()
def index():
    usuario = db.auth_user(auth.user.id
                           ) or redirect(URL('dashboard', 'index'))

    rol = db(db.auth_membership.user_id ==
             usuario.id).select().first().group_id.role

    four_months_ago = timedelta(days=120)

    db((db.notificacion.id_user == auth.user.id)
       & (db.notificacion.fecha < db.notificacion.fecha - four_months_ago)).delete()

    return dict(rol=rol)


@auth.requires_login()
def notificaciones():
    list_notify = db((db.notificacion.id_user == auth.user.id)
                     & (db.notificacion.leido == False)).select(orderby=~db.notificacion.fecha)
    return dict(list_notify=list_notify)


@auth.requires_membership('Administrador')
def administrador():
    maestrias = db(db.maestria.id > 0).count()
    coordinadores = db((db.auth_membership.group_id == db.auth_group.id) &
                       (db.auth_group.role == 'Coordinador')).count()
    profesores = db((db.auth_membership.group_id == db.auth_group.id) &
                    (db.auth_group.role == 'Profesor')).count()
    estudiantes = db((db.auth_membership.group_id == db.auth_group.id) &
                     (db.auth_group.role == 'Estudiante')).count()
    return dict(maestrias=maestrias, coordinadores=coordinadores, profesores=profesores, estudiantes=estudiantes)


@auth.requires_membership('Coordinador')
def coordinador():
    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()

    def query(estado): return db((db.admision.id_edicion == edicion_actual.id_edicion) &
                                 (db.admision.estado == estado)
                                 )

    admisiones_pendientes_list = query('Pendiente').select()
    admisiones_pendientes_count = query('Pendiente').count()

    matricula = query('Aprobado').count()

    tesis_pendientes = db((db.admision.id_edicion == edicion_actual.id) &
                          (db.admision.id == db.tesis.id_admision) &
                          (db.tesis.estado == 'Pendiente')
                          ).select()

    profesores = db((db.actividad_edicion.id_profesor == db.auth_user.id) &
                    (db.actividad_edicion.id_edicion == edicion_actual.id_edicion)).select(groupby=db.auth_user.id)

    return dict(admisiones_pendientes=admisiones_pendientes_count,
                matricula=matricula, edicion_actual=edicion_actual,
                admisiones=admisiones_pendientes_list, tesis_pendientes=tesis_pendientes,
                profesores=profesores)


@auth.requires_membership('Estudiante')
def estudiante():
    maestrias = db((db.edicion.id_maestria == db.maestria.id) &
                   (db.edicion.matricula_abierta == True)).select()

    maestrias = maestrias.find(lambda row: row.edicion.esta_llena == False)

    admision_enviada = db(db.admision.id_user == auth.user.id).select()

    coordinadores = db((db.auth_user.id == db.auth_membership.user_id) & (
        db.auth_membership.group_id == db.auth_group.id) & (db.auth_group.role == 'Coordinador')).select()

    if admision_enviada:
        admision_enviada = admision_enviada.first()

    tesis_row = db((db.admision.id_user == auth.user.id) &
                   (db.tesis.id_admision == db.admision.id)
                   ).select().first()

    return dict(maestrias=maestrias, admision_enviada=admision_enviada,
                coordinadores=coordinadores,
                tesis=tesis_row.tesis if tesis_row else None,
                )


@auth.requires_membership('Profesor')
def profesor():
    asignaturas = db((db.actividad_edicion.id_profesor == auth.user.id) &
                     (db.actividad_edicion.id_edicion == db.edicion.id) &
                     (db.edicion.activa == True)).count()
    
    tutorias = db((db.tesis.tutor == auth.user.id) &
               (db.tesis.id_admision == db.admision.id) &
               (db.admision.id_edicion == db.edicion.id) &
               (db.edicion.activa == True)).count()
    
    creditos = db.auth_user(auth.user.id).total_creditos

    sin_calificar = db((db.actividad_edicion.id_profesor == auth.user.id) &
                     (db.actividad_edicion.id_edicion == db.edicion.id) &
                     (db.edicion.activa == True)).select()
    
    count_sin_calificar = 0

    for act in sin_calificar:
        if not db(db.calificacion.id_actividad_edicion == act.actividad_edicion.id).select():
            count_sin_calificar += 1
    
    return dict(asignaturas=asignaturas, tutorias=tutorias, creditos=creditos, no_calificado=count_sin_calificar)
