import random
import os
import shutil

def mutate_genomes(input_directory, output_directory, mutation_rate):
    os.makedirs(output_directory, exist_ok=True)  # Creating the output directory

    genome_files = os.listdir(input_directory)  # List the genome files in the home directory

    for file_name in genome_files:
        if file_name.endswith('.fna'):  # Processing .fna files only
            input_file = os.path.join(input_directory, file_name)

            with open(input_file, 'r') as file:
                lines = file.readlines()  # Read file line by line

            original_genome_lines = [lines[0].strip()]  # Get first line and skip other lines

            mutated_genome_lines = []
            for line in lines[1:]:
                mutated_line = ''
                for base in line:
                    if base in ('A', 'T', 'G', 'C'):
                        if random.random() < mutation_rate:
                            new_base = random.choice('ATGC'.replace(base, ''))  # We randomly select a new nucleotide out of the current nucleotide
                            mutated_line += new_base
                        else:
                            mutated_line += base
                    else:
                        mutated_line += base

                mutated_genome_lines.append(mutated_line.strip())

            output_file = os.path.join(output_directory, file_name)
            with open(output_file, 'w') as file:
                file.write('\n'.join(original_genome_lines + mutated_genome_lines))  # Write mutated genome lines to new location

            print(f"The mutated genome has been successfully saved to '{output_file}'.")