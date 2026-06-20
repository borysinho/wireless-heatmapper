import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

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
        listener: (context, state) {
          if (state.error != null) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(state.error!)),
            );
          }
        },
        builder: (context, state) {
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              FilledButton.icon(
                onPressed: state.cargando
                    ? null
                    : () => context
                        .read<EscenariosCubit>()
                        .generar(proyectoId: proyectoId),
                icon: state.cargando
                    ? const SizedBox.square(
                        dimension: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.auto_awesome),
                label: const Text('Generar recomendación'),
              ),
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
                            Chip(label: Text('Banda ${escenario.banda} GHz')),
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
                                      .crearYDescargarReporte(
                                        proyectoId: proyectoId,
                                        escenarioId: escenario.id,
                                      ),
                              icon: const Icon(Icons.download),
                              label: const Text('Descargar PDF'),
                            ),
                          ],
                        ),
                        if (state.comparacion?.escenario.id == escenario.id)
                          _ComparacionCard(comparacion: state.comparacion!),
                        if (state.reporte?.escenarioId == escenario.id)
                          _ReporteDescargadoCard(
                              ruta: state.reporte!.rutaLocal),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 8),
              ],
            ],
          );
        },
      ),
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

class _ReporteDescargadoCard extends StatelessWidget {
  final String? ruta;

  const _ReporteDescargadoCard({required this.ruta});

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
          title: const Text('PDF descargado en este dispositivo'),
          subtitle:
              SelectableText(ruta ?? 'No se pudo resolver la ruta local.'),
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
