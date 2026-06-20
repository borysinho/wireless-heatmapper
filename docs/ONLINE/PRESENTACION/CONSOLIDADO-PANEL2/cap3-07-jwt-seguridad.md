## JSON Web Tokens (JWT) para Autenticación sin Estado

### El problema de la autenticación en APIs REST

Las APIs REST son, por definición, sin estado (stateless): el servidor no mantiene sesiones de usuario entre peticiones. Esto implica que cada petición HTTP debe ser autocontenida e incluir suficiente información para que el servidor pueda verificar la identidad del solicitante. Las dos alternativas principales son: sesiones con cookie de sesión (requieren estado en el servidor, incompatible con el principio REST) y tokens de portador (Bearer tokens), que incluyen la identidad del usuario en el token mismo.

### Estructura y funcionamiento de JWT

Un **JSON Web Token (JWT)** es un estándar abierto (RFC 7519) para transmitir información de forma segura entre partes como un objeto JSON firmado digitalmente (Jones, Bradley & Sakimura, 2015). Un JWT tiene tres partes separadas por puntos (`.`):

1. **Header (encabezado):** algoritmo de firma (`HS256` o `RS256`) y tipo de token (`JWT`), codificado en Base64URL.
2. **Payload (carga útil):** las **claims** (afirmaciones) del token: `sub` (subject = ID del usuario), `exp` (timestamp de expiración), `rol` (rol del usuario en el sistema), etc. Codificado en Base64URL.
3. **Signature (firma):** HMAC-SHA256 del encabezado y el payload con la clave secreta del servidor (`SECRET_KEY`). Garantiza que el token no fue alterado.

El proceso de autenticación en el Wireless HeatMapper es el siguiente:

1. El cliente envía credenciales (`email` + `contraseña`) al endpoint `POST /api/auth/login`.
2. El backend verifica la contraseña contra el hash bcrypt almacenado en PostgreSQL.
3. Si las credenciales son válidas, el backend genera:
   - Un **access token** con vida corta (15 minutos), que el cliente incluye en `Authorization: Bearer <token>` en cada petición subsiguiente.
   - Un **refresh token** con vida larga (7 días), almacenado en `flutter_secure_storage` (app móvil) o en una cookie HttpOnly (web), que permite renovar el access token cuando expira sin pedir las credenciales de nuevo.
4. En cada petición, el backend extrae y verifica la firma del JWT. Si la verificación es válida, extrae el ID de usuario del payload y lo usa para autorizar la operación.

### Seguridad del esquema JWT en el Wireless HeatMapper

El diseño del esquema de autenticación implementa las siguientes medidas de seguridad, alineadas con OWASP Top 10 (OWASP Foundation, 2021):

| Medida                             | Implementación                                                                                            |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Contraseñas hasheadas con bcrypt   | `passlib[bcrypt]` con factor de costo 12                                                                  |
| Access tokens de vida corta        | Expiración en 15 minutos                                                                                  |
| Refresh tokens revocables          | Hash del refresh token en tabla `refresh_token` con campo `revocado`; al cerrar sesión se revoca el token |
| Tokens almacenados de forma segura | `flutter_secure_storage` (Keystore Android) en la app; cookie HttpOnly + Secure en la web                 |
| Algoritmo de firma seguro          | HS256 con `SECRET_KEY` de 256 bits generada aleatoriamente (no hardcoded)                                 |
| Verificación de usuario activo     | Cada request verifica que el usuario exista y esté en estado ACTIVO                                       |
| Validación de rol                  | Endpoints de administración requieren `rol == ADMIN` verificado en el backend                             |

La separación entre access token (corto, sin persistencia en BD) y refresh token (largo, persistido y revocable) es una práctica recomendada por la RFC 6749 (OAuth 2.0) y por las guías de seguridad de la OWASP para APIs REST.
