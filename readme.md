# Maze Python

Este projeto implementa um sistema de labirinto (maze) que inclui tanto a geração quanto a resolução do labirinto. O projeto está dividido em três módulos principais:

1. MazeNode: representa um campo (ou célula) do labirinto
2. MazeGenerator: responsável por gerar um labirinto totalmente aleatório e único a cada execução
3. MazeSolver: um algoritmo que resolve o labirinto

A seguir, irei descrever o funcionamento de cada módulo separadamente

## MazeNode
Esta classe representa uma célula do labirinto, armazenando referências a quatro outras células, além de indicar se há paredes entre elas. Assim, a partir de uma célula, é possível alcançar todas as outras

```python
class MazeNode:
    def __init__(self, neighbors=None, walls=None, pos=(0, 0)):
        if walls is None:
            walls = [True, True, True, True]

        if neighbors is None:
            neighbors = [None, None, None, None]

        self.pos = pos
        self.neighbors = neighbors
        self.walls = walls
```

## MazeGenerator
Esta classe embaralha um labirinto inicialmente preenchido com todas as paredes no lugar e, aleatoriamente, remove algumas delas. Todas as células visitadas são adicionadas a uma lista, e as células identificadas como pendentes são armazenadas em outra lista, para serem processadas posteriormente e dar continuidade ao algoritmo

```python
 def next_step(self, pop_first=False):
        """
        Takes a step in the maze by randomly choosing an unvisited neighbor.

        Args:
            pop_first (bool): Whether to remove the current position from the remain positions list if it's empty. Default False.
        """
        x, y = self.cursor_pos
        root_node = self.maze[x][y]
        possible_moves = self.get_possible_moves(root_node)
        self.__random_control()

        if len(possible_moves) > 0:
            next_node = random.choice(possible_moves)
            self.__visited.append(next_node.pos)

            if len(possible_moves) > 1:
                self.__remain_pos.append(self.cursor_pos)

            self.cursor_pos = next_node.pos
            if root_node.top[0] == next_node:
                root_node.top = (root_node.top[0], False)
            elif root_node.bottom[0] == next_node:
                root_node.bottom = (root_node.bottom[0], False)
            elif root_node.right[0] == next_node:
                root_node.right = (root_node.right[0], False)
            elif root_node.left[0] == next_node:
                root_node.left = (root_node.left[0], False)
        else:
            while len(self.__remain_pos) > 0:
                x, y = self.cursor_pos = self.__remain_pos.pop(0 if pop_first else -1)
                if len(self.get_possible_moves(self.maze[x][y])) > 0:
                    break

        self.__first = False
```
Este é o algoritmo utilizado para embaralhar um labirinto de forma aleatória

## MazeSolver
O algoritmo implementado é o Greedy Best-First Search. Ele escolhe o próximo nó mais próximo ao objetivo, o que, na maioria dos casos, garante uma velocidade considerável. No entanto, em alguns cenários, pode ser ineficienteo 

O código abaixo mostra a implementação desse algoritmo
```python
    def next_step(self):
        """
        Advances to the next step in the maze by exploring adjacent nodes from the current position.

        This method uses a greedy approach, selecting the nearest from end unvisited node that does not lead back to the start position.

        If no such node is found, the solver will backtrack and try another path.
        """
        if self.has_next:
            x, y = self.__current_pos
            current_node = self.maze[x][y]
            nodes: list = [current_node.top, current_node.bottom, current_node.left, current_node.right]
            nodes = sorted([node for node in nodes if node[0] is not None], key=self.get_distance)

            for node in nodes:
                if self.check_node(node[0], node[1]):
                    self.__path.append(node[0].pos)
                    self.__current_pos = node[0].pos
                    return

            self.__blocked.append(self.__current_pos)
            self.__path.pop()
            self.__current_pos = self.__path[-1]
```

## Como Executar

Para executar este projeto, é necessário ter o Python instalado. Em seguida, execute os comandos abaixo:
```bash
# Cria um ambiente virtual Python
python -m venv .venv

# Ativa o ambiente virtual (Windows)
.\.venv\Scripts\activate

# Ativa o ambiente virtual (Linux/Mac)
source .venv/bin/activate

# Instala as dependências necessárias
pip install numpy opencv-python

# Executa o código
python main.py
```
## Demonstacao 

O labirinto pode ser configurado para ter diferentes níveis de aleatoriedade, ajustando seus parâmetros para torná-lo mais ou menos imprevisível. Abaixo, veja um exemplo com um labirinto mais aleatório:

[Exemplo labirinto 1.webm](https://github.com/user-attachments/assets/087aa213-7373-421d-ab65-b78c72b57ec7)

Neste segundo exemplo, os parâmetros foram ajustados para gerar um labirinto menos aleatório:

[Exemplo labirinto 2](https://github.com/user-attachments/assets/1eb51122-348d-4760-b2a7-a7c718e42a42)

# Conclusão   

Este projeto de labirinto em Python demonstra a geração e resolução de labirintos de forma eficiente e estruturada. A divisão em módulos, como MazeNode, MazeGenerator e MazeSolver, proporciona uma compreensão clara e uma fácil manutenção do código. O uso do algoritmo Greedy Best-First Search para resolver o labirinto é uma escolha interessante, pois, apesar de suas limitações em determinados cenários, oferece um desempenho geralmente rápido

# ✒️ Autor

Lucas Guimarães Kalil 

E-Mail - lucas.prokalil2020@outlook.com

[Linkedin](https://www.linkedin.com/in/lucas-kalil-436a6220a/) | [GitHub](https://github.com/LucasKalil-Programador)
