from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    BusquedaPacienteForm,
    PacienteForm,
    InternacionForm,
    ComorbilidadesForm,
    MuestraMicrobiologicaForm,
    EstudioMicrobiologicoForm,
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
            .order_by("apellido", "nombre")
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
        form = PacienteForm(request.POST, instance=paciente)
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
    paciente = get_object_or_404(Paciente, pk=paciente_pk)

    motivos_infecciosos = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_INFECCIOSO", activo=True).order_by("orden", "descripcion")
    motivos_obstructivos = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_OBSTRUCTIVO", activo=True).order_by("orden", "descripcion")
    motivos_intersticiales = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_INTERSTICIAL", activo=True).order_by("orden", "descripcion")
    motivos_pleurales = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_PLEURAL", activo=True).order_by("orden", "descripcion")
    motivos_vasculares = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_VASCULAR", activo=True).order_by("orden", "descripcion")
    motivos_oncologicos = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_ONCOLOGICO", activo=True).order_by("orden", "descripcion")
    motivos_otros = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_OTROS", activo=True).order_by("orden", "descripcion")

    motivos_otros_habitos_inhalatorios = Catalogo.objects.filter(
        tipo__codigo="OTROS_HABITOS_INHALATORIOS",
        activo=True
    ).order_by("orden", "descripcion")

    motivos_exposiciones_laborales = Catalogo.objects.filter(
        tipo__codigo="EXPOSICION_OCUPACIONAL",
        activo=True
    ).order_by("orden", "descripcion")

    motivos_exposiciones_ambientales = Catalogo.objects.filter(
        tipo__codigo="EXPOSICION_AMBIENTAL",
        activo=True
    ).order_by("orden", "descripcion")

    motivos_antecedentes = Catalogo.objects.filter(
        tipo__codigo__in=["ANTECEDENTE_RESPIRATORIO", "COMORBILIDAD"],
        activo=True
    ).order_by("orden", "descripcion")

    motivos_soporte = Catalogo.objects.filter(
        tipo__codigo="SOPORTE_RESPIRATORIO",
        activo=True
    ).order_by("orden", "descripcion")

    if request.method == "POST":
        form = InternacionForm(request.POST)
        if form.is_valid():
            internacion = form.save(commit=False)
            internacion.paciente = paciente
            internacion.save()
            form.save_m2m()
            messages.success(request, "Internación creada correctamente.")
            return redirect("pacientes:internacion_detalle", pk=internacion.pk)
        else:
            print("--- ERRORES DEL FORMULARIO ---", form.errors)
    else:
        form = InternacionForm()

    otros_habitos_inhalatorios_ids = [
        int(i) for i in request.POST.getlist("otros_habitos_inhalatorios")
    ] if request.method == "POST" else []

    exposiciones_laborales_ids = [
        int(i) for i in request.POST.getlist("exposiciones_laborales")
    ] if request.method == "POST" else []

    exposiciones_ambientales_ids = [
        int(i) for i in request.POST.getlist("exposiciones_ambientales")
    ] if request.method == "POST" else []

    antecedentes_ids = [
        int(i) for i in request.POST.getlist("antecedentes_respiratorios")
    ] if request.method == "POST" else []

    soporte_ids = [
        int(i) for i in request.POST.getlist("soporte_respiratorio")
    ] if request.method == "POST" else []

    return render(
        request,
        "pacientes/internacion.html",
        {
            "form": form,
            "paciente": paciente,
            "internacion": None,
            "es_nueva": True,

            "motivos_infecciosos": motivos_infecciosos,
            "motivos_obstructivos": motivos_obstructivos,
            "motivos_intersticiales": motivos_intersticiales,
            "motivos_pleurales": motivos_pleurales,
            "motivos_vasculares": motivos_vasculares,
            "motivos_oncologicos": motivos_oncologicos,
            "motivos_otros": motivos_otros,

            "motivos_otros_habitos_inhalatorios": motivos_otros_habitos_inhalatorios,
            "motivos_exposiciones_laborales": motivos_exposiciones_laborales,
            "motivos_exposiciones_ambientales": motivos_exposiciones_ambientales,

            "motivos_antecedentes": motivos_antecedentes,
            "motivos_soporte": motivos_soporte,

            "otros_habitos_inhalatorios_ids": otros_habitos_inhalatorios_ids,
            "exposiciones_laborales_ids": exposiciones_laborales_ids,
            "exposiciones_ambientales_ids": exposiciones_ambientales_ids,

            "antecedentes_ids": antecedentes_ids,
            "soporte_ids": soporte_ids,
        },
    )


@login_required
def internacion_detalle(request, pk):
    internacion = get_object_or_404(Internacion, pk=pk)

    motivos_infecciosos = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_INFECCIOSO", activo=True).order_by("orden", "descripcion")
    motivos_obstructivos = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_OBSTRUCTIVO", activo=True).order_by("orden", "descripcion")
    motivos_intersticiales = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_INTERSTICIAL", activo=True).order_by("orden", "descripcion")
    motivos_pleurales = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_PLEURAL", activo=True).order_by("orden", "descripcion")
    motivos_vasculares = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_VASCULAR", activo=True).order_by("orden", "descripcion")
    motivos_oncologicos = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_ONCOLOGICO", activo=True).order_by("orden", "descripcion")
    motivos_otros = Catalogo.objects.filter(tipo__codigo__iexact="MOTIVO_OTROS", activo=True).order_by("orden", "descripcion")

    motivos_tabaquismo_pasivo = Catalogo.objects.filter(
        tipo__codigo="TABAQUISMO_PASIVO", 
        activo=True
    ).order_by("orden", "descripcion")
    
    motivos_otros_habitos_inhalatorios = Catalogo.objects.filter(
        tipo__codigo="OTROS_HABITOS_INHALATORIOS", 
        activo=True
    ).order_by("orden", "descripcion")
    
    motivos_exposiciones_laborales = Catalogo.objects.filter(
        tipo__codigo="EXPOSICION_OCUPACIONAL", 
        activo=True
    ).order_by("orden", "descripcion")
    
    motivos_exposiciones_ambientales = Catalogo.objects.filter(
        tipo__codigo="EXPOSICION_AMBIENTAL", 
        activo=True
    ).order_by("orden", "descripcion")
    
    motivos_antecedentes = Catalogo.objects.filter(
        tipo__codigo__in=["ANTECEDENTE_RESPIRATORIO", "COMORBILIDAD"], 
        activo=True
    ).order_by("orden", "descripcion")
    
    motivos_soporte = Catalogo.objects.filter(
        tipo__codigo="SOPORTE_RESPIRATORIO", 
        activo=True
    ).order_by("orden", "descripcion")

    if request.method == "POST":
        form = InternacionForm(request.POST, instance=internacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Internación actualizada correctamente.")
            return redirect("pacientes:internacion_detalle", pk=internacion.pk)
    else:
        form = InternacionForm(instance=internacion)

    if request.method == "POST":
        tabaquismo_pasivo_ids = [int(i) for i in request.POST.getlist("tabaquismo_pasivo")]
        otros_habitos_inhalatorios_ids = [int(i) for i in request.POST.getlist("otros_habitos_inhalatorios")]
        exposiciones_laborales_ids = [int(i) for i in request.POST.getlist("exposiciones_laborales")]
        exposiciones_ambientales_ids = [int(i) for i in request.POST.getlist("exposiciones_ambientales")]
        antecedentes_ids = [int(i) for i in request.POST.getlist("antecedentes_respiratorios")]
        soporte_ids = [int(i) for i in request.POST.getlist("soporte_respiratorio")]
    else:
        tabaquismo_pasivo_ids = list(internacion.tabaquismo_pasivo.values_list("id", flat=True))
        otros_habitos_inhalatorios_ids = list(internacion.otros_habitos_inhalatorios.values_list("id", flat=True))
        exposiciones_laborales_ids = list(internacion.exposiciones_laborales.values_list("id", flat=True))
        exposiciones_ambientales_ids = list(internacion.exposiciones_ambientales.values_list("id", flat=True))
        antecedentes_ids = list(internacion.antecedentes_respiratorios.values_list("id", flat=True))
        soporte_ids = list(internacion.soporte_respiratorio.values_list("id", flat=True))

    return render(
        request,
        "pacientes/internacion.html",
        {
            "form": form,
            "paciente": internacion.paciente,
            "internacion": internacion,
            "es_nueva": False,
            "motivos_infecciosos": motivos_infecciosos,
            "motivos_obstructivos": motivos_obstructivos,
            "motivos_intersticiales": motivos_intersticiales,
            "motivos_pleurales": motivos_pleurales,
            "motivos_vasculares": motivos_vasculares,
            "motivos_oncologicos": motivos_oncologicos,
            "motivos_otros": motivos_otros,
            "motivos_tabaquismo_pasivo": motivos_tabaquismo_pasivo,
            "motivos_otros_habitos_inhalatorios": motivos_otros_habitos_inhalatorios,
            "motivos_exposiciones_laborales": motivos_exposiciones_laborales,
            "motivos_exposiciones_ambientales": motivos_exposiciones_ambientales,
            "motivos_antecedentes": motivos_antecedentes,
            "motivos_soporte": motivos_soporte,
            "tabaquismo_pasivo_ids": tabaquismo_pasivo_ids,
            "otros_habitos_inhalatorios_ids": otros_habitos_inhalatorios_ids,
            "exposiciones_laborales_ids": exposiciones_laborales_ids,
            "exposiciones_ambientales_ids": exposiciones_ambientales_ids,
            "antecedentes_ids": antecedentes_ids,
            "soporte_ids": soporte_ids,
        },
    )

# ==========================================================
# COMORBILIDADES
# ==========================================================

def _sincronizar_catalogos(internacion, tipo_codigo, catalogos_seleccionados):
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

# ==========================================================
# MICROBIOLOGÍA
# ==========================================================

@login_required
def microbiologia_view(request, pk):
    internacion = get_object_or_404(Internacion, pk=pk)
    muestras = (
    internacion.muestras_microbiologicas
    .all()
    .prefetch_related(
        "estudios__aislamientos__sensibilidades",
    )
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
        "estudio_form": EstudioMicrobiologicoForm(),
        "aislamiento_form": AislamientoMicrobiologicoForm(),
        "sensibilidad_form": SensibilidadMicrobiologicaForm(),
    },
)

@login_required
def aislamiento_agregar(request, muestra_pk):
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

# ==========================================================
# ESTUDIOS Y PROCEDIMIENTOS
# ==========================================================

@login_required
def estudios_procedimientos_view(request):
    return render(
        request,
        "pacientes/estudios_procedimientos.html",
    )

# ==========================================================
# TRATAMIENTO
# ==========================================================

@login_required
def tratamiento_view(request, pk):
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