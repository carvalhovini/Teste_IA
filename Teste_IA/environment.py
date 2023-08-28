import pygame
import random

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class GameEnvironment:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("IA Aprendendo a Jogar")
        self.clock = pygame.time.Clock()
        self.player = pygame.Rect(50, 300, 40, 40)
        self.obstacles = self.generate_obstacles()
        self.done = False
        self.reward = 0
        self.episode_data = []

        self.num_sensors = 5
        self.sensor_width = 10
        self.sensor_height = 20
        self.sensors = [
            pygame.Rect(self.player.right, self.player.centery - self.sensor_height // 2, self.sensor_width, self.sensor_height)
            for _ in range(self.num_sensors)
        ]

        self.distance_sensors = [
            pygame.Rect(self.player.right, self.player.centery - self.sensor_height // 2, 1500, 2),
            pygame.Rect(self.player.right, self.player.centery - self.sensor_height // 2 - 30, 1500, 2),
            pygame.Rect(self.player.right, self.player.centery - self.sensor_height // 2 + 30, 1500, 2),
        ]

    def generate_obstacles(self):
        obstacles = []
        min_distance = 300

        x = 800
        while x < 1200:
            gap_height = random.randint(150, 250)
            top_obstacle_height = random.randint(50, 400)
            bottom_obstacle_height = 600 - top_obstacle_height - gap_height

            top_obstacle = Obstacle(x, 0, 50, top_obstacle_height)
            bottom_obstacle = Obstacle(x, 600 - bottom_obstacle_height, 50, bottom_obstacle_height)

            obstacles.extend([top_obstacle, bottom_obstacle])
            x += top_obstacle.rect.width + min_distance

        return obstacles

    def reset(self):
        self.player = pygame.Rect(50, 300, 40, 40)
        self.obstacles = self.generate_obstacles()
        self.done = False
        self.reward = 0
        self.episode_data = []

    def step(self, action):
        if action == 0:
            self.player.y -= 10
        elif action == 1:
            self.player.y += 10

        for i, sensor in enumerate(self.sensors):
            sensor.x = self.player.right
            sensor.centery = self.player.centery - (i - self.num_sensors // 2) * (self.sensor_height + 10)

        for i, sensor in enumerate(self.distance_sensors):
            sensor.x = self.player.right
            sensor.centery = self.player.centery - (i - 1) * 30

        sensor_collisions = [sensor.colliderect(obstacle.rect) for sensor in self.sensors for obstacle in self.obstacles]

        if any(sensor_collisions):
            self.reward = -10
            self.done = True

        distances = []
        for sensor in self.distance_sensors:
            min_distance = float('inf')
            for obstacle in self.obstacles:
                if sensor.colliderect(obstacle.rect):
                    distance = obstacle.rect.x - self.player.right
                    if distance < min_distance:
                        min_distance = distance
            distances.append(min_distance)

        for obstacle in self.obstacles:
            if self.player.colliderect(obstacle.rect):
                self.reward = -10
                self.done = True

        for obstacle in self.obstacles:
            obstacle.rect.x -= 5
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)
                gap_height = random.randint(150, 250)
                top_obstacle_height = random.randint(50, 400)
                bottom_obstacle_height = 600 - top_obstacle_height - gap_height

                new_top_obstacle = Obstacle(800, 0, 50, top_obstacle_height)
                new_bottom_obstacle = Obstacle(800, 600 - bottom_obstacle_height, 50, bottom_obstacle_height)
                self.obstacles.extend([new_top_obstacle, new_bottom_obstacle])

        self.episode_data.append((self.get_normalized_state(), action, self.reward, self.get_normalized_state(), self.done))
        self.reward += 1

    def get_normalized_state(self):
        player_y = self.player.y / 600.0
        obstacle_data = []

        for obstacle in self.obstacles:
            obstacle_x = obstacle.rect.x / 800.0
            obstacle_y = obstacle.rect.y / 600.0
            obstacle_data.extend([obstacle_x, obstacle_y])

        while len(obstacle_data) < 10:
            obstacle_data.append(0.0)

        return [player_y] + obstacle_data
