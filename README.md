# Hunt the Wumpus with Alpha-Beta Pruning Implementation

### **Objectives:**
The player needs to first kill the Wumpus, then search for the gold, and finally return to the initial position. The game is designed so that these objectives should be completed in order, but there's flexibility if the gold is closer than the Wumpus.

### **Implementation and Explanation:**
Alpha-Beta Pruning is used to determine the best move based on the score. Each step reduces the score by 1. The following actions provide points:
- Killing the Wumpus: +500
- Taking the gold: +1000
- Returning to the initial position: +2000  

Even though the main goal is to kill the Wumpus first, the player may take the gold before killing the Wumpus if the gold is closer.

### **Environment:**
The game is set on a 6x6 grid. The code randomly generates the following elements, ensuring they are not too close to the player's initial position:
- 2 pits
- 1 Wumpus
- 1 gold  

Any grid cell adjacent to a pit will display a "B" (Breeze), and any cell adjacent to the Wumpus will display an "S" (Stench).

---

## **Alpha-Beta Pruning and Hunt the Wumpus: Detailed Explanation**

### **About the Game:**
Hunt the Wumpus is a classic text-based adventure game, first created by Gregory Yob in 1972. The player explores a series of connected rooms (or caves) to hunt a mythical creature called the "Wumpus" while avoiding hazards like pits. This game is one of the earliest examples of procedural generation and strategic gameplay, and it is often seen as an early inspiration for artificial intelligence in games.

### **Alpha-Beta Pruning Definition:**
Alpha-beta pruning is an optimization technique for the minimax algorithm. It reduces the number of nodes evaluated in the game tree by "pruning" branches that cannot affect the final decision. This is done by maintaining two values:
- **Alpha:** The best (highest) value the maximizer can guarantee, given the current state.
- **Beta:** The best (lowest) value the minimizer can guarantee, given the current state.

---

## **Collaborators:**
1. **Angelica Suti Whiharto** (hwasyui)  
2. **Intan Kumala Pasya** (tannpsy)  
3. **Muh. Fakhri Hisyam Akbar** (Grayzero15)
