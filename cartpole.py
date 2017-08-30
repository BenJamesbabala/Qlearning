# Simple Policy based agent for Cartpole

# Discounted Rewards are used instead of just current rewards

# For that we need to store the previous actions with weighted rewards

import tensorflow as tf
import numpy as np
import sys

from layers import *

import gym


env = gym.make('CartPole-v0')


class cartpole():

	def __init__(self):

		self.state = 0

		# State size os 4 correspodong tp theta, accn, distance, velocity
		self.state_size = 4

		# An action denote the force of magnitude 1 in the left or right direction corresponding to 0/1
		self.action_size = 2
		self.max_iter = 10
		self.num_episodes = 1
		self.e = -0.1
		self.lr = 0.001


	def model_setup(self):

		# Here we suppose that the network is a fully connected layer

		self.state_in = tf.placeholder(dtype=tf.float32, shape=[None, self.state_size])
		self.prob_action = linear1d(self.state_in, self.state_size, self.action_size)
		
		# Taking the action based on the weights

		self.action = tf.argmax(self.prob_action, 1)


	def loss_setup(self):

		self.action_hist = tf.placeholder(dtype=tf.int32, shape=[None,self.action_size])
		self.reward_hist = tf.placeholder(dtype=tf.float32, shape=[None])

		# Caclulation the temp weight by taking the weights corresponding action that we got earlier in the stage

		self.temp_weights = tf.reduce_sum(self.prob_action*tf.cast(self.action_hist, tf.float32), 1)

		self.loss = tf.reduce_mean(-tf.log(self.temp_weights)*self.reward_hist)

		# Calculating the gradients in tensorflow


		var_list = tf.trainable_variables()

		# for i in var_list:
		# 	print (i)

		self.gradients = tf.gradients(self.loss, var_list)


		# Defining the optimizer for updating the network

		self.optimizer = tf.train.AdamOptimizer(learning_rate=self.lr)





	def train(self):

		self.model_setup()
		self.loss_setup()

		init = tf.global_variables_initializer()

		with tf.Session() as sess:

			sess.run(init)

			for i in range(self.num_episodes):

				curr_state = env.reset()

				for j in range(self.max_iter):

					temp = np.random.uniform(1)

					if temp > self.e :
						temp_action, temp_prob_action = sess.run([self.action, self.prob_action], feed_dict={self.state_in:np.reshape(curr_state,[-1, self.state_size])})
					else :
						temp_action = np.random.randint(self.action_size, size=[1])

					new_state, reward, done, _ = env.step(temp_action[0])

					# print("Temp probs on action is ", temp_prob_action, " on state ", curr_state)

					if (j == 0):
						history = np.array([[temp_action, curr_state, new_state, reward]])
					else:
						history = np.insert(history, history.shape[0], np.array([temp_action, curr_state, new_state, reward]), axis=0)

					# print(history)
					# print(np.vstack(history[:,0]).flatten())

					temp_grad, temp_weight = sess.run([self.gradients, self.temp_weights], feed_dict={self.state_in:np.vstack(history[:,1]), self.reward_hist:history[:,3], self.action_hist:np.eye(self.action_size)[np.vstack(history[:,0]).flatten()] })
					# sys.exit()

					# if j%self.batch_size == 0:

					# print(temp_grad)



					for xs,grad_xs in enumerate(temp_grad):
						
						if(j%self.batch_size==1):
							grad_hist[xs] = grad_xs
						else :
							grad_hist[xs] += grad_xs
						
						# print(xs, grad_xs)

					if(j%self.batch_size == 0):

						

					sys.exit()


					print(history.shape)

					# sys.exit()

					# Here I am applying the gradients after some fixed number of steps.


					curr_state = new_state

					if(done):
						break

def main():

	model = cartpole()
	model.train()

if __name__ == "__main__":
	main()