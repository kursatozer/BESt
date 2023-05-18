import random
import os
import shutil

def mutate_genomes(input_directory, output_directory, mutation_rate):
    os.makedirs(output_directory, exist_ok=True)  # Creating the output directory
