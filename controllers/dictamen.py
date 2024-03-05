import query_db


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_solicitud_admision():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id_edicion) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_admision():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id_edicion) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def generar_admision():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    admision = db.admision(request.args(0, cast=int)
                           ) or redirect(URL('dashboard', 'index'))

    centro = query_db.get_centro(db)

    return dict(admision=admision, centro=centro)


@auth.requires(auth.has_membership('Coordinador'))
def generar_bajas():
    edicion_actual = query_db.get_edicion_actual(db, auth)

    centro = query_db.get_centro(db)

    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Baja') &
                    (db.admision.id == db.baja.id_admision)
                    ).select()

    return dict(admisiones=admisiones, edicion=edicion_actual.id_edicion, centro=centro)


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_tesis():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    temas = db((db.admision.id_edicion == edicion_actual.id_edicion) &
               (db.admision.id == db.tesis.id_admision) &
               (db.tesis.tutor > 0) &
               (db.tesis.estado == 'Aprobado')
               ).select()

    return dict(temas=temas)


@auth.requires(auth.has_membership('Coordinador'))
def generar_dictamen_tesis():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    tesis = db.tesis(request.args(0, cast=int)
                     ) or redirect(URL('dashboard', 'index'))

    return dict(tesis=tesis, edicion=query_db.get_edicion_actual(db, auth).id_edicion)


@auth.requires(auth.has_membership('Coordinador'))
def generar_actividades():
    centro = query_db.get_centro(db)
    edicion_actual = query_db.get_edicion_actual(db, auth)
    id_edicion = edicion_actual.id
    actividades = db(db.actividad_edicion.id_edicion == id_edicion).select()

    obligatorias = db((db.actividad_edicion.id_edicion == id_edicion) &
                      (db.actividad_edicion.id_actividad == db.actividad.id) &
                      (db.actividad.tipo == 'Lectiva') &
                      (db.actividad.optativo == False))
    optativas = db((db.actividad_edicion.id_edicion == id_edicion) &
                   (db.actividad_edicion.id_actividad == db.actividad.id) &
                   (db.actividad.tipo == 'Lectiva') &
                   (db.actividad.optativo == True))

    no_lectivas = db((db.actividad_edicion.id_edicion == id_edicion) &
                     (db.actividad_edicion.id_actividad == db.actividad.id) &
                     (db.actividad.tipo == 'No lectiva'))

    return dict(centro=centro, edicion=edicion_actual.id_edicion, actividades=actividades, obligatorias=obligatorias, optativas=optativas, no_lectivas=no_lectivas)


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_no_lectivos():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def generar_no_lectivos():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    estudiante = db.admision(request.args(0, cast=int)
                             ) or redirect(URL('dashboard', 'index'))

    centro = query_db.get_centro(db)

    edicion_actual = query_db.get_edicion_actual(db, auth)

    total_creditos = db.actividad_edicion.creditos.sum()

    no_lectivas = db((db.calificacion.id_estudiante == estudiante.id) &
                     (db.calificacion.id_actividad_edicion == db.actividad_edicion.id) &
                     (db.actividad_edicion.id == db.actividad.id) &
                     (db.actividad.tipo == 'No lectiva'))

    return dict(centro=centro, estudiante=estudiante,
                edicion_actual=edicion_actual,
                list_no_lectivas=no_lectivas.select(),
                count_no_lectivas=no_lectivas.count(),
                total_creditos=no_lectivas.select(
                    total_creditos).first()[total_creditos]
                )


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_suficiencia():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def generar_dictamen_suficiencia():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    estudiante = db.admision(request.args(0, cast=int)
                             ) or redirect(URL('dashboard', 'index'))

    centro = query_db.get_centro(db)

    edicion_actual = query_db.get_edicion_actual(db, auth)

    return dict(centro=centro, estudiante=estudiante,
                edicion_actual=edicion_actual,
                )


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_convalidacion():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def generar_dictamen_convalidacion():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    estudiante = db.admision(request.args(0, cast=int)
                             ) or redirect(URL('dashboard', 'index'))

    centro = query_db.get_centro(db)

    edicion_actual = query_db.get_edicion_actual(db, auth)

    return dict(centro=centro, estudiante=estudiante,
                edicion_actual=edicion_actual,
                )


@auth.requires(auth.has_membership('Coordinador'))
def generar_acta_defensa():
    centro = query_db.get_centro(db)

    return dict(centro=centro)


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_cierre_expediente():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def generar_cierre_expediente():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    estudiante = db.admision(request.args(0, cast=int)
                             ) or redirect(URL('dashboard', 'index'))

    centro = query_db.get_centro(db)

    edicion_actual = query_db.get_edicion_actual(db, auth)

    return dict(centro=centro, estudiante=estudiante,
                edicion_actual=edicion_actual,
                )


@auth.requires(auth.has_membership('Coordinador'))
def generar_matricula_oficial():
    centro = query_db.get_centro(db)
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones, centro=centro, edicion_actual=edicion_actual)


@auth.requires(auth.has_membership('Coordinador'))
def generar_calendario_oficial():
    centro = query_db.get_centro(db)
    edicion_actual = query_db.get_edicion_actual(db, auth)
    maestria_nombre = db.maestria(edicion_actual.id_edicion.id_maestria).nombre
    actividades = db(db.actividad_edicion.id_edicion ==
                     edicion_actual.id).select()
    return dict(actividades=actividades, centro=centro, edicion_actual=edicion_actual, maestria_nombre=maestria_nombre)


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_evaluacion_actividades():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    id_edicion = edicion_actual.id
    actividades = db(db.actividad_edicion.id_edicion == id_edicion).select()

    return dict(actividades=actividades)


@auth.requires(auth.has_membership('Coordinador'))
def generar_evaluacion_actividades():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    centro = query_db.get_centro(db)

    actividad_edicion = db.actividad_edicion(request.args(0, cast=int)
                                             ) or redirect(URL('dashboard', 'index'))

    calificaciones = db((db.admision.id_edicion == actividad_edicion.id_edicion) &
                        (db.admision.estado == "Aprobado")).select()

    return dict(centro=centro, actividad_edicion=actividad_edicion, calificaciones=calificaciones, get_calificacion=query_db.get_calificacion)


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_tribunal():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def generar_tribunal():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    estudiante = db.admision(request.args(0, cast=int)
                             ) or redirect(URL('dashboard', 'index'))

    centro = query_db.get_centro(db)
    edicion_actual = query_db.get_edicion_actual(db, auth)
    maestria_nombre = db.maestria(edicion_actual.id_edicion.id_maestria).nombre
    return dict(estudiante=estudiante, centro=centro, edicion_actual=edicion_actual,
                maestria_nombre=maestria_nombre)


@auth.requires(auth.has_membership('Coordinador'))
def generar_otorgamiento():
    centro = query_db.get_centro(db)
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones, centro=centro, edicion_actual=edicion_actual)


@auth.requires(auth.has_membership('Coordinador'))
def generar_otorgamiento():
    centro = query_db.get_centro(db)
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones, centro=centro, edicion_actual=edicion_actual)


@auth.requires(auth.has_membership('Coordinador'))
def generar_graduados():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones, edicion_actual=edicion_actual, get_tesis=query_db.get_tesis)


@auth.requires(auth.has_membership('Coordinador'))
def generar_cierre_edicion():
    centro = query_db.get_centro(db)
    edicion_actual = query_db.get_edicion_actual(db, auth)

    matricula_inicial = db((db.admision.id_edicion == edicion_actual.id) &
                           (db.admision.estado == 'Aprobado') |
                           (db.admision.estado == 'Baja')).count()
    matricula_final = db((db.admision.id_edicion == edicion_actual.id) &
                         (db.admision.estado == 'Aprobado')).count()

    porciento_matricula = (matricula_final / matricula_inicial) * \
        100 if matricula_inicial > 0 else 0
    porciento_matricula = "{:.1f}".format(porciento_matricula)

    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    sum = db.actividad_edicion.creditos.sum()
    creditos = db(db.actividad_edicion.id_edicion ==
                  edicion_actual.id_edicion).select(sum).first()[sum]
    return dict(admisiones=admisiones, centro=centro, edicion_actual=edicion_actual,
                meses=meses, creditos=creditos, matricula_inicial=matricula_inicial,
                matricula_final=matricula_final, porciento_matricula=porciento_matricula)


@auth.requires(auth.has_membership('Coordinador'))
def generar_dictamen_consejo():
    centro = query_db.get_centro(db)
    edicion_actual = query_db.get_edicion_actual(db, auth)

    matricula = db((db.admision.id_edicion == edicion_actual.id) &
                   (db.admision.estado == 'Aprobado') |
                   (db.admision.estado == 'Baja')).count()

    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)

    fecha_inicio = edicion_actual.id_edicion.fecha_inicio.strftime('%d/%m/%Y')
    fecha_fin = edicion_actual.id_edicion.fecha_fin.strftime('%d/%m/%Y')

    fecha = ' - '.join([fecha_inicio, fecha_fin])

    return dict(admisiones=admisiones, centro=centro, edicion_actual=edicion_actual,
                matricula=matricula, fecha=fecha)


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_certificado():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def generar_certificado():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    estudiante = db.admision(request.args(0, cast=int)
                             ) or redirect(URL('dashboard', 'index'))

    centro = query_db.get_centro(db)
    edicion_actual = query_db.get_edicion_actual(db, auth)
    maestria_nombre = db.maestria(edicion_actual.id_edicion.id_maestria).nombre

    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    return dict(estudiante=estudiante, centro=centro, edicion_actual=edicion_actual,
                maestria_nombre=maestria_nombre, meses=meses)


@auth.requires(auth.has_membership('Coordinador'))
def dictamen_certificacion_calificaciones():
    edicion_actual = query_db.get_edicion_actual(db, auth)
    admisiones = db((db.admision.id_edicion == edicion_actual.id) &
                    (db.admision.estado == 'Aprobado')).select(db.admision.ALL)
    return dict(admisiones=admisiones)


@auth.requires(auth.has_membership('Coordinador'))
def generar_certificacion_calificaciones():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    estudiante = db.admision(request.args(0, cast=int)
                             ) or redirect(URL('dashboard', 'index'))

    centro = query_db.get_centro(db)
    edicion_actual = query_db.get_edicion_actual(db, auth)
    maestria_nombre = db.maestria(edicion_actual.id_edicion.id_maestria).nombre

    calificaciones = db(db.calificacion.id_estudiante == estudiante.id).select()

    return dict(estudiante=estudiante, centro=centro, edicion_actual=edicion_actual,
                maestria_nombre=maestria_nombre, calificaciones=calificaciones)
