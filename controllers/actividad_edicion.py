from query_db import get_edicion_actual


@auth.requires(auth.has_membership('Coordinador'))
def manage():
    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()
    actividades = db(db.actividad_edicion.id_edicion ==
                     edicion_actual.id_edicion).select()
    return dict(actividades=actividades)


@request.restful()
def api_get_actividades():
    response.view = 'generic.json'

    def GET(*args, **vars):
        edicion_actual = get_edicion_actual(db, auth)
        actividades = db(db.actividad_edicion.id_edicion ==
                     edicion_actual.id_edicion).select()
        
        actividades_list = []

        for act in actividades:
            actividades_list.append({
                'id': act.id,
                'actividad': act.id_actividad.nombre,
                'tipo': act.id_actividad.tipo,
                'creditos': act.creditos, 
            })


        return dict(actividades=actividades_list)

    return locals()

@auth.requires(auth.has_membership('Coordinador'))
def detalles():
    if not request.args(0):
        redirect(URL('dashboard', 'index'))

    actividad_edicion = db.actividad_edicion(request.args(0, cast=int)
                                             ) or redirect(URL('dashboard', 'index'))

    return dict(actividad=actividad_edicion)


def __notificar_profesor(id_profesor, edicion):
    notificacion_data = {
        'titulo': 'Nueva actividad asociada',
        'descripcion': f'Se le ha asociado una actividad en la edición #{edicion.numero} de la maestría {edicion.id_maestria.nombre}.',
        'tipo': 'info',
        'id_user': id_profesor
    }

    db.notificacion.insert(**notificacion_data)


@auth.requires(auth.has_membership('Coordinador'))
def crear():
    db.actividad_edicion.id_edicion.writable = False
    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()

    form = SQLFORM(db.actividad_edicion)

    if form.validate(keepvalues=True):
        date1 = form.vars.fecha_inicio
        date2 = form.vars.fecha_fin

        if db(db.actividad_edicion.id_actividad == form.vars.id_actividad).select():

            plugin_toastr_message_config('error', T(
                'Existen errores en el formulario'))
            form.errors.id_actividad = 'La actividad ya se encuentra asociada'
        elif date1 < date2:
            db.actividad_edicion.insert(
                id_edicion=edicion_actual.id_edicion, **form.vars)

            __notificar_profesor(form.vars.id_profesor, edicion_actual.id_edicion)

            plugin_toastr_message_config('success', T(
                'Actividad añadida correctamente'))
            redirect(URL('manage'))
        else:
            plugin_toastr_message_config('error', T(
                'Existen errores en el formulario'))
            form.errors.fecha_fin = 'La fecha final debe ser mayor a la inicial'

    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form)


@auth.requires(auth.has_membership('Coordinador'))
def editar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.actividad_edicion(request.args(0, cast=int)
                                    ) or redirect(URL('manage'))

    edicion_actual = db(db.edicion_actual.id_user ==
                        auth.user.id).select().first()

    db.actividad_edicion.id_edicion.writable = False
    db.actividad_edicion.id_edicion.readable = False
    db.actividad_edicion.id.readable = False

    form = SQLFORM(db.actividad_edicion, registro)

    if form.validate(keepvalues=True):
        date1 = form.vars.fecha_inicio
        date2 = form.vars.fecha_fin

        if db((db.actividad_edicion.id_actividad != registro.id_actividad) &
              (db.actividad_edicion.id_actividad == form.vars.id_actividad)).select():

            plugin_toastr_message_config('error', T(
                'Existen errores en el formulario'))
            form.errors.id_actividad = 'La actividad ya se encuentra asociada'
        elif date1 < date2:
            if form.vars.id_profesor != registro.id:
                __notificar_profesor(form.vars.id_profesor, edicion_actual.id_edicion)

            registro.update_record(
                id_edicion=edicion_actual.id_edicion, **form.vars)
            plugin_toastr_message_config('success', T(
                'Actividad editada correctamente'))

            redirect(URL('manage'))
        else:
            plugin_toastr_message_config('error', T(
                'Existen errores en el formulario'))
            form.errors.fecha_fin = 'La fecha final debe ser mayor a la inicial'

    elif form.errors:
        plugin_toastr_message_config('error', T(
            'Existen errores en el formulario'))

    return dict(form=form)


@auth.requires(auth.has_membership('Coordinador'))
def eliminar():
    if not request.args(0):
        redirect(URL('manage'))

    registro = db.actividad_edicion(request.args(0, cast=int)
                                    ) or redirect(URL('manage'))

    db(db.actividad_edicion.id == registro.id).delete()

    plugin_toastr_message_config('success', T(
        'La actividad se ha eliminado correctamente de esta edición'))

    redirect(URL("manage"))

    return dict()
