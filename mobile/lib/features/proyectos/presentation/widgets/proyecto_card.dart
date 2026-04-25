import 'package:flutter/material.dart';
import '../../domain/entities/proyecto.dart';

/// Card de un proyecto en la lista principal.
/// Muestra: nombre, cliente, estado (badge de color), fecha última actividad.
/// HU PB-01 / PB-10 — Sp-13
class ProyectoCard extends StatelessWidget {
  final Proyecto proyecto;
  final VoidCallback onTap;
  final VoidCallback onArchivar;
  final VoidCallback onEliminar;

  const ProyectoCard({
    super.key,
    required this.proyecto,
    required this.onTap,
    required this.onArchivar,
    required this.onEliminar,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: const CircleAvatar(child: Icon(Icons.wifi_find_rounded)),
        title: Text(
          proyecto.nombre,
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(proyecto.cliente),
            const SizedBox(height: 4),
            Row(
              children: [
                _EstadoBadge(estado: proyecto.estado),
                const SizedBox(width: 8),
                Text(
                  _formatearFecha(proyecto.updatedAt),
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ],
            ),
          ],
        ),
        trailing: PopupMenuButton<_AccionProyecto>(
          tooltip: 'Opciones',
          onSelected: (accion) {
            switch (accion) {
              case _AccionProyecto.archivar:
                onArchivar();
              case _AccionProyecto.eliminar:
                onEliminar();
            }
          },
          itemBuilder: (_) => const [
            PopupMenuItem(
              value: _AccionProyecto.archivar,
              child: ListTile(
                leading: Icon(Icons.archive_outlined),
                title: Text('Archivar'),
                contentPadding: EdgeInsets.zero,
              ),
            ),
            PopupMenuItem(
              value: _AccionProyecto.eliminar,
              child: ListTile(
                leading: Icon(Icons.delete_outline, color: Colors.red),
                title: Text('Eliminar', style: TextStyle(color: Colors.red)),
                contentPadding: EdgeInsets.zero,
              ),
            ),
          ],
        ),
        onTap: onTap,
      ),
    );
  }

  String _formatearFecha(DateTime fecha) {
    return '${fecha.day.toString().padLeft(2, '0')}/'
        '${fecha.month.toString().padLeft(2, '0')}/'
        '${fecha.year}';
  }
}

enum _AccionProyecto { archivar, eliminar }

/// Badge de color para indicar el estado del proyecto.
class _EstadoBadge extends StatelessWidget {
  final EstadoProyecto estado;

  const _EstadoBadge({required this.estado});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: _color(context).withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: _color(context), width: 0.8),
      ),
      child: Text(
        estado.etiqueta,
        style: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w600,
          color: _color(context),
        ),
      ),
    );
  }

  Color _color(BuildContext context) {
    switch (estado) {
      case EstadoProyecto.nuevo:
        return Colors.blue.shade700;
      case EstadoProyecto.enProgreso:
        return Colors.orange.shade700;
      case EstadoProyecto.completado:
        return Colors.green.shade700;
      case EstadoProyecto.archivado:
        return Colors.grey.shade600;
    }
  }
}
