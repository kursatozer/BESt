import random
import os
import shutil

def mutate_genomes(input_directory, output_directory, mutation_rate, frame_shift_rate):
    os.makedirs(output_directory, exist_ok=True) # Creating the output directory

    genome_files = os.listdir(input_directory) # List the genome files in the home director

    for file_name in genome_files:
        if file_name.endswith('.fna'): # Processing .fna files only
            input_file = os.path.join(input_directory, file_name)

            with open(input_file, 'r') as file:
                lines = file.readlines() # Read file line by line

            original_genome_lines = [line.strip() for line in lines] # Get first line and skip other lines

            mutated_genome_lines = []
            for line in original_genome_lines:
                mutated_line = []
                for base in line:
                    if base in ['A', 'T', 'G', 'C']:
                        if random.random() < mutation_rate:
                            base = random.choice('ATGC') # We randomly select a new nucleotide out of the current nucleotide
                    mutated_line.append(base)

                # Apply frameshift mutation
                if random.random() < frame_shift_rate and len(mutated_line) > 0:
                    last_base = mutated_line[-1]
                    mutated_line = [last_base] + mutated_line[:-1]

                mutated_genome_lines.append(''.join(mutated_line))

            output_file = os.path.join(output_directory, file_name)
            with open(output_file, 'w') as file:
                file.write('\n'.join(mutated_genome_lines)) # Write mutated genome lines to new location

            print(f"Mutasyona uğramış genom başarıyla '{output_file}' konumuna kaydedildi.")

    print("Tüm bakteri genomları mutasyona uğratılarak yeni konumlara kaydedildi.")

input_directory = '/home/kratzer/Desktop/aMeta-sim/cont'
output_directory = 'mutated_genomes'
mutation_rate = 0.03
frame_shift_rate = 0.05

mutate_genomes(input_directory, output_directory, mutation_rate, frame_shift_rate)
