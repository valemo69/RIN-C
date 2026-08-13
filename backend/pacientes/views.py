from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import modelformset_factory
from django.urls import reverse
from django.http import HttpResponseRedirect


from .forms import (
    BusquedaPacienteForm,
    PacienteForm,
    InternacionForm,
    ComorbilidadesForm,
    MuestraMicrobiologicaForm,
    EstudioMicrobiologicoForm,
    AislamientoMicrobiologicoForm,
    AislamientoMicrobiologicoEditForm,
    MuestraMicrobiologicaEditForm,
    ResultadosTBCForm,
    SensibilidadMicrobiologicaForm,
    InternacionTratamientoAntimicrobianoForm,
    TomografiaForm,
)
from .models import (
    AislamientoMicrobiologico,
    Catalogo,
    EstudioMicrobiologico,
    Internacion,
    InternacionCatalogo,
    InternacionTratamientoAntimicrobiano,
    MuestraMicrobiologica,
    Paciente,
    SensibilidadMicrobiologica,
    BaciloscopiaDetalle,
    CultivoDetalle,
    GeneXpertDetalle,
    Tomografia,
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

    motivos_infecciosos = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_INFECCIOSO", activo=True
    ).order_by("orden", "descripcion")
    motivos_obstructivos = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_OBSTRUCTIVO", activo=True
    ).order_by("orden", "descripcion")
    motivos_intersticiales = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_INTERSTICIAL", activo=True
    ).order_by("orden", "descripcion")
    motivos_pleurales = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_PLEURAL", activo=True
    ).order_by("orden", "descripcion")
    motivos_vasculares = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_VASCULAR", activo=True
    ).order_by("orden", "descripcion")
    motivos_oncologicos = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_ONCOLOGICO", activo=True
    ).order_by("orden", "descripcion")
    motivos_otros = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_OTROS", activo=True
    ).order_by("orden", "descripcion")

    motivos_otros_habitos_inhalatorios = Catalogo.objects.filter(
        tipo__codigo="OTROS_HABITOS_INHALATORIOS", activo=True
    ).order_by("orden", "descripcion")

    motivos_exposiciones_laborales = Catalogo.objects.filter(
        tipo__codigo="EXPOSICION_OCUPACIONAL", activo=True
    ).order_by("orden", "descripcion")

    motivos_exposiciones_ambientales = Catalogo.objects.filter(
        tipo__codigo="EXPOSICION_AMBIENTAL", activo=True
    ).order_by("orden", "descripcion")

    motivos_antecedentes = Catalogo.objects.filter(
        tipo__codigo__in=["ANTECEDENTE_RESPIRATORIO", "COMORBILIDAD"], activo=True
    ).order_by("orden", "descripcion")

    motivos_soporte = Catalogo.objects.filter(
        tipo__codigo="SOPORTE_RESPIRATORIO", activo=True
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

    otros_habitos_inhalatorios_ids = (
        [int(i) for i in request.POST.getlist("otros_habitos_inhalatorios")]
        if request.method == "POST"
        else []
    )

    exposiciones_laborales_ids = (
        [int(i) for i in request.POST.getlist("exposiciones_laborales")]
        if request.method == "POST"
        else []
    )

    exposiciones_ambientales_ids = (
        [int(i) for i in request.POST.getlist("exposiciones_ambientales")]
        if request.method == "POST"
        else []
    )

    antecedentes_ids = (
        [int(i) for i in request.POST.getlist("antecedentes_respiratorios")]
        if request.method == "POST"
        else []
    )

    soporte_ids = (
        [int(i) for i in request.POST.getlist("soporte_respiratorio")]
        if request.method == "POST"
        else []
    )

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

    motivos_infecciosos = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_INFECCIOSO", activo=True
    ).order_by("orden", "descripcion")
    motivos_obstructivos = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_OBSTRUCTIVO", activo=True
    ).order_by("orden", "descripcion")
    motivos_intersticiales = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_INTERSTICIAL", activo=True
    ).order_by("orden", "descripcion")
    motivos_pleurales = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_PLEURAL", activo=True
    ).order_by("orden", "descripcion")
    motivos_vasculares = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_VASCULAR", activo=True
    ).order_by("orden", "descripcion")
    motivos_oncologicos = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_ONCOLOGICO", activo=True
    ).order_by("orden", "descripcion")
    motivos_otros = Catalogo.objects.filter(
        tipo__codigo__iexact="MOTIVO_OTROS", activo=True
    ).order_by("orden", "descripcion")

    motivos_tabaquismo_pasivo = Catalogo.objects.filter(
        tipo__codigo="TABAQUISMO_PASIVO", activo=True
    ).order_by("orden", "descripcion")

    motivos_otros_habitos_inhalatorios = Catalogo.objects.filter(
        tipo__codigo="OTROS_HABITOS_INHALATORIOS", activo=True
    ).order_by("orden", "descripcion")

    motivos_exposiciones_laborales = Catalogo.objects.filter(
        tipo__codigo="EXPOSICION_OCUPACIONAL", activo=True
    ).order_by("orden", "descripcion")

    motivos_exposiciones_ambientales = Catalogo.objects.filter(
        tipo__codigo="EXPOSICION_AMBIENTAL", activo=True
    ).order_by("orden", "descripcion")

    motivos_antecedentes = Catalogo.objects.filter(
        tipo__codigo__in=["ANTECEDENTE_RESPIRATORIO", "COMORBILIDAD"], activo=True
    ).order_by("orden", "descripcion")

    motivos_soporte = Catalogo.objects.filter(
        tipo__codigo="SOPORTE_RESPIRATORIO", activo=True
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
        tabaquismo_pasivo_ids = [
            int(i) for i in request.POST.getlist("tabaquismo_pasivo")
        ]
        otros_habitos_inhalatorios_ids = [
            int(i) for i in request.POST.getlist("otros_habitos_inhalatorios")
        ]
        exposiciones_laborales_ids = [
            int(i) for i in request.POST.getlist("exposiciones_laborales")
        ]
        exposiciones_ambientales_ids = [
            int(i) for i in request.POST.getlist("exposiciones_ambientales")
        ]
        antecedentes_ids = [
            int(i) for i in request.POST.getlist("antecedentes_respiratorios")
        ]
        soporte_ids = [int(i) for i in request.POST.getlist("soporte_respiratorio")]
    else:
        tabaquismo_pasivo_ids = list(
            internacion.tabaquismo_pasivo.values_list("id", flat=True)
        )
        otros_habitos_inhalatorios_ids = list(
            internacion.otros_habitos_inhalatorios.values_list("id", flat=True)
        )
        exposiciones_laborales_ids = list(
            internacion.exposiciones_laborales.values_list("id", flat=True)
        )
        exposiciones_ambientales_ids = list(
            internacion.exposiciones_ambientales.values_list("id", flat=True)
        )
        antecedentes_ids = list(
            internacion.antecedentes_respiratorios.values_list("id", flat=True)
        )
        soporte_ids = list(
            internacion.soporte_respiratorio.values_list("id", flat=True)
        )

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


def _sincronizar_catalogos(
    internacion, tipo_codigo, catalogos_seleccionados, request=None
):
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

    if ids_a_crear:
        InternacionCatalogo.objects.bulk_create(
            [
                InternacionCatalogo(internacion=internacion, catalogo_id=catalogo_id)
                for catalogo_id in ids_a_crear
            ]
        )

    if tipo_codigo == "INMUNIZACION" and request:
        for item in Catalogo.objects.filter(tipo__codigo="INMUNIZACION", activo=True):
            if "Antigripal" not in item.descripcion and "COVID" not in item.descripcion:
                campo_nombre = f"inmunizacion_fecha_{item.pk}"
                fecha_ingresada = request.POST.get(campo_nombre)

                if fecha_ingresada is not None:
                    relacion = InternacionCatalogo.objects.filter(
                        internacion=internacion, catalogo=item
                    ).first()
                    if relacion:
                        relacion.observacion = fecha_ingresada
                        relacion.save()


@login_required
def comorbilidades_view(request, pk):
    internacion = get_object_or_404(Internacion, pk=pk)

    comorbilidades_seleccionadas = Catalogo.objects.filter(
        internaciones__internacion=internacion,
        tipo__codigo="COMORBILIDAD",
    )

    comorbilidades_por_grupo = Catalogo.objects.comorbilidades_agrupadas()
    reumatologicas = Catalogo.objects.reumatologicas_excluyendo_vasculitis()
    vasculitis_anca = Catalogo.objects.vasculitis_anca()
    vasculitis_no_anca = Catalogo.objects.vasculitis_no_anca()

    print("=== COMORBILIDADES - DEBUG ===")
    print("Reumatológicas (excluyendo vasculitis):", reumatologicas.count())
    print("Vasculitis ANCA:", vasculitis_anca.count())
    print("Vasculitis no ANCA:", vasculitis_no_anca.count())
    print("Grupos agrupados:", comorbilidades_por_grupo.keys())

    ids_seleccionados = set(comorbilidades_seleccionadas.values_list("pk", flat=True))

    ids_inmunizaciones_seleccionadas = set(
        Catalogo.objects.filter(
            internaciones__internacion=internacion, tipo__codigo="INMUNIZACION"
        ).values_list("pk", flat=True)
    )

    inmunizaciones_con_fecha = []
    for item in Catalogo.objects.filter(
        tipo__codigo="INMUNIZACION", activo=True
    ).order_by("orden"):
        relacion = InternacionCatalogo.objects.filter(
            internacion=internacion, catalogo=item
        ).first()
        inmunizaciones_con_fecha.append(
            {
                "item": item,
                "seleccionado": item.pk in ids_inmunizaciones_seleccionadas,
                "fecha": (
                    relacion.observacion if relacion and relacion.observacion else ""
                ),
            }
        )

    if request.method == "POST":
        form = ComorbilidadesForm(request.POST)
        if form.is_valid():
            _sincronizar_catalogos(
                internacion, "COMORBILIDAD", form.cleaned_data["comorbilidades"]
            )
            inmunizaciones_ids = request.POST.getlist("inmunizaciones")
            catalogos_inmu = Catalogo.objects.filter(pk__in=inmunizaciones_ids)
            _sincronizar_catalogos(internacion, "INMUNIZACION", catalogos_inmu)

            for item in Catalogo.objects.filter(
                tipo__codigo="INMUNIZACION", activo=True
            ):
                if (
                    "Antigripal" not in item.descripcion
                    and "COVID" not in item.descripcion
                ):
                    campo_nombre = f"inmunizacion_fecha_{item.pk}"
                    fecha_ingresada = request.POST.get(campo_nombre)
                    if fecha_ingresada is not None:
                        relacion = InternacionCatalogo.objects.filter(
                            internacion=internacion, catalogo=item
                        ).first()
                        if relacion:
                            relacion.observacion = fecha_ingresada
                            relacion.save()

            messages.success(request, "Comorbilidades guardadas correctamente.")
            return redirect("pacientes:comorbilidades", pk=internacion.pk)
    else:
        form = ComorbilidadesForm(
            initial={
                "comorbilidades": comorbilidades_seleccionadas,
            }
        )

    return render(
        request,
        "pacientes/comorbilidades.html",
        {
            "form": form,
            "internacion": internacion,
            "paciente": internacion.paciente,
            "comorbilidades_por_grupo": comorbilidades_por_grupo,
            "reumatologicas": reumatologicas,
            "vasculitis_anca": vasculitis_anca,
            "vasculitis_no_anca": vasculitis_no_anca,
            "ids_comorbilidades_seleccionadas": ids_seleccionados,
            "inmunizaciones_con_fecha": inmunizaciones_con_fecha,
        },
    )


# ==========================================================
# MICROBIOLOGÍA
# ==========================================================


@login_required
def muestra_editar(request, pk):
    muestra = get_object_or_404(MuestraMicrobiologica, pk=pk)
    internacion = muestra.internacion

    if request.method == "POST":
        form = MuestraMicrobiologicaEditForm(request.POST, instance=muestra)
        if form.is_valid():
            form.save()
            messages.success(request, "Muestra actualizada correctamente.")
            return redirect("pacientes:microbiologia", pk=internacion.pk)
    else:
        form = MuestraMicrobiologicaEditForm(instance=muestra)

    return render(
        request,
        "pacientes/muestra_editar.html",
        {
            "form": form,
            "muestra": muestra,
            "paciente": internacion.paciente,
            "internacion": internacion,
        },
    )


@login_required
def muestra_eliminar(request, pk):
    muestra = get_object_or_404(MuestraMicrobiologica, pk=pk)
    internacion = muestra.internacion

    if request.method == "POST":
        muestra.delete()
        messages.success(request, "Muestra eliminada correctamente.")
        return redirect("pacientes:microbiologia", pk=internacion.pk)

    return render(
        request,
        "pacientes/muestra_eliminar.html",
        {
            "muestra": muestra,
            "paciente": internacion.paciente,
            "internacion": internacion,
        },
    )


@login_required
def microbiologia_view(request, pk):
    internacion = get_object_or_404(Internacion, pk=pk)

    # ==========================================================
    # OBTENER MUESTRAS (ordenadas: más nuevas primero)
    # ==========================================================
    muestras = (
        internacion.muestras_microbiologicas.all()
        .order_by("-fecha_toma", "-creado")
        .prefetch_related(
            "estudios__aislamientos__sensibilidades",
            "estudios__tipo_estudio",
        )
    )

    # ==========================================================
    # ==========================================================
    # FILTRAR GÉRMENES POR DESTINO (para cada muestra)
    # ==========================================================
    germenes_por_muestra = {}
    for muestra in muestras:
        destino_codigo = muestra.destino.codigo if muestra.destino else None

        if destino_codigo == 'BAC':          # Bacteriología
            germenes = Catalogo.objects.germenes_bacterias().exclude(descripcion__icontains='Mycobacterium')
        elif destino_codigo == 'MTB':        # Micobacterias (solo TBC y MNT)
            germenes = Catalogo.objects.filter(
                tipo__codigo='GERMEN',
                codigo__in=['MTB_TBC', 'MTB_NONTB'],
                activo=True
            ).order_by('orden', 'descripcion')
        elif destino_codigo == 'MIC':        # Micología
            germenes = Catalogo.objects.germenes_hongos()
        elif destino_codigo == 'VIR':        # Virología
            germenes = Catalogo.objects.germenes_virus()
        elif destino_codigo == 'PAR':        # Parasitología
            germenes = Catalogo.objects.germenes_parasitos()
        elif destino_codigo == 'PAT':        # Anatomía patológica
            germenes = Catalogo.objects.germenes()
        else:
            germenes = Catalogo.objects.germenes()  # fallback

        germenes_por_muestra[muestra.pk] = germenes

    # ==========================================================
    # FILTRAR ANTIMICROBIANOS POR TIPO DE GERMEN
    # ==========================================================
    antimicrobianos_por_aislamiento = {}
    for muestra in muestras:
        for estudio in muestra.estudios.all():
            for aislamiento in estudio.aislamientos.all():
                germen = aislamiento.germen

                # Determinar el queryset de antimicrobianos según el germen
                if germen.tipo_microorganismo == "bacteria":
                    if germen.grupo == "TBC":
                        qs = Catalogo.objects.filter(
                            tipo__codigo="ANTIMICROBIANO",
                            grupo="ANTIMICOBACTERIANO_TBC",
                            activo=True,
                        )
                    elif germen.grupo == "NO_TBC":
                        qs = Catalogo.objects.filter(
                            tipo__codigo="ANTIMICROBIANO",
                            grupo="ANTIMICOBACTERIANO_NO_TBC",
                            activo=True,
                        )
                    else:
                        qs = Catalogo.objects.filter(
                            tipo__codigo="ANTIMICROBIANO",
                            grupo="ANTIBIOTICO",
                            activo=True,
                        )
                elif germen.tipo_microorganismo == "hongo":
                    qs = Catalogo.objects.filter(
                        tipo__codigo="ANTIMICROBIANO", grupo="ANTIFUNGICO", activo=True
                    )
                else:
                    qs = Catalogo.objects.none()

                antimicrobianos_por_aislamiento[aislamiento.pk] = qs

    # ==========================================================
    # FORMULARIO DE NUEVA MUESTRA
    # ==========================================================
    form = MuestraMicrobiologicaForm()

    if request.method == "POST":
        form = MuestraMicrobiologicaForm(request.POST)
        if form.is_valid():
            muestra = form.save(commit=False)
            muestra.internacion = internacion
            muestra.save()

            # Crear estudio automáticamente según destino
            destino_codigo = muestra.destino.codigo if muestra.destino else None
            mapeo_destino_estudio = {
                "BAC": "CULTIVO",
                "MTB": "CULTIVO",
                "MIC": "CULTIVO",
                "VIR": "PANEL_VIRAL",
                "PAR": "CULTIVO",
                "PAT": "ANATOMIA_PATOLOGICA",
            }
            codigo_estudio = mapeo_destino_estudio.get(destino_codigo, "CULTIVO")
            try:
                tipo_estudio = Catalogo.objects.get(
                    tipo__codigo="TIPO_ESTUDIO_MICROBIOLOGICO",
                    codigo=codigo_estudio,
                    activo=True,
                )
                EstudioMicrobiologico.objects.create(
                    muestra=muestra, tipo_estudio=tipo_estudio, estado="PE"  # Pendiente
                )
                messages.success(
                    request, f"Muestra agregada con estudio {codigo_estudio}."
                )
            except Catalogo.DoesNotExist:
                messages.warning(
                    request,
                    f"No se encontró el tipo de estudio '{codigo_estudio}'. La muestra se creó sin estudio.",
                )

            # Redirigir con ancla a la muestra creada
            url = reverse("pacientes:microbiologia", kwargs={"pk": internacion.pk})
            return HttpResponseRedirect(f"{url}#muestra-{muestra.pk}")
    # ==========================================================
    # FORMULARIOS AUXILIARES
    # ==========================================================
    estudio_form = EstudioMicrobiologicoForm()
    aislamiento_form = AislamientoMicrobiologicoForm(
        germen_queryset=Catalogo.objects.none()
    )

    # Opciones para selects de micobacterias
    from .models import BaciloscopiaDetalle, CultivoDetalle, GeneXpertDetalle
    baciloscopia_opciones = BaciloscopiaDetalle.Resultado.choices
    baciloscopia_graduacion_opciones = BaciloscopiaDetalle.Graduacion.choices
    cultivo_opciones = CultivoDetalle.Resultado.choices
    genexpert_opciones = GeneXpertDetalle.Resultado.choices
    
    # ==========================================================
    # OBTENER RESULTADOS MTB POR ESTUDIO
    # ==========================================================
    resultados_mtb_por_estudio = {}
    for muestra in muestras:
        for estudio in muestra.estudios.all():
            if muestra.destino and muestra.destino.codigo == 'MTB':
                bacilo = BaciloscopiaDetalle.objects.filter(estudio=estudio).first()
                cultivo = CultivoDetalle.objects.filter(estudio=estudio).first()
                genexpert = GeneXpertDetalle.objects.filter(estudio=estudio).first()
                resultados_mtb_por_estudio[estudio.pk] = {
                    'baciloscopia_resultado': bacilo.resultado if bacilo else '',
                    'baciloscopia_graduacion': bacilo.graduacion if bacilo else '',
                    'cultivo_resultado': cultivo.resultado if cultivo else '',
                    'genexpert_mtb': genexpert.mtb_detectado if genexpert else '',
                    'genexpert_rif': genexpert.resistencia_rifampicina if genexpert else '',
                }

    # ==========================================================
    # RENDER
    # ==========================================================
    return render(
        request,
        "pacientes/microbiologia.html",
        {
            "internacion": internacion,
            "paciente": internacion.paciente,
            "muestras": muestras,
            "form": form,
            "aislamiento_form": aislamiento_form,
            "germenes_por_muestra": germenes_por_muestra,
            "estudio_form": estudio_form,
            "antimicrobianos_por_aislamiento": antimicrobianos_por_aislamiento,
            "baciloscopia_opciones": baciloscopia_opciones,
            "baciloscopia_graduacion_opciones": baciloscopia_graduacion_opciones,
            "cultivo_opciones": cultivo_opciones,
            "genexpert_opciones": genexpert_opciones,
            "resultados_mtb_por_estudio": resultados_mtb_por_estudio,   
        },
)

@login_required
def aislamiento_agregar(request, muestra_pk):
    muestra = get_object_or_404(MuestraMicrobiologica, pk=muestra_pk)
    estudio = muestra.estudios.first()

    if estudio is None:
        messages.error(request, "La muestra no posee un estudio microbiológico.")
        return redirect("pacientes:microbiologia", pk=muestra.internacion.pk)

    # ==========================================================
    # FILTRAR GÉRMENES SEGÚN EL DESTINO DE LA MUESTRA
    # ==========================================================
    destino_codigo = muestra.destino.codigo if muestra.destino else None

    if destino_codigo == 'BAC':          # Bacteriología
        germenes = Catalogo.objects.germenes_bacterias().exclude(descripcion__icontains='Mycobacterium')
    elif destino_codigo == 'MTB':        # Micobacterias (solo TBC y MNT)
        germenes = Catalogo.objects.filter(
            tipo__codigo='GERMEN',
            codigo__in=['MTB_TBC', 'MTB_NONTB'],
            activo=True
        ).order_by('orden', 'descripcion')
    elif destino_codigo == 'MIC':        # Micología
        germenes = Catalogo.objects.germenes_hongos()
    elif destino_codigo == 'VIR':        # Virología
        germenes = Catalogo.objects.germenes_virus()
    elif destino_codigo == 'PAR':        # Parasitología
        germenes = Catalogo.objects.germenes_parasitos()
    elif destino_codigo == 'PAT':        # Anatomía patológica
        germenes = Catalogo.objects.germenes()
    else:
        germenes = Catalogo.objects.germenes()  # fallback

    # ==========================================================
    # DEPURACIÓN: VER QUÉ QUERYSET ESTÁ LLEGANDO
    # ==========================================================
    print("=== GERMENES FILTRADOS ===")
    print(f"Destino: {destino_codigo}, Cantidad: {germenes.count()}")
    print("Primeros 5 IDs:", list(germenes.values_list("pk", flat=True)[:5]))

    if request.method == "POST":
        print("=== POST DATA (aislamiento) ===")
        print(request.POST)  # Muestra todo el POST

        form = AislamientoMicrobiologicoForm(request.POST, germen_queryset=germenes)

        print("=== QUERYSET DEL FORMULARIO ===")
        print(
            form.fields["germen"].queryset.count()
        )  # Debe ser el mismo que germenes.count()

        if form.is_valid():
            aislamiento = form.save(commit=False)
            aislamiento.estudio = estudio
            aislamiento.save()
            messages.success(request, "Aislamiento agregado correctamente.")
            return redirect("pacientes:microbiologia", pk=muestra.internacion.pk)
        else:
            print("=== ERRORES DEL FORMULARIO ===")
            print(form.errors)
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"{campo}: {error}")

    # Si es GET o falló el POST, redirigimos
    return redirect("pacientes:microbiologia", pk=muestra.internacion.pk)


@login_required
def aislamiento_editar(request, pk):
    aislamiento = get_object_or_404(AislamientoMicrobiologico, pk=pk)
    estudio = aislamiento.estudio
    muestra = estudio.muestra
    internacion = muestra.internacion

    # Obtener los gérmenes filtrados por destino de la muestra
    destino_codigo = muestra.destino.codigo if muestra.destino else None
    if destino_codigo == "BAC":
        germenes = Catalogo.objects.germenes_bacterias().exclude(
            descripcion__icontains="Mycobacterium"
        )
    elif destino_codigo == "MTB":
        germenes = Catalogo.objects.germenes_bacterias().filter(
            descripcion__icontains="Mycobacterium"
        )
    elif destino_codigo == "MIC":
        germenes = Catalogo.objects.germenes_hongos()
    elif destino_codigo == "VIR":
        germenes = Catalogo.objects.germenes_virus()
    elif destino_codigo == "PAR":
        germenes = Catalogo.objects.germenes_parasitos()
    elif destino_codigo == "PAT":
        germenes = Catalogo.objects.germenes()
    else:
        germenes = Catalogo.objects.germenes()

    if request.method == "POST":
        form = AislamientoMicrobiologicoEditForm(request.POST, instance=aislamiento)
        form.fields["germen"].queryset = germenes
        if form.is_valid():
            form.save()
            messages.success(request, "Aislamiento actualizado correctamente.")
            return redirect("pacientes:microbiologia", pk=internacion.pk)
    else:
        form = AislamientoMicrobiologicoEditForm(instance=aislamiento)
        form.fields["germen"].queryset = germenes

    return render(
        request,
        "pacientes/aislamiento_editar.html",
        {
            "form": form,
            "aislamiento": aislamiento,
            "muestra": muestra,
            "paciente": internacion.paciente,
            "internacion": internacion,
        },
    )


@login_required
def aislamiento_eliminar(request, pk):
    aislamiento = get_object_or_404(AislamientoMicrobiologico, pk=pk)
    muestra = aislamiento.estudio.muestra
    internacion = muestra.internacion

    if request.method == "POST":
        aislamiento.delete()
        messages.success(request, "Aislamiento eliminado correctamente.")
        return redirect("pacientes:microbiologia", pk=internacion.pk)

    return render(
        request,
        "pacientes/aislamiento_eliminar.html",
        {
            "aislamiento": aislamiento,
            "muestra": muestra,
            "paciente": internacion.paciente,
            "internacion": internacion,
        },
    )


@login_required
def sensibilidad_agregar(request, aislamiento_pk):
    aislamiento = get_object_or_404(AislamientoMicrobiologico, pk=aislamiento_pk)
    muestra = aislamiento.estudio.muestra
    internacion = muestra.internacion

    if request.method == "POST":
        antibiotico_id = request.POST.get("antibiotico")
        resultado = request.POST.get("resultado")

        if antibiotico_id and resultado:
            antibiotico = get_object_or_404(Catalogo, pk=antibiotico_id)
            SensibilidadMicrobiologica.objects.create(
                aislamiento=aislamiento, antibiotico=antibiotico, resultado=resultado
            )
            messages.success(request, "Sensibilidad agregada correctamente.")
        else:
            messages.error(
                request, "Debe seleccionar un antimicrobiano y un resultado."
            )
        return redirect("pacientes:microbiologia", pk=internacion.pk)

    return redirect("pacientes:microbiologia", pk=internacion.pk)


@login_required
def resultados_tbc(request, estudio_pk):
    estudio = get_object_or_404(EstudioMicrobiologico, pk=estudio_pk)
    muestra = estudio.muestra
    internacion = muestra.internacion

    if muestra.destino.codigo != 'MTB':
        messages.warning(request, "Esta muestra no es para micobacterias.")
        return redirect("pacientes:microbiologia", pk=internacion.pk)

    if request.method == 'POST':
        # Baciloscopía
        bac_resultado = request.POST.get('baciloscopia_resultado')
        bac_graduacion = request.POST.get('baciloscopia_graduacion')
        if bac_resultado:
            BaciloscopiaDetalle.objects.update_or_create(
                estudio=estudio,
                defaults={
                    'resultado': bac_resultado,
                    'graduacion': bac_graduacion or '',
                }
            )
        else:
            BaciloscopiaDetalle.objects.filter(estudio=estudio).delete()

        # Cultivo
        cultivo_resultado = request.POST.get('cultivo_resultado')
        if cultivo_resultado:
            CultivoDetalle.objects.update_or_create(
                estudio=estudio,
                defaults={
                    'tipo_cultivo': 'MTB',
                    'resultado': cultivo_resultado,
                }
            )
        else:
            CultivoDetalle.objects.filter(estudio=estudio).delete()

        # GeneXpert
        genexpert_mtb = request.POST.get('genexpert_mtb')
        genexpert_rif = request.POST.get('genexpert_rif')
        if genexpert_mtb:
            GeneXpertDetalle.objects.update_or_create(
                estudio=estudio,
                defaults={
                    'mtb_detectado': genexpert_mtb,
                    'resistencia_rifampicina': genexpert_rif or '',
                }
            )
        else:
            GeneXpertDetalle.objects.filter(estudio=estudio).delete()

        messages.success(request, "Resultados de micobacterias guardados correctamente.")
        return redirect("pacientes:microbiologia", pk=internacion.pk)

    # Si es GET, redirigir a microbiología (ya no usamos template)
    return redirect("pacientes:microbiologia", pk=internacion.pk)


# ==========================================================
# ESTUDIOS Y PROCEDIMIENTOS
# ==========================================================


@login_required
def estudios_procedimientos_view(request, pk):
    internacion = get_object_or_404(Internacion, pk=pk)
    paciente = internacion.paciente

    seccion = request.GET.get("seccion", "tomografias")

    context = {
        "internacion": internacion,
        "paciente": paciente,
        "seccion": seccion,
        "tomografias": (
            internacion.tomografias.all().order_by("-fecha")
            if seccion == "tomografias"
            else None
        ),
    }

    return render(request, "pacientes/estudios_procedimientos.html", context)


@login_required
def tomografia_agregar(request, internacion_pk):
    internacion = get_object_or_404(Internacion, pk=internacion_pk)

    # Obtener el tipo de la URL (GET)
    tipo_codigo = request.GET.get("tipo")

    if request.method == "POST":
        form = TomografiaForm(request.POST)
        if form.is_valid():
            tomografia = form.save(commit=False)
            tomografia.internacion = internacion
            tomografia.save()
            if "hallazgos" in request.POST:
                tomografia.hallazgos.set(request.POST.getlist("hallazgos"))
            messages.success(request, "Tomografía agregada correctamente.")
            return redirect("pacientes:estudios_procedimientos", pk=internacion_pk)
    else:
        # GET: inicializar con el tipo seleccionado (si existe)
        initial = {}
        if tipo_codigo:
            initial["tipo"] = tipo_codigo
        form = TomografiaForm(initial=initial)

    # Construir hallazgos según el tipo seleccionado
    hallazgos_agrupados = {}
    if tipo_codigo == "TORAX":
        hallazgos_agrupados["TORAX"] = Catalogo.objects.filter(
            tipo__codigo="HALLAZGO_TORAX", activo=True
        ).order_by("descripcion")
    elif tipo_codigo == "ANGIO_TORAX":
        hallazgos_agrupados["ANGIO"] = Catalogo.objects.filter(
            tipo__codigo="HALLAZGO_ANGIO", activo=True
        ).order_by("descripcion")
    elif tipo_codigo == "MACIZO_FACIAL":
        hallazgos_agrupados["MACIZO"] = Catalogo.objects.filter(
            tipo__codigo="HALLAZGO_MACIZO", activo=True
        ).order_by("descripcion")
    # Si no hay tipo, no mostrar ningún grupo

    return render(
        request,
        "pacientes/tomografia_form.html",
        {
            "form": form,
            "internacion": internacion,
            "paciente": internacion.paciente,
            "hallazgos_agrupados": hallazgos_agrupados,
            "tipo_seleccionado": tipo_codigo,
        },
    )


@login_required
def tomografia_editar(request, pk):
    tomografia = get_object_or_404(Tomografia, pk=pk)
    internacion = tomografia.internacion

    tipo_codigo = (
        request.GET.get("tipo") or tomografia.tipo.codigo if tomografia.tipo else None
    )

    if request.method == "POST":
        form = TomografiaForm(request.POST, instance=tomografia)
        if form.is_valid():
            form.save()
            if "hallazgos" in request.POST:
                tomografia.hallazgos.set(request.POST.getlist("hallazgos"))
            messages.success(request, "Tomografía actualizada.")
            return redirect("pacientes:estudios_procedimientos", pk=internacion.pk)
    else:
        form = TomografiaForm(instance=tomografia)

    hallazgos_agrupados = {}
    if tipo_codigo == "TORAX":
        hallazgos_agrupados["TORAX"] = Catalogo.objects.filter(
            tipo__codigo="HALLAZGO_TORAX", activo=True
        ).order_by("descripcion")
    elif tipo_codigo == "ANGIO_TORAX":
        hallazgos_agrupados["ANGIO"] = Catalogo.objects.filter(
            tipo__codigo="HALLAZGO_ANGIO", activo=True
        ).order_by("descripcion")
    elif tipo_codigo == "MACIZO_FACIAL":
        hallazgos_agrupados["MACIZO"] = Catalogo.objects.filter(
            tipo__codigo="HALLAZGO_MACIZO", activo=True
        ).order_by("descripcion")

    return render(
        request,
        "pacientes/tomografia_form.html",
        {
            "form": form,
            "internacion": internacion,
            "paciente": internacion.paciente,
            "hallazgos_agrupados": hallazgos_agrupados,
            "tipo_seleccionado": tipo_codigo,
            "tomografia": tomografia,
        },
    )


@login_required
def tomografia_eliminar(request, pk):
    tomografia = get_object_or_404(Tomografia, pk=pk)
    internacion = tomografia.internacion
    if request.method == "POST":
        tomografia.delete()
        messages.success(request, "Tomografía eliminada correctamente.")
        return redirect("pacientes:estudios_procedimientos", pk=internacion.pk)
    return render(
        request,
        "pacientes/tomografia_confirm_delete.html",
        {
            "tomografia": tomografia,
            "internacion": internacion,
            "paciente": internacion.paciente,
        },
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
