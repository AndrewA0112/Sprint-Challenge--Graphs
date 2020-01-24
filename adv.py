from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {}

def opp_dir(dir):
    if dir == 's':
        return 'n'
    if dir == 'n':
        return 's'
    if dir =='w':
        return 'e'
    if dir == 'e':
        return 'w'

def discover_paths(room_exits): # Return dict of all exits that are currently '?'
    exits = {}
    for exit in room_exits:
        exits[exit] = '?'
    return exits

def random_path(exits):
    random_exit = exits[random.randint(0,len(exits) - 1)]
    return random_exit



exits = player.current_room.get_exits() # All exits from room, Ex: ['n', 's', 'w', 'e']
direction = random_path(exits) # Grab random exit
unknown_exits = discover_paths(exits) # All exits that are unknown

graph[player.current_room.id] = unknown_exits # Starting Room, Ex: {0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}

while len(room_graph) > len(graph): # Traversal loop

    last_room = player.current_room # Save room for later

    player.travel(direction) # Use random direction to move
    traversal_path.append(direction)

    available_exits = {}

    if player.current_room.id in graph: # Line 71-78 is setting everything up to replace '?' with room id on the graph
        available_exits = graph[player.current_room.id] 
    else:
        available_exits = discover_paths(player.current_room.get_exits())

    available_exits[opp_dir(direction)] = last_room.id
    graph[player.current_room.id] = available_exits
    graph[last_room.id][direction] = player.current_room.id

    unknown = 0
    unknown_paths = []

    for exit,dire in graph[player.current_room.id].items(): # Find all the directions that have not been explored on the current room
        if dire == '?':
            unknown += 1
            unknown_paths.append(exit)

    if unknown == 0 or len(available_exits) == 1: # BFS if there is no more unknown directions, else run again with a new random direction

        qq= Queue()
        visited = set()
        qq.enqueue([(opp_dir(direction),last_room.id)])

        while qq.size() > 0:
            path = qq.dequeue()

            temp = path[-1]
            room_direct = temp[0]
            room_id = temp[1]

            if len(room_graph) == len(graph):
                break

            if room_id not in visited:
                visited.add(room_id)

                unexplored = None
                for exit,direc in graph[room_id].items():
                    if direc == '?':
                        unexplored = exit
                        break
                    else:
                        path_copy = path.copy()
                        path_copy.append((exit,direc))
                        qq.enqueue(path_copy)

                if unexplored is not None:
                    for item in path:
                        player.travel(item[0])
                        traversal_path.append(item[0])

                    direction = unexplored
                    break
    else:
        direction = random_path(unknown_paths)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
