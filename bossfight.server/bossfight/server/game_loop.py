# -*- coding: utf-8 -*-

import sys
import math
import random
import pygase.shared
import pygase.server
import tensorflow
import euclid3 as euclid
from bossfight.core import character_bases
from bossfight.server.ai import actors

GRAPH = None


class BFGameLoop(pygase.server.GameLoop):
    """
    Subclasses the GameLoop from the PyGaSe package and defines server-side
    game logic.
    """

    def __init__(self, server: pygase.server.Server):
        super().__init__(server)
        self.player_characters = {}
        self.npc_actors = {}
        test_enemy = actors.TestEnemyActor("Test Enemy")
        test_enemy.position = (200, 100)
        test_enemy.direction = (-1, 0)
        test_enemy.velocity = (-1 * actors.ENEMY_VELOCITY, 0)
        self.npc_actors[0] = test_enemy
        self.server.game_state.npcs[0] = test_enemy.get_state()

        self.learn_counter = 0
        global GRAPH
        GRAPH = tensorflow.get_default_graph()

    def on_join(self, player_id, update):
        """
        Initial assignments for when a new player joins the game.
        """
        new_player = character_bases.PlayerCharacter(update.players[player_id]["name"])
        update.players[player_id].update(new_player.get_state())
        self.player_characters[player_id] = new_player

    def handle_activity(self, activity: pygase.shared.ClientActivity, update, dt):
        """
        Handling of custom BossFight client activities, like player movement or actions.
        """
        if activity.activity_type == pygase.shared.ActivityType.MovePlayer:
            player = self.player_characters[activity.activity_data["player_id"]]
            player.handle_move_activity(activity, update)

    def update_game_state(self, update, dt):
        """
        BossFight game state update. Simulates enemies and game world objects.
        """
        done = False
        hit = False
        if 0 in self.player_characters.keys():
            r_player = euclid.Vector2(
                self.player_characters[0].position[0],
                self.player_characters[0].position[1],
            )
            r_enemy = euclid.Vector2(
                self.npc_actors[0].position[0], self.npc_actors[0].position[1]
            )
            r = r_player - r_enemy
            distance = r.magnitude()
            if distance > 900:
                done = True
                sys.stderr.write("Left arena\n")
            elif distance < 140 and self.npc_actors[0].is_attacking():
                d_enemy = euclid.Vector2(
                    self.npc_actors[0].direction[0], self.npc_actors[0].direction[1]
                )
                angle = r.angle(d_enemy)
                if angle < 1.4 or (distance < 50 and angle < 1.57):
                    hit = True
                    sys.stderr.write("Hit\n")

        global GRAPH
        with GRAPH.as_default():
            if 0 in self.player_characters.keys():
                self.npc_actors[0].observe_and_act(self.player_characters[0], done, hit)
                if self.learn_counter >= 68:
                    self.npc_actors[0]._agent.replay(66)
                    self.learn_counter = 0
                else:
                    self.learn_counter += 1
        for npc_id, actor in self.npc_actors.items():
            if done or hit:
                rand_angle = random.random() * 2 * math.pi
                actor.position = (
                    r_player.x + 600 * math.sin(rand_angle),
                    r_player.y + 600 * math.cos(rand_angle),
                )
            else:
                actor.update(npc_id, update, dt)
