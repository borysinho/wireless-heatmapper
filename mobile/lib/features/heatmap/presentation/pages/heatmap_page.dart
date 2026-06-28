import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../domain/entities/ap_disponible.dart';
import '../../domain/entities/conjunto_ap.dart';
import '../../domain/entities/escala_heatmap.dart';
import '../../domain/entities/mapa_calor.dart';
import '../../../planos/domain/entities/plano.dart';
import '../cubit/heatmap_cubit.dart';
import '../cubit/heatmap_state.dart';

/// Pantalla de heatmap. Sprint 4 — PB-05.
class HeatmapPage extends StatefulWidget {
  final int planoId;
  final String imagenUrl;
  final double anchoPlanoPx;
  final double altoPlanoPx;

  const HeatmapPage({
    super.key,
    required this.planoId,
    required this.imagenUrl,
    required this.anchoPlanoPx,
    required this.altoPlanoPx,
  });

  @override
  State<HeatmapPage> createState() => _HeatmapPageState();
}

class _HeatmapPageState extends State<HeatmapPage> {
  String _algoritmo = 'IDW';
  int _resolucion = 128;

  Size get _tamanoPlano => Size(widget.anchoPlanoPx, widget.altoPlanoPx);

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _cargar());
  }

  void _cargar() {
    context.read<HeatmapCubit>().iniciar(widget.planoId);
  }

  void _generarHeatmap() {
    context.read<HeatmapCubit>().generar(
          planoId: widget.planoId,
          algoritmo: _algoritmo,
          resolucion: _resolucion,
        );
  }

  void _alternarFiltroAP(APDisponible ap) {
    context.read<HeatmapCubit>().alternarFiltroAP(
          planoId: widget.planoId,
          ap: ap,
          algoritmo: _algoritmo,
          resolucion: _resolucion,
        );
  }

  void _limpiarFiltroAP() {
    context.read<HeatmapCubit>().limpiarFiltroAP(
          planoId: widget.planoId,
          algoritmo: _algoritmo,
          resolucion: _resolucion,
        );
  }

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<HeatmapCubit, HeatmapState>(
      listener: (context, state) {
        if (state is HeatmapReady && state.mensaje != null) {
          ScaffoldMessenger.of(context)
            ..clearSnackBars()
            ..showSnackBar(SnackBar(content: Text(state.mensaje!)));
        } else if (state is HeatmapSeleccionAP && state.mensaje != null) {
          ScaffoldMessenger.of(context)
            ..clearSnackBars()
            ..showSnackBar(SnackBar(content: Text(state.mensaje!)));
        } else if (state is HeatmapConjuntos && state.mensaje != null) {
          ScaffoldMessenger.of(context)
            ..clearSnackBars()
            ..showSnackBar(SnackBar(content: Text(state.mensaje!)));
        } else if (state is HeatmapError) {
          ScaffoldMessenger.of(context)
            ..clearSnackBars()
            ..showSnackBar(
              SnackBar(
                content: Text(state.mensaje),
                backgroundColor: Theme.of(context).colorScheme.error,
              ),
            );
        }
      },
      builder: (context, state) {
        final listo = state is HeatmapReady ? state : null;
        final apsSeleccionadosListo = listo == null
            ? <APDisponible>[]
            : listo.aps
                .where((ap) => listo.bssidsSeleccionados.contains(ap.bssid))
                .toList();
        final apsInteresListo = listo == null
            ? <APDisponible>[]
            : listo.bssidActivo == null
                ? apsSeleccionadosListo
                : apsSeleccionadosListo
                    .where((ap) => ap.bssid == listo.bssidActivo)
                    .toList();
        return Scaffold(
          appBar: AppBar(
            title: Text(
              state is HeatmapConjuntos ? 'Conjuntos de APs' : 'Heatmap',
            ),
            actions: [
              if (state is HeatmapConjuntos)
                IconButton(
                  tooltip: 'Crear conjunto',
                  icon: const Icon(Icons.add),
                  onPressed: () => _mostrarCrearConjunto(state),
                ),
              if (state is HeatmapSeleccionAP || state is HeatmapReady)
                IconButton(
                  tooltip: 'Conjuntos',
                  icon: const Icon(Icons.list_alt),
                  onPressed: context.read<HeatmapCubit>().volverAConjuntos,
                ),
              if (state is HeatmapSeleccionAP || state is HeatmapReady) ...[
                _SelectorAlgoritmo(
                  valor: _algoritmo,
                  onChanged: (valor) => setState(() => _algoritmo = valor),
                ),
                _SelectorResolucion(
                  valor: _resolucion,
                  onChanged: (valor) => setState(() => _resolucion = valor),
                ),
                IconButton(
                  tooltip: 'Actualizar',
                  icon: const Icon(Icons.refresh),
                  onPressed: _cargar,
                ),
              ],
            ],
          ),
          body: switch (state) {
            HeatmapInitial() =>
              const Center(child: CircularProgressIndicator()),
            HeatmapLoading(:final mensaje) => Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const CircularProgressIndicator(),
                    const SizedBox(height: 12),
                    Text(mensaje),
                  ],
                ),
              ),
            HeatmapError(:final mensaje) => _HeatmapErrorView(
                mensaje: mensaje,
                onRetry: _cargar,
              ),
            HeatmapConjuntos() => _ConjuntosAPView(
                state: state,
                onAbrir: context.read<HeatmapCubit>().abrirConjunto,
                onCrear: () => _mostrarCrearConjunto(state),
                onEditar: (conjunto) => _mostrarEditarConjunto(state, conjunto),
                onEliminar: _confirmarEliminarConjunto,
              ),
            HeatmapSeleccionAP() => Column(
                children: [
                  Expanded(
                    child: _HeatmapCanvas(
                      planoUrl: widget.imagenUrl,
                      tamanoPlano: _tamanoPlano,
                      apsInteres: state.apsSeleccionados,
                      bssidActivo: state.bssidActivo,
                      apPosXPorBssid: state.apPosXPorBssid,
                      apPosYPorBssid: state.apPosYPorBssid,
                      onTapPlano: (pos) =>
                          context.read<HeatmapCubit>().ubicarAP(
                                posX: pos.dx,
                                posY: pos.dy,
                              ),
                      onTapAPInteres: (ap) =>
                          context.read<HeatmapCubit>().activarAP(ap),
                      onMoverAPInteres: (ap, pos) =>
                          context.read<HeatmapCubit>().ubicarAP(
                                bssid: ap.bssid,
                                posX: pos.dx,
                                posY: pos.dy,
                                persistir: false,
                              ),
                      onSoltarAPInteres: (ap, pos) =>
                          context.read<HeatmapCubit>().ubicarAP(
                                bssid: ap.bssid,
                                posX: pos.dx,
                                posY: pos.dy,
                                persistir: true,
                              ),
                    ),
                  ),
                  _SeleccionAPPanel(
                    state: state,
                    onAlternar: (ap) =>
                        context.read<HeatmapCubit>().alternarAPInteres(ap),
                    onGenerar: _generarHeatmap,
                  ),
                ],
              ),
            HeatmapReady() => Column(
                children: [
                  Expanded(
                    child: _HeatmapCanvas(
                      planoUrl: widget.imagenUrl,
                      heatmapMatriz: listo!.mapa.matriz,
                      puntosLectura: listo.mapa.puntosLectura,
                      poligonoInteres: listo.mapa.poligonoInteres,
                      tamanoPlano: _tamanoPlano,
                      apsInteres: apsInteresListo,
                      bssidActivo: listo.bssidActivo,
                      apPosXPorBssid: {
                        for (final ap in apsInteresListo)
                          ap.bssid: listo.apPosXPorBssid[ap.bssid] ?? ap.posX,
                      },
                      apPosYPorBssid: {
                        for (final ap in apsInteresListo)
                          ap.bssid: listo.apPosYPorBssid[ap.bssid] ?? ap.posY,
                      },
                      onTapPlano: (_) => _limpiarFiltroAP(),
                      onTapAPInteres: _alternarFiltroAP,
                      onTapPuntoLectura: _mostrarDetallePuntoLectura,
                    ),
                  ),
                  _HeatmapInfoPanel(
                    mapa: listo.mapa,
                    escala: listo.mapa.escala,
                    apsInteres: apsInteresListo,
                    bssidActivo: listo.bssidActivo,
                    onLimpiarFiltro: _limpiarFiltroAP,
                    onRegenerarHeatmap: _generarHeatmap,
                  ),
                ],
              ),
          },
        );
      },
    );
  }

  void _mostrarDetallePuntoLectura(PuntoLecturaHeatmap punto) {
    showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      builder: (ctx) => _PuntoLecturaSheet(punto: punto),
    );
  }

  void _mostrarCrearConjunto(HeatmapConjuntos state) {
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      builder: (ctx) => _CrearConjuntoAPSheet(
        aps: state.aps,
        onGuardar: ({
          required nombre,
          required proposito,
          required bssids,
        }) {
          context.read<HeatmapCubit>().crearConjunto(
                planoId: widget.planoId,
                nombre: nombre,
                proposito: proposito,
                descripcion: null,
                bssids: bssids,
              );
        },
      ),
    );
  }

  void _mostrarEditarConjunto(HeatmapConjuntos state, ConjuntoAP conjunto) {
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      builder: (ctx) => _CrearConjuntoAPSheet(
        aps: state.aps,
        conjunto: conjunto,
        onGuardar: ({
          required nombre,
          required proposito,
          required bssids,
        }) {
          context.read<HeatmapCubit>().actualizarConjunto(
                conjuntoId: conjunto.id,
                nombre: nombre,
                proposito: proposito,
                descripcion: null,
                bssids: bssids,
              );
        },
      ),
    );
  }

  Future<void> _confirmarEliminarConjunto(ConjuntoAP conjunto) async {
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Eliminar conjunto'),
        content: Text('Se eliminará "${conjunto.nombre}".'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(false),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            onPressed: () => Navigator.of(ctx).pop(true),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );
    if (!mounted) return;
    if (confirmar ?? false) {
      context.read<HeatmapCubit>().eliminarConjunto(conjunto.id);
    }
  }
}

class _CrearConjuntoAPSheet extends StatefulWidget {
  final List<APDisponible> aps;
  final ConjuntoAP? conjunto;
  final void Function({
    required String nombre,
    required String proposito,
    required List<String> bssids,
  }) onGuardar;

  const _CrearConjuntoAPSheet({
    required this.aps,
    this.conjunto,
    required this.onGuardar,
  });

  @override
  State<_CrearConjuntoAPSheet> createState() => _CrearConjuntoAPSheetState();
}

class _CrearConjuntoAPSheetState extends State<_CrearConjuntoAPSheet> {
  late final TextEditingController _nombreCtrl;
  late final TextEditingController _propositoCtrl;
  late final TextEditingController _filtroCtrl;
  late final Set<String> _seleccionados;

  @override
  void initState() {
    super.initState();
    _nombreCtrl = TextEditingController(text: widget.conjunto?.nombre ?? '');
    _propositoCtrl = TextEditingController(
      text: widget.conjunto?.proposito ?? '',
    );
    _filtroCtrl = TextEditingController();
    _seleccionados = widget.conjunto == null
        ? {for (final ap in widget.aps) ap.bssid}
        : {for (final ap in widget.conjunto!.items) ap.bssid};
  }

  @override
  void dispose() {
    _nombreCtrl.dispose();
    _propositoCtrl.dispose();
    _filtroCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final filtro = _filtroCtrl.text.trim().toLowerCase();
    final apsFiltrados = filtro.isEmpty
        ? widget.aps
        : widget.aps.where((ap) {
            final canal = ap.canal?.toString() ?? '';
            return ap.ssid.toLowerCase().contains(filtro) ||
                ap.bssid.toLowerCase().contains(filtro) ||
                canal.contains(filtro);
          }).toList();
    final todosSeleccionados = _seleccionados.length == widget.aps.length;
    return Padding(
      padding: EdgeInsets.fromLTRB(
        20,
        8,
        20,
        24 + MediaQuery.of(context).viewInsets.bottom,
      ),
      child: ListView(
        shrinkWrap: true,
        children: [
          Text(
            widget.conjunto == null
                ? 'Nuevo conjunto de APs'
                : 'Editar conjunto de APs',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _nombreCtrl,
            decoration: const InputDecoration(labelText: 'Nombre'),
            textInputAction: TextInputAction.next,
          ),
          const SizedBox(height: 8),
          TextField(
            controller: _propositoCtrl,
            decoration: const InputDecoration(labelText: 'Propósito opcional'),
            maxLines: 2,
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: Text(
                  'APs seleccionados: ${_seleccionados.length}/${widget.aps.length}',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
              ),
              TextButton.icon(
                onPressed: () {
                  setState(() {
                    if (todosSeleccionados) {
                      _seleccionados.clear();
                    } else {
                      _seleccionados
                        ..clear()
                        ..addAll(widget.aps.map((ap) => ap.bssid));
                    }
                  });
                },
                icon: Icon(
                  todosSeleccionados
                      ? Icons.deselect_outlined
                      : Icons.select_all,
                ),
                label: Text(
                  todosSeleccionados ? 'Desmarcar todos' : 'Marcar todos',
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          TextField(
            controller: _filtroCtrl,
            decoration: InputDecoration(
              labelText: 'Filtrar APs',
              prefixIcon: const Icon(Icons.search),
              suffixIcon: _filtroCtrl.text.isEmpty
                  ? null
                  : IconButton(
                      tooltip: 'Limpiar filtro',
                      icon: const Icon(Icons.close),
                      onPressed: () {
                        _filtroCtrl.clear();
                        setState(() {});
                      },
                    ),
            ),
            onChanged: (_) => setState(() {}),
          ),
          const SizedBox(height: 8),
          if (apsFiltrados.isEmpty)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 16),
              child: Text('No hay APs que coincidan con el filtro.'),
            )
          else
            ...apsFiltrados.map(
              (ap) => CheckboxListTile(
                value: _seleccionados.contains(ap.bssid),
                onChanged: (checked) {
                  setState(() {
                    if (checked ?? false) {
                      _seleccionados.add(ap.bssid);
                    } else {
                      _seleccionados.remove(ap.bssid);
                    }
                  });
                },
                title: Text(ap.ssid.isEmpty ? 'SSID oculto' : ap.ssid),
                subtitle: Text(_detalleAP(ap)),
              ),
            ),
          const SizedBox(height: 12),
          FilledButton.icon(
            onPressed: _guardar,
            icon: const Icon(Icons.save_outlined),
            label: Text(
              widget.conjunto == null ? 'Guardar conjunto' : 'Guardar cambios',
            ),
          ),
        ],
      ),
    );
  }

  void _guardar() {
    final nombre = _nombreCtrl.text.trim();
    final proposito = _propositoCtrl.text.trim();
    if (nombre.isEmpty) {
      _mostrarMensaje('El nombre es obligatorio.');
      return;
    }
    if (_seleccionados.isEmpty) {
      _mostrarMensaje('Selecciona al menos un AP.');
      return;
    }
    widget.onGuardar(
      nombre: nombre,
      proposito: proposito,
      bssids: _seleccionados.toList(),
    );
    Navigator.of(context).pop();
  }

  void _mostrarMensaje(String mensaje) {
    ScaffoldMessenger.of(context)
      ..clearSnackBars()
      ..showSnackBar(SnackBar(content: Text(mensaje)));
  }
}

class _ConjuntosAPView extends StatelessWidget {
  final HeatmapConjuntos state;
  final ValueChanged<ConjuntoAP> onAbrir;
  final VoidCallback onCrear;
  final ValueChanged<ConjuntoAP> onEditar;
  final ValueChanged<ConjuntoAP> onEliminar;

  const _ConjuntosAPView({
    required this.state,
    required this.onAbrir,
    required this.onCrear,
    required this.onEditar,
    required this.onEliminar,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 24),
      children: [
        Row(
          children: [
            Expanded(
              child: Text(
                'Conjuntos de APs',
                style: theme.textTheme.titleLarge,
              ),
            ),
            FilledButton.icon(
              onPressed: onCrear,
              icon: const Icon(Icons.add),
              label: const Text('Crear'),
            ),
          ],
        ),
        const SizedBox(height: 18),
        if (state.conjuntos.isEmpty)
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Sin conjuntos creados',
                      style: theme.textTheme.titleMedium),
                  const SizedBox(height: 6),
                  Text(
                    'Crea un conjunto para generar heatmaps focalizados.',
                    style: theme.textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
          )
        else
          ...state.conjuntos.map(
            (conjunto) => _ConjuntoAPTile(
              conjunto: conjunto,
              onTap: () => onAbrir(conjunto),
              onEditar: () => onEditar(conjunto),
              onEliminar: () => onEliminar(conjunto),
            ),
          ),
      ],
    );
  }
}

class _ConjuntoAPTile extends StatelessWidget {
  final ConjuntoAP conjunto;
  final VoidCallback onTap;
  final VoidCallback onEditar;
  final VoidCallback onEliminar;

  const _ConjuntoAPTile({
    required this.conjunto,
    required this.onTap,
    required this.onEditar,
    required this.onEliminar,
  });

  @override
  Widget build(BuildContext context) {
    final proposito = conjunto.proposito.trim();
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Card(
        margin: EdgeInsets.zero,
        child: ListTile(
          onTap: onTap,
          leading: const Icon(Icons.wifi_tethering),
          title: Text(conjunto.nombre),
          subtitle: Text(
            proposito.isEmpty
                ? '${conjunto.cantidadAps} APs'
                : '$proposito\n${conjunto.cantidadAps} APs',
          ),
          isThreeLine: proposito.isNotEmpty,
          trailing: PopupMenuButton<_AccionConjuntoAP>(
            tooltip: 'Opciones',
            onSelected: (accion) {
              switch (accion) {
                case _AccionConjuntoAP.abrir:
                  onTap();
                case _AccionConjuntoAP.editar:
                  onEditar();
                case _AccionConjuntoAP.eliminar:
                  onEliminar();
              }
            },
            itemBuilder: (ctx) => const [
              PopupMenuItem(
                value: _AccionConjuntoAP.abrir,
                child: ListTile(
                  leading: Icon(Icons.open_in_new),
                  title: Text('Abrir'),
                ),
              ),
              PopupMenuItem(
                value: _AccionConjuntoAP.editar,
                child: ListTile(
                  leading: Icon(Icons.edit_outlined),
                  title: Text('Editar'),
                ),
              ),
              PopupMenuItem(
                value: _AccionConjuntoAP.eliminar,
                child: ListTile(
                  leading: Icon(Icons.delete_outline),
                  title: Text('Eliminar'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

enum _AccionConjuntoAP { abrir, editar, eliminar }

class _HeatmapCanvas extends StatefulWidget {
  final String planoUrl;
  final List<List<double>>? heatmapMatriz;
  final List<PuntoLecturaHeatmap> puntosLectura;
  final List<PuntoPlano> poligonoInteres;
  final Size tamanoPlano;
  final List<APDisponible> apsInteres;
  final String? bssidActivo;
  final Map<String, double> apPosXPorBssid;
  final Map<String, double> apPosYPorBssid;
  final void Function(Offset posPlano)? onTapPlano;
  final void Function(APDisponible ap)? onTapAPInteres;
  final void Function(APDisponible ap, Offset posPlano)? onMoverAPInteres;
  final void Function(APDisponible ap, Offset posPlano)? onSoltarAPInteres;
  final void Function(PuntoLecturaHeatmap punto)? onTapPuntoLectura;

  const _HeatmapCanvas({
    required this.planoUrl,
    this.heatmapMatriz,
    this.puntosLectura = const [],
    this.poligonoInteres = const [],
    required this.tamanoPlano,
    this.apsInteres = const [],
    this.bssidActivo,
    this.apPosXPorBssid = const {},
    this.apPosYPorBssid = const {},
    this.onTapPlano,
    this.onTapAPInteres,
    this.onMoverAPInteres,
    this.onSoltarAPInteres,
    this.onTapPuntoLectura,
  });

  @override
  State<_HeatmapCanvas> createState() => _HeatmapCanvasState();
}

class _HeatmapCanvasState extends State<_HeatmapCanvas> {
  static const double _hitRadioPx = 24.0;
  static const double _apMarkerSize = 32.0;
  static const double _apMarkerHalf = _apMarkerSize / 2;

  final TransformationController _transformController =
      TransformationController();

  Offset? _ultimoTapDown;
  String? _bssidArrastrado;
  Offset? _ultimaPosArrastradaPlano;
  double _zoomEscala = 1.0;

  @override
  void initState() {
    super.initState();
    _transformController.addListener(_actualizarZoomEscala);
  }

  @override
  void dispose() {
    _transformController.removeListener(_actualizarZoomEscala);
    _transformController.dispose();
    super.dispose();
  }

  void _actualizarZoomEscala() {
    final nuevaEscala = _transformController.value.getMaxScaleOnAxis();
    if ((nuevaEscala - _zoomEscala).abs() > 0.001) {
      setState(() => _zoomEscala = nuevaEscala);
    }
  }

  @override
  Widget build(BuildContext context) {
    return InteractiveViewer(
      transformationController: _transformController,
      panEnabled: true,
      scaleEnabled: true,
      minScale: 0.5,
      maxScale: 5,
      child: LayoutBuilder(
        builder: (context, constraints) {
          final puedeTocar = widget.onTapPlano != null ||
              widget.onTapAPInteres != null ||
              widget.onTapPuntoLectura != null;
          final aspect = widget.tamanoPlano.width / widget.tamanoPlano.height;
          double w = constraints.maxWidth;
          double h = w / aspect;
          if (h > constraints.maxHeight) {
            h = constraints.maxHeight;
            w = h * aspect;
          }
          return Center(
            child: SizedBox(
              width: w,
              height: h,
              child: GestureDetector(
                behavior: HitTestBehavior.opaque,
                onTapDown: puedeTocar
                    ? (details) => _ultimoTapDown = details.localPosition
                    : null,
                onTap: puedeTocar ? () => _onTap(w: w, h: h) : null,
                onLongPressStart: widget.onMoverAPInteres == null
                    ? null
                    : (details) => _onLongPressStart(details, w: w, h: h),
                onLongPressMoveUpdate: widget.onMoverAPInteres == null
                    ? null
                    : (details) => _onLongPressMoveUpdate(
                          details,
                          w: w,
                          h: h,
                        ),
                onLongPressEnd: widget.onMoverAPInteres == null
                    ? null
                    : (_) => _onLongPressEnd(),
                child: Stack(
                  fit: StackFit.expand,
                  children: [
                    Image.network(
                      widget.planoUrl,
                      fit: BoxFit.fill,
                      errorBuilder: (_, __, ___) => const Center(
                        child: Icon(Icons.broken_image, size: 56),
                      ),
                    ),
                    if (widget.heatmapMatriz != null)
                      CustomPaint(
                        isComplex: true,
                        painter: _HeatmapMatrixPainter(
                          matriz: widget.heatmapMatriz!,
                          poligonoInteres: widget.poligonoInteres,
                          tamanoPlano: widget.tamanoPlano,
                        ),
                      ),
                    if (widget.puntosLectura.isNotEmpty)
                      CustomPaint(
                        painter: _PuntosLecturaPainter(
                          puntos: widget.puntosLectura,
                          tamanoPlano: widget.tamanoPlano,
                          zoomEscala: _zoomEscala,
                        ),
                      ),
                    ...widget.apsInteres.map((ap) {
                      final escalaMarcador =
                          _zoomEscala <= 0 ? 1.0 : 1.0 / _zoomEscala;
                      final posX = widget.apPosXPorBssid[ap.bssid] ?? ap.posX;
                      final posY = widget.apPosYPorBssid[ap.bssid] ?? ap.posY;
                      final activo = ap.bssid == widget.bssidActivo ||
                          ap.bssid == _bssidArrastrado;
                      final left = ((posX / widget.tamanoPlano.width) * w -
                              _apMarkerHalf)
                          .clamp(0, w - _apMarkerSize)
                          .toDouble();
                      final top = ((posY / widget.tamanoPlano.height) * h -
                              _apMarkerHalf)
                          .clamp(0, h - _apMarkerSize)
                          .toDouble();
                      return Positioned(
                        left: left,
                        top: top,
                        child: Transform.scale(
                          scale: escalaMarcador,
                          child: _APInteresMarker(ap: ap, activo: activo),
                        ),
                      );
                    }),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  void _onTap({required double w, required double h}) {
    final pos = _ultimoTapDown;
    if (pos == null) return;
    final ap = _apEnPosicion(pos, w: w, h: h);
    if (ap != null) {
      widget.onTapAPInteres?.call(ap);
      return;
    }
    final punto = _puntoLecturaEnPosicion(pos, w: w, h: h);
    if (punto != null) {
      widget.onTapPuntoLectura?.call(punto);
      return;
    }
    widget.onTapPlano?.call(_tapAPlano(pos, w: w, h: h));
  }

  void _onLongPressStart(
    LongPressStartDetails details, {
    required double w,
    required double h,
  }) {
    final ap = _apEnPosicion(details.localPosition, w: w, h: h);
    if (ap == null) return;
    setState(() => _bssidArrastrado = ap.bssid);
    _ultimaPosArrastradaPlano = _tapAPlano(details.localPosition, w: w, h: h);
    widget.onTapAPInteres?.call(ap);
  }

  void _onLongPressMoveUpdate(
    LongPressMoveUpdateDetails details, {
    required double w,
    required double h,
  }) {
    final bssid = _bssidArrastrado;
    if (bssid == null) return;
    final ap = _apPorBssid(bssid);
    if (ap == null) return;
    final pos = _tapAPlano(details.localPosition, w: w, h: h);
    _ultimaPosArrastradaPlano = pos;
    widget.onMoverAPInteres?.call(ap, pos);
  }

  void _onLongPressEnd() {
    final bssid = _bssidArrastrado;
    final pos = _ultimaPosArrastradaPlano;
    final ap = bssid == null ? null : _apPorBssid(bssid);
    if (ap != null && pos != null) {
      widget.onSoltarAPInteres?.call(ap, pos);
    }
    setState(() => _bssidArrastrado = null);
    _ultimaPosArrastradaPlano = null;
  }

  APDisponible? _apEnPosicion(
    Offset local, {
    required double w,
    required double h,
  }) {
    for (final ap in widget.apsInteres.reversed) {
      final posX = widget.apPosXPorBssid[ap.bssid] ?? ap.posX;
      final posY = widget.apPosYPorBssid[ap.bssid] ?? ap.posY;
      final pantalla = Offset(
        (posX / widget.tamanoPlano.width) * w,
        (posY / widget.tamanoPlano.height) * h,
      );
      if ((local - pantalla).distance <= _hitRadioPx) return ap;
    }
    return null;
  }

  APDisponible? _apPorBssid(String bssid) {
    for (final ap in widget.apsInteres) {
      if (ap.bssid == bssid) return ap;
    }
    return null;
  }

  PuntoLecturaHeatmap? _puntoLecturaEnPosicion(
    Offset local, {
    required double w,
    required double h,
  }) {
    if (widget.onTapPuntoLectura == null) return null;
    for (final punto in widget.puntosLectura.reversed) {
      final pantalla = Offset(
        (punto.posX / widget.tamanoPlano.width) * w,
        (punto.posY / widget.tamanoPlano.height) * h,
      );
      if ((local - pantalla).distance <= 18 / _zoomEscala) return punto;
    }
    return null;
  }

  Offset _tapAPlano(
    Offset tap, {
    required double w,
    required double h,
  }) {
    return Offset(
      ((tap.dx / w) * widget.tamanoPlano.width)
          .clamp(0.0, widget.tamanoPlano.width)
          .toDouble(),
      ((tap.dy / h) * widget.tamanoPlano.height)
          .clamp(0.0, widget.tamanoPlano.height)
          .toDouble(),
    );
  }
}

class _APInteresMarker extends StatelessWidget {
  final APDisponible ap;
  final bool activo;

  const _APInteresMarker({
    required this.ap,
    required this.activo,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final color = theme.colorScheme.surfaceContainerHighest;
    final borde = activo
        ? Border.all(color: Colors.amberAccent, width: 2.5)
        : Border.all(
            color: theme.colorScheme.outline.withValues(alpha: 0.55),
            width: 1,
          );
    return Semantics(
      label: ap.ssid.isEmpty ? ap.bssid : ap.ssid,
      child: IgnorePointer(
        child: DecoratedBox(
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
            border: borde,
            boxShadow: const [
              BoxShadow(
                blurRadius: 6,
                offset: Offset(0, 2),
                color: Color(0x33000000),
              ),
            ],
          ),
          child: const SizedBox(
            width: 32,
            height: 32,
            child: Icon(Icons.router, color: Colors.white, size: 15),
          ),
        ),
      ),
    );
  }
}

class _PanelHeader extends StatelessWidget {
  final String titulo;
  final String subtitulo;
  final Widget accion;

  const _PanelHeader({
    required this.titulo,
    required this.subtitulo,
    required this.accion,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                titulo,
                style: theme.textTheme.titleSmall,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 2),
              Text(
                subtitulo,
                style: theme.textTheme.bodySmall,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
        accion,
      ],
    );
  }
}

class _SeleccionAPPanel extends StatelessWidget {
  final HeatmapSeleccionAP state;
  final ValueChanged<APDisponible> onAlternar;
  final VoidCallback onGenerar;

  const _SeleccionAPPanel({
    required this.state,
    required this.onAlternar,
    required this.onGenerar,
  });

  @override
  Widget build(BuildContext context) {
    final ap = state.apActivo;
    final theme = Theme.of(context);
    return Material(
      elevation: 8,
      color: theme.colorScheme.surface,
      child: SafeArea(
        top: false,
        child: _PanelInferiorDesplazable(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _PanelHeader(
                  titulo: 'APs (${state.apsSeleccionados.length})',
                  subtitulo: 'Toca un marcador para moverlo o seleccionarlo.',
                  accion: IconButton(
                    tooltip: 'Cambiar APs',
                    onPressed: () => _mostrarSelectorAP(context),
                    icon: const Icon(Icons.playlist_add_check),
                  ),
                ),
                const SizedBox(height: 8),
                _APSeleccionadoTile(
                  ap: ap,
                  onTap: () => _mostrarSelectorAP(context),
                ),
                const SizedBox(height: 10),
                SizedBox(
                  width: double.infinity,
                  child: FilledButton.icon(
                    onPressed: onGenerar,
                    icon: const Icon(Icons.local_fire_department_outlined),
                    label: const Text('Generar heatmap'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _mostrarSelectorAP(BuildContext context) {
    final cubit = context.read<HeatmapCubit>();
    showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      isScrollControlled: true,
      builder: (ctx) => BlocBuilder<HeatmapCubit, HeatmapState>(
        bloc: cubit,
        builder: (context, cubitState) {
          final selectorState =
              cubitState is HeatmapSeleccionAP ? cubitState : state;
          return _SelectorAPSheet(
            aps: selectorState.aps,
            bssidsSeleccionados: selectorState.bssidsSeleccionados,
            bssidActivo: selectorState.bssidActivo,
            onAlternar: onAlternar,
          );
        },
      ),
    );
  }
}

class _APSeleccionadoTile extends StatelessWidget {
  final APDisponible ap;
  final VoidCallback onTap;

  const _APSeleccionadoTile({
    required this.ap,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Material(
      color: theme.colorScheme.surfaceContainerHighest,
      borderRadius: BorderRadius.circular(8),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
          child: Row(
            children: [
              Icon(Icons.router, color: theme.colorScheme.primary),
              const SizedBox(width: 12),
              Expanded(
                child: _APResumen(ap: ap),
              ),
              const SizedBox(width: 8),
              const Icon(Icons.touch_app_outlined),
            ],
          ),
        ),
      ),
    );
  }
}

class _SelectorAPSheet extends StatelessWidget {
  final List<APDisponible> aps;
  final Set<String> bssidsSeleccionados;
  final String? bssidActivo;
  final ValueChanged<APDisponible> onAlternar;

  const _SelectorAPSheet({
    required this.aps,
    required this.bssidsSeleccionados,
    required this.bssidActivo,
    required this.onAlternar,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SafeArea(
      top: false,
      child: DraggableScrollableSheet(
        expand: false,
        initialChildSize: 0.70,
        minChildSize: 0.35,
        maxChildSize: 0.92,
        builder: (context, scrollController) => Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 12),
              child: Text(
                'Seleccionar AP',
                style: theme.textTheme.titleLarge,
              ),
            ),
            Expanded(
              child: ListView.separated(
                controller: scrollController,
                itemCount: aps.length,
                separatorBuilder: (_, __) => const Divider(height: 1),
                itemBuilder: (context, index) {
                  final ap = aps[index];
                  return _APSelectorItem(
                    key: ValueKey('selector-ap-${ap.bssid}'),
                    ap: ap,
                    seleccionado: bssidsSeleccionados.contains(ap.bssid),
                    activo: ap.bssid == bssidActivo,
                    onAlternar: onAlternar,
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _APSelectorItem extends StatelessWidget {
  final APDisponible ap;
  final bool seleccionado;
  final bool activo;
  final ValueChanged<APDisponible> onAlternar;

  const _APSelectorItem({
    super.key,
    required this.ap,
    required this.seleccionado,
    required this.activo,
    required this.onAlternar,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return CheckboxListTile(
      value: seleccionado,
      secondary: Icon(
        activo ? Icons.my_location : Icons.router_outlined,
        color: activo ? theme.colorScheme.primary : null,
      ),
      title: Text(
        ap.ssid.isEmpty ? 'SSID oculto' : ap.ssid,
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
      ),
      subtitle: Text(
        '${_detalleAP(ap)} · ${ap.rssiPromedio.toStringAsFixed(0)} dBm',
        maxLines: 2,
        overflow: TextOverflow.ellipsis,
      ),
      controlAffinity: ListTileControlAffinity.trailing,
      onChanged: (_) => onAlternar(ap),
      selected: activo,
    );
  }
}

class _APResumen extends StatelessWidget {
  final APDisponible ap;

  const _APResumen({required this.ap});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          ap.ssid.isEmpty ? 'SSID oculto' : ap.ssid,
          style: theme.textTheme.titleSmall,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        const SizedBox(height: 2),
        Text(
          _detalleAP(ap),
          style: theme.textTheme.bodySmall,
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
        ),
      ],
    );
  }
}

String _detalleAP(APDisponible ap) {
  final canal = ap.canal == null ? 'Canal s/d' : 'Canal ${ap.canal}';
  return '${ap.bssid} · $canal · ${ap.cantidadPuntos} puntos';
}

class _HeatmapInfoPanel extends StatelessWidget {
  final MapaCalor mapa;
  final List<EscalaHeatmap> escala;
  final List<APDisponible> apsInteres;
  final String? bssidActivo;
  final VoidCallback onLimpiarFiltro;
  final VoidCallback onRegenerarHeatmap;

  const _HeatmapInfoPanel({
    required this.mapa,
    required this.escala,
    required this.apsInteres,
    required this.bssidActivo,
    required this.onLimpiarFiltro,
    required this.onRegenerarHeatmap,
  });

  @override
  Widget build(BuildContext context) {
    APDisponible? apActivo;
    for (final ap in apsInteres) {
      if (ap.bssid == bssidActivo) {
        apActivo = ap;
        break;
      }
    }
    final titulo = apActivo == null
        ? 'Todos los APs seleccionados'
        : (apActivo.ssid.isEmpty ? 'SSID oculto' : apActivo.ssid);
    final subtitulo = apActivo == null
        ? 'Toca un AP para ver su heatmap individual.'
        : '${apActivo.rssiPromedio.toStringAsFixed(0)} dBm · toca el plano para volver al conjunto';
    return Material(
      elevation: 8,
      color: Theme.of(context).colorScheme.surface,
      child: SafeArea(
        top: false,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 8, 8, 8),
          child: _PanelHeader(
            titulo: titulo,
            subtitulo: subtitulo,
            accion: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (bssidActivo != null)
                  IconButton(
                    tooltip: 'Ver conjunto',
                    onPressed: onLimpiarFiltro,
                    icon: const Icon(Icons.layers_clear_outlined),
                  ),
                IconButton(
                  tooltip: 'Información del heatmap',
                  onPressed: () => _mostrarInfoHeatmap(context),
                  icon: const Icon(Icons.info_outline),
                ),
                IconButton(
                  tooltip: 'Regenerar heatmap',
                  onPressed: onRegenerarHeatmap,
                  icon: const Icon(Icons.local_fire_department_outlined),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _mostrarInfoHeatmap(BuildContext context) {
    showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      isScrollControlled: true,
      builder: (ctx) => _InfoHeatmapSheet(
        mapa: mapa,
        escala: escala,
      ),
    );
  }

}

class _PanelInferiorDesplazable extends StatelessWidget {
  final Widget child;

  const _PanelInferiorDesplazable({required this.child});

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.sizeOf(context);
    final esHorizontal = size.width > size.height;
    final maxHeight = size.height * (esHorizontal ? 0.58 : 0.46);

    return ConstrainedBox(
      constraints: BoxConstraints(maxHeight: maxHeight),
      child: SingleChildScrollView(
        physics: const ClampingScrollPhysics(),
        child: child,
      ),
    );
  }
}

class _InfoHeatmapSheet extends StatelessWidget {
  final MapaCalor mapa;
  final List<EscalaHeatmap> escala;

  const _InfoHeatmapSheet({
    required this.mapa,
    required this.escala,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SafeArea(
      top: false,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(20, 0, 20, 24),
        child: ListView(
          shrinkWrap: true,
          children: [
            Text('Información del heatmap', style: theme.textTheme.titleLarge),
            const SizedBox(height: 12),
            _LeyendaHeatmap(escala: escala),
            const SizedBox(height: 16),
            _ResumenMapaCalor(mapa: mapa),
            if (mapa.advertencias.isNotEmpty) ...[
              const SizedBox(height: 16),
              Text('Recomendaciones', style: theme.textTheme.titleMedium),
              const SizedBox(height: 8),
              for (final advertencia in mapa.advertencias)
                Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Icon(
                        Icons.info_outline,
                        size: 18,
                        color: theme.colorScheme.primary,
                      ),
                      const SizedBox(width: 8),
                      Expanded(child: Text(advertencia)),
                    ],
                  ),
                ),
            ],
          ],
        ),
      ),
    );
  }
}

class _PuntoLecturaSheet extends StatelessWidget {
  final PuntoLecturaHeatmap punto;

  const _PuntoLecturaSheet({required this.punto});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return SafeArea(
      top: false,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(20, 0, 20, 24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Punto de lectura #${punto.puntoId}',
                style: theme.textTheme.titleLarge),
            const SizedBox(height: 12),
            _DatoAP(
              label: 'RSSI',
              value: '${punto.rssi.toStringAsFixed(0)} dBm',
            ),
            _DatoAP(
              label: 'Ubicación',
              value:
                  'x ${punto.posX.toStringAsFixed(1)} · y ${punto.posY.toStringAsFixed(1)}',
            ),
            const SizedBox(height: 8),
            Text(
              _descripcionRSSI(punto.rssi),
              style: theme.textTheme.bodyMedium,
            ),
          ],
        ),
      ),
    );
  }

  String _descripcionRSSI(double rssi) {
    if (rssi >= -60) return 'Señal excelente para diseño de alta calidad.';
    if (rssi >= -67) return 'Señal muy buena para uso normal.';
    if (rssi >= -70) return 'Cumple el objetivo de diseño ≥ -70 dBm.';
    if (rssi >= -75) return 'Advertencia: conviene revisar cobertura.';
    if (rssi >= -80) return 'Señal débil en esta ubicación.';
    if (rssi >= -90) return 'Señal muy débil; posible zona problemática.';
    return 'Zona muerta: RSSI < -90 dBm.';
  }
}

class _ResumenMapaCalor extends StatelessWidget {
  final MapaCalor mapa;

  const _ResumenMapaCalor({required this.mapa});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: _Metrica(
            icon: Icons.scatter_plot_outlined,
            valor: mapa.cantidadPuntos.toString(),
            label: 'Muestras',
          ),
        ),
        Expanded(
          child: _Metrica(
            icon: Icons.arrow_downward,
            valor: '${mapa.rssiMin.toStringAsFixed(0)} dBm',
            label: 'Mín.',
          ),
        ),
        Expanded(
          child: _Metrica(
            icon: Icons.speed,
            valor: '${mapa.rssiPromedio.toStringAsFixed(0)} dBm',
            label: 'Prom.',
          ),
        ),
        Expanded(
          child: _Metrica(
            icon: Icons.arrow_upward,
            valor: '${mapa.rssiMax.toStringAsFixed(0)} dBm',
            label: 'Máx.',
          ),
        ),
      ],
    );
  }
}

class _LeyendaHeatmap extends StatelessWidget {
  final List<EscalaHeatmap> escala;
  const _LeyendaHeatmap({required this.escala});

  @override
  Widget build(BuildContext context) {
    final textStyle = Theme.of(context).textTheme.labelSmall;
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Row(
          children: escala
              .map(
                (item) => Expanded(
                  child: Container(
                    height: 8,
                    color: _colorDesdeHex(item.colorHex),
                  ),
                ),
              )
              .toList(),
        ),
        const SizedBox(height: 6),
        Wrap(
          spacing: 10,
          runSpacing: 4,
          alignment: WrapAlignment.center,
          children: escala
              .map(
                (item) => Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      width: 8,
                      height: 8,
                      color: _colorDesdeHex(item.colorHex),
                    ),
                    const SizedBox(width: 4),
                    Text(
                      item.etiqueta,
                      style: textStyle,
                    ),
                  ],
                ),
              )
              .toList(),
        ),
      ],
    );
  }

  Color _colorDesdeHex(String hex) {
    final clean = hex.replaceFirst('#', '');
    return Color(int.parse('FF$clean', radix: 16));
  }
}

class _Metrica extends StatelessWidget {
  final IconData icon;
  final String valor;
  final String label;

  const _Metrica({
    required this.icon,
    required this.valor,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    final color = Theme.of(context).colorScheme.primary;
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 18, color: color),
        Text(valor, style: Theme.of(context).textTheme.labelLarge),
        Text(label, style: Theme.of(context).textTheme.labelSmall),
      ],
    );
  }
}

class _HeatmapMatrixPainter extends CustomPainter {
  final List<List<double>> matriz;
  final List<PuntoPlano> poligonoInteres;
  final Size tamanoPlano;

  const _HeatmapMatrixPainter({
    required this.matriz,
    this.poligonoInteres = const [],
    required this.tamanoPlano,
  });

  @override
  void paint(Canvas canvas, Size size) {
    if (matriz.isEmpty || matriz.first.isEmpty) {
      return;
    }
    final filas = matriz.length;
    final columnas = matriz.first.length;
    final celdaW = size.width / columnas;
    final celdaH = size.height / filas;
    final paint = Paint()
      ..style = PaintingStyle.fill
      ..isAntiAlias = false;

    if (poligonoInteres.length >= 3 && !tamanoPlano.isEmpty) {
      canvas.save();
      canvas.clipPath(_pathPoligono(size));
    }

    for (var fila = 0; fila < filas; fila++) {
      final valores = matriz[fila];
      for (var columna = 0; columna < columnas; columna++) {
        paint.color = _colorParaRssi(valores[columna]);
        canvas.drawRect(
          Rect.fromLTRB(
            columna * celdaW,
            fila * celdaH,
            (columna + 1) * celdaW,
            (fila + 1) * celdaH,
          ),
          paint,
        );
      }
    }

    if (poligonoInteres.length >= 3 && !tamanoPlano.isEmpty) {
      canvas.restore();
      canvas.drawPath(
        _pathPoligono(size),
        Paint()
          ..color = const Color(0xFF2980B9).withValues(alpha: 0.78)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1.4,
      );
    }
  }

  Path _pathPoligono(Size size) {
    final path = Path();
    final scaleX = size.width / tamanoPlano.width;
    final scaleY = size.height / tamanoPlano.height;
    for (var i = 0; i < poligonoInteres.length; i++) {
      final punto = poligonoInteres[i];
      final x = punto.x * scaleX;
      final y = punto.y * scaleY;
      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    return path..close();
  }

  Color _colorParaRssi(double rssi) {
    const paradas = [
      _ColorStop(-120, Color(0xFFD7263D)),
      _ColorStop(-91, Color(0xFFD7263D)),
      _ColorStop(-90, Color(0xFFD95D39)),
      _ColorStop(-80, Color(0xFFD95D39)),
      _ColorStop(-76, Color(0xFFF08A24)),
      _ColorStop(-75, Color(0xFFF4D35E)),
      _ColorStop(-71, Color(0xFFF4D35E)),
      _ColorStop(-70, Color(0xFFA7C957)),
      _ColorStop(-68, Color(0xFFA7C957)),
      _ColorStop(-67, Color(0xFF57B65A)),
      _ColorStop(-61, Color(0xFF57B65A)),
      _ColorStop(-60, Color(0xFF0B7A3B)),
      _ColorStop(-50, Color(0xFF0B7A3B)),
      _ColorStop(0, Color(0xFF0B7A3B)),
    ];
    if (rssi <= paradas.first.valor) {
      return paradas.first.color.withValues(alpha: 0.60);
    }
    for (var i = 1; i < paradas.length; i++) {
      final inicio = paradas[i - 1];
      final fin = paradas[i];
      if (rssi <= fin.valor) {
        final t = (rssi - inicio.valor) / (fin.valor - inicio.valor);
        return Color.lerp(inicio.color, fin.color, t)!.withValues(alpha: 0.60);
      }
    }
    return paradas.last.color.withValues(alpha: 0.60);
  }

  @override
  bool shouldRepaint(covariant _HeatmapMatrixPainter oldDelegate) {
    return oldDelegate.matriz != matriz ||
        oldDelegate.poligonoInteres != poligonoInteres ||
        oldDelegate.tamanoPlano != tamanoPlano;
  }
}

class _ColorStop {
  final double valor;
  final Color color;

  const _ColorStop(this.valor, this.color);
}

class _PuntosLecturaPainter extends CustomPainter {
  final List<PuntoLecturaHeatmap> puntos;
  final Size tamanoPlano;
  final double zoomEscala;

  const _PuntosLecturaPainter({
    required this.puntos,
    required this.tamanoPlano,
    this.zoomEscala = 1.0,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final escalaSegura = zoomEscala <= 0 ? 1.0 : zoomEscala;
    final radio = 4.5 / escalaSegura;
    final relleno = Paint()..style = PaintingStyle.fill;
    final borde = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.5 / escalaSegura
      ..color = Colors.white.withValues(alpha: 0.85);

    for (final punto in puntos) {
      final centro = Offset(
        (punto.posX / tamanoPlano.width) * size.width,
        (punto.posY / tamanoPlano.height) * size.height,
      );
      relleno.color = _colorParaRssi(punto.rssi).withValues(alpha: 0.95);
      canvas.drawCircle(centro, radio, relleno);
      canvas.drawCircle(centro, radio, borde);
    }
  }

  Color _colorParaRssi(double rssi) {
    if (rssi >= -60) return const Color(0xFF0B7A3B);
    if (rssi >= -67) return const Color(0xFF57B65A);
    if (rssi >= -70) return const Color(0xFFA7C957);
    if (rssi >= -75) return const Color(0xFFF4D35E);
    if (rssi >= -80) return const Color(0xFFF08A24);
    if (rssi >= -90) return const Color(0xFFD95D39);
    return const Color(0xFFD7263D);
  }

  @override
  bool shouldRepaint(covariant _PuntosLecturaPainter oldDelegate) {
    return oldDelegate.puntos != puntos ||
        oldDelegate.tamanoPlano != tamanoPlano ||
        oldDelegate.zoomEscala != zoomEscala;
  }
}

class _SelectorAlgoritmo extends StatelessWidget {
  final String valor;
  final ValueChanged<String> onChanged;

  const _SelectorAlgoritmo({
    required this.valor,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return PopupMenuButton<String>(
      tooltip: 'Algoritmo',
      icon: const Icon(Icons.functions),
      initialValue: valor,
      onSelected: onChanged,
      itemBuilder: (_) => const [
        PopupMenuItem(value: 'IDW', child: Text('IDW')),
        PopupMenuItem(value: 'KRIGING', child: Text('Kriging')),
      ],
    );
  }
}

class _SelectorResolucion extends StatelessWidget {
  final int valor;
  final ValueChanged<int> onChanged;

  const _SelectorResolucion({
    required this.valor,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return PopupMenuButton<int>(
      tooltip: 'Resolución',
      icon: const Icon(Icons.grid_on),
      initialValue: valor,
      onSelected: onChanged,
      itemBuilder: (_) => const [
        PopupMenuItem(value: 64, child: Text('64')),
        PopupMenuItem(value: 128, child: Text('128')),
        PopupMenuItem(value: 256, child: Text('256')),
      ],
    );
  }
}

class _DatoAP extends StatelessWidget {
  final String label;
  final String value;

  const _DatoAP({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: Row(
        children: [
          SizedBox(
            width: 96,
            child: Text(
              label,
              style: Theme.of(context).textTheme.labelMedium,
            ),
          ),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }
}

class _HeatmapErrorView extends StatelessWidget {
  final String mensaje;
  final VoidCallback onRetry;

  const _HeatmapErrorView({
    required this.mensaje,
    required this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.heat_pump_outlined, size: 64),
            const SizedBox(height: 12),
            Text(mensaje, textAlign: TextAlign.center),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: const Text('Reintentar'),
            ),
          ],
        ),
      ),
    );
  }
}
