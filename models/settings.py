import os

app_title = "GesMaster"
app_author = "Ines"
app_description = "GesMaster"
app_keywords = "Sistema Informático para la Gestión de la Maestría Informática Aplicada"
app_icon = URL('static', 'images/ico.png')

app_rol = None

# Definir Roles
if not db(db.auth_group.id > 0).select():
    db.auth_group.truncate()
    db.auth_group.insert(role="Administrador")
    db.auth_group.insert(role="Coordinador")
    db.auth_group.insert(role="Profesor")
    db.auth_group.insert(role="Estudiante")

# Crear administrador
def __open_csv(url):
    with open(url, 'r', encoding='utf-8', newline='') as dumpfile:
        db.import_from_csv_file(dumpfile)


if not db(db.auth_user.id > 0).select():
    db.auth_user.truncate()

    url = os.path.join(
        request.folder, "static/database/db_auth_user.csv")

    __open_csv(url)

    group_id = db(db.auth_group.role == "Administrador").select().first().id

    db.auth_membership.insert(user_id=1, group_id=group_id)

# Rol de usuario
if auth.user:
    auth_user = db(db.auth_membership.user_id ==
                 auth.user.id).select()
    app_rol = auth_user.first().group_id.role if auth_user else None


# Inicializar settings
if not db(db.settings.id > 0).select():
    db.settings.truncate()
    db.settings.insert(centro="Universidad de Ciego de Ávila", en_mantenimiento=False)


# Verificar que no existan Coordinadores sin una edición asociada
if auth.user and auth.has_membership('Coordinador'):
    maestria_usuario = db(db.coordinador_maestria.id_user ==
                  auth.user.id).select().first()
    ediciones = db(db.edicion.id_maestria ==
                   maestria_usuario.id_maestria).select()
    has_edicion = db(db.edicion_actual.id_user == auth.user.id).select()

    if ediciones and not has_edicion:
        datos = {
            'id_edicion': ediciones.first().id,
            'id_user': auth.user.id
        }

        db.edicion_actual.insert(**datos)
