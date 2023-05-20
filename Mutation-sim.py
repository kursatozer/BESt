import random
import os
import shutil

def mutate_genomes(input_directory, output_directory, point_mutation_rate, frame_shift_rate, insertion_lengths, insertion_rates, deletion_lengths, deletion_rates):
    os.makedirs(output_directory, exist_ok=True)  # Create the output directory if it doesn't exist

    genome_files = os.listdir(input_directory)  # List the genome files in the input directory

    for file_name in genome_files:
        if file_name.endswith('.fna'):  # Process only .fna files
            input_file = os.path.join(input_directory, file_name)

            with open(input_file, 'r', encoding='latin-1') as file:
                lines = file.readlines()  # Read the file line by line

            original_genome_lines = []
            for line in lines:
                if line.startswith('>'):  # If the line starts with '>', it is an information line, so append it directly
                    original_genome_lines.append(line.strip())
                else:
                    mutated_line = []
                    for base in line.strip():
                        if base in ['A', 'T', 'G', 'C']:
                            if random.random() < point_mutation_rate:
                                base = random.choice('ATGC')  # Select a new nucleotide from 'ATGC' with a given probability
                        mutated_line.append(base)
                    original_genome_lines.append(''.join(mutated_line))

            mutated_genome_lines = []
            for line in original_genome_lines:
                if line.startswith('>'):  # If the line starts with '>', it is an information line, so append it directly
                    mutated_genome_lines.append(line)
                else:
                    mutated_line = []
                    for base in line:
                        # Apply frameshift mutation
                        if random.random() < frame_shift_rate and len(mutated_line) > 0:
                            last_base = mutated_line[-1]
                            mutated_line = [last_base] + mutated_line[:-1]
                        mutated_line.append(base)
                    mutated_genome_lines.append(''.join(mutated_line))

            # Apply insertion mutation
            mutated_genome_with_insertions = insertions(mutated_genome_lines, insertion_lengths, insertion_rates)

            # Apply deletion mutation
            mutated_genome_with_deletions = deletions(mutated_genome_with_insertions, deletion_lengths, deletion_rates)

            output_file = os.path.join(output_directory, "mutated_" + file_name)
            with open(output_file, 'w', encoding='latin-1') as file:
                file.write('\n'.join(mutated_genome_with_deletions))  # Write the mutated genome lines to the new location

            print(f"Mutated genome successfully saved to '{output_file}'.")

    print("All bacterial genomes have been mutated and saved in new locations.")

def insertions(genome_lines, insertion_lengths, insertion_rates):
    mutated_genome_lines = []
    for line in genome_lines:
        if line.startswith('>'):  # If the line starts with '>', it is an information line, so append it directly
            mutated_genome_lines.append(line)
        else:
            mutated_line = []
            for base in line:
                mutated_line.append(base)
                for length, rate in zip(insertion_lengths, insertion_rates):
                    if random.random() < rate:
                        insertion = ''.join(random.choice('ATGC') for _ in range(length))
                        mutated_line.append(insertion)
            mutated_genome_lines.append(''.join(mutated_line))
    return mutated_genome_lines

def deletions(genome_lines, deletion_lengths, deletion_rates):
    mutated_genome_lines = []
    for line in genome_lines:
        if line.startswith('>'):  # If the line starts with '>', it is an information line, so append it directly
            mutated_genome_lines.append(line)
        else:
            mutated_line = []
            i = 0
            while i < len(line):
                base = line[i]
                if base in ['A', 'T', 'G', 'C']:
                    mutated_line.append(base)
                    for length, rate in zip(deletion_lengths, deletion_rates):
                        if random.random() < rate:
                            i += length  # Skip the deletion length
                            break
                else:
                    mutated_line.append(base)
                i += 1
            mutated_genome_lines.append(''.join(mutated_line))
    return mutated_genome_lines

# Set the input and output directories, mutation rates, and lengths/rates for insertions and deletions
input_directory = './original_genomes'
output_directory = 'mutated_genomes'
point_mutation_rate = 0.03
frame_shift_rate = 0.01
insertion_lengths = [1, 2, 3]
insertion_rates = [0.04, 0.02, 0.01]
deletion_lengths = [1, 2, 3]
deletion_rates = [0.03, 0.02, 0.01]

# Mutate the genomes using the provided parameters
mutate_genomes(input_directory, output_directory, point_mutation_rate, frame_shift_rate, insertion_lengths, insertion_rates, deletion_lengths, deletion_rates)
