import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../domain/entities/plano.dart';
import '../cubit/planos_cubit.dart';
import '../cubit/planos_state.dart';
import '../utils/url_resolver.dart';

/// Página del editor de plano: visualiza la imagen y permite calibrar la
/// escala (PB-11) seleccionando dos puntos sobre el plano e indicando la
/// distancia real entre ellos.
class PlanoEditorPage extends StatefulWidget {
  final Plano plano;

  const PlanoEditorPage({super.key, required this.plano});

  @override
  State<PlanoEditorPage> createState() => _PlanoEditorPageState();
}

class _PlanoEditorPageState extends State<PlanoEditorPage> {
  /// Modo activo de calibración: en true, los taps marcan puntos.
  bool _modoCalibracion = false;

  /// Puntos seleccionados en coordenadas de imagen (px del plano original).
  Offset? _puntoA;
  Offset? _puntoB;

  /// Tamaño actual del widget que muestra la imagen (en px de pantalla).
  Size _renderSize = Size.zero;

  late Plano _plano;

  @override
  void initState() {
    super.initState();
    _plano = widget.plano;
    if (_plano.calibrado) {
      _puntoA = Offset(_plano.calibracionX1!, _plano.calibracionY1!);
      _puntoB = Offset(_plano.calibracionX2!, _plano.calibracionY2!);
    }
  }

  /// Convierte un tap (en px de pantalla) a coordenadas en px del plano.
  Offset _tapAImagen(Offset tap) {
    if (_renderSize == Size.zero) return Offset.zero;
    final factorX = _plano.anchoPx / _renderSize.width;
    final factorY = _plano.altoPx / _renderSize.height;
    return Offset(tap.dx * factorX, tap.dy * factorY);
  }

  /// Convierte coordenadas del plano a px de pantalla para pintar overlays.
  Offset _imagenAPantalla(Offset puntoImagen) {
    if (_renderSize == Size.zero) return Offset.zero;
    final factorX = _renderSize.width / _plano.anchoPx;
    final factorY = _renderSize.height / _plano.altoPx;
    return Offset(puntoImagen.dx * factorX, puntoImagen.dy * factorY);
  }

  void _onTapImagen(TapDownDetails details) {
    if (!_modoCalibracion) return;
    final puntoImagen = _tapAImagen(details.localPosition);
    setState(() {
      if (_puntoA == null || (_puntoA != null && _puntoB != null)) {
        _puntoA = puntoImagen;
        _puntoB = null;
      } else {
        _puntoB = puntoImagen;
      }
    });
  }

  Future<void> _confirmarCalibracion() async {
    if (_puntoA == null || _puntoB == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Marca los dos puntos sobre el plano.')),
      );
      return;
    }
    final distancia = await _pedirDistancia();
    if (distancia == null) return;
    if (!mounted) return;
    await context.read<PlanosCubit>().calibrarPlano(
          planoId: _plano.id,
          x1: _puntoA!.dx,
          y1: _puntoA!.dy,
          x2: _puntoB!.dx,
          y2: _puntoB!.dy,
          distanciaRealM: distancia,
        );
  }

  Future<double?> _pedirDistancia() async {
    final controller = TextEditingController();
    final formKey = GlobalKey<FormState>();
    return showDialog<double>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Distancia real'),
        content: Form(
          key: formKey,
          child: TextFormField(
            controller: controller,
            autofocus: true,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: const InputDecoration(
              labelText: 'Metros entre los dos puntos',
              suffixText: 'm',
              hintText: 'Ej. 5.20',
            ),
            validator: (value) {
              final v = double.tryParse((value ?? '').replaceAll(',', '.'));
              if (v == null) return 'Ingresa un número válido.';
              if (v < 1) return 'Debe ser ≥ 1 metro.';
              return null;
            },
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            onPressed: () {
              if (!(formKey.currentState?.validate() ?? false)) return;
              final v = double.parse(
                controller.text.replaceAll(',', '.'),
              );
              Navigator.of(ctx).pop(v);
            },
            child: const Text('Calibrar'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final url = resolverUrlFirmada(_plano.urlFirmada);
    return BlocListener<PlanosCubit, PlanosState>(
      listener: (context, state) {
        if (state is PlanosOperacionExitosa &&
            state.planoAfectado != null &&
            state.planoAfectado!.id == _plano.id) {
          setState(() {
            _plano = state.planoAfectado!;
            _modoCalibracion = false;
            _puntoA = Offset(_plano.calibracionX1!, _plano.calibracionY1!);
            _puntoB = Offset(_plano.calibracionX2!, _plano.calibracionY2!);
          });
        }
      },
      child: Scaffold(
        appBar: AppBar(
          title: Text(_plano.nombre),
          actions: [
            IconButton(
              tooltip: _modoCalibracion
                  ? 'Cancelar calibración'
                  : 'Calibrar escala',
              icon: Icon(_modoCalibracion ? Icons.close : Icons.straighten),
              onPressed: () => setState(() {
                _modoCalibracion = !_modoCalibracion;
                if (!_modoCalibracion && !_plano.calibrado) {
                  _puntoA = null;
                  _puntoB = null;
                }
              }),
            ),
          ],
        ),
        body: Column(
          children: [
            _StatusBar(plano: _plano, modoCalibracion: _modoCalibracion),
            Expanded(
              child: LayoutBuilder(
                builder: (context, constraints) {
                  // Mantener el aspect ratio del plano dentro del Box.
                  final aspect = _plano.anchoPx / _plano.altoPx;
                  double w = constraints.maxWidth;
                  double h = w / aspect;
                  if (h > constraints.maxHeight) {
                    h = constraints.maxHeight;
                    w = h * aspect;
                  }
                  WidgetsBinding.instance.addPostFrameCallback((_) {
                    if (_renderSize != Size(w, h)) {
                      setState(() => _renderSize = Size(w, h));
                    }
                  });
                  return Center(
                    child: SizedBox(
                      width: w,
                      height: h,
                      child: InteractiveViewer(
                        panEnabled: !_modoCalibracion,
                        scaleEnabled: !_modoCalibracion,
                        child: GestureDetector(
                          onTapDown: _onTapImagen,
                          child: Stack(
                            fit: StackFit.expand,
                            children: [
                              Image.network(
                                url,
                                fit: BoxFit.contain,
                                errorBuilder: (_, __, ___) => const Center(
                                  child: Padding(
                                    padding: EdgeInsets.all(16),
                                    child: Text(
                                      'No se pudo cargar la imagen del plano. '
                                      'La URL pudo expirar; vuelve a entrar al editor.',
                                      textAlign: TextAlign.center,
                                    ),
                                  ),
                                ),
                              ),
                              if (_puntoA != null || _puntoB != null)
                                CustomPaint(
                                  painter: _CalibracionPainter(
                                    puntoA: _puntoA == null
                                        ? null
                                        : _imagenAPantalla(_puntoA!),
                                    puntoB: _puntoB == null
                                        ? null
                                        : _imagenAPantalla(_puntoB!),
                                  ),
                                ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
        floatingActionButton: _modoCalibracion
            ? FloatingActionButton.extended(
                onPressed: _confirmarCalibracion,
                icon: const Icon(Icons.check),
                label: const Text('Confirmar'),
              )
            : null,
      ),
    );
  }
}

class _StatusBar extends StatelessWidget {
  final Plano plano;
  final bool modoCalibracion;
  const _StatusBar({required this.plano, required this.modoCalibracion});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final color = modoCalibracion
        ? theme.colorScheme.tertiaryContainer
        : (plano.calibrado
            ? Colors.green.shade100
            : Colors.orange.shade100);
    final texto = modoCalibracion
        ? 'Modo calibración: marca el punto A y luego el punto B sobre el plano.'
        : (plano.calibrado
            ? 'Calibrado · ${plano.escalaMPorPx!.toStringAsFixed(4)} m/px '
                '(${plano.distanciaRealM!.toStringAsFixed(2)} m)'
            : 'Sin calibrar. Toca el ícono de la regla para iniciar.');
    return Container(
      width: double.infinity,
      color: color,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Text(texto, style: theme.textTheme.bodyMedium),
    );
  }
}

class _CalibracionPainter extends CustomPainter {
  final Offset? puntoA;
  final Offset? puntoB;
  _CalibracionPainter({this.puntoA, this.puntoB});

  @override
  void paint(Canvas canvas, Size size) {
    final paintLinea = Paint()
      ..color = Colors.redAccent
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;
    final paintPunto = Paint()..color = Colors.redAccent;

    if (puntoA != null && puntoB != null) {
      canvas.drawLine(puntoA!, puntoB!, paintLinea);
    }
    if (puntoA != null) {
      canvas.drawCircle(puntoA!, 6, paintPunto);
    }
    if (puntoB != null) {
      canvas.drawCircle(puntoB!, 6, paintPunto);
    }
  }

  @override
  bool shouldRepaint(covariant _CalibracionPainter old) {
    return old.puntoA != puntoA || old.puntoB != puntoB;
  }
}
