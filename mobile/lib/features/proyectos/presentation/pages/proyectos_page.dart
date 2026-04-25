import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';
import '../bloc/proyecto_cubit.dart';
import '../bloc/proyecto_state.dart';
import '../widgets/proyecto_card.dart';

/// Pantalla principal de la lista de proyectos activos.
/// CA-1, CA-2, CA-3, CA-4, CA-5 PB-01 / CA-1..CA-5 PB-10.
/// HU PB-01 — Sp-13
class ProyectosPage extends StatefulWidget {
  const ProyectosPage({super.key});

  @override
  State<ProyectosPage> createState() => _ProyectosPageState();
}

class _ProyectosPageState extends State<ProyectosPage> {
  final _busquedaCtrl = TextEditingController();
  String _filtro = '';

  @override
  void initState() {
    super.initState();
    context.read<ProyectoCubit>().cargarProyectos();
  }

  @override
  void dispose() {
    _busquedaCtrl.dispose();
    super.dispose();
  }

  Future<void> _confirmarArchivar(
      BuildContext context, int id, String nombre) async {
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Archivar proyecto'),
        content: Text(
            '¿Archivar "$nombre"? Podrás verlo en la sección de archivados.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Archivar'),
          ),
        ],
      ),
    );
    if (confirmar == true && context.mounted) {
      context.read<ProyectoCubit>().archivarProyecto(id);
    }
  }

  Future<void> _confirmarEliminar(
      BuildContext context, int id, String nombre) async {
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Eliminar proyecto'),
        content: Text(
          'Esta acción eliminará todos los datos del proyecto "$nombre". ¿Continuar?',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            style: FilledButton.styleFrom(
              backgroundColor: Theme.of(context).colorScheme.error,
            ),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );
    if (confirmar == true && context.mounted) {
      context.read<ProyectoCubit>().eliminarProyecto(id);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mis Proyectos'),
        centerTitle: false,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout_outlined),
            tooltip: 'Cerrar sesión',
            onPressed: () => context.go('/login'),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.push('/proyectos/nuevo',
            extra: context.read<ProyectoCubit>()),
        icon: const Icon(Icons.add),
        label: const Text('Nuevo proyecto'),
      ),
      body: BlocConsumer<ProyectoCubit, ProyectoState>(
        listener: (context, state) {
          if (state is ProyectoError) {
            ScaffoldMessenger.of(context)
              ..hideCurrentSnackBar()
              ..showSnackBar(SnackBar(
                content: Text(state.mensaje),
                backgroundColor: Theme.of(context).colorScheme.error,
                behavior: SnackBarBehavior.floating,
              ));
          }
          if (state is ProyectoEliminado) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Proyecto eliminado.'),
                behavior: SnackBarBehavior.floating,
              ),
            );
            context.read<ProyectoCubit>().cargarProyectos();
          }
          if (state is ProyectoOperacionExitosa) {
            context.read<ProyectoCubit>().cargarProyectos();
          }
        },
        builder: (context, state) {
          if (state is ProyectoLoading || state is ProyectoInitial) {
            return const Center(child: CircularProgressIndicator());
          }

          if (state is ProyectoListaExitosa) {
            final proyectosFiltrados = _filtro.isEmpty
                ? state.proyectos
                : state.proyectos
                    .where((p) =>
                        p.nombre.toLowerCase().contains(_filtro) ||
                        p.cliente.toLowerCase().contains(_filtro))
                    .toList();

            return Column(
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
                  child: TextField(
                    controller: _busquedaCtrl,
                    decoration: InputDecoration(
                      hintText: 'Buscar por proyecto o cliente…',
                      prefixIcon: const Icon(Icons.search),
                      border: const OutlineInputBorder(),
                      suffixIcon: _filtro.isNotEmpty
                          ? IconButton(
                              icon: const Icon(Icons.clear),
                              onPressed: () {
                                _busquedaCtrl.clear();
                                setState(() => _filtro = '');
                              },
                            )
                          : null,
                    ),
                    onChanged: (v) => setState(() => _filtro = v.toLowerCase()),
                  ),
                ),
                Expanded(
                  child: proyectosFiltrados.isEmpty
                      ? _EstadoVacio(
                          hayFiltro: _filtro.isNotEmpty,
                          onCrear: () => context.push('/proyectos/nuevo',
                              extra: context.read<ProyectoCubit>()),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.only(bottom: 88),
                          itemCount: proyectosFiltrados.length,
                          itemBuilder: (_, i) {
                            final proyecto = proyectosFiltrados[i];
                            return ProyectoCard(
                              proyecto: proyecto,
                              onTap: () =>
                                  context.push('/proyectos/${proyecto.id}'),
                              onArchivar: () => _confirmarArchivar(
                                context,
                                proyecto.id,
                                proyecto.nombre,
                              ),
                              onEliminar: () => _confirmarEliminar(
                                context,
                                proyecto.id,
                                proyecto.nombre,
                              ),
                            );
                          },
                        ),
                ),
              ],
            );
          }

          // ProyectoError sin lista previa o estado inesperado
          return Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.error_outline, size: 48, color: Colors.grey),
                const SizedBox(height: 12),
                const Text('No se pudo cargar la lista de proyectos.'),
                const SizedBox(height: 12),
                OutlinedButton(
                  onPressed: () =>
                      context.read<ProyectoCubit>().cargarProyectos(),
                  child: const Text('Reintentar'),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}

/// Widget de estado vacío (sin proyectos o sin resultados de búsqueda).
class _EstadoVacio extends StatelessWidget {
  final bool hayFiltro;
  final VoidCallback onCrear;

  const _EstadoVacio({required this.hayFiltro, required this.onCrear});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              hayFiltro ? Icons.search_off : Icons.folder_off_outlined,
              size: 64,
              color: Colors.grey,
            ),
            const SizedBox(height: 16),
            Text(
              hayFiltro
                  ? 'Sin resultados para la búsqueda.'
                  : 'No hay proyectos. Crea tu primer survey.',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            if (!hayFiltro) ...[
              const SizedBox(height: 20),
              FilledButton.icon(
                onPressed: onCrear,
                icon: const Icon(Icons.add),
                label: const Text('Crear primer proyecto'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
