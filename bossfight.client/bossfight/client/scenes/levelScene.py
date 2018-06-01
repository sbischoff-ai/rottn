# -*- coding: utf-8 -*-
'''
This is going to be the module containing the base level classes and components.
'''

import random
import cocos
import pyglet
import pygase.shared
import pygase.client
import bossfight.client.player_controls as player_controls
import bossfight.core.activities as activities

class LevelData:
    def __init__(self, server_address, scrolling_manager):
        self.connection = pygase.client.Connection(server_address, closed=True)
        self.scrolling_manager = scrolling_manager

class LevelScene(cocos.scene.Scene):
    '''
    Base class for alls kinds of ingame levels. It provides access to
    the level coordinate space, let's you add ingame objects like
    characters to the level, manages controls and HUD etc.

    Note: Currently this class implements a *Scene* that contains test content.
    '''

    def __init__(self, server_address, local_player_names):
        super().__init__()
        scrolling_manager = cocos.layer.ScrollingManager(
            viewport=cocos.rect.Rect(0, 90, 1920, 900)
        )
        self.add(scrolling_manager)
        self.level_data = LevelData(server_address, scrolling_manager)
        scrolling_manager.add(LevelLayer(self.level_data))
        self.add(HUDLayer(self.level_data))
        self.level_data.connection.connect()
        for name in local_player_names:
            self.level_data.connection.post_client_activity(
                pygase.shared.join_server_activity(name)
            )

    def on_exit(self):
        self.level_data.connection.disconnect()
        super().on_exit()

class LevelLayer(cocos.layer.ScrollableLayer):
    '''
    Layer that contains the actual level itself and everything in it.
    '''

    def __init__(self, level_data: LevelData):
        super().__init__()
        self.level_data = level_data
        ### floor for testing!
        self.iso_map = create_iso_map(
            dimensions=(15, 20),
            origin=(-1000, 0)
        )
        self.add(self.iso_map)
        image = pyglet.resource.image('fireball.png')
        image_seq = pyglet.image.ImageGrid(image, 1, 4)
        self.fireball = player_controls.ControllableNode()
        self.fireball.add(cocos.sprite.Sprite(
            image=image_seq.get_animation(0.1),
            scale=3.0
        ))
        self.add(self.fireball)
        self.schedule(self.update_focus)
        #self.schedule_interval(self.post_move_activity, 0.03)

    def update_focus(self, dt):
        self.level_data.scrolling_manager.set_focus(
            self.fireball.position[0],
            self.fireball.position[1]
        )

    def post_move_activity(self, dt):
        self.level_data.connection.post_client_activity(
            activities.move_player_activity()
        )

class HUDLayer(cocos.layer.Layer):

    def __init__(self, level_data: LevelData):
        super().__init__()
        self.level_data = level_data
        ip = level_data.connection.server_address[0]
        port = str(level_data.connection.server_address[1])
        connection_text = 'Server Address: ' + ip + ':' + port
        connection_label = cocos.text.Label(
            text=connection_text,
            position=(1920, 1080),
            font_name='Arial',
            font_size=24,
            anchor_x='right',
            anchor_y='top'
        )
        self.add(connection_label)
        self.connection_status_texts = [
            'Connected',
            'Waiting for Server ...',
            'Disconnnected'
        ]
        self.connection_status_label = cocos.text.Label(
            text=self.connection_status_texts[
                level_data.connection.connection_status-1
            ] + ' - ' + \
            'Latency: ' + str(int(level_data.connection.latency)) + ' ms',
            position=(1920, 1050),
            font_name='Arial',
            font_size=24,
            anchor_x='right',
            anchor_y='top'
        )
        self.add(self.connection_status_label)
        self.schedule(self.update_text)

    def update_text(self, dt):
        self.connection_status_label.element.text = \
            self.connection_status_texts[
                self.level_data.connection.connection_status-1
            ] + ' - ' + \
            'Latency: ' + str(int(self.level_data.connection.latency)) + ' ms'

def create_iso_map(dimensions, origin):
    image = pyglet.resource.image('iso_floor_tiles.png')
    image_grid = pyglet.image.ImageGrid(image, 8, 4)
    batch = cocos.batch.BatchNode()
    for row in range(dimensions[0]):
        for column in range(dimensions[1]):
            batch.add(cocos.sprite.Sprite(
                image=image_grid[random.randint(0, 31)],
                position=(
                    origin[0] + column*64 + row*64,
                    origin[1] - column*32 + row*32
                ),
                scale=2.0
            ))
    return batch