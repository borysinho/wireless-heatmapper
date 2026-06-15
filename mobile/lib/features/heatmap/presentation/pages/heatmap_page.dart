import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../domain/entities/analisis_cobertura.dart';
import '../../domain/entities/ap_disponible.dart';
import '../../domain/entities/ap_detectado.dart';
import '../../domain/entities/escala_heatmap.dart';
import '../cubit/heatmap_cubit.dart';
import '../cubit/heatmap_state.dart';

/// Pantalla de heatmap y análisis. Sprint 4 — PB-05 / PB-06.
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

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<HeatmapCubit, HeatmapState>(
      listener: (context, state) {
        if (state is HeatmapReady && state.mensaje != null) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.mensaje!)),
          );
        } else if (state is HeatmapSeleccionAP && state.mensaje != null) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.mensaje!)),
          );
        } else if (state is HeatmapError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(state.mensaje),
              backgroundColor: Theme.of(context).colorScheme.error,
            ),
          );
        }
      },
      builder: (context, state) {
        final listo = state is HeatmapReady ? state : null;
        return Scaffold(
          appBar: AppBar(
            title: const Text('Heatmap'),
            actions: [
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
            HeatmapSeleccionAP() => Column(
                children: [
                  Expanded(
                    child: _HeatmapCanvas(
                      planoUrl: widget.imagenUrl,
                      tamanoPlano: _tamanoPlano,
                      aps: const [],
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
                              ),
                      onTapAP: _mostrarDetalleAP,
                    ),
                  ),
                  _SeleccionAPPanel(
                    state: state,
                    onAlternar: (ap) =>
                        context.read<HeatmapCubit>().alternarAPInteres(ap),
                    onActivar: (ap) =>
                        context.read<HeatmapCubit>().activarAP(ap),
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
                      tamanoPlano: _tamanoPlano,
                      aps: const [],
                      apsInteres: listo.mapa.apsInteres,
                      bssidActivo: listo.bssidActivo,
                      apPosXPorBssid: {
                        for (final ap in listo.mapa.apsInteres)
                          ap.bssid: ap.posX,
                      },
                      apPosYPorBssid: {
                        for (final ap in listo.mapa.apsInteres)
                          ap.bssid: ap.posY,
                      },
                      onTapAP: _mostrarDetalleAP,
                    ),
                  ),
                  _AnalisisPanel(
                    analisis: listo.analisis,
                    analizando: listo.analizando,
                    escala: listo.mapa.escala,
                    bssidsPermitidos: {
                      for (final ap in listo.mapa.apsInteres) ap.bssid,
                    },
                    onRefreshAnalisis: () =>
                        context.read<HeatmapCubit>().regenerarAnalisis(),
                    onTapAP: _mostrarDetalleAP,
                  ),
                ],
              ),
          },
        );
      },
    );
  }

  void _mostrarDetalleAP(APDetectado ap) {
    showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      builder: (ctx) => Padding(
        padding: const EdgeInsets.fromLTRB(20, 8, 20, 24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(ap.ssid, style: Theme.of(ctx).textTheme.titleLarge),
            const SizedBox(height: 8),
            _DatoAP(label: 'BSSID', value: ap.bssid),
            _DatoAP(label: 'Canal', value: ap.canal?.toString() ?? 'Sin dato'),
            _DatoAP(
              label: 'RSSI prom.',
              value: '${ap.rssiPromedio.toStringAsFixed(1)} dBm',
            ),
            _DatoAP(
              label: 'Ubicación',
              value:
                  'x ${ap.posX.toStringAsFixed(1)} · y ${ap.posY.toStringAsFixed(1)}',
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                onPressed: ap.confirmado
                    ? null
                    : () {
                        context.read<HeatmapCubit>().confirmarAP(ap);
                        Navigator.of(ctx).pop();
                      },
                icon: Icon(ap.confirmado
                    ? Icons.verified
                    : Icons.add_location_alt_outlined),
                label: Text(ap.confirmado
                    ? 'Ubicación confirmada'
                    : 'Confirmar ubicación estimada'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _HeatmapCanvas extends StatefulWidget {
  final String planoUrl;
  final List<List<double>>? heatmapMatriz;
  final Size tamanoPlano;
  final List<APDetectado> aps;
  final List<APDisponible> apsInteres;
  final String? bssidActivo;
  final Map<String, double> apPosXPorBssid;
  final Map<String, double> apPosYPorBssid;
  final void Function(Offset posPlano)? onTapPlano;
  final void Function(APDisponible ap)? onTapAPInteres;
  final void Function(APDisponible ap, Offset posPlano)? onMoverAPInteres;
  final void Function(APDetectado ap) onTapAP;

  const _HeatmapCanvas({
    required this.planoUrl,
    this.heatmapMatriz,
    required this.tamanoPlano,
    required this.aps,
    this.apsInteres = const [],
    this.bssidActivo,
    this.apPosXPorBssid = const {},
    this.apPosYPorBssid = const {},
    this.onTapPlano,
    this.onTapAPInteres,
    this.onMoverAPInteres,
    required this.onTapAP,
  });

  @override
  State<_HeatmapCanvas> createState() => _HeatmapCanvasState();
}

class _HeatmapCanvasState extends State<_HeatmapCanvas> {
  static const double _hitRadioPx = 24.0;
  static const double _apMarkerSize = 32.0;
  static const double _apMarkerHalf = _apMarkerSize / 2;

  Offset? _ultimoTapDown;
  String? _bssidArrastrado;

  @override
  Widget build(BuildContext context) {
    return InteractiveViewer(
      panEnabled: widget.onMoverAPInteres == null,
      scaleEnabled: widget.onMoverAPInteres == null,
      minScale: 0.5,
      maxScale: 5,
      child: LayoutBuilder(
        builder: (context, constraints) {
          final puedeTocar =
              widget.onTapPlano != null || widget.onTapAPInteres != null;
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
                onPanStart: widget.onMoverAPInteres == null
                    ? null
                    : (details) => _onPanStart(details, w: w, h: h),
                onPanUpdate: widget.onMoverAPInteres == null
                    ? null
                    : (details) => _onPanUpdate(details, w: w, h: h),
                onPanEnd: widget.onMoverAPInteres == null
                    ? null
                    : (_) => setState(() => _bssidArrastrado = null),
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
                        ),
                      ),
                    CustomPaint(
                      painter: _APPainter(
                        aps: widget.aps,
                        tamanoPlano: widget.tamanoPlano,
                      ),
                    ),
                    ...widget.apsInteres.map((ap) {
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
                        child: _APInteresMarker(ap: ap, activo: activo),
                      );
                    }),
                    ...widget.aps.map((ap) {
                      final left =
                          (ap.posX / widget.tamanoPlano.width) * w - 22;
                      final top =
                          (ap.posY / widget.tamanoPlano.height) * h - 22;
                      return Positioned(
                        left: left.clamp(0, w - 44).toDouble(),
                        top: top.clamp(0, h - 44).toDouble(),
                        child: IconButton.filledTonal(
                          tooltip: 'AP ${ap.ssid}',
                          iconSize: 18,
                          onPressed: () => widget.onTapAP(ap),
                          icon: Icon(ap.confirmado
                              ? Icons.router
                              : Icons.router_outlined),
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
    widget.onTapPlano?.call(_tapAPlano(pos, w: w, h: h));
  }

  void _onPanStart(
    DragStartDetails details, {
    required double w,
    required double h,
  }) {
    final ap = _apEnPosicion(details.localPosition, w: w, h: h);
    if (ap == null) return;
    setState(() => _bssidArrastrado = ap.bssid);
    widget.onTapAPInteres?.call(ap);
  }

  void _onPanUpdate(
    DragUpdateDetails details, {
    required double w,
    required double h,
  }) {
    final bssid = _bssidArrastrado;
    if (bssid == null) return;
    final ap = _apPorBssid(bssid);
    if (ap == null) return;
    widget.onMoverAPInteres?.call(
      ap,
      _tapAPlano(details.localPosition, w: w, h: h),
    );
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
    return Tooltip(
      message: ap.ssid.isEmpty ? ap.bssid : ap.ssid,
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
    );
  }
}

class _SeleccionAPPanel extends StatelessWidget {
  final HeatmapSeleccionAP state;
  final ValueChanged<APDisponible> onAlternar;
  final ValueChanged<APDisponible> onActivar;
  final VoidCallback onGenerar;

  const _SeleccionAPPanel({
    required this.state,
    required this.onAlternar,
    required this.onActivar,
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
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Expanded(
                    child: Text(
                      'APs de interés (${state.apsSeleccionados.length})',
                      style: theme.textTheme.labelLarge,
                    ),
                  ),
                  TextButton.icon(
                    onPressed: () => _mostrarSelectorAP(context),
                    icon: const Icon(Icons.playlist_add_check),
                    label: const Text('Cambiar'),
                  ),
                ],
              ),
              const SizedBox(height: 6),
              _APSeleccionadoTile(
                ap: ap,
                onTap: () => _mostrarSelectorAP(context),
              ),
              const SizedBox(height: 8),
              SizedBox(
                height: 40,
                child: ListView.separated(
                  scrollDirection: Axis.horizontal,
                  itemCount: state.apsSeleccionados.length,
                  separatorBuilder: (_, __) => const SizedBox(width: 8),
                  itemBuilder: (context, index) {
                    final item = state.apsSeleccionados[index];
                    return ChoiceChip(
                      selected: item.bssid == state.bssidActivo,
                      label: Text(
                        item.ssid.isEmpty ? item.bssid : item.ssid,
                        overflow: TextOverflow.ellipsis,
                      ),
                      avatar: const Icon(Icons.router, size: 16),
                      onSelected: (_) => onActivar(item),
                    );
                  },
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Puntos medidos: ${ap.cantidadPuntos} · '
                'RSSI prom. ${ap.rssiPromedio.toStringAsFixed(1)} dBm · '
                'Canal ${ap.canal?.toString() ?? 's/d'}',
                style: theme.textTheme.bodySmall,
              ),
              const SizedBox(height: 4),
              Text(
                'Ubicación AP activo: x ${state.posXDe(ap).toStringAsFixed(1)} · '
                'y ${state.posYDe(ap).toStringAsFixed(1)}',
                style: theme.textTheme.bodySmall,
              ),
              const SizedBox(height: 12),
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
    );
  }

  void _mostrarSelectorAP(BuildContext context) {
    showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      isScrollControlled: true,
      builder: (ctx) => _SelectorAPSheet(
        aps: state.aps,
        bssidsSeleccionados: state.bssidsSeleccionados,
        bssidActivo: state.bssidActivo,
        onAlternar: onAlternar,
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
              const Icon(Icons.keyboard_arrow_up),
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
  final String bssidActivo;
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
                itemBuilder: (context, index) => _APSelectorItem(
                  ap: aps[index],
                  seleccionado: bssidsSeleccionados.contains(aps[index].bssid),
                  activo: aps[index].bssid == bssidActivo,
                  onAlternar: onAlternar,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _APSelectorItem extends StatefulWidget {
  final APDisponible ap;
  final bool seleccionado;
  final bool activo;
  final ValueChanged<APDisponible> onAlternar;

  const _APSelectorItem({
    required this.ap,
    required this.seleccionado,
    required this.activo,
    required this.onAlternar,
  });

  @override
  State<_APSelectorItem> createState() => _APSelectorItemState();
}

class _APSelectorItemState extends State<_APSelectorItem> {
  late bool _seleccionado = widget.seleccionado;
  late bool _activo = widget.activo;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return CheckboxListTile(
      value: _seleccionado,
      secondary: Icon(
        _activo ? Icons.my_location : Icons.router_outlined,
        color: _activo ? theme.colorScheme.primary : null,
      ),
      title: Text(
        widget.ap.ssid.isEmpty ? 'SSID oculto' : widget.ap.ssid,
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
      ),
      subtitle: Text(
        '${_detalleAP(widget.ap)} · '
        '${widget.ap.rssiPromedio.toStringAsFixed(0)} dBm',
        maxLines: 2,
        overflow: TextOverflow.ellipsis,
      ),
      controlAffinity: ListTileControlAffinity.trailing,
      onChanged: (_) {
        setState(() {
          _seleccionado = !_seleccionado;
          _activo = true;
        });
        widget.onAlternar(widget.ap);
      },
      selected: _activo,
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

class _AnalisisPanel extends StatelessWidget {
  final AnalisisCobertura? analisis;
  final bool analizando;
  final List<EscalaHeatmap> escala;
  final Set<String> bssidsPermitidos;
  final VoidCallback onRefreshAnalisis;
  final void Function(APDetectado ap) onTapAP;

  const _AnalisisPanel({
    required this.analisis,
    required this.analizando,
    required this.escala,
    required this.bssidsPermitidos,
    required this.onRefreshAnalisis,
    required this.onTapAP,
  });

  @override
  Widget build(BuildContext context) {
    final a = analisis;
    final apsVisibles = a == null
        ? <APDetectado>[]
        : a.apsDetectados
            .where((ap) => bssidsPermitidos.contains(ap.bssid))
            .toList();
    return Material(
      elevation: 8,
      color: Theme.of(context).colorScheme.surface,
      child: SafeArea(
        top: false,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              _LeyendaHeatmap(escala: escala),
              const SizedBox(height: 12),
              if (a == null)
                Row(
                  children: [
                    const SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    ),
                    const SizedBox(width: 12),
                    Text(analizando ? 'Analizando cobertura…' : 'Sin análisis'),
                  ],
                )
              else ...[
                Row(
                  children: [
                    Expanded(
                      child: _Metrica(
                        icon: Icons.check_circle_outline,
                        valor: '${a.pctCobertura.toStringAsFixed(1)}%',
                        label: 'Cobertura',
                      ),
                    ),
                    Expanded(
                      child: _Metrica(
                        icon: Icons.warning_amber,
                        valor: a.celdasZonasMuertas.toString(),
                        label: 'Zonas muertas',
                      ),
                    ),
                    Expanded(
                      child: _Metrica(
                        icon: Icons.hub_outlined,
                        valor: a.cantidadSolapamientos.toString(),
                        label: 'Solap.',
                      ),
                    ),
                    Expanded(
                      child: _Metrica(
                        icon: Icons.wifi_tethering_error,
                        valor: a.cantidadInterferencias.toString(),
                        label: 'Interf.',
                      ),
                    ),
                    IconButton(
                      tooltip: 'Reanalizar',
                      onPressed: analizando ? null : onRefreshAnalisis,
                      icon: analizando
                          ? const SizedBox(
                              width: 18,
                              height: 18,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Icon(Icons.analytics_outlined),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                SizedBox(
                  height: 72,
                  child: ListView.separated(
                    scrollDirection: Axis.horizontal,
                    itemCount: apsVisibles.length,
                    separatorBuilder: (_, __) => const SizedBox(width: 8),
                    itemBuilder: (context, index) {
                      final ap = apsVisibles[index];
                      return ActionChip(
                        avatar: Icon(
                          ap.confirmado ? Icons.verified : Icons.router,
                          size: 18,
                        ),
                        label: Text(
                          '${ap.ssid}\n${ap.rssiPromedio.toStringAsFixed(0)} dBm',
                          maxLines: 2,
                        ),
                        onPressed: () => onTapAP(ap),
                      );
                    },
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class _LeyendaHeatmap extends StatelessWidget {
  final List<EscalaHeatmap> escala;
  const _LeyendaHeatmap({required this.escala});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: escala
          .map(
            (item) => Expanded(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    height: 8,
                    color: _colorDesdeHex(item.colorHex),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    item.etiqueta,
                    style: Theme.of(context).textTheme.labelSmall,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
          )
          .toList(),
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

  const _HeatmapMatrixPainter({required this.matriz});

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
  }

  Color _colorParaRssi(double rssi) {
    if (rssi >= -50) {
      return const Color(0xFF0B7A3B).withValues(alpha: 0.60);
    }
    if (rssi >= -70) {
      return const Color(0xFF57B65A).withValues(alpha: 0.60);
    }
    if (rssi >= -80) {
      return const Color(0xFFF4D35E).withValues(alpha: 0.60);
    }
    if (rssi >= -90) {
      return const Color(0xFFF08A24).withValues(alpha: 0.60);
    }
    return const Color(0xFFD7263D).withValues(alpha: 0.60);
  }

  @override
  bool shouldRepaint(covariant _HeatmapMatrixPainter oldDelegate) {
    return oldDelegate.matriz != matriz;
  }
}

class _APPainter extends CustomPainter {
  final List<APDetectado> aps;
  final Size tamanoPlano;

  const _APPainter({
    required this.aps,
    required this.tamanoPlano,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.black.withValues(alpha: 0.25)
      ..strokeWidth = 1;
    for (final ap in aps) {
      final center = Offset(
        (ap.posX / tamanoPlano.width) * size.width,
        (ap.posY / tamanoPlano.height) * size.height,
      );
      canvas.drawCircle(center, 18, paint..style = PaintingStyle.stroke);
    }
  }

  @override
  bool shouldRepaint(covariant _APPainter oldDelegate) {
    return oldDelegate.aps != aps || oldDelegate.tamanoPlano != tamanoPlano;
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
