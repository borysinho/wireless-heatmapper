import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

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
                            Chip(
                              label: Text(
                                'Bs ${escenario.costoEstimado.toStringAsFixed(0)}',
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        for (final rec in escenario.recomendaciones)
                          ListTile(
                            dense: true,
                            contentPadding: EdgeInsets.zero,
                            leading: const Icon(Icons.router),
                            title: Text('${rec.accion} · ${rec.modeloAp}'),
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
                                      .crearReporte(
                                        proyectoId: proyectoId,
                                        escenarioId: escenario.id,
                                      ),
                              icon: const Icon(Icons.picture_as_pdf),
                              label: const Text('Reporte'),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 8),
              ],
              if (state.comparacion != null)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Comparación',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        const SizedBox(height: 8),
                        _DeltaRow(
                          etiqueta: 'Cobertura',
                          valor:
                              '${state.comparacion!.resumen.deltaPctCobertura.toStringAsFixed(1)}%',
                        ),
                        _DeltaRow(
                          etiqueta: 'Zonas muertas',
                          valor:
                              '${state.comparacion!.resumen.deltaZonasMuertas}',
                        ),
                        _DeltaRow(
                          etiqueta: 'Cambios',
                          valor:
                              '${state.comparacion!.resumen.cantidadCambios}',
                        ),
                      ],
                    ),
                  ),
                ),
              if (state.reporte != null)
                Card(
                  child: ListTile(
                    leading: const Icon(Icons.fact_check),
                    title: Text('Reporte ${state.reporte!.estado}'),
                    subtitle: Text(
                      state.reporte!.urlDescarga ??
                          state.reporte!.error ??
                          'Sin URL disponible',
                    ),
                  ),
                ),
            ],
          );
        },
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
