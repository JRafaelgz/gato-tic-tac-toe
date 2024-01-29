"""
Agente jugador de gato usando minimax
Autor: JRafaelgz

Código basado en: 
Algoritmo Minimax y poda Alfa-Beta
Autor: jpiramirez https://github.com/jpiramirez

Curso IA, UG
"""
import math
import numpy as np 

class TicTacToeGame():
    def __init__(self):
        self.plantilla = [  '_','_','_',
                            '_','_','_',
                            '_','_','_']

    def printTab(self,board): #Función que se usara para imprimir el tablero actual
        print(board[0],board[1],board[2])
        print(board[3],board[4],board[5])
        print(board[6],board[7],board[8])

    def genmoves(self, b, cross): #b será un tablero, y cross indica que marca se usará
        lmov = []
        move = [] #Esta lista contendrá la posición de donde se colocó una marca
        if cross == True: #Cross indica que debe usar el jugador
            mark = 'X'
        else:
            mark = 'O'
        for mv in range(len(b)):
            if b[mv] == '_':
                lmov.append(b.copy()) #mete una copia de todo el tablero al final de la lista mov
                lmov[-1][mv] = mark #Dependiendo del jugador se colocará 'X' o 'O'
                i = mv // 3 #Esto nos dice la fila donde se coloco
                j = mv % 3 #Esto nos dice la columna donde se coloco
                move.append((i,j))
        return lmov, move #Retorna los posibles movimientos con su respectivas jugadas

    def alphabeta(self, board, depth, alpha, beta, maxplayer, cross): #Tablero, profundidad, alpha, beta, maxplayer, cross nos indica la marca según quien sea el jugador
        # maxplayer: True Es turno de la máquina, False es turno del rival
        aux = self.gamestatus(board,cross) #Se usara esta variable para saber si el tablero gano o empato
        if depth == 0 or aux == 1 or aux == 2: #Se entrará en este if hasta que se haya generado un tablero con una solución, empate o se haya pasado la profundidad
            puntuacion = self.scoreBoard(board,cross) #Se genera la puntuación del tablero actual dependiendo del sujeto
            if maxplayer: #Turno de la maquina
                if puntuacion > 0: #Como es turno de la máquina, si existe una puntuación significa que es un buen tablero...
                    return puntuacion #...porque tiene la posibilidad de ganar
                else: #Sí llegamos al límite de la profundidad y/o no ha habido puntuación significa que el tablero no es bueno para la maquina
                    return -self.scoreBoard(board, not cross) #Vemos la puntuación del tablero del rival y lo colocamos como negativo ya si tiene valor es malo para la maquina por eso el signo
            else: #Es turno del rival
                if puntuacion > 0: #Si le toca al rival y tiene puntuación es malo para la maquina
                    return -puntuacion
                else:#Si llegamos a la profundidad revisamos el tablero de la máquina para ver si es mejor, si es cero es mejor empatar que perder,...
                    return self.scoreBoard(board,not cross) #...pero si es mayor es un tablero mejor para la maquina
        #Se generan los movimientos del jugador actual para después hacer la recursión según quien sea el siguiente
        t,nouse = self.genmoves(board, cross) #Se generan los movimientos futuros dependiendo de quien sea el sujeto, la segunda variable no se usara ya que de momento no nos interesa el movimiento que se hizo sino todo el tablero
        if maxplayer: #Es el turno de la máquina de evaluar
            val = -math.inf
            for child in t:
                val = max(val, self.alphabeta(child, depth-1, alpha, beta, False, not cross)) # Vamos un nivel más adentro, le toca al oponente
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return val
        else: #Es turno del rival/jugador
            val = math.inf
            for child in t:
                val = min(val, self.alphabeta(child, depth-1, alpha, beta, True, not cross)) # Vamos un nivel más adentro, le toca a nuestro jugador (maquina) por ello invertimos la marca
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return val

    def scoreBoard(self, board, cross): #La siguiente función sirve para comprobar si un tablero está a punto de ganar, además de comprobar si es un tablero ganador
        if cross == True: #Cross indica que marca se debe de evaluar
            mark = 'X'
        else:
            mark = 'O'
        # Conversión de la lista board a una matriz de 3x3 para facilitar su manejo
        matrix = np.array(board).reshape(3, 3) #Se convierte a matriz para poder revisar las situaciones de gane más fácil
        mT = np.transpose(matrix) #Si calculamos la transpuesta de la matriz podemos cambiar filas por columnas para poder verificar si hay gane en las columnas
        aux = self.gamestatus(board,cross) #Usare esta auxiliar para que se hagan las evaluaciones hasta que se encuentre un tablero ganador
        #Apartir de aquí se encuentra el código que evalúa el tablero
        puntuacion, diagonal1,diagonal11,diagonal2,diagonal22 = 0,0,0,0,0
        for j in range(0,3): #Este for ira recorriendo todo el tablero en busca de líneas ganadoras de 3 o líneas con 2 marcas y un hueco que sería casi ganar
            conth,conth2, contv, contv2 = 0,0,0,0 #Estas variables recorren filas por lo que deberá reiniciarse en cada fila
            for i in range(0,3):
                #Se revisan las filas
                if matrix[j][i] == mark: conth += 1 #Se busca que en una fila haya tres marcas, se contaran esas marcas (Ganador)
                if matrix[j][i] == '_': conth2 +=1 #Este if se usará para ver si se tiene un tablero casi ganador (Casi ganador)
                #Se revisan las columnas
                if mT[j][i] == mark: contv += 1 #Comprueba las columnas (aunque en realidad revisa las filas de la transpuesta) (Ganador)
                if mT[j][i] == '_': contv2 += 1 #(casi ganador)
            #Se revisan las diagonales como si fuera de 0,0 a 2,2
            if matrix[j][j] == mark: diagonal1 +=1 #Comprueba las diagonales (Ganador)
            if matrix[j][j] == '_': diagonal11 +=1 #(casi ganador)
            #Se revisan las diagonales como si fuera de 2,0 a 0,2
            if matrix[j][-(j-2)] == mark: diagonal2 +=1 #Comprueba las diagonales (Ganador)
            if matrix[j][-(j-2)] == '_': diagonal22 +=1 #Comprueba las diagonales
            #Se revisa que haya una línea de 3 en filas y columnas
            if conth == 3 or contv == 3: puntuacion += 350 #Si se cumple este if significa que hay una línea de 3
            #Se revisa que haya dos marcas y un hueco en las filas y columnas
            if conth == 2 and conth2 == 1 and aux == 1: puntuacion += 500 #Si se cumple este if significa que hay un tablero con una posibilidad de ganar
            if contv == 2 and contv2 == 1 and aux == 1: puntuacion += 500 #Si se cumple este if significa que hay un tablero con una posibilidad de ganar
        #Se revisa que haya una diagonal de 3 
        if diagonal1 == 3 or diagonal2 == 3: puntuacion += 350 #Si se cumple este if significa que hay una línea de 3
        #Se revisa si hay una diagonal con dos marcas y un hueco
        if diagonal1 == 2 and diagonal11 == 1 and aux == 1: puntuacion +=500 #Si se cumple este if significa que hay un tablero con una posibilidad de ganar
        if diagonal2 == 2 and diagonal22 == 1 and aux == 1: puntuacion +=500 #Si se cumple este if significa que hay un tablero con una posibilidad de ganar
        return puntuacion

    def tttplayer(self, board, cross):
        lmov,mv = self.genmoves(board,cross) #Se le mete un tablero y el simbolo, regresa posibles movimientos y jugada de cada movimiento
        score = []
        i = 0
        for lm in lmov:
            score.append((mv[i],self.alphabeta(lm,10, -math.inf, math.inf, False,not cross))) #En score se guardara la jugada y el valor de alphabeta. Se le carga el turno del rival y la marca del rival
            i +=1 #Linea anterior, le toca al rival generar los movimientos por eso el False y not cross 
        m = sorted(score, key=lambda res:res[1]) #Se ordena score de tal forma que el valor de alphabeta más grande este al final de la lista
        move = m[-1][0]
        print('-La máquina escogió: {}'.format(move))
        return move

    def gamestatus(self,board,cross):#Función similar a scoreBoard solo que esta revisara si alguien ha ganado o a empatado
        if cross == True: #Solo se comentará lo nuevo
            mark = 'X'
        else:
            mark = 'O'
        matrix = np.array(board).reshape(3, 3) 
        mT = np.transpose(matrix)
        pendiente1,pendiente2,estado,completo = 0,0,0,0 #estado: nos dirá si se ha ganado o empatado, completo: contara los huecos
        for j in range(0,3): 
            conth, contv = 0,0
            for i in range(0,3):
                if matrix[j][i] == '_': completo +=1 #Contamos cuantos huecos hay en el tablero
                if matrix[j][i] == mark: conth += 1 
                if mT[j][i] == mark: contv += 1
            if matrix[j][j] == mark: pendiente1 +=1
            if matrix[j][-(j-2)] == mark: pendiente2 +=1
            if conth == 3 or contv == 3: #Si se cumplen estos if significa que se ha ganado
                estado = 1 #Este valor retornado significa que gano
        if pendiente1 == 3 or pendiente2 == 3:
                estado = 1
        if estado == 0 and completo == 0: #Si no se ha ganado y además no hay ningún hueco significa que es un empate
            estado = 2#Este valor retornado significa que hubo un empate
        return estado

    def StartGame(self): #Función que dará inicio al juego
        print('Juego del gato #')
        self.printTab(self.plantilla)
        print('*Escriba que símbolo desea usar (sin los paréntesis): [X] o [O]')
        invalid = True
        while invalid:
            player = input()
            if player == 'O' or player == 'X':
                invalid = False
            else:
                print('*Escriba el símbolo correctamente')
        print('*Escogió: '+str(player))
        if player == 'X': #Dependiendo de que haya elegido el humano, se colocara lo contrario a la maquina
            cross = False #False equivale a O para la maquina
            machine = 'O' #Variable que se usara para poder agregar marcas al tablero
        else:
            cross = True #True equivale a X para la maquina
            machine = 'X'
        endgame = 0 #Variable que se usara para hacer un ciclo infinito hasta que alguien gane, pierda o empate
        while endgame == 0:
            if player == 'X': #Si el humano elige X, inicia primero
                invalid = True
                print('*Su turno [{}]. Introduzca la posición de su jugada: fila,columna'.format(player))
                while invalid:
                    x,y = input().split(',') #Se digitara la posición separada por una coma
                    x,y = int(x), int(y)
                    if x < 3 and x > -1 and y < 3 and y > -1 and self.plantilla[3*x+y] == '_':
                        invalid = False 
                    else:
                        print('*Movimiento invalido. Verifique que este vacía y que sea del rango 0 a 2')
                print('*Movimiento: ({},{})'.format(x,y))
                #Se coloca una marca en el tablero:
                self.plantilla[3*x+y] = player
                print('*Tablero actual:')
                self.printTab(self.plantilla)
                #Comprobación de si se ha terminado el juego o aun no
                endgame = self.gamestatus(self.plantilla, not cross) #Le pasamos el tablero y la marca del jugador
                if endgame == 1:
                    print('--------Has ganado--------')
                    break
                if endgame == 2:
                    print('--------Empate--------')
                    break
                #Si aun no termina el juego, es turno de la maquina
                print('-Turno de la maquina [{}]...'.format(machine))
                move = self.tttplayer(self.plantilla,cross)
                #Se coloca una marca en el tablero:
                self.plantilla[3*move[0]+move[1]] = machine
                print('-Tablero actual:')
                self.printTab(self.plantilla)
                endgame = self.gamestatus(self.plantilla,cross)
                if endgame == 1:
                    print('--------Ha ganado la maquina--------')
                    break
                if endgame == 2:
                    print('--------Empate--------')
                    break
                #Se repetirá el ciclo hasta que el juego termine
            else: #Si el jugado elige O primero iniciara la maquina
                print('-Turno de la maquina [{}]...'.format(machine))
                move = self.tttplayer(self.plantilla,cross)
                #Se coloca una marca en el tablero:
                self.plantilla[3*move[0]+move[1]] = machine
                print('-Tablero actual:')
                self.printTab(self.plantilla)
                endgame = self.gamestatus(self.plantilla,cross)
                if endgame == 1:
                    print('--------Ha ganado la maquina--------')
                    break
                if endgame == 2:
                    print('--------Empate--------')
                    break
                #Turno del humano
                invalid = True
                print('*Su turno [{}]. Introduzca la posición de su jugada: fila,columna'.format(player))
                while invalid:
                    x,y = input().split(',') #Se digitara la posición separada por una coma
                    x,y = int(x), int(y)
                    if x < 3 and x > -1 and y < 3 and y > -1 and self.plantilla[3*x+y] == '_':
                        invalid = False 
                    else:
                        print('*Movimiento invalido. Verifique que este vacia y que sea del rango 0 a 2')
                print('*Movimiento: ({},{})'.format(x,y))
                #Se coloca una marca en el tablero:
                self.plantilla[3*x+y] = player
                print('*Tablero actual:')
                self.printTab(self.plantilla)
                #Comprobación de si se ha terminado el juego o aun no
                endgame = self.gamestatus(self.plantilla,not cross) #Le pasamos el tablero y la marca del jugador
                if endgame == 1:
                    print('--------Has ganado--------')
                    break
                if endgame == 2:
                    print('--------Empate--------')
                    break
                #Sí no ha terminado la partida, se repite el ciclo hasta que termine

#Ejecución de la clase que contiene al juego
partida = TicTacToeGame()
partida.StartGame()
