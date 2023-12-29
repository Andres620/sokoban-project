# SISTEMAS INTELIGENTES 1

El juego de Sokoban es un rompecabezas clásico y desafiante que se originó en
Japón en la década de 1980. En Sokoban, los jugadores controlan a un personaje
(a menudo representado como un operario) que debe mover cajas en un almacén
o un laberinto hacia ubicaciones específicas. El juego se desarrolla en un tablero
cuadriculado donde cada celda puede estar vacía, contener una pared, una caja o
una ubicación de destino.

El objetivo del juego de Sokoban es empujar todas las cajas hacia las ubicaciones
de destino en el tablero, una vez que todas las cajas estén en su lugar, el jugador
ha completado el nivel.

Reglas Básicas:

Las reglas principales del juego de Sokoban son las siguientes:

1. El jugador puede mover al personaje una casilla a la vez en las cuatro
    direcciones cardinales (arriba, abajo, izquierda y derecha).
2. El jugador puede empujar una caja si está al lado de ella y hay una casilla
    vacía en la dirección en la que se desea empujar la caja.
3. No se puede empujar más de una caja a la vez, y no se pueden empujar las
    cajas a través de las paredes o ubicaciones de destino.
4. El jugador puede retroceder moviendo al personaje en la dirección opuesta
    a su último movimiento.

Para el presente proyecto, será una inteligencia artificial quien se encargará de
manipular los operarios que de ahora en adelante se denominarán robots, cada uno
de estos son agentes que se desenvolverán en el modelo (laberinto) para conseguir
el objetivo del juego.

Este es un juego que se desarrolla en un denominado “mundo grilla” en el cual se
compone de una cuadrícula de n*m (donde n puede ser diferente de m) y cada
espacio puede tener 3 estados posibles: camino “C”, rocas “R”, meta “M”. Es de
aclarar que los robots solo se pueden desplazar por las cuadrillas tipo camino.

Para este proyecto pueden varias cajas (que se identificarán con la letra “b”) y por
cada una de ellas un robot (que se identificarán con la letra “a”). Los robots
transportarán las cajas que se asignen en la carga del mapa correspondiente.

![imagen 1](/ruta/a/la/image1.jpg)

Representación Mapa Mapa real
El mundo se debe poder cargar desde un archivo plano, el cual es representado en
una cadena de texto, el cual representa la configuración del mapa y la ubicación de
las cajas y robots. Para esto es necesario tener en cuenta las anotaciones: <br>

Camino -> C <br>
Roca -> R <br>
Meta ->  M <br>
Robot -> a <br>
Caja -> b <br>

R, R, R, R, R, <br>
R, C-a, C, C, R, <br>
R, C, C-b-1, C, R, <br>
R, R, R, C, R, <br>
R, M, C-b-2, C, R, <br>
R, C-a-2, C, M, R, <br>
R, R, R, R, R, <br>

La cadena “C-a” significa que esa cuadricula es un camino que contiene a un
agente. A su vez la cadena “C-b” significa que esa cuadricula es un camino que
contiene una caja.

En esta primera entrega se debe permitir la carga del mapa.
Dentro del proyecto debe existir un menú en el cual se permita seleccionar el tipo
de algoritmo a aplicar ya sea por búsqueda no informada o informada. Los
algoritmos de búsqueda tendrán como inicio la posición del robot y como destino la
meta. Se garantiza que para esta entrega solo existirá un robot y una meta.

Específicamente los algoritmos son:

1. Búsqueda No informada:
    a. Anchura
    b. Profundidad
    c. Costo Uniforme
2. Búsqueda informada
    a. Beam Search
    b. Hill climbing
    c. A estrella

Nota 1: Para las búsquedas informadas se debe permitir seleccionar la heurística
de Manhattan o Euclidiana.

Nota 2: Debe garantizar la siguiente prioridad al momento de expandir.
Primero a la izquierda, arriba, derecha y abajo.

Una vez se seleccione el algoritmo, en el mapa se debe de mostrar el orden de los
nodos como se expandieron para dar tal solución. Ejemplo búsqueda en anchura.

![imagen 2](/ruta/a/la/image2.jpg)

Segunda entrega
En esta entrega los agentes deberán resolver el problema de llevar las cajas al
destino, para esto es necesario programar el árbol de búsqueda que resuelve el
juego. Se debe realizar por anchura (búsqueda no informada) y con los algoritmos
de Hill climbing y beam search (búsqueda informada), la heurística es de la libre
elección. Aquí se debe aplicar la prioridad de mover primero a la caja que esté mas
hacia la izquierda, y para cada una de ellas aplicar la prioridad: abajo, arriba,
izquierda y derecha.

Los estados de juego se deben guardar en archivos de texto plano con la notación
mencionada en la carga. Esto quiere decir que por cada nodo de juego se debe
guardar la configuración del mapa y de los demás visitados. Ejemplo: Búsqueda en
anchura

Archivo de texto: Búsqueda en anchura

![imagen 3](/ruta/a/la/image3.jpg)

Luego de encontrar el camino para cada una de las cajas, evitando atascos, se debe
programar la lógica del robot para que lleve la caja al destino, teniendo especial
cuidado con no interferir en la ruta de otro robot.

Para tener una idea general del juego se puede ver el siguiente video:
https://youtu.be/5fdVSfprZ54?si=Oam4X58fD7rx96Yr
