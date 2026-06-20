UNIVERSIDAD AUTÓNOMA GABRIEL RENÉ MORENO
FACULTAD DE INGENIERÍA EN CIENCIAS DE LA COMPUTACIÓN Y
TELECOMUNICACIONES
Ingeniería Informática

PANEL 2
Plataforma educativa de cursos gamificados dedicado al nivel de educación primario para
el colegio particular mixto “Los Ángeles”
Grupo: 22
Autores:
- Cayo Terrazas Eben Ezer 219011680
- Chambi Gonzales Niels Roy 219012441
Materia: Taller de Grado I (INF511-SC)
Docente: Ing. Martínez Canedo Rolando Antonio

Santa Cruz de la Sierra - Bolivia
Junio – 2025

Índice
# CAPITULO I. DEFINICIÓN DEL PROYECTO ........................................................................... 1
Introducción ................................................................................................................................ 1
Antecedentes ............................................................................................................................... 2
Revisión Literaria ................................................................................................................... 2
La Pedagogía del Juego según Friedrich Fröbel ................................................................. 2
El Método Montessori......................................................................................................... 3
Referencias de Aplicaciones ................................................................................................... 4
Duolingo ............................................................................................................................. 4
Khan Academy Kids ........................................................................................................... 5
Smartick .............................................................................................................................. 6
Caso de Estudio ...................................................................................................................... 6
Descripción del Problema ........................................................................................................... 7
Situación Problemática ............................................................................................................... 9
Situación Deseada ....................................................................................................................... 9
Objetivos Del Proyecto ............................................................................................................. 10
Objetivo General ................................................................................................................... 10
Objetivos Específicos ........................................................................................................... 10
Alcance ..................................................................................................................................... 10
Tecnología ................................................................................................................................. 11
Estrategia .............................................................................................................................. 11
Métodos ................................................................................................................................ 11
Herramientas: ........................................................................................................................ 12


Herramientas de Software: ................................................................................................ 12
Herramientas de Hardware: .............................................................................................. 12
Cronograma ............................................................................................................................... 13
Sprint 0 .................................................................................................................................. 13
Sprint 1 .................................................................................................................................. 13
Sprint 2 .................................................................................................................................. 14
Sprint 3 .................................................................................................................................. 14
# CAPITULO II. FUNDAMENTACIÓN TEÓRICA DE LA APLICACIÓN ............................... 15
Teoría de la Gamificación ......................................................................................................... 15
Elementos Fundamentales de la Gamificación ..................................................................... 15
Principios Fundamentales de la Gamificación Educativa ..................................................... 16
## Teoría de la Autodeterminación de Deci y Ryan ...................................................................... 16
## Teoría del Flujo de Csikszentmihalyi ....................................................................................... 17
Aplicación de la Teoría ............................................................................................................. 18
Implementación de los Elementos de Werbach en la Plataforma ......................................... 18
Aplicación de la Teoría de la Autodeterminación ................................................................ 19
Implementación de la Teoría del Flujo ................................................................................. 20
# CAPITULO III. FUNDAMENTACIÓN TEÓRICA TECNOLÓGICA ...................................... 21
Modelo Bayesian Knowledge Tracing (BKT) .......................................................................... 21
Formulación Matemática del BKT ....................................................................................... 21
Proceso de Funcionamiento del BKT ................................................................................... 23
Clasificación de Estudiantes Basada en Umbrales de Dominio ........................................... 23
Ejemplo de Clasificación de Estudiantes con BKT .............................................................. 24


Algoritmo Expectation-Maximization (EM) ............................................................................ 26
Formulación Matemática del Algoritmo EM ........................................................................ 26
Proceso del Algoritmo EM ................................................................................................... 27
Aplicación del Algoritmo EM para Estimación de Parámetros BKT ................................... 27
GraphQL ................................................................................................................................... 29
Características Principales de GraphQL ............................................................................... 29
Comparación con APIs REST .............................................................................................. 29
Beneficios Específicos para el Desarrollo Móvil ................................................................. 30
# CAPITULO IV. PROCESO DE DESARROLLO SCRUM ......................................................... 31
Sprint 2 ...................................................................................................................................... 31
Sprint Planning ..................................................................................................................... 31
Objetivo del Sprint ............................................................................................................ 31
Contexto del Sistema ........................................................................................................ 31
Historias de Usuario .......................................................................................................... 32
Sprint Backlog .................................................................................................................. 34
Patrón de Desarrollo ............................................................................................................. 35
Diseño de la Arquitectura ................................................................................................. 35
Diseño de Datos ................................................................................................................ 37
Sprint Review ....................................................................................................................... 38
Sprint Retrospective .............................................................................................................. 39
Bibliografía ................................................................................................................................... 40
Anexos .......................................................................................................................................... 43
Anexo A. Sprint 0 ..................................................................................................................... 43


Definiciones Iniciales ........................................................................................................... 43
Definición del Equipo Scrum............................................................................................ 43
Objetivo del Producto ....................................................................................................... 43
Definición de la Duración de los Sprints .......................................................................... 43
Product Backlog ................................................................................................................ 44
Anexo B. Sprint 1 ..................................................................................................................... 45
Sprint Planning ..................................................................................................................... 45
Objetivo del Sprint. ........................................................................................................... 45
Contexto del Sistema ........................................................................................................ 45
Historias de Usuario .......................................................................................................... 46
Sprint Backlog .................................................................................................................. 48
Patrón de Desarrollo ............................................................................................................. 49
Diseño de la Arquitectura ................................................................................................. 49
Diseño de Datos ................................................................................................................ 51
Sprint Review ....................................................................................................................... 52
Sprint Restrospective ............................................................................................................ 53
Anexo C. Esquemas gráficos: Situación problemática y situación deseada ............................. 54
Anexo D. Carta caso de estudio ................................................................................................ 55
Anexo E. Diapositivas .............................................................................................................. 56

Tabla de Ilustraciones
Ilustración 1. Interfaz Gráfica de Duolingo .................................................................................... 5
Ilustración 2. Interfaz Gráfica de Khan Academy Kids .................................................................. 5


Ilustración 3. Interfaz Gráfica de Smartick ..................................................................................... 6
Ilustración 4. Diagrama de Gantt para el Sprint 0 ........................................................................ 13
Ilustración 5. Diagrama de Gantt para el Sprint 1 ........................................................................ 13
Ilustración 6. Diagrama de Gantt para el Sprint 2 ........................................................................ 14
Ilustración 7. Diagrama de Gantt para el Sprint 3 ........................................................................ 14
Ilustración 8. Teoría del flujo de Csikszentmihalyi ...................................................................... 18
Ilustración 9. Diagrama de casos de uso ....................................................................................... 31
Ilustración 10. Diagrama de Despliegue ....................................................................................... 35
Ilustración 11. Diagrama de Paquetes Organizado en Capas ....................................................... 36
Ilustración 12. Diagrama de clases de la base de datos ................................................................ 37
Ilustración 13. Gráfico de la Situación Problemática ................................................................... 54
Ilustración 14. Gráfico de la Situación Deseada ........................................................................... 54


1


# CAPITULO I. DEFINICIÓN DEL PROYECTO
## Introducción
La educación primaria representa una etapa fundamental en la formación académica de
todo individuo, ya que durante estos años se construyen las bases del conocimiento, los hábitos
de estudio y la motivación por aprender. En esta fase temprana, los métodos tradicionales de
enseñanza frecuentemente se enfrentan a desafíos relacionados con la falta de interés genuino
por parte de los estudiantes, lo cual genera consecuencias académicas que se arrastran en los
niveles educativos posteriores. Frente a este escenario, surgen propuestas que exploran nuevas
formas de capturar la atención de los estudiantes y fomentar un vínculo más sólido con el
proceso de aprendizaje.
El presente documento describe el desarrollo de una plataforma educativa diseñada
específicamente para estudiantes de quinto y sexto de primaria del Colegio Particular Mixto “Los
Ángeles”. Esta solución integra elementos de gamificación y tecnologías de inteligencia artificial
con el objetivo de transformar la experiencia educativa tradicional en una experiencia más
dinámica, interactiva y adaptativa. La plataforma no solo se enfoca en la transmisión de
contenidos, sino que también analiza el comportamiento y desempeño individual de cada
estudiante, con el fin de ajustar automáticamente la dificultad de los retos académicos y brindar
una retroalimentación personalizada, permitiendo así una comprensión más profunda de los
contenidos.
La implementación de este tipo de tecnología educativa responde a una problemática
ampliamente observada en el entorno escolar: la desmotivación y pasividad de los estudiantes
frente al aprendizaje. A través del diseño de una experiencia basada en niveles, desafíos y
recompensas, se busca fomentar el compromiso y la participación activa, promoviendo un

2


aprendizaje que resulte significativo tanto en términos académicos como personales. Asimismo,
el uso de herramientas de análisis y diagnóstico educativo brinda a los docentes la posibilidad de
intervenir de manera más precisa, adaptando sus estrategias pedagógicas a las necesidades
particulares de cada estudiante.
En este contexto, la plataforma se concibe como un entorno de aprendizaje continuo,
donde la inteligencia artificial no sustituye al docente, sino que lo complementa. Esto permite no
solo mejorar el rendimiento individual, sino también elevar los estándares del proceso educativo
institucional, fortaleciendo la preparación de los alumnos para etapas educativas futuras y
posicionando al colegio como una institución pionera en innovación pedagógica.
A lo largo del documento, se detallarán los aspectos conceptuales, técnicos y
metodológicos que fundamentan el diseño e implementación de esta solución educativa,
abordando sus componentes clave, objetivos, alcance y procesos de validación. De este modo, se
presenta un proyecto que, más allá de su componente tecnológico, busca generar un impacto
duradero en la forma en que los estudiantes se relacionan con el conocimiento, sentando las
bases para una educación más personalizada, inclusiva y eficaz.

## Antecedentes
Revisión Literaria
La Pedagogía del Juego según Friedrich Fröbel
A principios del siglo XIX, el pedagogo alemán Friedrich Fröbel revolucionó la
educación infantil al proponer una visión radicalmente nueva: el juego como eje central del
aprendizaje. Fröbel, quien había sido influenciado por las ideas de Rousseau y Pestalozzi, creía
firmemente que los niños no solo disfrutan jugando, sino que a través del juego construyen su

3


comprensión del mundo. Su enfoque marcó un antes y después en la pedagogía, sentando las
bases de lo que hoy conocemos como educación lúdica.
Fröbel desarrolló su teoría en un momento en que la educación infantil era rígida y
centrada en la memorización. Frente a esto, él propuso que el verdadero aprendizaje surge de la
exploración activa y la interacción con materiales concretos. Para ello, diseñó los famosos
"dones", una serie de objetos como esferas, cubos y cilindros, que los niños manipulaban para
comprender conceptos matemáticos y espaciales. Estos materiales no eran simples juguetes, sino
herramientas pedagógicas cuidadosamente pensadas para estimular el razonamiento. Además,
introdujo las "ocupaciones", actividades manuales como el tejido o el modelado en barro, que
fomentaban la creatividad y la motricidad fina.
Un aspecto clave de su método era el juego simbólico, donde los niños imitaban roles
adultos —como ser padres, maestros o artesanos— para entender su entorno social. Fröbel
también incorporó canciones, rimas y juegos en grupo, creando un ambiente dinámico donde el
lenguaje y el movimiento se integraban naturalmente. Su famoso Kindergarten (jardín de
infancia) no era solo un lugar de cuidado, sino un espacio diseñado para que los niños
interactuaran con la naturaleza y entre sí, aprendiendo valores como la cooperación y el respeto.

El Método Montessori
A comienzos del siglo XX, la médica y pedagoga italiana María Montessori desarrolló un
enfoque educativo que cambiaría para siempre la forma de entender el aprendizaje infantil. Tras
observar minuciosamente el comportamiento de los niños en diferentes contextos, Montessori
llegó a una conclusión revolucionaria: los pequeños poseen una capacidad innata para aprender
cuando se les proporciona un ambiente adecuado y libertad para explorar. Su método, que

4


inicialmente se aplicó con niños en situación de vulnerabilidad en Roma, pronto demostró ser tan
efectivo que se expandió por todo el mundo, trascendiendo barreras culturales y sociales.
El corazón del método Montessori late en la idea de que los niños aprenden mejor cuando
pueden seguir sus propios intereses en un entorno cuidadosamente preparado. Montessori diseñó
aulas llenas de materiales didácticos específicos —desde bloques de madera hasta letras de lija—
que invitaban a los niños a tocar, experimentar y descubrir conceptos abstractos a través de lo
concreto. Estos materiales no eran meras herramientas, sino puertas hacia el autodescubrimiento,
dispuestas en estantes bajos para que los niños pudieran acceder a ellos sin ayuda. En este
espacio, el rol del maestro se transformaba radicalmente: ya no era un instructor que dictaba
conocimientos, sino un guía discreto que observaba y facilitaba el proceso de aprendizaje sin
interferir en la autonomía del niño.
Uno de los pilares más innovadores de la pedagogía Montessori era su comprensión de
los "períodos sensibles", etapas en las que los niños muestran una predisposición natural para
adquirir ciertas habilidades, como el lenguaje o el orden. Montessori sostenía que, si se
aprovechaban estos momentos críticos con los estímulos adecuados, el aprendizaje ocurría de
manera casi espontánea y con alegría. Por ejemplo, en lugar de obligar a un niño a memorizar las
letras, este las trazaba en arena o las recortaba en papel, asociando el sonido con la forma de
manera multisensorial.

Referencias de Aplicaciones
Duolingo
Aplicación de aprendizaje de idiomas que implementa un sistema de gamificación para
motivar al usuario a través de niveles, recompensas y seguimiento del progreso. Emplea IA para

5


adaptar las explicaciones y mejorar el proceso de retroalimentación, ofreciendo una experiencia
personalizada de aprendizaje.

Khan Academy Kids
App educativa para niños entre 2 y 8 años, enfocada en el aprendizaje temprano con una
ruta personalizada según el ritmo de cada usuario. Sus actividades interactivas fomentan el
desarrollo autónomo y el refuerzo de habilidades clave como lectura y matemáticas, usando IA
para ajustar contenidos y recomendar actividades específicas.
Ilustración 1. Interfaz Gráfica de Duolingo
Ilustración 2. Interfaz Gráfica de Khan Academy Kids

6


Smartick
Es una aplicación educativa para niños de 4 a 14 años que destaca por su uso innovador
de inteligencia artificial para personalizar el aprendizaje de matemáticas. Su algoritmo adaptativo
ajusta en tiempo real la dificultad de los ejercicios según el rendimiento del niño, asegurando
sesiones diarias de 15 minutos que son desafiantes pero accesibles. Esta personalización permite
que cada estudiante avance a su propio ritmo, fomentando la autonomía y la confianza en sí
mismo.

Caso de Estudio
Uno de los principales casos de estudio identificados es el Colegio Los Ángeles, una
institución educativa interesada en mejorar el rendimiento y la motivación de sus estudiantes
mediante el uso de tecnologías de aprendizaje personalizadas.
Actualmente, el colegio enfrenta desafíos relacionados con la diversidad de niveles de
aprendizaje en sus aulas, lo que dificulta ofrecer una atención personalizada a cada estudiante. La
aplicación de un sistema de gamificación educativa con análisis personalizado mediante IA
puede mejorar la eficiencia del proceso educativo y reducir las brechas de aprendizaje.
Ilustración 3. Interfaz Gráfica de Smartick

7


Otros potenciales interesados podrían ser:
- Centros de refuerzo escolar con alta rotación de estudiantes.
- Escuelas rurales con pocos recursos pedagógicos individualizados.
- Instituciones educativas interesadas en incorporar tecnología como herramienta de
mejora académica.

## Descripción del Problema
La educación tradicional enfrenta una creciente desconexión con las nuevas generaciones de
estudiantes, quienes han nacido en una era digital llena de estímulos visuales, interacción
constante y recompensas inmediatas. Esta realidad se ve reflejada con claridad en el Colegio
Particular Mixto “Los Ángeles”, una institución educativa que, a pesar de mantener estándares
aceptables de rendimiento, enfrenta diversos desafíos que limitan su capacidad de formar
estudiantes plenamente motivados, comprometidos y preparados para destacar académicamente.
Falta de apoyo digital y herramientas modernas
Actualmente, el colegio carece de una plataforma tecnológica que complemente o modernice sus
métodos de enseñanza. No se cuenta con una aplicación móvil ni una plataforma web que facilite
el aprendizaje interactivo, el monitoreo del rendimiento académico ni la retroalimentación
personalizada. Esta carencia deja al colegio en desventaja frente a instituciones que ya han
incorporado tecnologías educativas (EdTech) en su modelo pedagógico.
Débil retención de conocimientos fundamentales
Los docentes han identificado una brecha significativa entre los conocimientos adquiridos en
primaria y los requerimientos de secundaria. Muchos estudiantes no recuerdan conceptos básicos
necesarios para avanzar en el nuevo ciclo. Por ejemplo, algunos alumnos olvidan cómo realizar

8


operaciones aritméticas básicas como divisiones o fracciones, lo cual retrasa el avance del curso
y genera frustración en estudiantes y docentes por igual. Este fenómeno evidencia una
desconexión entre la forma en la que se enseña y la manera en la que los niños aprenden y
retienen información.
Falta de motivación intrínseca en el proceso de aprendizaje
Aunque el promedio de notas del colegio se mantiene entre los 70 y 75 puntos sobre 100, esto no
se traduce en un aprendizaje significativo o motivador. Los estudiantes aprueban sus materias,
pero no muestran interés genuino ni entusiasmo por aprender. La enseñanza se percibe como una
obligación, más que una experiencia emocionante o desafiante. No existen mecanismos que
premien el esfuerzo, ni sistemas que estimulen la curiosidad ni el deseo de superación personal.
Limitación del tiempo de enseñanza formal
Los estudiantes del nivel primario solo asisten al colegio durante la mañana, en un horario
restringido de 08:00 a 12:00, con un único receso corto. Este tiempo es insuficiente para
consolidar conocimientos, practicar lo aprendido, y mucho menos para incorporar estrategias de
aprendizaje diferenciado o personalizado. Además, fuera del horario escolar, no hay
herramientas que permitan continuar el aprendizaje de manera autónoma y estructurada.
Falta de personalización en el proceso educativo
El actual modelo educativo sigue un enfoque homogéneo, donde todos los estudiantes reciben el
mismo contenido, al mismo ritmo y con la misma metodología. Esta rigidez ignora las
diferencias individuales en habilidades, estilos de aprendizaje, intereses y ritmos de progreso.
Algunos estudiantes se aburren porque van más avanzados que el resto, mientras que otros se
sienten frustrados porque no logran alcanzar el ritmo del grupo.


9


## Situación Problemática
La mayoría de los estudiantes de nivel primario del Colegio Particular Mixto "Los
Ángeles" carecen de un interés genuino por el aprendizaje, realizando tareas y estudiando para
exámenes únicamente por obligación, lo que posteriormente ocasiona que al llegar a secundaria
presenten significativas dificultades para recordar conceptos básicos, ralentizando
considerablemente su adaptación al nuevo contenido académico y afectando no solo su
desempeño individual sino también limitando el rendimiento académico general de la institución,
situación que obstaculiza las posibilidades del colegio para destacar y sobresalir en las diversas
competencias educativas regionales y nacionales donde participa.

## Situación Deseada
El colegio logra transformar su modelo educativo mediante la implementación de un
ambiente de aprendizaje dinámico donde los estudiantes anteriormente desinteresados ahora se
encuentran altamente motivados y comprometidos con su formación académica, desarrollando
una conexión profunda y significativa con su proceso de aprendizaje que les permite retener
conocimientos de manera efectiva y superar la pasividad académica que los caracterizaba,
manifestando mayor autonomía, confianza y genuino entusiasmo por la adquisición de nuevos
conocimientos, lo cual se traduce en un rendimiento académico notablemente mejorado que se
refleja tanto en la comprensión sólida de conceptos fundamentales como en un desempeño
sobresaliente en diversas evaluaciones.



10


## Objetivos Del Proyecto
### Objetivo General
Desarrollar una plataforma educativa gamificada potenciada con inteligencia artificial,
para los cursos de 5to y 6to de primaria basado en el contenido del programa de educación
primaria indicado por el ministerio de educación de Bolivia.
### Objetivos Específicos
- Analizar los requisitos del sistema.
- Diseñar la estructura de la base de datos y la arquitectura del sistema.
- Implementar un prototipo funcional de plataforma educativa con módulos de
evaluación continua no intrusiva y rutas de aprendizaje personalizadas.
- Entrenar un modelo probabilístico mediante el algoritmo EM, para identificar los
conceptos que los estudiantes necesitan reforzar y de cuales pueden profundizar.
- Validar la efectividad del software mediante pruebas de caja blanca y caja negra.

## Alcance
Cursos con ejercicios dinámicos: Los cursos de la plataforma presentarán su contenido
estructurado en un formato de niveles lineal donde para pasar a un siguiente nivel deberán
completar el anterior, los cuales contendrán información de los temas, ejercicios y desafíos
interactivos.
Aprendizaje Adaptativo: El programa debe ajustar automáticamente la dificultad de los
retos y actividades basándose en el estado de "flujo" del estudiante, creando una experiencia de
aprendizaje personalizada que optimice la adquisición de conocimientos.

11


Aspectos de la Gamificación: La app debe implementar elementos de gamificación
como puntos, insignias, niveles, personalización de avatares y un sistema de recompensas
configurables por el docente para incrementar la motivación y compromiso de los estudiantes.
Módulo de Análisis y Reportes: Los docentes tendrán acceso a paneles de control con
métricas detalladas sobre el progreso de cada estudiante. El sistema generará informes que
identificarán fortalezas, debilidades y patrones de aprendizaje, facilitando una intervención
pedagógica personalizada.
Módulo de Remediación: Para estudiantes que presenten dificultades en temas
específicos mediante el uso de inteligencia artificial, se generarán explicaciones personalizadas y
ejercicios de refuerzo adaptados a las necesidades individuales de cada estudiante.
Competencias colaborativas: El sistema permitirá a estudiantes participar en desafíos
multijugador, competencias periódicas y torneos que incentiven el aprendizaje colaborativo. La
plataforma incluirá un asistente virtual para resolver dudas en tiempo real y ofrecer apoyo
educativo adicional.

## Tecnología
### Estrategia
Proceso de desarrollo basado en SCRUM.
### Métodos
Lenguaje para representar los modelos: UML (Lenguaje de Modelado Unificado).
Fundamentación teórica: Bayesian Knowledge Tracing (BKT) y el algoritmo EM



12


Herramientas:
Herramientas de Software:
- Herramientas de control de versiones: Git y GitHub
- Herramientas CASE: Enterprise Architect, Jira
- Aplicación web de diseño Figma
- Lenguaje de programación Dart
- Framework Flutter
- Framework Nest
- SGBD: PostgreSQL
- Editor de código: Visual Studio Code
- Servicio de alojamiento en la nube: Railway
Herramientas de Hardware:
- Computadoras portátiles
- Impresoras
- Celulares inteligentes



13


## Cronograma
## Sprint 0


## Sprint 1


Ilustración 4. Diagrama de Gantt para el Sprint 0
Ilustración 5. Diagrama de Gantt para el Sprint 1

14


## Sprint 2

## Sprint 3






Ilustración 7. Diagrama de Gantt para el Sprint 3
Ilustración 6. Diagrama de Gantt para el Sprint 2

15


# CAPITULO II. FUNDAMENTACIÓN TEÓRICA DE LA APLICACIÓN
## Teoría de la Gamificación
La gamificación, según Kapp (2012), se define como "el uso de mecánicas, estéticas y
pensamiento basado en juegos para involucrar a las personas, motivar la acción, promover el
aprendizaje y resolver problemas" (Kapp, 2012). Esta definición se complementa con la
propuesta por Werbach y Hunter (2012), quienes la describen como "el uso de elementos de
diseño de juegos en contextos no lúdicos" (Werbach & Hunter, 2012).
La gamificación es una técnica de aprendizaje que traslada la mecánica de los juegos al
ámbito educativo-profesional con el fin de conseguir mejores resultados, ya sea para absorber
mejor algunos conocimientos, mejorar alguna habilidad, o bien recompensar acciones concretas
(Garris, Ahlers, & Driskell, 2002). Este tipo de aprendizaje gana terreno en las metodologías de
formación debido a su carácter lúdico, que facilita la interiorización de conocimientos de una
forma más divertida, generando una experiencia positiva en el usuario (Kapp, 2012).
### Elementos Fundamentales de la Gamificación
Según Werbach, los fundamentos de la gamificación se estructuran en tres niveles
jerárquicos: las dinámicas, las mecánicas y los componentes (Werbach & Hunter, 2014):
Dinámicas: Son el concepto, la estructura implícita del juego. Representan los aspectos
conceptuales de mayor nivel que dan cohesión y estructura a la experiencia gamificada.
Mecánicas: Son los procesos que provocan el desarrollo del juego. Incluyen elementos
como desafíos, oportunidades, competencia, cooperación y retroalimentación.
Componentes: Son las implementaciones específicas de las dinámicas y mecánicas:
avatares, insignias, puntos, colecciones, rankings, niveles, equipos, entre otros.
La interacción de estos tres elementos es lo que genera la actividad gamificada.

16


### Principios Fundamentales de la Gamificación Educativa
Scott y Neustaedter recogen cuatro conceptos fundamentales a la hora de entender la
importancia y los beneficios de la gamificación: libertad para fallar, rápido feedback, progreso,
historia (Scott & Neustaedter, 2013).
Entre los principales beneficios de la gamificación en la educación se incluyen: permite
involucrar a los estudiantes en el propio diseño de la clase, admite "segundas oportunidades",
retroalimenta a los estudiantes sobre sus errores, hace visibles los progresos individuales dentro
del espacio colectivo, desafía a los estudiantes en nuevas tareas, ayuda a generar un ambiente
distendido que permite aumentar el nivel de atención y concentración (Garris, Ahlers, &
Driskell, 2002).

## Teoría de la Autodeterminación de Deci y Ryan
La teoría de la autodeterminación (SDT) es una macro teoría de la motivación humana y
la personalidad que trata de las preocupaciones inherentes al crecimiento y las tendencias innatas
y necesidades psicológicas de las personas. Se refiere a la motivación que hay detrás de las
decisiones de las personas, sin influencia externa e interferencia (Deci & Ryan, 2000).
Deci y Ryan proponen tres necesidades intrínsecas principales involucradas en la
autodeterminación: competencia, autonomía y relación psicológica.
- Autonomía: La necesidad de sentir que uno está de acuerdo y siente que controla su
propio comportamiento. Representa la capacidad de una persona de controlar su propio
comportamiento conforme a sus propias reglas.
- Competencia: Necesidad de sentir que uno hace las cosas bien o que es capaz de mejorar
su capacidad. Se relaciona con la sensación de eficacia y dominio sobre las tareas.

17


- Relación: La necesidad de sentirse conectado de forma significativa con los demás.
Implica el deseo de establecer relaciones cercanas con los demás, sentirse conectado y
cuidado.
La teoría de la autodeterminación maneja la motivación que actúa tras las decisiones de
los seres humanos sin ninguna interferencia o influencia externa, distinguiendo entre motivación
intrínseca, un sentimiento de felicidad y logro, y motivación extrínseca, que se caracteriza por
recompensas tangibles.

## Teoría del Flujo de Csikszentmihalyi
La Teoría del Flow es un estado en el que la persona se encuentra completamente absorta
en una actividad para su propio placer y disfrute. El Flow o Experiencia Óptima es un "estado en
el que la persona se encuentra completamente absorta en una actividad para su propio placer y
disfrute, durante la cual el tiempo vuela y las acciones, pensamientos y movimientos se suceden
unas a otras sin pausa" (Csikszentmihalyi, 1997).
Mihaly Csikszentmihalyi define el flujo como "un estado en el que las personas están tan
involucradas en la actividad que nada parece importarles, la experiencia es tan placentera que las
personas realizan la tarea por el puro motivo de hacerla".
Las características comunes que tienen las experiencias para que sean óptimas incluyen:
la tarea o meta es posible de alcanzar, es necesario el establecimiento de objetivos concretos,
poder concentrarse de forma plena, la tarea ha de tener unas metas claras, las metas claras
permiten una retroalimentación directa e inmediata, actuamos sin esfuerzo, totalmente
concentrados y distanciados de preocupaciones, se crea un sentimiento de control sobre la
situación.

18


En relación con la gamificación, el flujo sobreviene cuando se produce un equilibrio entre
los desafíos de la tarea o actividad que estamos afrontando y las habilidades de las que
disponemos para dicho afrontamiento, esto es la actividad no nos resulta ni demasiado fácil, ni
demasiado complicada.
Mediante un esquema simple (Ilustración 8), Csikszentmihalyi representa esta
experiencia óptima en un eje de coordenadas en el que de un lado tenemos la complejidad de la
tarea o grado de desafío, y de otro, las habilidades con las que la persona cuenta para afrontarlo.

## Aplicación de la Teoría
Implementación de los Elementos de Werbach en la Plataforma
Dinámicas Implementadas:
- Progresión: Sistema de niveles que refleja el avance académico del estudiante
- Narrativa: Contexto educativo gamificado que mantiene la coherencia temática
Ilustración 8. Teoría del flujo de Csikszentmihalyi

19


- Relaciones: Interacción social a través de competencias grupales y salas de clase
Mecánicas del Sistema:
- Desafíos: Ejercicios interactivos y dinámicos que varían en dificultad
- Competencia: Sistema de competencias por curso programadas por docentes
- Retroalimentación: Correcciones con IA y seguimiento detallado del progreso
- Recompensas: Sistema de monedas virtuales y elementos de personalización
Componentes Específicos:
- Avatar personalizable: Permite expresión individual (cabello, ropa, accesorios)
- Sistema de puntos XP: Medición cuantitativa del progreso de aprendizaje
- Monedas virtuales: Recompensa canjeable por elementos de personalización
- Logros: Reconocimiento de hitos específicos de aprendizaje
- Niveles: Representación visual del progreso académico
- Tablas de clasificación implícitas: A través de competencias grupales

Aplicación de la Teoría de la Autodeterminación
Satisfacción de la Necesidad de Autonomía:
- Personalización del avatar: Permite a los estudiantes expresar su identidad única
- Sistema de recompensas: Los estudiantes eligen cómo canjear sus monedas
virtuales
- Aprendizaje adaptativo: El sistema se adapta a la capacidad individual según el
avance
Satisfacción de la Necesidad de Competencia:
- Niveles progresivos: Proporcionan sensación de dominio y crecimiento

20


- Retroalimentación inmediata: El asistente virtual con IA resuelve dudas
instantáneamente
- Prácticas interactivas: Permiten desarrollar habilidades de manera gradual
- Sistema de puntos XP: Cuantifica el progreso y logros académicos
Satisfacción de la Necesidad de Relación:
- Competencias grupales: Fomentan la interacción y colaboración entre estudiantes
- Salas de curso: Crean comunidades de aprendizaje específicas
- Seguimiento docente: Proporciona apoyo personalizado y conexión humana

Implementación de la Teoría del Flujo
Equilibrio Desafío-Habilidad:
- Aprendizaje adaptativo: Ajusta automáticamente la dificultad según el
rendimiento individual
- Progresión gradual: Los niveles aumentan en complejidad de manera escalonada
Objetivos Claros:
- Niveles visibles: Los estudiantes conocen su posición actual y siguiente meta
- Logros específicos: Objetivos concretos y alcanzables claramente definidos
- Progreso cuantificado: Sistema de XP que muestra avance numérico preciso
Retroalimentación Inmediata:
- Correcciones con IA: Asistente virtual que responde dudas al instante
- Alertas de seguimiento: Notificaciones automáticas sobre el progreso
- Visualización de estadísticas: Perfil que muestra logros y progreso en tiempo real


21


# CAPITULO III. FUNDAMENTACIÓN TEÓRICA TECNOLÓGICA
## Modelo Bayesian Knowledge Tracing (BKT)
El modelo Bayesian Knowledge Tracing (BKT) es un modelo probabilístico desarrollado
por Corbett y Anderson, que permite rastrear el conocimiento de un estudiante a lo largo del
tiempo durante el proceso de aprendizaje. Este modelo se fundamenta en la teoría bayesiana para
actualizar las creencias sobre el estado de conocimiento del estudiante basándose en sus
respuestas observadas (Corbett & Anderson, 1995).
El modelo BKT asume que el conocimiento de un estudiante sobre una habilidad
específica puede representarse como una variable binaria latente que indica si el estudiante ha
"aprendido" o "no ha aprendido" la habilidad (Van de Sande, 2013). El modelo se basa en cuatro
parámetros fundamentales:
- P(L₀): Probabilidad inicial de que el estudiante ya conozca la habilidad antes de
comenzar
- P(T): Probabilidad de transición, es decir, la probabilidad de que el estudiante aprenda la
habilidad en cada oportunidad de práctica
- P(G): Probabilidad de "guess" (adivinanza), probabilidad de responder correctamente sin
conocer la habilidad
- P(S): Probabilidad de "slip" (desliz), probabilidad de responder incorrectamente
conociendo la habilidad

### Formulación Matemática del BKT
El modelo BKT utiliza las siguientes ecuaciones para actualizar las creencias sobre el
estado de conocimiento:

22


Predicción de la respuesta correcta: Esta ecuación predice la probabilidad de que un
estudiante responda correctamente. Combina dos escenarios: (1) el estudiante conoce la
habilidad y no comete un desliz, y (2) el estudiante no conoce la habilidad, pero adivina
correctamente.
P(Correct) = P(L) × (1 − P(S)) + (1 − P(L)) × P(G)

Actualización bayesiana después de una respuesta correcta: Utiliza el teorema de
Bayes para actualizar la probabilidad de que el estudiante haya aprendido la habilidad, dado que
respondió correctamente. La evidencia positiva aumenta la confianza en el conocimiento del
estudiante.
P(L|Correct) = P(L) × (1 − P(S)) / [P(L) × (1 − P(S)) + (1 − P(L)) × P(G)]

Actualización bayesiana después de una respuesta incorrecta: Actualiza la
probabilidad de conocimiento cuando el estudiante responde incorrectamente. La evidencia
negativa generalmente reduce la confianza, pero considera la posibilidad de que el estudiante
conociera la habilidad, pero cometió un desliz.
P(L|Incorrect) = P(L) × P(S) / [P(L) × P(S) + (1 − P(L)) × (1 − P(G))]

Actualización por oportunidad de aprendizaje: Modela el aprendizaje que ocurre
durante cada oportunidad de práctica. Si el estudiante no había aprendido la habilidad, existe una
probabilidad P(T) de que la aprenda en esta iteración.
P(L𝑛 + 1) = P(L𝑛|Evidence) + (1 − P(L𝑛|Evidence)) × P(T)


23


### Proceso de Funcionamiento del BKT
El modelo BKT opera en un ciclo iterativo que consta de los siguientes pasos:
- Inicialización: Se establece P(L₀) como la probabilidad inicial de conocimiento
- Predicción: Se calcula la probabilidad de respuesta correcta usando la ecuación de
predicción
- Observación: Se registra la respuesta real del estudiante
- Actualización de evidencia: Se actualiza P(L) basándose en la respuesta observada
- Actualización de aprendizaje: Se incorpora la oportunidad de aprendizaje usando P(T)
- Iteración: Se repite el proceso para la siguiente pregunta

### Clasificación de Estudiantes Basada en Umbrales de Dominio
La literatura especializada en sistemas adaptativos de aprendizaje establece criterios
específicos para la clasificación de estudiantes basándose en los valores de probabilidad de
dominio estimados por BKT. Según las investigaciones de Corbett y Anderson (1995) y los
estándares adoptados en sistemas como ALEKS y Cognitive Tutors, se reconocen los siguientes
umbrales:
Estudiantes con Dominio Avanzado (P(L) ≥ 0.95) Los estudiantes que alcanzan una
probabilidad de dominio de 95% o superior se consideran que han logrado el dominio completo
del tema. Este umbral del 95% es ampliamente utilizado en sistemas de aprendizaje adaptativo
como estándar para declarar maestría (Doroudi, 2020; Slater & Baker, 2018). Estos estudiantes
requieren ejercicios de mayor complejidad y actividades de enriquecimiento para mantener su
motivación y continuar su crecimiento académico.

24


Estudiantes con Desempeño Intermedio (0.60 ≤ P(L) < 0.95) Los estudiantes en este
rango demuestran un conocimiento parcial pero aún no han alcanzado el dominio completo. Este
grupo se beneficia de la práctica adicional con ejercicios de dificultad estándar y
retroalimentación constructiva. La investigación en sistemas de tutoría inteligente sugiere que
este rango representa una zona de desarrollo próximo óptima para el aprendizaje (Pelánek &
Řihák, 2018).
Estudiantes con Dificultades de Aprendizaje (P(L) < 0.60) Los estudiantes con
probabilidades de dominio inferiores al 60% requieren intervención remedial y ejercicios
simplificados. Según las mejores prácticas en aprendizaje adaptativo, estos estudiantes se
benefician de estrategias de andamiaje, instrucción más detallada y ejercicios con mayor apoyo
(Guskey, 2010; Bloom, 1984).

### Ejemplo de Clasificación de Estudiantes con BKT
Para ilustrar el funcionamiento detallado del modelo BKT, consideremos el caso de un
estudiante trabajando en el tema "Operaciones con fracciones" con los siguientes parámetros del
modelo:
Parámetros establecidos:
- P(L₀) = 0.1 (probabilidad inicial de conocimiento)
- P(T) = 0.3 (probabilidad de transición/aprendizaje)
- P(G) = 0.25 (probabilidad de adivinanza)
- P(S) = 0.1 (probabilidad de desliz)
Secuencia de respuestas del estudiante:
[Incorrecta, Correcta, Correcta, Incorrecta, Correcta]

25


Iteración 1: Respuesta Incorrecta
Predicción inicial:
P(Correct₁) = P(L₀) × (1 - P(S)) + (1 - P(L₀)) × P(G)
P(Correct₁) = 0.1 × (1 - 0.1) + (1 - 0.1) × 0.25 = 0.09 + 0.225 = 0.315
Actualización después de respuesta incorrecta:
P(L₁|Incorrect) = P(L₀) × P(S) / [P(L₀) × P(S) + (1 - P(L₀)) × (1 - P(G))]
P(L₁|Incorrect) = 0.1 × 0.1 / [0.1 × 0.1 + 0.9 × 0.75] = 0.01 / 0.685 = 0.015
Actualización por oportunidad de aprendizaje:
P(L₁) = P(L₁|Incorrect) + (1 - P(L₁|Incorrect)) × P(T)
P(L₁) = 0.015 + (1 - 0.015) × 0.3 = 0.015 + 0.295 = 0.310

Iteración 2: Respuesta Correcta
Predicción:
P(Correct₂) = 0.310 × 0.9 + 0.690 × 0.25 = 0.279 + 0.173 = 0.452
Actualización después de respuesta correcta:
P(L₂|Correct) = 0.310 × 0.9 / 0.452 = 0.279 / 0.452 = 0.617
Actualización por oportunidad de aprendizaje:
P(L₂) = 0.617 + (1 - 0.617) × 0.3 = 0.617 + 0.115 = 0.732

Iteración 3: Respuesta Correcta
Predicción:
P(Correct₃) = 0.732 × 0.9 + 0.268 × 0.25 = 0.659 + 0.067 = 0.726


26


Actualización después de respuesta correcta:
P(L₃|Correct) = 0.732 × 0.9 / 0.726 = 0.659 / 0.726 = 0.908
Actualización por oportunidad de aprendizaje:
P(L₃) = 0.908 + (1 - 0.908) × 0.3 = 0.908 + 0.028 = 0.936

Resultado de la Clasificación: Después de tres iteraciones, el estudiante alcanza una
probabilidad de dominio P(L₃) = 0.936, lo que lo clasifica en la categoría de Desempeño
Intermedio (0.60 ≤ P(L) < 0.95).
Este ejemplo demuestra cómo el modelo BKT utiliza cada respuesta del estudiante para
actualizar dinámicamente su estimación del estado de conocimiento, proporcionando una base
cuantitativa sólida para las decisiones pedagógicas adaptativas.

## Algoritmo Expectation-Maximization (EM)
El algoritmo Expectation-Maximization, desarrollado por Dempster, Laird y Rubin
(1977), es un método iterativo para encontrar estimaciones de máxima verosimilitud de
parámetros en modelos estadísticos con variables latentes. En el contexto de BKT, las variables
latentes son los estados de conocimiento no observables de los estudiantes.
### Formulación Matemática del Algoritmo EM
El algoritmo EM maximiza la función de log-verosimilitud esperada:
Q(θ|θ(𝑡)) = E[log L(θ|X, Z)|X, θ(𝑡)]
Donde:
- θ representa los parámetros del modelo (P(T), P(G), P(S))
- X son las observaciones (respuestas de los estudiantes)

27


- Z son las variables latentes (estados de conocimiento)
- t es la iteración actual

### Proceso del Algoritmo EM
- Paso E (Expectation):
Se calcula la esperanza de la log-verosimilitud completa dados los parámetros actuales:
γ_i(j) = P(L_j = 1|respuestas, θ^(t))
- Paso M (Maximization):
Se actualizan los parámetros maximizando la función Q:
Para P(T):
P(T)(t+1) = Σᵢ Σⱼ γᵢ(j − 1)(1 − γᵢ(j − 1))γᵢ(j) / Σᵢ Σⱼ γᵢ(j − 1)(1 − γᵢ(j − 1))
Para P(G):
P(G)(t+1) = Σᵢ Σⱼ (1 − γᵢ(j))Cᵢⱼ / Σᵢ Σⱼ (1 − γᵢ(j))
Para P(S):
P(S)(t+1) = Σᵢ Σⱼ γᵢ(j)(1 − Cᵢⱼ) / Σᵢ Σⱼ γᵢ(j)

Donde Cᵢⱼ es 1 si la respuesta del estudiante i en la pregunta j es correcta, 0 en caso contrario.
### Aplicación del Algoritmo EM para Estimación de Parámetros BKT
La elección del algoritmo EM para estimar los parámetros del modelo BKT se justifica
por las siguientes razones:
- Variables latentes: Los estados de conocimiento de los estudiantes no son directamente
observables
- Máxima verosimilitud: Proporciona estimaciones estadísticamente robustas

28


- Convergencia garantizada: El algoritmo converge monotónicamente hacia un máximo
local
- Eficiencia computacional: Es computacionalmente eficiente para conjuntos de datos
grandes

Ejemplo de Aplicación: Consideremos un estudiante que responde a una secuencia de 5
preguntas sobre una habilidad específica:
Secuencia de respuestas: [Incorrecto, Correcto, Correcto, Incorrecto, Correcto]
Inicialización (t=0):
- P(L₀) = 0.1
- P(T)⁽⁰⁾ = 0.3
- P(G)⁽⁰⁾ = 0.2
- P(S)⁽⁰⁾ = 0.1

Iteración del Algoritmo EM:
- Paso E: Se calculan las probabilidades posteriores de conocimiento para cada
respuesta usando forward-backward algorithm:
Para la primera respuesta (Incorrecta):
P(L₁|Incorrect) = 0.1 × 0.1 / (0.1 × 0.1 + 0.9 × 0.8) = 0.014
- Paso M: Se actualizan los parámetros usando las fórmulas de maximización
presentadas anteriormente.
Este proceso se repite hasta convergencia, típicamente cuando la diferencia entre
iteraciones es menor a un umbral predefinido (ε = 0.001).

29


## GraphQL
Es un lenguaje de consulta y manipulación de datos desarrollado por Facebook en 2012 y
liberado como código abierto en 2015. A diferencia de las arquitecturas REST tradicionales,
GraphQL proporciona una alternativa más eficiente, potente y flexible para el desarrollo de
APIs, permitiendo a los clientes solicitar exactamente los datos que necesitan en una sola
consulta.
### Características Principales de GraphQL
Consultas Específicas y Eficientes: GraphQL permite a los clientes especificar
exactamente qué datos necesitan, evitando el problema de "over-fetching" (obtener más datos de
los necesarios) y "under-fetching" (obtener menos datos de los requeridos) común en las APIs
REST. Esto resulta especialmente beneficioso para aplicaciones móviles donde el ancho de
banda y la batería son recursos limitados.
Esquema Fuertemente Tipado: GraphQL utiliza un sistema de tipos robusto que define
claramente la estructura de los datos disponibles, proporcionando mejor documentación
automática, validación en tiempo de desarrollo y herramientas de introspección.
Subscripciones en Tiempo Real: A través de las subscripciones, GraphQL permite
actualizaciones en tiempo real, fundamentales para funcionalidades como notificaciones y
seguimiento en vivo del progreso estudiantil.

### Comparación con APIs REST
Múltiples Peticiones HTTP: En una arquitectura REST tradicional, para mostrar el
perfil completo de un estudiante (nivel, XP, monedas, logros, avatar personalizado), se
requerirían múltiples peticiones a diferentes endpoints:

30


- /api/students/{id}/profile
- /api/students/{id}/achievements
- /api/students/{id}/avatar
- /api/students/{id}/progress

Transferencia de Datos Innecesaria: REST devuelve estructuras de datos fijas, lo que
puede resultar en la transferencia de información no requerida para vistas específicas,
impactando negativamente en el rendimiento de la aplicación móvil.
Complejidad en Relaciones: La gestión de relaciones complejas entre estudiantes,
docentes, cursos y salas requiere lógica adicional del lado del cliente para ensamblar los datos
necesarios.

### Beneficios Específicos para el Desarrollo Móvil
Reducción de Latencia: Al consolidar múltiples consultas en una sola petición,
GraphQL reduce significativamente la latencia de red, crucial para la experiencia en dispositivos
móviles.
Optimización de Batería: Menos peticiones HTTP resultan en menor consumo de
batería, especialmente importante en una aplicación educativa que los estudiantes pueden usar
durante períodos extendidos.
Adaptabilidad a Diferentes Tamaños de Pantalla: GraphQL permite solicitar
diferentes niveles de detalle según el dispositivo, optimizando la experiencia tanto en tablets
como en smartphones.


31


# CAPITULO IV. PROCESO DE DESARROLLO SCRUM
## Sprint 2
## Sprint Planning
Objetivo del Sprint
Implementar funcionalidades de personalización para estudiantes, sistemas de
recompensa y herramientas de seguimiento para proporcionar información valiosa sobre el
progreso de los estudiantes a los docentes.
Contexto del Sistema



Ilustración 9. Diagrama de casos de uso

32


### Historias de Usuario
Historia de Usuario

ID Nombre HU Prioridad PHU Estado
HU02 Personalización de avatar Media 8 Completo
Como: Estudiante
Quiero: Cambiar el cabello, ropa, accesorios y más de mi avatar
Para: Identificarme de manera única en la plataforma
Criterios de
aceptación:
- El sistema debe ofrecer al menos 10 opciones diferentes para cada
categoría (cabello, ropa, accesorios)
- Los cambios deben guardarse automáticamente
- El avatar personalizado debe mostrarse en todas las áreas relevantes de
la plataforma
- La interfaz debe ser intuitiva y adaptada para niños de 5to y 6to de
primaria
Desarrollador: Eben Ezer Cayo Terrazas

Historia de Usuario

ID Nombre HU Prioridad PHU Estado
HU05 Sistema de recompensas Media 13 Completo
Como: Estudiante
Quiero: Canjear monedas virtuales, propias de la plataforma

33


Para: Adquirir elementos de personalización y ventajas
Criterios de
aceptación:
- El sistema debe mostrar claramente el saldo de monedas disponibles
- Debe existir una tienda virtual con al menos 10 elementos diferentes
para comprar
- Cada elemento debe tener un precio claro en monedas
- Debe existir una confirmación antes de realizar la compra
- Las compras deben reflejarse inmediatamente en el inventario del
estudiante
- Debe existir una categorización de elementos (personalización, ventajas,
etc.)
Desarrollador: Eben Ezer Cayo Terrazas

Historia de Usuario

ID Nombre HU Prioridad PHU Estado
HU06 Correcciones con IA Media 13 Completo
Como: Estudiante
Quiero: Consultar a un asistente virtual
Para: Resolver dudas respecto a mis fallas
Criterios de
aceptación:
- El asistente debe identificar correctamente al menos el 90% de los
errores comunes
- Las explicaciones deben ser adaptadas al nivel educativo (5to y 6to de
primaria)
- El asistente debe ofrecer ejemplos adicionales cuando sea necesario
- Las sugerencias deben estar alineadas con el currículo educativo
- Debe funcionar con los temas de todas las materias incluidas en la
plataforma
Desarrollador: Niels Roy Chambi Gonzales

34



Historia de Usuario

ID Nombre HU Prioridad PHU Estado
HU10 Seguimiento general Alta 8 Completo
Como: Docente
Quiero: Visualizar el progreso general de mis estudiantes
Para: Conocer el avance del grupo y tomar decisiones pedagógicas
Criterios de
aceptación:
- El dashboard debe mostrar métricas clave (participación, rendimiento,
tiempo dedicado)
- Debe permitir filtrar por fecha, materia y actividad
- Los datos deben poder exportarse en formatos estándar (PDF, Excel)
Desarrollador: Niels Roy Chambi Gonzales

### Sprint Backlog
### Sprint Backlog
Objetivo del Sprint:
Implementar funcionalidades de personalización para estudiantes, sistemas de recompensa y
herramientas de seguimiento para proporcionar información valiosa sobre el progreso de los
estudiantes a los docentes.
Sprint número: 2 Tiempo programado: 20 días
Fecha de inicio: 17/04/2025 Fecha de finalización: 14/05/2025
ID Tarea Estimación Responsable Estado
1 Desarrollar HU02 8 hr Eben Cayo Completo
2 Desarrollar HU05 13 hr Eben Cayo Completo

35


3 Desarrollar HU06 13 hr Niels Chambi Completo
4 Desarrollar HU10 8 hr Niels Chambi Completo

### Patrón de Desarrollo
### Diseño de la Arquitectura
Arquitectura Física


Ilustración 10. Diagrama de Despliegue

36


Arquitectura Lógica

Ilustración 11. Diagrama de Paquetes Organizado en Capas



37


### Diseño de Datos
Diseño Lógico

Ilustración 12. Diagrama de clases de la base de datos



38


## Sprint Review
Revisión del Sprint 2
Nombre del proyecto:
Plataforma educativa de cursos gamificados dedicado al
nivel de educación primario para el colegio particular
mixto “Los Ángeles”
Numero de revisión: 2
Objetivo de la revisión:
- Verificar la culminación de las tareas
- Realizar pruebas unitarias
- Comprobar que el objetivo del sprint fue completado
Lugar: Santa Cruz de la Sierra Fecha: 14/05/2025 Hora: 20:30
Participantes
Nombre Rol
Eben Ezer Cayo Terrazas Product Owner
Niels Roy Chambi Gonzales Scrum Master
Presentación del Incremento
Función Presentada Retroalimentación
Personalizar avatar
La carga de las opciones de
personalización podría optimizarse
para dispositivos de menor capacidad
Sistema de recompensas Considerar implementar ofertas
especiales o descuentos temporales
Correcciones con IA
Considerar un sistema de
retroalimentación para mejorar las
respuestas
Seguimiento general Agregar más opciones de
visualización (gráficos, tendencias)
Tareas completadas
Tarea Estado

39


Desarrollar HU02 Terminado
Desarrollar HU05 Terminado
Desarrollar HU06 Terminado
Desarrollar HU10 Terminado
Para lo que viene
Registro masivo de estudiantes: Implementar una opción para registrar muchos estudiantes en un
curso/sala mediante un archivo Excel.
Inicio de sesión por huella dactilar: Simplificar el ingreso a la aplicación móvil.

## Sprint Retrospective
Retrospectiva del Sprint 2
Sprint número: 2 Fecha: 15/05/2025
Asistentes:
- Eben Ezer Cayo Terrazas
- Niels Roy Chambi Gonzales
Discusión
¿Qué salió bien?
Se logró integrar exitosamente tecnologías complejas (IA, gamificación)
La comunicación entre los desarrolladores fue fluida y efectiva
¿Qué no salió bien?
Retraso considerable en la implementación del sistema de recompensas
en relación con la personalización del avatar debido a que esta última
funcionalidad fue implementada mediante una librería.
¿Qué deberíamos
cambiar?
Asignación de tareas sin retrasos
Realizar pruebas de funcionamiento





40


## Bibliografía
- Baker, R. S. J. d., & Yacef, K. (2009). The state of educational data mining in 2009: A
review and future visions. Journal of Educational Data Mining, 1(1), 3–17.
- Caponetto, I., Earp, J., & Ott, M. (2014). Gamification and education: A literature
review. In European Conference on Games Based Learning (Vol. 1, p. 50). Academic
Conferences International Limited.
- Deterding, S., Dixon, D., Khaled, R., & Nacke, L. (2011). From game design elements to
gamefulness: Defining "gamification". In Proceedings of the 15th International Academic
MindTrek Conference: Envisioning Future Media Environments (pp. 9–15).
- Domínguez, A., Saenz-de-Navarrete, J., de-Marcos, L., Fernández-Sanz, L., Pagés, C., &
Martínez-Herráiz, J.-J. (2013). Gamifying learning experiences: Practical implications
and outcomes. Computers & Education, 63, 380–392.
- Rabahallah, M., & Ouadfel, S. (2020). Adaptive learning based on the learner’s
motivation and cognitive profile in a gamified environment. Education and Information
Technologies, 25(6), 5521–5546.
- J.R. Quinlan. C4. 5: programs for machine learning. Morgan Kaufmann, 1993.
- T. Hastie, R. Tibshirani and J. Friedman. Elements of Statistical Learning, Springer,
2009.
- Bloom, B. S. (1984). The 2 sigma problem: The search for methods of group instruction
as effective as one-to-one tutoring. Educational researcher, 13(6), 4-16.
- Corbett, A. T., & Anderson, J. R. (1994). Knowledge tracing: Modeling the acquisition of
procedural knowledge. User Modeling and User-Adapted Interaction, 4(4), 253-278.

41


- Corbett, A. T., & Anderson, J. R. (1995). Knowledge tracing: Modeling the acquisition of
procedural knowledge. User Modeling and User-Adapted Interaction, 4(4), 253-278.
- Dempster, A. P., Laird, N. M., & Rubin, D. B. (1977). Maximum likelihood from
incomplete data via the EM algorithm. Journal of the Royal Statistical Society: Series B
(Methodological), 39(1), 1-22.
- Doroudi, S. (2020). The bias-variance tradeoff: How data science can inform educational
debates. AERA Open, 6(4), 2332858420977208.
- Doroudi, S., Aleven, V., & Brunskill, E. (2015). Where's the reward? A review of
reinforcement learning for instructional sequencing. International Journal of Artificial
Intelligence in Education, 29(4), 568-620.
- Guskey, T. R. (2010). Lessons of mastery learning. Educational Leadership, 68(2), 52-57.
- Kulik, C. L. C., Kulik, J. A., & Bangert-Drowns, R. L. (1990). Effectiveness of mastery
learning programs: A meta-analysis. Review of educational research, 60(2), 265-299.
- Pelánek, R., & Řihák, J. (2018). Analysis and design of mastery learning criteria. In
International Conference on Artificial Intelligence in Education (pp. 278-291). Springer.
- Slater, S., & Baker, R. (2018). Mastery learning heuristics and their hidden models. In
International Conference on Artificial Intelligence in Education (pp. 494-498). Springer.
- Beck, J. E., & Chang, K. M. (2007). Identifiability: A fundamental problem of student
modeling. In User Modeling 2007 (pp. 137-146). Springer.
- Yudelson, M. V., Koedinger, K. R., & Gordon, G. J. (2013). Individualized bayesian
knowledge tracing models. In International conference on artificial intelligence in
education (pp. 171-180). Springer.

42


- Piech, C., Bassen, J., Huang, J., Ganguli, S., Sahami, M., Guibas, L. J., & Sohl-Dickstein,
J. (2015). Deep knowledge tracing. In Advances in neural information processing
systems (pp. 505-513).
- Van de Sande, B. (2013). Properties of the Bayesian Knowledge Tracing Model. Journal
of Educational Data Mining, 5(2), 1-10.
- Csikszentmihalyi, M. (1997). Fluir (Flow). Una psicología de la felicidad. Barcelona:
Kairos.
- Deci, E. L., & Ryan, R. M. (2000). La Teoría de la Autodeterminación y la Facilitación
de la Motivación Intrínseca, el Desarrollo Social y el Bienestar. American Psychologist,
55(1), 68-78.
- Garris, R., Ahlers, R., & Driskell, J. E. (2002). Games, motivation, and learning: A
research and practice model. Simulation & Gaming, 33(4), 441-467.
- Kapp, K. M. (2012). The Gamification of learning and instruction: Game-based methods
and strategies for training and education. San Francisco: John Wiley & Sons Inc.
- Scott, B., & Neustaedter, C. (2013). Analysis of gamification in education. Technical
Report, Surrey, BC, Canada: Simon Fraser University.
- Werbach, K., & Hunter, D. (2012). For the win: How game thinking can revolutionize
your business. Philadelphia: Wharton Digital Press.
- Werbach, K., & Hunter, D. (2014). Gamificación: revoluciona tu negocio con las
técnicas de los juegos. Madrid: Pearson Educación.



43


## Anexos
Anexo A. Sprint 0
Definiciones Iniciales
Definición del Equipo Scrum
Persona Rol Descripción
Eben Ezer Cayo Terrazas Product Owner Es el responsable de maximizar el valor del
producto y de los desarrolladores.
Niels Roy Chambi Gonzales Scrum Master
Es el responsable de ayudar a entender al
equipo la metodología scrum, esto implica
eliminar obstáculos que puedan afectar el
proceso del equipo.
Eben Ezer Cayo Terrazas
Niels Roy Chambi Gonzales
Developers
Encargados de trabajar en el incremento de
cada sprint creando productos que cumplan
con los criterios acordados

Objetivo del Producto
El objetivo del software es que se convierta en una herramienta que, mediante la
implementación de características comunes entre los videojuegos, incentive el interés por el
aprendizaje en los estudiantes.

Definición de la Duración de los Sprints
Sprint Inicio Fin Duración
0 06/03/2025 19/03/205 14 días
1 20/03/2025 16/04/2025 28 días
2 17/04/2025 14/05/2025 28 dias
3 15/05/2025 11/06/2025 28 días


44


Product Backlog
Product Backlog
Proyecto Plataforma educativa de cursos gamificados dedicado al nivel de
educación primario para el colegio particular mixto “Los Ángeles”
Product Owner Eben Ezer Cayo Terrazas
Versión: 1.0 Fecha: 01/04/2025
ID Nombre Descripción Prioridad
HU01 Perfil de estudiante
Como estudiante quiero visualizar mi
nivel actual, puntos XP, monedas
acumuladas, logros y más, para conocer
mi progreso en general
Alta
HU02 Personalizar avatar
Como estudiante quiero cambiar el
cabello, ropa, accesorios, y más, de mi
avatar, para identificarme de manera
única.
Media
HU03 Lecciones entretenidas
Como estudiante quiero acceder a
lecciones con contenido multimedia
para comprender mejor los conceptos.
Media
HU04 Practicas interactivas
Como estudiante quiero realizar
ejercicios interactivos y dinámicos para
practicar lo aprendido.
Alta
HU05 Sistema de recompensas
Como estudiante quiero canjear
monedas virtuales para adquirir
elementos de personalización y
ventajas.
Media
HU06 Correcciones con IA
Como estudiante quiero consultar a un
asistente virtual para resolver dudas
respecto a mis fallas.
Media
HU07 Aprendizaje Adaptativo
Como estudiante quiero que el juego se
adapte a mi capacidad según mi avance
para lograr un mejor interés y
rendimiento en el aprendizaje
Alta
HU08 Alertas de seguimiento
Como docente quiero recibir alertas
sobre estudiantes con dificultades para
brindar apoyo oportuno.
Media

45


HU09 Gestionar cursos/salas
Como docente quiero crear salas para
cada curso en el que enseñe para invitar
a los estudiantes a unirse
Alta
HU10 Seguimiento general
Como docente quiero visualizar el
progreso general de mis estudiantes
para conocer el avance del grupo
Alta
HU11 Seguimiento personal
Como docente, quiero acceder al perfil
detallado de cada estudiante para
analizar su desempeño individual.
Media
HU12 Competencias por curso
Como docente, quiero programar
competencias y desafíos grupales para
fomentar la participación y motivación.
Media

Anexo B. Sprint 1
## Sprint Planning
Objetivo del Sprint.
Establecer la infraestructura básica del sistema e implementar las funcionalidades
principales necesarias del software.

Contexto del Sistema


46


### Historias de Usuario
Historia de Usuario

ID Nombre HU Prioridad PHU Estado
HU01 Perfil de estudiante Alta 3 Completo
Como: Estudiante
Quiero: Visualizar mi nivel actual, puntos xp, monedas acumuladas, logros y más
Para: Conocer mi progreso en general
Criterios de
aceptación:
- Mostrar barra de progreso de XP hacia el siguiente nivel
- Indicar nivel actual con número y/o rango (ej: "Explorador Nivel 5")
- Contador visible de monedas virtuales disponibles
- Galería visual de insignias obtenidas y bloqueadas
- Información sobre cómo desbloquear insignias pendientes
- Categorización de logros (académicos, participación, constancia)
Desarrollador: Eben Ezer Cayo Terrazas

Historia de Usuario

ID Nombre HU Prioridad PHU Estado
HU09 Gestionar cursos/salas Alta 5 Completo
Como: Docente
Quiero: Gestionar salas para cada curso en el que enseñe

47



Historia de Usuario

ID Nombre HU Prioridad PHU Estado
HU04 Practicas interactivas Alta 5 Completo
Como: Estudiante
Quiero: Realizar ejercicios interactivos y dinámicos
Para: Practicar lo aprendido
Criterios de
aceptación:
- Variedad de formatos (mini juegos, arrastrar y soltar, completar, etc.)
- Retroalimentación inmediata tras cada respuesta
- Incremento gradual de dificultad
- Pistas disponibles en caso de dificultad
- Límite de intentos configurado por tipo de ejercicio
Desarrollador: Eben Ezer Cayo Terrazas



Para: Invitar a estudiantes a unirse
Criterios de
aceptación:
- El docente podra crear un nuevo curso o sala
- Deberá colocar un nombre y la/las materias que quiera asignar
- Una vez creado tendrá la posibilidad de invitar a sus alumnos a unirse al
curso por medio de un código o QR
- Los estudiantes deberán acceder al curso para participar de las
actividades
Desarrollador: Niels Roy Chambi Gonzales

48


Historia de Usuario

ID Nombre HU Prioridad PHU Estado
HU03 Lecciones entretenidas Media 5 Completo
Como: Estudiante
Quiero: Acceder a lecciones con contenido multimedia más allá de solo texto
Para: Comprender mejor los conceptos
Criterios de
aceptación:
- Presentación visual atractiva de cada materia
- Indicador de progreso general por materia
- Presentación del contenido teórico en formatos diversos (texto, imagen,
video)
- Integración del contenido con la narrativa gamificada
- Controles de reproducción para contenido audiovisual
Desarrollador: Niels Roy Chambi Gonzales

### Sprint Backlog
### Sprint Backlog
Objetivo del Sprint:
Establecer la infraestructura básica del sistema e implementar las funcionalidades principales
necesarias del software.
Sprint número: 1 Tiempo programado: 20 días
Fecha de inicio: 20/03/2025 Fecha de finalización: 16/04/2025
ID Tarea Estimación Responsable Estado
1 Diseñar la arquitectura 3 hr Niels Chambi Completo
2 Diseñar la base de datos 3 hr Niels Chambi Completo

49


3 Instalar y configurar framework Flutter 30 min Eben Cayo Completo
4 Implementar gestión de usuarios 2 hr Eben Cayo Completo
5 Desarrollar HU01 3 hr Eben Cayo Completo
6 Desarrollar HU04 5 hr Eben Cayo Completo
7 Desarrollar HU03 5 hr Niels Chambi Completo
7 Desarrollar HU09 5 hr Niels Chambi Completo


### Patrón de Desarrollo
### Diseño de la Arquitectura
Arquitectura Física


50


Arquitectura Lógica








51


### Diseño de Datos
Diseño Lógico







52


## Sprint Review
Revisión del Sprint 1
Nombre del proyecto:
Plataforma educativa de cursos gamificados dedicado al
nivel de educación primario para el colegio particular
mixto “Los Ángeles”
Numero de revisión: 1
Objetivo de la revisión:
- Verificar la culminación de las tareas
- Realizar pruebas unitarias
- Comprobar que el objetivo del sprint fue completado
Lugar: Santa Cruz de la Sierra Fecha: 16/04/2025 Hora: 20:30
Participantes
Nombre Rol
Eben Ezer Cayo Terrazas Product Owner
Niels Roy Chambi Gonzales Scrum Master
Presentación del Incremento
Función Presentada Retroalimentación
Perfil de estudiante
Gestionar cursos/salas
Mejorar el método de invitación a
salas, mediante códigos temporales
de 4 caracteres por términos de
seguridad.
Practicas interactivas Implementar más practicas respecto a
otros temas y materias.
Lecciones entretenidas Implementar más lecciones respecto
a otros temas y materias.
Tareas completadas
Tarea Estado
Diseñar la base de datos Terminado

53


Instalar y configurar framework Flutter Terminado
Implementar gestión de usuarios Terminado
Desarrollar HU01 Terminado
Desarrollar HU03 Terminado
Desarrollar HU04 Terminado
Desarrollar HU09 Terminado
Para lo que viene
Registro masivo de estudiantes: Implementar una opción para registrar muchos estudiantes en un
curso/sala mediante un archivo Excel.
Inicio de sesión por huella dactilar: Simplificar el ingreso a la aplicación móvil.

Sprint Restrospective
Retrospectiva del Sprint 1
Sprint número: 1 Fecha: 17/04/2025
Asistentes:
- Eben Ezer Cayo Terrazas
- Niels Roy Chambi Gonzales
Discusión
¿Qué salió bien?
Se completaron las tareas designadas
Se implemento las bases para el proyecto con sus funcionalidades
principales
¿Qué no salió bien?
Integración del front móvil con el back al usar graphql, se solucionó
investigando sobre el tema y con la ayuda de la IA
Problemas en la compatibilidad de las versiones, se resolvieron
descargando la última versión de Flutter y actualizando los paquetes.
¿Qué deberíamos
cambiar?
Asignación de tareas sin retrasos
Revisión de cada tarea al culminar
Realizar pruebas de funcionamiento


54


Anexo C. Esquemas gráficos: Situación problemática y situación deseada










35%
51%
14%
Tiempo dedicado al estudio fuera de clases
30 minutos 1 hora 2 horas
55%38%
7%
Tiempo dedicado al estudio fuera de clases
30 minutos 1 hora 2 horas
Ilustración 13. Gráfico de la Situación Problemática
Ilustración 14. Gráfico de la Situación Deseada

55


Anexo D. Carta caso de estudio

56


Anexo E. Diapositivas




57







58







59








60







61







62







63








64







65







66







67





