# qlearning_agent.py

import numpy as np
import random
from tensorflow import keras
from collections import deque

class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.01
        self.gamma = 0.99
        self.model = self.build_model()
        self.memory = deque(maxlen=5000)

    def build_model(self):
        model = keras.Sequential()
        model.add(keras.layers.Dense(32, input_dim=self.state_size, activation='relu'))
        model.add(keras.layers.Dense(32, activation='relu'))
        model.add(keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(np.array([state]))[0]
        return np.argmax(q_values)

    def train(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > 128:  # Treine com lotes de 128 amostras
            batch = random.sample(self.memory, 128)
            for state, action, reward, next_state, done in batch:
                target = reward
                if not done:
                    target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
                target_f = self.model.predict(np.array([state]))
                target_f[0][action] = target
                self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay