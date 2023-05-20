import random
import os
import shutil

def mutate_genomes(input_directory, output_directory, point_mutation_rate, frame_shift_rate, insertion_lengths, insertion_rates, deletion_lengths, deletion_rates):
    os.makedirs(output_directory, exist_ok=True)  # Create the output directory if it doesn't exist

    genome_files = os.listdir(input_directory)  # List the genome files in the input directory

    for file_name in genome_files:
        if file_name.endswith('.fna'):  # Process only .fna files
            input_file = os.path.join(input_directory, file_name)
            output_file = os.path.join(output_directory, "mutated_" + file_name)

            with open(input_file, 'r', encoding='latin-1') as input_file, open(output_file, 'w', encoding='latin-1') as output_file:
                content = input_file.read()  # Read the file content as a single string

                # Apply point mutations
                mutated_content = ''
                for base in content:
                    if base in ['A', 'T', 'G', 'C']:
                        if random.random() < point_mutation_rate:
                            base = random.choice('ATGC')
                    mutated_content += base

                # Apply frame shift mutations
                mutated_content = ''.join(random.choice('ATGC') + base if random.random() < frame_shift_rate else base for base in mutated_content)

                # Apply insertion mutations
                for length, rate in zip(insertion_lengths, insertion_rates):
                    mutated_content = ''.join(random.choice('ATGC') * length if random.random() < rate else base for base in mutated_content)

                # Apply deletion mutations
                for length, rate in zip(deletion_lengths, deletion_rates):
                    mutated_content = ''.join(base for base in mutated_content if random.random() >= rate or random.random() < rate and random.random() >= length)

                output_file.write(mutated_content)  # Write the mutated content to the output file

            print(f"Mutated genome successfully saved to '{output_file.name}'.")

    print("All bacterial genomes were mutated and saved in new locations.")

input_directory = './original_genomes'
output_directory = 'mutated_genomes'
point_mutation_rate = 0.03
frame_shift_rate = 0.01
insertion_lengths = [1, 2, 3]
insertion_rates = [0.04, 0.02, 0.01]
deletion_lengths = [1, 2, 3]
deletion_rates = [0.03, 0.02, 0.01]