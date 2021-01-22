# Artificial-Intelligence

# Multiagent
This assignment involves enabling the Pacman agent to act appropriately in the game where there are ghosts in the world. The Pacman still aims at eating all the dots but must plan its action taking the behaviour of the ghosts into account. This exercise will involve modeling the decision-making task as an adversarial search problem that allows the Pacman to decide actions while taking into account the behaviour of ghosts. Designed and implemented a Reflex Agent with evaluation function for states which state to choose who aims at eating food and avoiding ghost based on the current situation of world. Designed and implemented minimax, alpha-beta pruning and expectimax algorithm which goes in future states and determines which is the best optimal move for the agent to take for eating food and avoiding ghost and scored 23.91/25 in the assignment more than the class average which was 21.52/25 in which competitive grading was given.


# Decision Making in Team
This assignment explores planning and decision making for teams. The setup involves two teams where each team tries to safeguard its resources (food pellets) and tries to capture resources held by the other team. You will design AI agents that control Pacman and ghosts in coordinated team-based strategies.

This assignment involves two teams (named red and blue) present in the 2D map competing against each other. Your team will try to eat the food on the far side of the map, while defending the food on your home side. Each team (red and blue) consists of two agents each.

Your agents are in the form of ghosts on your home side and Pacman on your opponent’s side. If you are a ghost then you are permitted to consume the opponent. If Pacman is eaten by a ghost before reaching its own side of the board, he will explode into a cloud of food dots that will be deposited back on the board. Additionally, the map includes power capsules which will be explained later. Further, there is an added time limit of computation which will add new challenges.

The AI agent must reason about trading off trying to capture resources versus trying to defend its own resources and effectively functioning both as a ghost and a Pacman in a team setting.

Designed and implemented Monte Carlo Tree Search simulation for the decision making algorithm for agents in pacman game in which should be computed in time limit of one second where they have to gather food from the opponent team while defending in our own area..
