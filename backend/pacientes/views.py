from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    BusquedaPacienteForm,
    PacienteForm,
    InternacionForm,
    RecorridoInternacionForm,
    ComorbilidadesForm,
    MuestraMicrobiologicaForm,
    AislamientoMicrobiologicoForm,
    SensibilidadMicrobiologicaForm,
    InternacionTratamientoAntimicrobianoForm,
)
from .models import (
    AislamientoMicrobiologico,
    Catalogo,
    Internacion,
    InternacionCatalogo,
    InternacionTratamientoAntimicrobiano,
    MuestraMicrobiologica,
    Paciente,
    RecorridoInternacion,
    SensibilidadMicrobiologica,
)

# ==========================================================
# INICIO - BÚSQUEDA DE PACIENTES
# ==========================================================


@login_required
def inicio(request):

    form = BusquedaPacienteForm(request.GET or None)

    pacientes = Paciente.objects.none()

    if form.is_valid():

        numero_documento = form.cleaned_data.get("numero_documento")
        apellido = form.cleaned_data.get("apellido")

        filtros = Q()

        if numero_documento:
            filtros &= Q(numero_documento__icontains=numero_documento)

        if apellido:
            filtros &= Q(apellido__icontains=apellido)

        pacientes = (
            Paciente.objects.filter(filtros)
            .select_related(
                "tipo_documento",
                "sexo",
                "cobertura",
                "estado_vital",
            )
            .order_by(
                "apellido",
                "nombre",
            )
        )

    return render(
        request,
        "pacientes/inicio.html",
        {
            "form": form,
            "pacientes": pacientes,
        },
    )


# ==========================================================
# FICHA DEL PACIENTE
# ==========================================================


@login_required
def paciente_nuevo(request):

    if request.method == "POST":

        form = PacienteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("pacientes:inicio")

    else:

        form = PacienteForm()

    return render(
        request,
        "pacientes/paciente_ficha.html",
        {
            "form": form,
            "titulo": "Nuevo paciente",
            "es_nuevo": True,
        },
    )


@login_required
def paciente_editar(request, pk):

    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == "POST":

        form = PacienteForm(
            request.POST,
            instance=paciente,
        )

        if form.is_valid():
            form.save()
            return redirect("pacientes:paciente_ver", pk=paciente.pk)

    else:

        form = PacienteForm(instance=paciente)

    return render(
        request,
        "pacientes/paciente_ficha.html",
        {
            "form": form,
            "paciente": paciente,
            "titulo": "Ficha del paciente",
            "es_nuevo": False,
        },
    )


@login_required
def paciente_ver(request, pk):

    paciente = get_object_or_404(Paciente, pk=pk)

    form = PacienteForm(instance=paciente)
    for field in form.fields.values():
        field.disabled = True
    return render(
        request,
        "pacientes/paciente_ver.html",
        {
            "form": form,
            "paciente": paciente,
            "titulo": "Ficha del paciente",
        },
    )


# ==========================================================
# INTERNACIÓN
# ==========================================================


@login_required
def internaciones_paciente(request, paciente_pk):
    """
    Lista las internaciones de un paciente puntual y permite
    abrir una nueva.

    Por qué una vista aparte y no meterla dentro de la ficha del
    paciente: separamos "datos del paciente" (que casi no cambian)
    de "internaciones" (que es un historial que va creciendo), así
    cada vista tiene una sola responsabilidad y es más fácil de
    entender y de testear.
    """

    paciente = get_object_or_404(Paciente, pk=paciente_pk)

    internaciones = paciente.internaciones.all()

    return render(
        request,
        "pacientes/internaciones_lista.html",
        {
            "paciente": paciente,
            "internaciones": internaciones,
        },
    )


@login_required
def internacion_nueva(request, paciente_pk):
    """
    Crea una internación nueva para un paciente.

    Usamos request.method == "POST" para distinguir dos casos:
    - GET: el usuario recién entra a la pantalla -> mostramos un
      formulario vacío.
    - POST: el usuario ya completó el formulario y le dio a
      "Guardar" -> intentamos guardar los datos.

    Esto es el mismo patrón que ya usa paciente_nuevo más arriba,
    así que si entendiste ese, este es igual pero para Internación.
    """

    paciente = get_object_or_404(Paciente, pk=paciente_pk)

    if request.method == "POST":

        form = InternacionForm(request.POST)

        if form.is_valid():

            internacion = form.save(commit=False)

            # El paciente no viene del formulario (no lo mostramos
            # en pantalla): lo fijamos nosotros a partir de la URL,
            # para no depender de que el usuario no lo manipule.
            internacion.paciente = paciente

            internacion.save()

            messages.success(request, "Internación creada correctamente.")

            return redirect(
                "pacientes:internacion_detalle",
                pk=internacion.pk,
            )

    else:

        form = InternacionForm()
    motivos_infecciosos = Catalogo.objects.filter(
        tipo__codigo="MOTIVO_INFECCIOSO",
        activo=True,
    ).order_by("orden")
    
    motivos_obstructivos = Catalogo.objects.filter(
    tipo__codigo="MOTIVO_OBSTRUCTIVO",
    activo=True,
    ).order_by("orden")

    motivos_intersticiales = Catalogo.objects.filter(
        tipo__codigo="MOTIVO_INTERSTICIAL",
        activo=True,
    ).order_by("orden")

    motivos_pleurales = Catalogo.objects.filter(
        tipo__codigo="MOTIVO_PLEURAL",
        activo=True,
    ).order_by("orden")

    motivos_vasculares = Catalogo.objects.filter(
        tipo__codigo="MOTIVO_VASCULAR",
        activo=True,
    ).order_by("orden")

    motivos_oncologicos = Catalogo.objects.filter(
        tipo__codigo="MOTIVO_ONCOLOGICO",
        activo=True,
    ).order_by("orden")

    motivos_otros = Catalogo.objects.filter(
        tipo__codigo="MOTIVO_OTROS",
        activo=True,
    ).order_by("orden")

    return render(
        request,
        "pacientes/internacion.html",
        {
            "form": form,
            "paciente": paciente,
            "internacion": None,
            "recorridos": [],
            "recorrido_form": RecorridoInternacionForm(),
            "es_nueva": True,
            "motivos_infecciosos": motivos_infecciosos,
            "motivos_obstructivos": motivos_obstructivos,
            "motivos_intersticiales": motivos_intersticiales,
            "motivos_pleurales": motivos_pleurales,
            "motivos_vasculares": motivos_vasculares,
            "motivos_oncologicos": motivos_oncologicos,
            "motivos_otros": motivos_otros,
        },
    )


@login_required
def internacion_detalle(request, pk):
    """
    Muestra y permite editar una internación ya existente, junto
    con el recorrido (los distintos sectores por los que pasó el
    paciente durante esa internación).
    """

    internacion = get_object_or_404(Internacion, pk=pk)

    if request.method == "POST":

        form = InternacionForm(
            request.POST,
            instance=internacion,
        )

        form_motivos = InternacionMotivosForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Internación actualizada correctamente.",
            )

            return redirect(
                "pacientes:internacion_detalle",
                pk=internacion.pk,
            )

    else:

        form = InternacionForm(instance=internacion)

        form_motivos = InternacionMotivosForm()

    return render(
        request,
        "pacientes/internacion.html",
        {
            "form": form,
            "form_motivos": form_motivos,
            "paciente": internacion.paciente,
            "internacion": internacion,
            "recorridos": internacion.recorridos.all(),
            "recorrido_form": RecorridoInternacionForm(),
            "es_nueva": False,
        },
    )


@login_required
def recorrido_agregar(request, internacion_pk):
    """
    Agrega una fila al recorrido de una internación (por ejemplo:
    "pasó por Guardia del 3/7 al 5/7").

    Solo aceptamos POST acá: esta vista no tiene sentido por GET,
    porque no hay nada para "mostrar", solo procesamos el envío del
    formulario y volvemos a la pantalla de la internación.
    """

    internacion = get_object_or_404(Internacion, pk=internacion_pk)

    if request.method == "POST":

        form = RecorridoInternacionForm(request.POST)

        if form.is_valid():

            fecha_desde = form.cleaned_data["fecha_desde"]

            ultimo_recorrido = internacion.recorridos.order_by("-orden").first()

            if ultimo_recorrido and fecha_desde < ultimo_recorrido.fecha_desde:

                messages.error(
                    request,
                    "La fecha de este traslado no puede ser anterior a la "
                    f"del último sector cargado ({ultimo_recorrido.fecha_desde:%d/%m/%Y}).",
                )

                return redirect("pacientes:internacion_detalle", pk=internacion.pk)

            recorrido = form.save(commit=False)
            recorrido.internacion = internacion

            # El siguiente orden es 1 más que el máximo actual (o 1
            # si todavía no hay ningún recorrido cargado). Se calcula
            # acá, en la vista, porque el usuario no debería tener
            # que pensar en ese número.
            ultimo_orden = (
                internacion.recorridos.order_by("-orden")
                .values_list("orden", flat=True)
                .first()
            )
            recorrido.orden = (ultimo_orden or 0) + 1

            # Un paciente está en un solo sector a la vez: si había
            # un sector "abierto" (sin fecha_hasta, es decir, el
            # último lugar registrado), lo cerramos automáticamente
            # con la fecha en que arranca este nuevo sector. Así el
            # usuario no tiene que acordarse de "cerrar" el anterior
            # a mano cada vez que carga un traslado.
            anterior_abierto = (
                internacion.recorridos.filter(fecha_hasta__isnull=True)
                .order_by("-orden")
                .first()
            )

            if anterior_abierto:
                anterior_abierto.fecha_hasta = recorrido.fecha_desde
                anterior_abierto.save(update_fields=["fecha_hasta"])

            recorrido.save()
            if internacion.fecha_egreso:
                recorrido.fecha_hasta = internacion.fecha_egreso
                recorrido.save(update_fields=["fecha_hasta"])
                
            messages.success(request, "Recorrido agregado.")

        else:

            # Si el formulario tiene errores, se los mostramos al
            # usuario como mensajes en vez de perderlos, ya que acá
            # no re-renderizamos el formulario con los errores
            # marcados campo por campo (eso sería el siguiente paso
            # si querés pulirlo más).
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{campo}: {error}")

    return redirect(
        "pacientes:internacion_detalle",
        pk=internacion.pk,
    )


def _sincronizar_catalogos(internacion, tipo_codigo, catalogos_seleccionados):
    """
    Hace que las filas de InternacionCatalogo de un tipo puntual
    (por ejemplo "COMORBILIDAD") queden exactamente iguales a lo
    que el usuario tildó en el formulario.

    Por qué borrar y crear en vez de "actualizar": InternacionCatalogo
    no tiene más datos que el vínculo en sí (no hay nada que
    "actualizar" en una fila existente), así que el problema se
    reduce a comparar dos conjuntos de ids:
    - lo que ya estaba guardado (ids_actuales)
    - lo que el usuario tildó ahora (ids_seleccionados)
    Lo que está en el primero pero no en el segundo, se borra.
    Lo que está en el segundo pero no en el primero, se crea.
    Filtramos siempre por tipo_codigo para no tocar por accidente
    las filas de otro tipo (por ejemplo, no queremos que al guardar
    comorbilidades se borren las inmunizaciones).
    """

    actuales = InternacionCatalogo.objects.filter(
        internacion=internacion,
        catalogo__tipo__codigo=tipo_codigo,
    )

    ids_actuales = set(actuales.values_list("catalogo_id", flat=True))
    ids_seleccionados = set(c.pk for c in catalogos_seleccionados)

    ids_a_borrar = ids_actuales - ids_seleccionados
    ids_a_crear = ids_seleccionados - ids_actuales

    if ids_a_borrar:
        actuales.filter(catalogo_id__in=ids_a_borrar).delete()

    InternacionCatalogo.objects.bulk_create(
        [
            InternacionCatalogo(internacion=internacion, catalogo_id=catalogo_id)
            for catalogo_id in ids_a_crear
        ]
    )


@login_required
def comorbilidades_view(request, pk):

    internacion = get_object_or_404(Internacion, pk=pk)

    comorbilidades_seleccionadas = Catalogo.objects.filter(
        internaciones__internacion=internacion,
        tipo__codigo="COMORBILIDAD",
    )

    inmunizaciones_seleccionadas = Catalogo.objects.filter(
        internaciones__internacion=internacion,
        tipo__codigo="INMUNIZACION",
    )

    if request.method == "POST":

        form = ComorbilidadesForm(request.POST)

        if form.is_valid():

            _sincronizar_catalogos(
                internacion, "COMORBILIDAD", form.cleaned_data["comorbilidades"]
            )
            _sincronizar_catalogos(
                internacion, "INMUNIZACION", form.cleaned_data["inmunizaciones"]
            )

            messages.success(request, "Comorbilidades guardadas correctamente.")

            return redirect("pacientes:comorbilidades", pk=internacion.pk)

    else:

        form = ComorbilidadesForm(
            initial={
                "comorbilidades": comorbilidades_seleccionadas,
                "inmunizaciones": inmunizaciones_seleccionadas,
            }
        )

    # Agrupamos los ítems de comorbilidad por "grupo" (Cardiovasculares,
    # Endócrino - Metabólicas, etc) para poder armar una tarjeta por
    # grupo en el template, igual que en el mockup original. Ojo: el
    # orden de los GRUPOS queda alfabético (Cardiovasculares, Endócrino,
    # Inmunológicas...) porque Catalogo no tiene un campo para ordenar
    # grupos entre sí, solo ítems dentro de un mismo grupo. Si en algún
    # momento te importa reproducir el orden exacto del mockup, se
    # puede agregar ese campo más adelante.
    comorbilidades_por_grupo = {}

    for item in Catalogo.objects.filter(
        tipo__codigo="COMORBILIDAD", activo=True
    ).order_by("grupo", "orden"):
        comorbilidades_por_grupo.setdefault(item.grupo, []).append(item)

    ids_seleccionados = set(comorbilidades_seleccionadas.values_list("pk", flat=True))

    inmunizaciones = Catalogo.objects.filter(
        tipo__codigo="INMUNIZACION", activo=True
    ).order_by("orden")

    ids_inmunizaciones_seleccionadas = set(
        inmunizaciones_seleccionadas.values_list("pk", flat=True)
    )

    return render(
        request,
        "pacientes/comorbilidades.html",
        {
            "form": form,
            "internacion": internacion,
            "paciente": internacion.paciente,
            "comorbilidades_por_grupo": comorbilidades_por_grupo,
            "ids_comorbilidades_seleccionadas": ids_seleccionados,
            "inmunizaciones": inmunizaciones,
            "ids_inmunizaciones_seleccionadas": ids_inmunizaciones_seleccionadas,
        },
    )


@login_required
def microbiologia_view(request, pk):
    """
    Pantalla principal de Microbiología: lista las muestras
    (estudios) de una internación, cada una con sus aislamientos y
    las sensibilidades de cada aislamiento, y muestra el formulario
    para cargar una muestra nueva.

    Por qué traemos todo con prefetch_related en vez de dejar que
    cada {% for %} del template dispare su propia consulta: sin
    esto, por cada muestra se haría una consulta para sus
    aislamientos, y por cada aislamiento otra para sus
    sensibilidades (el problema clásico de "N+1 consultas"). Con
    prefetch_related, Django trae todo en unas pocas consultas
    armadas de antemano, sin importar cuántas muestras haya.
    """

    internacion = get_object_or_404(Internacion, pk=pk)

    muestras = internacion.muestras_microbiologicas.all().prefetch_related(
        "aislamientos__sensibilidades"
    )

    if request.method == "POST":

        form = MuestraMicrobiologicaForm(request.POST)

        if form.is_valid():

            muestra = form.save(commit=False)
            muestra.internacion = internacion
            muestra.save()

            messages.success(request, "Muestra microbiológica agregada.")

            return redirect("pacientes:microbiologia", pk=internacion.pk)

    else:

        form = MuestraMicrobiologicaForm()

    return render(
        request,
        "pacientes/microbiologia.html",
        {
            "internacion": internacion,
            "paciente": internacion.paciente,
            "muestras": muestras,
            "form": form,
            "aislamiento_form": AislamientoMicrobiologicoForm(),
            "sensibilidad_form": SensibilidadMicrobiologicaForm(),
        },
    )


@login_required
def aislamiento_agregar(request, muestra_pk):
    """Agrega un germen aislado a una muestra puntual (solo POST, igual que recorrido_agregar)."""

    muestra = get_object_or_404(MuestraMicrobiologica, pk=muestra_pk)

    if request.method == "POST":

        form = AislamientoMicrobiologicoForm(request.POST)

        if form.is_valid():

            aislamiento = form.save(commit=False)
            aislamiento.muestra = muestra
            aislamiento.save()

            messages.success(request, "Aislamiento agregado.")

        else:

            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{campo}: {error}")

    return redirect("pacientes:microbiologia", pk=muestra.internacion.pk)


@login_required
def sensibilidad_agregar(request, aislamiento_pk):
    """Agrega un resultado de sensibilidad (antibiograma) a un aislamiento puntual."""

    aislamiento = get_object_or_404(AislamientoMicrobiologico, pk=aislamiento_pk)

    if request.method == "POST":

        form = SensibilidadMicrobiologicaForm(request.POST)

        if form.is_valid():

            sensibilidad = form.save(commit=False)
            sensibilidad.aislamiento = aislamiento
            sensibilidad.save()

            messages.success(request, "Sensibilidad agregada.")

        else:

            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{campo}: {error}")

    return redirect(
        "pacientes:microbiologia",
        pk=aislamiento.muestra.internacion.pk,
    )


@login_required
def estudios_procedimientos_view(request):
    return render(
        request,
        "pacientes/estudios_procedimientos.html",
    )


@login_required
def tratamiento_view(request, pk):
    """
    Pantalla de Tratamiento: lista y permite agregar tratamientos
    antimicrobianos de una internación (antibióticos, antifúngicos,
    antituberculosos y antivirales quedan unificados acá, porque en
    el modelo son la misma cosa: un antimicrobiano + vía + dosis +
    fechas).
    """

    internacion = get_object_or_404(Internacion, pk=pk)

    tratamientos = internacion.tratamientos_antimicrobianos.all()

    if request.method == "POST":

        form = InternacionTratamientoAntimicrobianoForm(request.POST)

        if form.is_valid():

            tratamiento = form.save(commit=False)
            tratamiento.internacion = internacion
            tratamiento.save()

            messages.success(request, "Tratamiento agregado.")

            return redirect("pacientes:tratamiento", pk=internacion.pk)

    else:

        form = InternacionTratamientoAntimicrobianoForm()

    return render(
        request,
        "pacientes/tratamiento.html",
        {
            "internacion": internacion,
            "paciente": internacion.paciente,
            "tratamientos": tratamientos,
            "form": form,
        },
    )
