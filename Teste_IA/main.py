# main.py

import pygame
import threading
from environment import GameEnvironment
from qlearning_agent import QLearningAgent

def render_game(env):
    env.screen.fill((0, 0, 0))
    pygame.draw.rect(env.screen, (255, 0, 0), env.player)
    for obstacle in env.obstacles:
        pygame.draw.rect(env.screen, (0, 255, 0), obstacle.rect)
    for sensor in env.sensors:
        pygame.draw.rect(env.screen, (0, 0, 255), sensor, 2)  # Desenhe os sensores em azul
    for sensor in env.distance_sensors:
        pygame.draw.rect(env.screen, (255, 255, 0), sensor, 2)  # Desenhe os sensores de distância em amarelo
    pygame.display.flip()

# Função para rodar o jogo em uma thread separada
def game_thread(env):
    while True:
        if env.done:
            env.reset()
        action = agent.choose_action(env.get_normalized_state())
        env.step(action)
        render_game(env)
        pygame.time.delay(10)  # Adiciona um pequeno atraso para evitar travamentos

# Treine a IA em uma thread separada
def train_agent(agent):
    for episode in range(1000):
        state = env.get_normalized_state()
        total_reward = 0
        env.reset()

        while not env.done:
            action = agent.choose_action(state)
            env.step(action)
            next_state = env.get_normalized_state()
            reward = env.reward
            agent.train(state, action, reward, next_state, env.done)
            state = next_state
            total_reward += reward

        agent.memory.extend(env.episode_data)

        print(f"Episódio: {episode + 1}, Recompensa Total: {total_reward}, Epsilon: {agent.epsilon}")

if __name__ == "__main__":
    env = GameEnvironment()
    state_size = 11
    action_size = 2
    agent = QLearningAgent(state_size, action_size)

    # Inicie o jogo em uma thread separada
    game_thread = threading.Thread(target=game_thread, args=(env,))
    game_thread.start()

    # Treine a IA em outra thread separada
    train_agent = threading.Thread(target=train_agent, args=(agent,))
    train_agent.start()
