import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:share_plus/share_plus.dart';

import '../../domain/entities/escenario_optimizado.dart';
import '../cubit/escenarios_cubit.dart';
import '../cubit/escenarios_state.dart';

class EscenariosPage extends StatelessWidget {
  final int proyectoId;

  const EscenariosPage({super.key, required this.proyectoId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Escenarios IA')),
      body: BlocConsumer<EscenariosCubit, EscenariosState>(
        listenWhen: (previous, current) {
          final rutaAnterior = previous.reporte?.rutaLocal;
          final rutaActual = current.reporte?.rutaLocal;
          final nuevoReporte = rutaActual != null &&
              (rutaAnterior != rutaActual ||
                  previous.reporte?.id != current.reporte?.id);
          final nuevoError =
              current.error != null && previous.error != current.error;
          return nuevoReporte || nuevoError;
        },
        listener: (context, state) {
          if (state.error != null) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(state.error!)),
            );
            return;
          }
          final rutaLocal = state.reporte?.rutaLocal;
          if (rutaLocal != null) {
            _compartirReporte(context, rutaLocal);
          }
        },
        builder: (context, state) {
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              FilledButton.icon(
                onPressed:
                    state.cargando ? null : () => _configurarYGenerar(context),
                icon: state.cargando
                    ? const SizedBox.square(
                        dimension: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.auto_awesome),
                label: const Text('Generar recomendación'),
              ),
              const SizedBox(height: 8),
              OutlinedButton.icon(
                onPressed: state.cargando
                    ? null
                    : () => context
                        .read<EscenariosCubit>()
                        .cargarInventario(proyectoId),
                icon: const Icon(Icons.router_outlined),
                label: const Text('Cargar inventario RF'),
              ),
              if (state.inventario != null) ...[
                ListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(
                    'Inventario ${state.inventario!.nivelCompletitud}',
                  ),
                  subtitle: Text(
                    '${state.inventario!.aps.length} APs · '
                    '${state.inventario!.porcentajeCompletitud.toStringAsFixed(0)}% completo',
                  ),
                  trailing: IconButton(
                    tooltip: 'Registrar AP físico',
                    onPressed: () => _registrarAP(context),
                    icon: const Icon(Icons.add),
                  ),
                ),
                for (final ap in state.inventario!.aps)
                  Card(
                    child: ListTile(
                      leading: const Icon(Icons.router),
                      title: Text('${ap.nombre} · ${ap.modelo}'),
                      subtitle: Text(
                        '${ap.restriccionMovimiento} · '
                        '${ap.radios.map((r) => '${r.banda} GHz C${r.canal}').join(' · ')}',
                      ),
                    ),
                  ),
              ],
              const SizedBox(height: 12),
              for (final escenario in state.escenarios) ...[
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          escenario.nombre,
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        const SizedBox(height: 6),
                        Text(escenario.resumen),
                        const SizedBox(height: 8),
                        Wrap(
                          spacing: 8,
                          children: [
                            Chip(
                              label: Text(
                                '${escenario.pctCobertura.toStringAsFixed(1)}% cobertura',
                              ),
                            ),
                            Chip(label: Text('${escenario.cantidadAps} APs')),
                            Chip(
                              label: Text(
                                'Bandas ${escenario.bandas.join(' / ')} GHz',
                              ),
                            ),
                            Chip(
                                label:
                                    Text('Confianza ${escenario.confianza}')),
                          ],
                        ),
                        const SizedBox(height: 8),
                        for (final rec in escenario.recomendaciones)
                          ListTile(
                            dense: true,
                            contentPadding: EdgeInsets.zero,
                            leading: const Icon(Icons.router),
                            title: Text(
                              '${rec.accion} AP con potencia ajustable',
                            ),
                            subtitle: Text(rec.justificacion),
                            isThreeLine: true,
                            trailing: rec.radios.isEmpty
                                ? null
                                : Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      for (final radio in rec.radios)
                                        Text(
                                          '${radio.banda}G · C${radio.canal} · '
                                          '${radio.potenciaDbm.toStringAsFixed(0)} dBm',
                                          style: Theme.of(context)
                                              .textTheme
                                              .labelSmall,
                                        ),
                                    ],
                                  ),
                          ),
                        Row(
                          children: [
                            TextButton.icon(
                              onPressed: state.cargando
                                  ? null
                                  : () => context
                                      .read<EscenariosCubit>()
                                      .comparar(escenario.id),
                              icon: const Icon(Icons.compare),
                              label: const Text('Comparar'),
                            ),
                            TextButton.icon(
                              onPressed: state.cargando
                                  ? null
                                  : () => context
                                      .read<EscenariosCubit>()
                                      .crearYCompartirReporte(
                                        proyectoId: proyectoId,
                                        escenarioId: escenario.id,
                                      ),
                              icon: const Icon(Icons.ios_share),
                              label: const Text('Compartir PDF'),
                            ),
                          ],
                        ),
                        if (state.comparacion?.escenario.id == escenario.id)
                          _ComparacionCard(comparacion: state.comparacion!),
                        if (state.reporte?.escenarioId == escenario.id)
                          _ReporteCompartidoCard(
                            ruta: state.reporte!.rutaLocal,
                            onCompartir: state.reporte!.rutaLocal == null
                                ? null
                                : () => _compartirReporte(
                                      context,
                                      state.reporte!.rutaLocal!,
                                    ),
                          ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 8),
              ],
              if (state.escenarios.isNotEmpty)
                const Padding(
                  padding: EdgeInsets.only(top: 8),
                  child: Text(
                    'Los resultados son estimaciones RF y no reemplazan el '
                    'survey de validación posterior a la instalación.',
                    textAlign: TextAlign.center,
                  ),
                ),
            ],
          );
        },
      ),
    );
  }

  Future<void> _configurarYGenerar(BuildContext context) async {
    final config = await showDialog<_ConfiguracionEscenario>(
      context: context,
      builder: (_) => const _ConfiguracionEscenarioDialog(),
    );
    if (config == null || !context.mounted) return;
    await context.read<EscenariosCubit>().generar(
          proyectoId: proyectoId,
          maxAps: config.maxAps,
          presupuesto: config.presupuesto,
          bandas: config.bandas,
          bandaPreferida: config.bandas.contains('5') ? '5' : '2.4',
          tipoNegocio: config.tipoNegocio,
          perfil: config.perfil,
        );
  }

  Future<void> _registrarAP(BuildContext context) async {
    final datos = await showDialog<Map<String, dynamic>>(
      context: context,
      builder: (_) => const _APFisicoDialog(),
    );
    if (datos == null || !context.mounted) return;
    await context.read<EscenariosCubit>().crearAPFisico(
          proyectoId: proyectoId,
          datos: datos,
        );
  }

  Future<void> _compartirReporte(BuildContext context, String rutaLocal) async {
    try {
      await SharePlus.instance.share(
        ShareParams(
          title: 'Reporte Wireless HeatMapper',
          subject: 'Reporte Wireless HeatMapper',
          text: 'Reporte técnico generado por Wireless HeatMapper.',
          files: [
            XFile(
              rutaLocal,
              mimeType: 'application/pdf',
              name: 'reporte-wireless-heatmapper.pdf',
            ),
          ],
        ),
      );
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('No se pudo compartir el PDF: $e')),
      );
    }
  }
}

class _ConfiguracionEscenario {
  final String tipoNegocio;
  final String perfil;
  final List<String> bandas;
  final int maxAps;
  final double? presupuesto;

  const _ConfiguracionEscenario({
    required this.tipoNegocio,
    required this.perfil,
    required this.bandas,
    required this.maxAps,
    required this.presupuesto,
  });
}

class _APFisicoDialog extends StatefulWidget {
  const _APFisicoDialog();

  @override
  State<_APFisicoDialog> createState() => _APFisicoDialogState();
}

class _APFisicoDialogState extends State<_APFisicoDialog> {
  final _nombre = TextEditingController(text: 'AP existente');
  final _fabricante = TextEditingController(text: 'Bulldog Tech.');
  final _modelo = TextEditingController(text: 'AP empresarial dual-band');
  final _x = TextEditingController(text: '100');
  final _y = TextEditingController(text: '100');
  final _altura = TextEditingController(text: '2.5');
  final _potencia24 = TextEditingController(text: '8');
  final _potencia5 = TextEditingController(text: '14');
  final _ssid = TextEditingController(text: 'Red corporativa');
  final _bssid24 = TextEditingController();
  final _bssid5 = TextEditingController();
  String _movimiento = 'MOVIBLE';

  @override
  void dispose() {
    for (final controller in [
      _nombre,
      _fabricante,
      _modelo,
      _x,
      _y,
      _altura,
      _potencia24,
      _potencia5,
      _ssid,
      _bssid24,
      _bssid5,
    ]) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Registrar AP físico'),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
                controller: _nombre,
                decoration: const InputDecoration(labelText: 'Nombre')),
            TextField(
                controller: _fabricante,
                decoration: const InputDecoration(labelText: 'Fabricante')),
            TextField(
                controller: _modelo,
                decoration: const InputDecoration(labelText: 'Modelo')),
            Row(children: [
              Expanded(
                  child: TextField(
                      controller: _x,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(labelText: 'X'))),
              const SizedBox(width: 8),
              Expanded(
                  child: TextField(
                      controller: _y,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(labelText: 'Y'))),
            ]),
            TextField(
                controller: _altura,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: 'Altura (m)')),
            DropdownButtonFormField<String>(
              initialValue: _movimiento,
              decoration: const InputDecoration(labelText: 'Movimiento'),
              items: const [
                DropdownMenuItem(value: 'MOVIBLE', child: Text('Movible')),
                DropdownMenuItem(value: 'FIJO', child: Text('Fijo')),
                DropdownMenuItem(value: 'RETIRABLE', child: Text('Retirable')),
              ],
              onChanged: (value) => setState(() => _movimiento = value!),
            ),
            TextField(
                controller: _potencia24,
                keyboardType: TextInputType.number,
                decoration:
                    const InputDecoration(labelText: 'Potencia 2,4 GHz (dBm)')),
            TextField(
                controller: _potencia5,
                keyboardType: TextInputType.number,
                decoration:
                    const InputDecoration(labelText: 'Potencia 5 GHz (dBm)')),
            TextField(
                controller: _ssid,
                decoration: const InputDecoration(labelText: 'SSID')),
            TextField(
                controller: _bssid24,
                decoration: const InputDecoration(
                    labelText: 'BSSID 2,4 GHz (opcional)')),
            TextField(
                controller: _bssid5,
                decoration:
                    const InputDecoration(labelText: 'BSSID 5 GHz (opcional)')),
          ],
        ),
      ),
      actions: [
        TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar')),
        FilledButton(
          onPressed: () {
            final potencia24 = double.tryParse(_potencia24.text);
            final potencia5 = double.tryParse(_potencia5.text);
            final x = double.tryParse(_x.text);
            final y = double.tryParse(_y.text);
            final altura = double.tryParse(_altura.text);
            if (potencia24 == null ||
                potencia5 == null ||
                x == null ||
                y == null ||
                altura == null) {
              return;
            }
            Navigator.pop(context, {
              'nombre': _nombre.text.trim(),
              'fabricante': _fabricante.text.trim(),
              'modelo': _modelo.text.trim(),
              'rol': 'EXISTENTE',
              'restriccion_movimiento': _movimiento,
              'coord_x': x,
              'coord_y': y,
              'altura_m': altura,
              'tipo_montaje': 'TECHO',
              'procedencia': 'INGRESADA_TECNICO',
              'verificado': true,
              'radios': [
                _radioJson('2.4', 6, potencia24, 20, _bssid24.text),
                _radioJson('5', 44, potencia5, 23, _bssid5.text),
              ],
            });
          },
          child: const Text('Guardar'),
        ),
      ],
    );
  }

  Map<String, dynamic> _radioJson(
    String banda,
    int canal,
    double potencia,
    double maxima,
    String bssid,
  ) {
    return {
      'banda': banda,
      'canal': canal,
      'ancho_canal_mhz': 20,
      'potencia_original': potencia,
      'unidad_potencia_original': 'DBM',
      'referencia_potencia': 'IR',
      'potencia_dbm': potencia,
      'potencia_max_dbm': maxima,
      'modo_gestion_rf': 'ESTATICO',
      'dfs_permitido': false,
      'dominio_regulatorio': 'BO',
      'tipo_antena': 'OMNIDIRECCIONAL',
      'ganancia_dbi': 2.14,
      'beamwidth_horizontal': 360,
      'beamwidth_vertical': 60,
      'azimut_grados': 0,
      'inclinacion_grados': 0,
      'perdida_cable_db': 0,
      'procedencia': 'INGRESADA_TECNICO',
      'bssids': bssid.trim().isEmpty
          ? <Map<String, dynamic>>[]
          : [
              {
                'bssid': bssid.trim().toLowerCase(),
                'ssid': _ssid.text.trim(),
                'observado': true,
                'procedencia': 'INGRESADA_TECNICO',
              },
            ],
    };
  }
}

class _ConfiguracionEscenarioDialog extends StatefulWidget {
  const _ConfiguracionEscenarioDialog();

  @override
  State<_ConfiguracionEscenarioDialog> createState() =>
      _ConfiguracionEscenarioDialogState();
}

class _ConfiguracionEscenarioDialogState
    extends State<_ConfiguracionEscenarioDialog> {
  String _tipo = 'INSTALACION_NUEVA';
  String _perfil = 'COBERTURA_EQUILIBRADA';
  bool _banda24 = true;
  bool _banda5 = true;
  double _maxAps = 3;
  final _presupuesto = TextEditingController();

  @override
  void dispose() {
    _presupuesto.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Configurar optimización RF'),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            DropdownButtonFormField<String>(
              initialValue: _tipo,
              decoration: const InputDecoration(labelText: 'Escenario'),
              items: const [
                DropdownMenuItem(
                  value: 'INSTALACION_NUEVA',
                  child: Text('Instalación nueva'),
                ),
                DropdownMenuItem(
                  value: 'RED_EXISTENTE',
                  child: Text('Optimizar red existente'),
                ),
              ],
              onChanged: (value) => setState(() => _tipo = value!),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              initialValue: _perfil,
              decoration: const InputDecoration(labelText: 'Prioridad'),
              items: const [
                DropdownMenuItem(
                  value: 'COBERTURA_EQUILIBRADA',
                  child: Text('Cobertura equilibrada'),
                ),
                DropdownMenuItem(
                  value: 'PRIORIZAR_5_GHZ',
                  child: Text('Priorizar 5 GHz'),
                ),
                DropdownMenuItem(
                  value: 'MENOR_COSTO_CAMBIOS',
                  child: Text('Menor costo/cambios'),
                ),
              ],
              onChanged: (value) => setState(() => _perfil = value!),
            ),
            CheckboxListTile(
              value: _banda24,
              title: const Text('2,4 GHz'),
              contentPadding: EdgeInsets.zero,
              onChanged: (value) => setState(() => _banda24 = value!),
            ),
            CheckboxListTile(
              value: _banda5,
              title: const Text('5 GHz'),
              contentPadding: EdgeInsets.zero,
              onChanged: (value) => setState(() => _banda5 = value!),
            ),
            Text('Máximo de APs: ${_maxAps.round()}'),
            Slider(
              value: _maxAps,
              min: 1,
              max: 5,
              divisions: 4,
              onChanged: (value) => setState(() => _maxAps = value),
            ),
            TextField(
              controller: _presupuesto,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Presupuesto opcional',
                prefixText: 'Bs ',
              ),
            ),
            if (_tipo == 'RED_EXISTENTE')
              const Padding(
                padding: EdgeInsets.only(top: 12),
                child: Text(
                  'La red existente requiere inventario RF completo en el '
                  'backend antes de generar el escenario.',
                ),
              ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancelar'),
        ),
        FilledButton(
          onPressed: !_banda24 && !_banda5
              ? null
              : () => Navigator.pop(
                    context,
                    _ConfiguracionEscenario(
                      tipoNegocio: _tipo,
                      perfil: _perfil,
                      bandas: [
                        if (_banda24) '2.4',
                        if (_banda5) '5',
                      ],
                      maxAps: _maxAps.round(),
                      presupuesto: double.tryParse(_presupuesto.text),
                    ),
                  ),
          child: const Text('Generar'),
        ),
      ],
    );
  }
}

class _ComparacionCard extends StatelessWidget {
  final ComparacionEscenario comparacion;

  const _ComparacionCard({required this.comparacion});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 8),
      child: DecoratedBox(
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(8),
        ),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Comparación',
                style: Theme.of(context).textTheme.titleSmall,
              ),
              const SizedBox(height: 8),
              _DeltaRow(
                etiqueta: 'Cobertura',
                valor:
                    '${comparacion.resumen.deltaPctCobertura.toStringAsFixed(1)}%',
              ),
              _DeltaRow(
                etiqueta: 'Zonas muertas',
                valor: '${comparacion.resumen.deltaZonasMuertas}',
              ),
              _DeltaRow(
                etiqueta: 'Cambios',
                valor: '${comparacion.resumen.cantidadCambios}',
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _ReporteCompartidoCard extends StatelessWidget {
  final String? ruta;
  final VoidCallback? onCompartir;

  const _ReporteCompartidoCard({
    required this.ruta,
    required this.onCompartir,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 8),
      child: DecoratedBox(
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(8),
        ),
        child: ListTile(
          contentPadding: const EdgeInsets.symmetric(horizontal: 12),
          leading: const Icon(Icons.picture_as_pdf),
          title: const Text('PDF listo para compartir'),
          subtitle: const Text('Elige una aplicación para enviarlo o abrirlo.'),
          trailing: IconButton(
            tooltip: 'Compartir nuevamente',
            onPressed: ruta == null ? null : onCompartir,
            icon: const Icon(Icons.ios_share),
          ),
        ),
      ),
    );
  }
}

class _DeltaRow extends StatelessWidget {
  final String etiqueta;
  final String valor;

  const _DeltaRow({required this.etiqueta, required this.valor});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Expanded(child: Text(etiqueta)),
          Text(valor, style: const TextStyle(fontWeight: FontWeight.w700)),
        ],
      ),
    );
  }
}
