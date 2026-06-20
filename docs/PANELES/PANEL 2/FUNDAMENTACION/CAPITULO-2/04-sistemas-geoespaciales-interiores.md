## 2.3 Sistemas de Información Geoespacial para Interiores

Los sistemas de posicionamiento en interiores, conocidos como *Indoor Positioning Systems* (IPS, sistemas de posicionamiento en interiores), surgieron para suplir la pérdida de precisión del GPS en ambientes cerrados. Las cubiertas, muros y elementos estructurales atenúan o bloquean la señal satelital, por lo que el posicionamiento absoluto deja de ser confiable dentro de edificios. En ese contexto se recurre a alternativas basadas en coordenadas relativas, sensores inerciales, triangulación por radio, *fingerprinting* (huellas de señal) o marcación manual sobre un plano digital.

Para aplicaciones de survey WiFi, el plano de planta cumple el papel de sistema de referencia local. En lugar de coordenadas geográficas globales, el software trabaja con una superficie bidimensional donde cada punto se expresa mediante coordenadas relativas sobre la imagen del edificio. Esa decisión simplifica la captura en campo y evita depender de infraestructura adicional. No obstante, obliga a calibrar la escala con rigor para que un desplazamiento en píxeles represente una distancia física consistente.

La digitalización de planos puede partir de formatos raster, como PNG o JPG, o de formatos vectoriales, como PDF o SVG. Los primeros almacenan la imagen como malla de píxeles y son sencillos de renderizar en clientes móviles. Los segundos preservan trazos geométricos y pueden escalar sin pérdida, aunque requieren procesamiento adicional para su visualización homogénea. En Wireless HeatMapper se admite la importación de PNG, JPG y PDF, con renderizado de la primera página a imagen utilizable dentro del editor de planos.

El factor de escala se calcula como la razón entre la distancia real medida y la distancia observada en el plano digital. Si dos puntos separados 100 píxeles equivalen a 10 metros reales, entonces la escala es de 0.1 metros por píxel. A partir de ese valor, cualquier medición posterior puede convertirse desde la superficie digital a una magnitud física interpretable. Esa operación resulta central para la georreferenciación de muestras, ya que cada punto (x, y) marcado sobre el plano adquiere significado espacial dentro del edificio.

En el proyecto, la calibración definida en PB-11 establece esa relación métrica, mientras que PB-04 reutiliza el plano calibrado para registrar puntos de medición en coordenadas consistentes. La decisión de usar marcación manual sobre plano responde al contexto operativo: no requiere infraestructura de balizas, funciona con recursos disponibles en campo y deja evidencia visual inmediata del recorrido realizado.

**Tabla 13.** Comparativa de métodos de posicionamiento en interiores aplicables a levantamientos WiFi

| Método | Principio operativo | Ventajas | Limitaciones | Aplicación en el proyecto |
| ------ | ------------------- | -------- | ------------ | ------------------------- |
| Triangulación | Estima posición a partir de distancias o ángulos respecto a múltiples emisores | Puede automatizar ubicación | Requiere geometría controlada y referencias adicionales | No se adopta como mecanismo principal |
| *Fingerprinting* | Compara patrones de señal observados con una base histórica del entorno | Buena precisión en ambientes estables | Exige entrenamiento previo y mantenimiento del mapa de huellas | Se considera insumo analítico futuro, no para captura base |
| *Dead reckoning* | Integra acelerómetro, giroscopio y rumbo para estimar desplazamiento | Funciona sin infraestructura externa | Acumula error con rapidez en recorridos largos | No es suficiente para la precisión requerida |
| Marcación manual sobre plano | El técnico selecciona el punto exacto sobre el plano digital calibrado | Simple, controlable y alineado al flujo de survey | Depende de disciplina operativa del técnico | Método adoptado en PB-04 |

### Referencias

Li, B., Gallagher, T., Dempster, A. G., & Rizos, C. (2012). How feasible is the use of magnetic field alone for indoor positioning? *2012 International Conference on Indoor Positioning and Indoor Navigation*, 1–9. https://doi.org/10.1109/IPIN.2012.6418880

OGC. (2019). *IndoorGML 1.1*. Open Geospatial Consortium. https://www.ogc.org/standards/indoorgml

Zlatanova, S., Sithole, G., Nakagawa, M., & Zhu, Q. (2013). Problems in indoor mapping and modelling. *ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, II-4/W1*, 63–68. https://doi.org/10.5194/isprsannals-II-4-W1-63-2013

---
