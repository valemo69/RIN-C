from django.db import migrations

# ==========================================================
# POR QUÉ ESTA MIGRACIÓN
# ==========================================================
#
# En internación los gérmenes relevantes son otros que en un
# cultivo ambulatorio: importa la resistencia (MRSA vs MSSA
# cambia todo el manejo clínico) y hay especies de estafilococo
# coagulasa-negativo y estreptococos que no estaban en el set
# inicial. Se agregan acá como ítems de germen NUEVOS (no se
# borra nada existente, por si ya guardaste un aislamiento
# apuntando al "Staphylococcus aureus" genérico).
#
# El "Staphylococcus aureus" genérico que cargó la migración 0007
# se marca como inactivo (activo=False) en vez de borrarse: así
# deja de aparecer en los combos para casos nuevos, pero sigue
# existiendo en la base por si algún aislamiento ya lo usaba (a
# un Catalogo con on_delete=PROTECT no se lo puede borrar de
# todos modos si está en uso).


GERMENES_INTERNACION = [
    ("MSSA", "Staphylococcus aureus sensible (MSSA)", 20),
    ("MRSA", "Staphylococcus aureus resistente (MRSA)", 21),
    ("S_HAEMOLYTICUS", "Staphylococcus haemolyticus", 22),
    ("S_LUGDUNENSIS", "Staphylococcus lugdunensis", 23),
    ("S_PYOGENES", "Streptococcus pyogenes", 24),
    ("S_AGALACTIAE", "Streptococcus agalactiae", 25),
    ("S_VIRIDANS", "Streptococcus grupo viridans", 26),
    ("E_FAECIUM", "Enterococcus faecium", 27),
]


def cargar(apps, schema_editor):

    TipoCatalogo = apps.get_model("pacientes", "TipoCatalogo")
    Catalogo = apps.get_model("pacientes", "Catalogo")

    tipo_germen = TipoCatalogo.objects.get(codigo="GERMEN")

    for codigo, descripcion, orden in GERMENES_INTERNACION:
        Catalogo.objects.get_or_create(
            tipo=tipo_germen,
            codigo=codigo,
            defaults={"descripcion": descripcion, "orden": orden},
        )

    # Desactivar (no borrar) el "Staphylococcus aureus" genérico,
    # ahora que existen MSSA/MRSA como opciones específicas.
    Catalogo.objects.filter(
        tipo__codigo="GERMEN", codigo="S_AUREUS"
    ).update(activo=False)


def deshacer(apps, schema_editor):

    Catalogo = apps.get_model("pacientes", "Catalogo")

    codigos = [codigo for codigo, _, _ in GERMENES_INTERNACION]

    Catalogo.objects.filter(tipo__codigo="GERMEN", codigo__in=codigos).delete()

    Catalogo.objects.filter(
        tipo__codigo="GERMEN", codigo="S_AUREUS"
    ).update(activo=True)


class Migration(migrations.Migration):

    dependencies = [
        ("pacientes", "0010_cargar_hongos_y_antifungicos"),
    ]

    operations = [
        migrations.RunPython(cargar, deshacer),
    ]
