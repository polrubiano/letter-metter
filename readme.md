# Analizador Ergonómico: Eye Sense vs. QWERTY

Herramienta de validación clínica y ergonómica en Python diseñada para medir y comparar objetivamente la eficiencia física entre un teclado tradicional (QWERTY) y el teclado optimizado **Eye Sense**.

## Propósito General

El objetivo principal de este script es calcular la distancia que un usuario debe recorrer para escribir un texto determinado. 
Basándose en la velocidad de movimiento del ojo del usuario, el script extrapola la mejora en su velocidad de escritura y el tiempo físico ahorrado.
Hay que tener en cuenta no obstante, que los cálculos se hacen con base en un "escenario ideal", es decir, el usuario va de letra a letra en una diagonal perfecta, no pierde tiempo buscando la letra que desea... pero aun así nos sirve como herramienta teórica de medición, ya que podemos introducir la velocidad real de pulsaciones de teclas por minuto del usuario.

## Estructura del Código

El script está dividido en varios bloques lógicos para facilitar su comprensión y mantenimiento:

### 1. Diccionarios de Coordenadas (`eye_sense_coords` y `qwerty_coords`)
Actúan como el mapa físico de los teclados. Asignan a cada letra una coordenada espacial `(X, Y)` en milímetros. El teclado QWERTY incluye el desplazamiento real escalonado (*staggered*) de las teclas para garantizar una precisión absoluta en la comparativa física con la cuadrícula de Eye Sense. Se podría hacer cualquier diseño de teclado respetando las siguientes premisas:

- Las teclas deben estar definidas en un área de 10 x 10 mm.
- El inicio de las coordenadas (0,0) debe estar en la esquina superior izquierda.

Con esto en mente paso a mostrar un ejemplo con el teclado QWERTY realizado en un programa de diseño gráfico estándar, muy útil debido a las herramientas que proporciona.

![qwerty_01.png](resources%2Fqwerty_01.png)

- En el círculo verde se muestra el punto de inicio de la medición (coordenadas (0,0))
- Con la flecha estoy indicando qué parte de la figura seleccionada (en el caso de la imagen, el cuadrado superior izquierdo) quiero tomar como punto de referencia (en este caso, el centro de la figura).
- Con el círculo rojo se muestra las coordenadas del punto seleccionado; en este caso, x = 5 e y = 5 (recordemos que la tecla mide 10 x 10 mm, cuadrado azul).

![qwerty_02.png](resources%2Fqwerty_02.png)

Si seleccionamos una tecla distinta, podemos ver como los puntos de coordenadas cambian en relación con la nueva figura haciendo muy fácil crear tablas con las coordenadas de las teclas de nuestro diseño de teclado y añadirlas como una variable para su medición con el script.

![eyesense_01.png](resources%2Feyesense_01.png)

![eyesense_02.png](resources%2Feyesense_02.png)

### 2. Factor de Escala (Scaling Factor)
Permite adaptar el cálculo matemático a prototipos físicos reales sin necesidad de modificar el diccionario de coordenadas. 
* Si imprimes un prototipo cuyas teclas son un 50% más grandes que el diseño original (10 mm -> 15 mm), simplemente ajustas el multiplicador a `1.5`. 
* Las variables `eye_sense_scale` y `qwerty_scale` operan de forma independiente, permitiendo cruzar mediciones de teclados de diferentes tamaños.

#### teclado qwerty
| **letra** | **x** | **y** |
| :----------: | :----------: | :----------: |
| q | 5  | 5 |
| w | 15 | 5 |
| e | 25 | 5 |
| r | 35 | 5 |
| t | 45 | 5 |
| y | 55 | 5 |
| u | 65 | 5 |
| i | 75 | 5 |
| o | 85 | 5 |
| p | 95 | 5 |
| | | |
| a | 8  | 15 |
| s | 18 | 15 |
| d | 28 | 15 |
| f | 38 | 15 |
| g | 48 | 15 |
| h | 58 | 15 |
| j | 68 | 15 |
| k | 78 | 15 |
| l | 88 | 15 |
| ñ | 98 | 15 |
| | | |
| z | 13 | 25 |
| x | 23 | 25 |
| c | 33 | 25 |
| v | 43 | 25 |
| b | 53 | 25 |
| n | 63 | 25 |
| m | 73 | 25 |

#### teclado eye sense
| **letra** | **x** | **y** |
| :----------: | :----------: | :----------: |
| k | 4.7 | 5 |
| f | 14.5 | 5 |
| m | 24.3 | 5 |
| t | 34.1 | 5 |
| b | 43.9 | 5 |
| q | 53.7 | 5 |
| | | |
| z | 9.6 | 13.5 |
| i | 19.4 | 13.5 |
| d | 29.2 | 13.5 |
| s | 39 | 13.5 |
| u | 48.8 | 13.5 |
| j | 58.7 | 13.5 |
| | | |
| ñ | 4.7 | 22 |
| l | 14.5 | 22 |
| a | 24.3 | 22 |
| e | 34.1 | 22 |
| o | 43.9 | 22 |
| g | 53.7 | 22 |
| x | 63.6 | 22 |
| | | |
| h | 9.6 | 30.5 |
| c | 19.4 | 30.5 |
| r | 29.2 | 30.5 |
| n | 39 | 30.5 |
| p | 48.8 | 30.5 |
| w | 58.7 | 30.5 |
| | | |
| y | 24.3 | 39 |
| v | 43.9 | 39 |


### 2. Funciones de Preparación y Formateo
* **`clean_text(text)`**: Prepara el texto ingresado. Convierte todo a minúsculas y sustituye las vocales acentuadas por vocales simples (respetando la 'ñ'). Las teclas de función (como intro, espacio y signos de puntuación), no son tenidas en cuenta durante este proceso debido a que su uso en el entorno de la aplicación Eye Sense (por parte de usuarios con movilidad reducida y el uso de la Inteligencia Artificial para reducir al mínimo las interacciones del usuario con el teclado) no tiene demasiada relevancia. 

* **`format_distance(distance_mm)` y `format_time(seconds)`**: Hacen que los resultados sean comprensibles. Si la distancia supera los 1000 mm, la muestra automáticamente en metros (m). Si el tiempo supera los 60 segundos, lo formatea en minutos y segundos.

### 3. Motor Matemático
* **`calculate_distance(text, keyboard)`**: Es el núcleo del cálculo. Utiliza el Teorema de Pitágoras (distancia euclidiana) para medir la línea recta exacta entre el centro de una tecla y la siguiente de forma consecutiva. Devuelve la distancia total acumulada y el número exacto de teclas válidas pulsadas.

### 4. Lógica de Análisis y Extrapolación
* **`process_file(path, current_kpm)`**: Es la función principal que orquesta el análisis y calcula el beneficio clínico del teclado:
    1. **Lectura:** Extrae el contenido del archivo `.txt` suministrado.
    2. **Cálculo de Distancia:** Obtiene los milímetros totales que requiere el texto en ambos teclados.
    3. **Deducción de Velocidad Física:** Toma los *Keystrokes Per Minute* (KPM) actuales del usuario en QWERTY y calcula a qué velocidad real (mm/s) se mueve físicamente.
    4. **Predicción en Eye Sense:** Aplica esa misma velocidad física al recorrido en el teclado de Eye Sense para predecir matemáticamente cuál será su nueva velocidad de escritura (nuevos KPM) y cuánto tiempo de fatiga se ahorrará.

## 🚀 Instrucciones de Uso

1. Crea un archivo llamado `texto.txt` en el mismo directorio que el script y pega dentro el texto que deseas analizar. (Asegúrate de que esté guardado con codificación UTF-8).
2. Abre el script de Python y dirígete a la última línea.
3. Modifica la variable `user_current_kpm` con las pulsaciones por minuto que el usuario logra actualmente en un teclado tradicional:
   ```python
   user_current_kpm = 15 # Cambia este valor por las KPM reales del usuario