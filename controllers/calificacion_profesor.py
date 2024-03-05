from query_db import get_calificacion


@auth.requires_membership('Profesor')
def select_maestria():
    maestrias = db((db.actividad_edicion.id_profesor == auth.user.id) &
                   (db.actividad_edicion.id_edicion == db.edicion.id) &
                   (db.edicion.activa == True) &
                   (db.maestria.id == db.edicion.id_maestria)).select(groupby=db.maestria.id)
    return dict(maestrias=maestrias)


@auth.requires_membership('Profesor')
def select_edicion():
    if not request.args(0):
        redirect(URL('select_maestria'))

    maestria = db.maestria(request.args(0, cast=int)
                           ) or redirect(URL('select_maestria'))

    session.id_maestria = maestria.id

    ediciones = db((db.actividad_edicion.id_profesor == auth.user.id) &
                   (db.actividad_edicion.id_edicion == db.edicion.id) &
                   (db.edicion.activa == True) &
                   (db.maestria.id == maestria.id)).select(groupby=db.edicion.id)

    return dict(ediciones=ediciones, maestria=maestria)


@auth.requires_membership('Profesor')
def select_actividad():
    if not request.args(0) or not session.id_maestria:
        redirect(URL('select_maestria'))

    edicion = db.edicion(request.args(0, cast=int)
                         ) or redirect(URL('select_edicion', args=session.id_maestria))

    session.id_edicion = edicion.id

    actividades = db((db.actividad_edicion.id_profesor == auth.user.id) &
                     (db.actividad_edicion.id_edicion == edicion.id)).select()

    return dict(actividades=actividades, edicion=edicion)


@auth.requires_membership('Profesor')
def calificar():
    if not request.args(0) or not session.id_edicion:
        redirect(URL('seleccionar_actividad'))

    # Mostrar mensaje en caso de que se califique el estudiante
    if session.show_calificado_msg:
        plugin_toastr_message_config('success', T(
            'Se ha calificado correctamente'))
        session.show_calificado_msg = False
    
    session.id_actividad_edicion = request.args(0, cast=int)

    actividad_edicion = db.actividad_edicion(request.args(0, cast=int)
                                             ) or redirect(URL('seleccionar_actividad', args=session.id_edicion))

    calificaciones = db((db.admision.id_edicion == actividad_edicion.id_edicion) &
                        (db.admision.estado == "Aprobado")).select()

    return dict(calificaciones=calificaciones, actividad_edicion=actividad_edicion, get_calificacion=get_calificacion)


@auth.requires_membership('Profesor')
def send_calificacion():
    db.calificacion.id_actividad_edicion.writable = False
    db.calificacion.id_estudiante.writable = False

    id_actividad_edicion = request.vars['id_actividad_edicion']
    id_estudiante = request.vars['id_estudiante']

    calificacion = db((db.calificacion.id_actividad_edicion == id_actividad_edicion) &
                      (db.calificacion.id_estudiante == id_estudiante)).select().first()

    form = SQLFORM(db.calificacion) if not calificacion else SQLFORM(
        db.calificacion, calificacion)

    if form.validate():
        if not calificacion:
            db.calificacion.insert(
                nota=form.vars.nota,
                tipo=form.vars.tipo,
                id_actividad_edicion=id_actividad_edicion,
                id_estudiante=id_estudiante
            )
        else:
            calificacion.update_record(
                nota=form.vars.nota,
                tipo=form.vars.tipo,
            )

        session.show_calificado_msg = True

        redirect(request.env.http_web2py_component_location, client_side=True)

    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form)




@auth.requires(auth.has_membership('Profesor'))
def eliminar_calificacion():
    if not request.args(0) or not session.id_actividad_edicion:
        redirect(URL('select_maestria'))

    registro = db.calificacion(request.args(0, cast=int)
                           ) or redirect(URL('select_maestria'))
    x = registro.id

    db(db.calificacion.id == x).delete()

    plugin_toastr_message_config('success', T(
        'Calificación eliminada correctamente'))

    redirect(URL("calificar", args=session.id_actividad_edicion))
    return dict()
