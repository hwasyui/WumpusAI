# Hunt the Wumpus with Alpha Beta Pruning Implementation
**Objectives:** Player needs to kill Wumpus first then search for gold, after both are fulfilled, player goes back to its initial position.
**Implementation and Explanation:** Using Alpha Beta Pruning, it decides the best move based on the score. For every step, it will get -1 score, killing Wumpus +500 score, taking the Gold +1000, back to initial position +2000. Therefore, even though the objective is to kill the Wumpus first, there's a chance for the player to take the gold first if it's much closer than the Wumpus.
**Environment:** It is a table with 6x6 grid. The code will generates 2 pits, 1 Wumpus, and 1 gold with random placement but while ensuring that it will not be too close to the initial position. Grid that is adjacent to pit will create this B text which is 'Breeze', while grid that is adjacent to Wumpus will create'S' text for 'Stench'.

### Alpha Beta Pruning and Hunt the Wumpus Detailed Explanation
**About the Game:** Hunt the Wumpus is a classic text-based adventure game from the early 1970s, often seen as an early example of procedural generation and strategic gameplay. The game was created by Gregory Yob in 1972. The goal is to explore a series of connected rooms or caves to hunt a mythical creature called the "Wumpus" while avoiding various hazards. It's often considered one of the early inspirations for AI in games due to the strategic elements players need to consider.
**Alpha Beta Pruning Definition:** Alpha - beta pruning is an optimization technique for the minimax algorithm. It reduces the number of nodes evaluated in the game tree by eliminating branches that cannot influence the final decision. This is achieved by maintaining two values, alpha and beta, which represent the minimum score that the maximizing player is assured of and the maximum score that the minimizing player is assured of, respectively.
Alpha: The best (highest) value that the maximizer can guarantee given the current state.
Beta: The best (lowest) value that the minimizer can guarantee given the current state.

## Collabolators:
1. Angelica Suti Whiharto (hwasyui)
2. Intan Kumala Pasya (tannpsy)
3. Muh. Fakhri Hisyam Akbar (Grayzero15)

