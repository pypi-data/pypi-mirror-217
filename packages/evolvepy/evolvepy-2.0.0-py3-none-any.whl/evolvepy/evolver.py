from typing import List, Tuple, Union
import time
import numpy as np

from evolvepy.generator import Generator
from evolvepy.evaluator import Evaluator
from evolvepy.callbacks import Callback
from evolvepy.integrations import nvtx

class Evolver:
    '''
    Basic class for evolving generations.

    It combines the generator, evaluator and callbacks and runs the evolutionary process.
    '''

    def __init__(self, generator:Generator, evaluator:Evaluator, population_size:int, callbacks:Union[Callback, List[Callback]]=None):
        '''
        Evolver constructor.

        Args:
            generator (Generator): Generator for generating populations.
            evaluator (Evaluator): Evaluator for evaluating individuals.
            population_size (int): Size of population.
            callbacks (Union[Callback, List[Callback]], optional): Callabacks that will be called during evolution. Defaults to None.
        '''
        
        self._generator = generator
        self._evaluator = evaluator
        self._population_size = population_size
        
        if callbacks is None:
            callbacks = []
        elif isinstance(callbacks, Callback):
            callbacks = [callbacks]
        self._callbacks = callbacks

        for callback in self._callbacks:
            callback._generator = generator
            callback._evaluator = evaluator
            callback._callbacks = self._callbacks

        self._started = False

    def evolve(self, generations:int, verbose:bool=False) -> Tuple[np.ndarray, np.ndarray]:
        '''
        Evolves the population for a few generations

        Args:
            generations (int): Number of generations to evolve
            verbose (bool): If should print the generation number, maximum fitness and time. Defaults to False.

        Returns:
            Tuple[np.ndarray, np.ndarray]: The first element is the fitness history of all generations, in order. 
                The second is the last population evaluated.
        '''

        self._history = np.empty((generations, self._population_size), np.float64)

        if not self._started:
            with nvtx.annotate_se("callback_start", domain="evolvepy", category="evolution_stage", color=nvtx.callback_color):
                for callback in self._callbacks:
                    callback._on_start()
                self._started = True

        for i in range(generations):
            range_name = "generation_iteration"
            profile_range = nvtx.start_range(range_name, domain="evolvepy", category="evolution_iteration", color=nvtx.evolver_color)
            
            if verbose:
                start_time = time.time()

            with nvtx.annotate_se("callback_generator_start", domain="evolvepy", category="evolution_stage", color=nvtx.callback_color ):
                for callback in self._callbacks:
                    if callback._parameters["run"]:
                        callback._on_generator_start()

            with nvtx.annotate_se("generator", domain="evolvepy", category="evolution_stage", color=nvtx.generator_color):
                population = self._generator.generate(self._population_size)

            with nvtx.annotate_se("callback_generator_end", domain="evolvepy", category="evolution_stage", color=nvtx.callback_color):
                for callback in self._callbacks:
                    if callback._parameters["run"]:
                        callback._on_generator_end(population)

            with nvtx.annotate_se("evaluator", domain="evolvepy", category="evolution_stage", color=nvtx.evaluator_color):
                fitness = self._evaluator(population)

            with nvtx.annotate_se("callback_evaluator_end", domain="evolvepy", category="evolution_stage", color=nvtx.callback_color):
                for callback in self._callbacks:
                    if callback._parameters["run"]:
                        callback._on_evaluator_end(fitness)

            self._generator.fitness = fitness

            self._history[i] = fitness.flatten()

            if verbose:
                with nvtx.annotate_se("verbose_print", domain="evolvepy", category="evolution_stage", color=nvtx.evolver_color):
                    end_time = time.time()
                    delta_t = end_time-start_time
                    print("Generation "+str(i)
                            +" | Max fitness "+str(np.max(fitness))
                            +" | Time "+str(delta_t)+" s")
            
            nvtx.end_range(profile_range)
        
        with nvtx.annotate_se("callback_end", domain="evolvepy", category="evolution_stage", color=nvtx.callback_color):
            for callback in self._callbacks:
                if callback._parameters["run"]:
                    callback._on_stop()

        return self._history, population

