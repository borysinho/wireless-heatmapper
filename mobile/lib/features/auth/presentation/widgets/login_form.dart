import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import '../bloc/auth_cubit.dart';
import '../bloc/auth_state.dart';

/// Formulario de inicio de sesión (correo electrónico + contraseña).
/// Usa [flutter_form_builder] para validación declarativa.
/// Sp1-17 — PB-09 / Sprint 1
class LoginForm extends StatefulWidget {
  const LoginForm({super.key});

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormBuilderState>();
  bool _passwordVisible = false;

  void _submit() {
    if (!(_formKey.currentState?.saveAndValidate() ?? false)) return;
    final datos = _formKey.currentState!.value;
    context.read<AuthCubit>().login(
          (datos['email'] as String).trim(),
          datos['password'] as String,
        );
  }

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AuthCubit>().state;
    final estaCargando = state is AuthLoading;
    final sinConexion = state is AuthSinConexion;
    final bloqueado = estaCargando || sinConexion;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Banner de sin conexión (Sp1-20 / CA-5)
        if (sinConexion) ...[
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: const Color(0xFFFFEBEE),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: const Color(0xFFEF5350)),
            ),
            child: Row(
              children: [
                const Icon(Icons.wifi_off, color: Color(0xFFC62828), size: 20),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'Sin conexión. Verifique su conexión a internet.',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          color: const Color(0xFFC62828),
                        ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
        ],
        FormBuilder(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              FormBuilderTextField(
                name: 'email',
                keyboardType: TextInputType.emailAddress,
                textInputAction: TextInputAction.next,
                autocorrect: false,
                enabled: !bloqueado,
                decoration: const InputDecoration(
                  labelText: 'Correo electrónico',
                  hintText: 'usuario@bulldogtech.bo',
                  prefixIcon: Icon(Icons.email_outlined),
                  border: OutlineInputBorder(),
                ),
                validator: (valor) {
                  if (valor == null || valor.trim().isEmpty) {
                    return 'Ingrese su correo electrónico';
                  }
                  if (!valor.contains('@') || !valor.contains('.')) {
                    return 'Ingrese un correo electrónico válido';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              FormBuilderTextField(
                name: 'password',
                obscureText: !_passwordVisible,
                textInputAction: TextInputAction.done,
                enabled: !bloqueado,
                onSubmitted: (_) => bloqueado ? null : _submit(),
                decoration: InputDecoration(
                  labelText: 'Contraseña',
                  prefixIcon: const Icon(Icons.lock_outlined),
                  border: const OutlineInputBorder(),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _passwordVisible
                          ? Icons.visibility_off_outlined
                          : Icons.visibility_outlined,
                    ),
                    onPressed: () =>
                        setState(() => _passwordVisible = !_passwordVisible),
                    tooltip: _passwordVisible ? 'Ocultar' : 'Mostrar',
                  ),
                ),
                validator: (valor) {
                  if (valor == null || valor.isEmpty) {
                    return 'Ingrese su contraseña';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              if (sinConexion) ...[
                OutlinedButton(
                  onPressed: () =>
                      context.read<AuthCubit>().resetearParaReintentar(),
                  style: OutlinedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: const Text('Reintentar'),
                ),
              ] else ...[
                FilledButton(
                  onPressed: bloqueado ? null : _submit,
                  style: FilledButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: estaCargando
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                      : const Text(
                          'Iniciar Sesión',
                          style: TextStyle(fontSize: 16),
                        ),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }
}
