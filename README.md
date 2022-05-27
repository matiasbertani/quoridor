# quoridor 

Quoridor is a project made for EDA 6. It is a bot that connects to a server with websocket to compete against other bots in quoridor, a game about pawns and walls.


The project consists of 6 classes each hosted in a different mode with its respective name

## Bot

Class in charge of making the connection with the websocket server and managing the different events

## partida

Class in charge of managing each game, its current state and making the best decision based on the available options. Move a pawn or put up a wall

## Action, Move, WallAction

Classes that return the response expected by the websocke

## Peon

the pawn in the game, places it on the board establishing its valid moves and scores each one of them to then offer the best of them to the class to be carried out.


## wall

Class that interprets the wall, tells us if the move to place a certain learning is valid and offers methods for the class to leave so that it can make decisions

## scanner

Class responsible for "scanning" the board to validate if the placement of a wall is a move that encloses any of the pawns on the board
