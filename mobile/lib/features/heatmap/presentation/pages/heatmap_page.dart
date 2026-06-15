import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../planos/presentation/utils/url_resolver.dart';
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

  void _generarHeatmap(HeatmapSeleccionAP state) {
    context.read<HeatmapCubit>().generar(
          planoId: widget.planoId,
          ap: state.apSeleccionado,
          apPosX: state.apPosX,
          apPosY: state.apPosY,
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
                      apPosX: state.apPosX,
                      apPosY: state.apPosY,
                      apLabel: state.apSeleccionado.ssid,
                      onTapPlano: (pos) =>
                          context.read<HeatmapCubit>().ubicarAP(
                                posX: pos.dx,
                                posY: pos.dy,
                              ),
                      onTapAP: _mostrarDetalleAP,
                    ),
                  ),
                  _SeleccionAPPanel(
                    state: state,
                    onSeleccionar: (ap) =>
                        context.read<HeatmapCubit>().seleccionarAP(ap),
                    onGenerar: () => _generarHeatmap(state),
                  ),
                ],
              ),
            HeatmapReady() => Column(
                children: [
                  Expanded(
                    child: _HeatmapCanvas(
                      planoUrl: widget.imagenUrl,
                      heatmapUrl: resolverUrlFirmada(listo!.mapa.urlImagen),
                      tamanoPlano: _tamanoPlano,
                      aps: listo.analisis?.apsDetectados ?? const [],
                      apPosX: listo.mapa.apPosX,
                      apPosY: listo.mapa.apPosY,
                      apLabel: listo.mapa.ssid,
                      onTapAP: _mostrarDetalleAP,
                    ),
                  ),
                  _AnalisisPanel(
                    analisis: listo.analisis,
                    analizando: listo.analizando,
                    escala: listo.mapa.escala,
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

class _HeatmapCanvas extends StatelessWidget {
  final String planoUrl;
  final String? heatmapUrl;
  final Size tamanoPlano;
  final List<APDetectado> aps;
  final double? apPosX;
  final double? apPosY;
  final String? apLabel;
  final void Function(Offset posPlano)? onTapPlano;
  final void Function(APDetectado ap) onTapAP;

  const _HeatmapCanvas({
    required this.planoUrl,
    this.heatmapUrl,
    required this.tamanoPlano,
    required this.aps,
    this.apPosX,
    this.apPosY,
    this.apLabel,
    this.onTapPlano,
    required this.onTapAP,
  });

  @override
  Widget build(BuildContext context) {
    return InteractiveViewer(
      minScale: 0.5,
      maxScale: 5,
      child: LayoutBuilder(
        builder: (context, constraints) {
          final aspect = tamanoPlano.width / tamanoPlano.height;
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
              child: Stack(
                fit: StackFit.expand,
                children: [
                  GestureDetector(
                    onTapUp: onTapPlano == null
                        ? null
                        : (details) {
                            final pos = Offset(
                              (details.localPosition.dx / w) *
                                  tamanoPlano.width,
                              (details.localPosition.dy / h) *
                                  tamanoPlano.height,
                            );
                            onTapPlano!(pos);
                          },
                    child: Image.network(
                      planoUrl,
                      fit: BoxFit.fill,
                      errorBuilder: (_, __, ___) => const Center(
                        child: Icon(Icons.broken_image, size: 56),
                      ),
                    ),
                  ),
                  if (heatmapUrl != null)
                    Opacity(
                      opacity: 0.60,
                      child: Image.network(
                        heatmapUrl!,
                        fit: BoxFit.fill,
                        errorBuilder: (_, __, ___) => const SizedBox.shrink(),
                      ),
                    ),
                  CustomPaint(
                    painter: _APPainter(
                      aps: aps,
                      tamanoPlano: tamanoPlano,
                    ),
                  ),
                  if (apPosX != null && apPosY != null)
                    Positioned(
                      left: ((apPosX! / tamanoPlano.width) * w - 22)
                          .clamp(0, w - 44)
                          .toDouble(),
                      top: ((apPosY! / tamanoPlano.height) * h - 22)
                          .clamp(0, h - 44)
                          .toDouble(),
                      child: Tooltip(
                        message: apLabel == null ? 'AP seleccionado' : apLabel!,
                        child: IconButton.filled(
                          onPressed: null,
                          icon: const Icon(Icons.router),
                          iconSize: 18,
                        ),
                      ),
                    ),
                  ...aps.map((ap) {
                    final left = (ap.posX / tamanoPlano.width) * w - 22;
                    final top = (ap.posY / tamanoPlano.height) * h - 22;
                    return Positioned(
                      left: left.clamp(0, w - 44).toDouble(),
                      top: top.clamp(0, h - 44).toDouble(),
                      child: IconButton.filledTonal(
                        tooltip: 'AP ${ap.ssid}',
                        iconSize: 18,
                        onPressed: () => onTapAP(ap),
                        icon: Icon(ap.confirmado
                            ? Icons.router
                            : Icons.router_outlined),
                      ),
                    );
                  }),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

class _SeleccionAPPanel extends StatelessWidget {
  final HeatmapSeleccionAP state;
  final ValueChanged<APDisponible> onSeleccionar;
  final VoidCallback onGenerar;

  const _SeleccionAPPanel({
    required this.state,
    required this.onSeleccionar,
    required this.onGenerar,
  });

  @override
  Widget build(BuildContext context) {
    final ap = state.apSeleccionado;
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
              Text(
                'AP de interés',
                style: theme.textTheme.labelLarge,
              ),
              const SizedBox(height: 6),
              _APSeleccionadoTile(
                ap: ap,
                onTap: () => _mostrarSelectorAP(context),
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
                'Ubicación AP: x ${state.apPosX.toStringAsFixed(1)} · '
                'y ${state.apPosY.toStringAsFixed(1)}',
                style: theme.textTheme.bodySmall,
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                child: FilledButton.icon(
                  onPressed: onGenerar,
                  icon: const Icon(Icons.local_fire_department_outlined),
                  label: const Text('Generar heatmap del AP'),
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
        seleccionado: state.apSeleccionado,
        onSeleccionar: (ap) {
          Navigator.of(ctx).pop();
          onSeleccionar(ap);
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
  final APDisponible seleccionado;
  final ValueChanged<APDisponible> onSeleccionar;

  const _SelectorAPSheet({
    required this.aps,
    required this.seleccionado,
    required this.onSeleccionar,
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
                  final activo = ap.bssid == seleccionado.bssid;
                  return ListTile(
                    leading: Icon(
                      activo ? Icons.check_circle : Icons.router_outlined,
                      color: activo ? theme.colorScheme.primary : null,
                    ),
                    title: Text(
                      ap.ssid.isEmpty ? 'SSID oculto' : ap.ssid,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    subtitle: Text(
                      _detalleAP(ap),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    trailing: Text(
                      '${ap.rssiPromedio.toStringAsFixed(0)} dBm',
                      style: theme.textTheme.labelMedium,
                    ),
                    selected: activo,
                    onTap: () => onSeleccionar(ap),
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
  final VoidCallback onRefreshAnalisis;
  final void Function(APDetectado ap) onTapAP;

  const _AnalisisPanel({
    required this.analisis,
    required this.analizando,
    required this.escala,
    required this.onRefreshAnalisis,
    required this.onTapAP,
  });

  @override
  Widget build(BuildContext context) {
    final a = analisis;
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
                    itemCount: a.apsDetectados.length,
                    separatorBuilder: (_, __) => const SizedBox(width: 8),
                    itemBuilder: (context, index) {
                      final ap = a.apsDetectados[index];
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
