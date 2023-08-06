import unittest
import sys

import numpy as np

 

from evolvepy.generator.basic_layers import RandomPredation as RP

class TestSelection(unittest.TestCase):

	n_individuals = 100

	def test_selection(self):

		for i in range(10):
			population = [x for x in range(100)]
			fitness = np.sort(np.random.uniform(-100, 100, TestSelection.n_individuals))
			n_selected = 12
			rp = RP(n_to_predate = n_selected)
			selected, selected_fitness = rp(population, fitness)

			self.assertEqual(len(population), len(selected))
			self.assertEqual(len(fitness), len(selected_fitness))

			for j in range(n_selected):
				self.assertLessEqual(fitness[-n_selected], selected_fitness[j])
