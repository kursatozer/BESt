import random
import os


def optimize_insertion_lengths(insertion_lengths, insertion_rates):
    # Generate new insertion lengths based on rates
    total_rate = sum(insertion_rates)
    normalized_rates = [rate / total_rate for rate in insertion_rates]

    new_insertion_lengths = []
    for _ in range(len(insertion_lengths)):
        selected_length = random.choices(insertion_lengths, weights=normalized_rates)[0]
        new_insertion_lengths.append(selected_length)

    return new_insertion_lengths


def optimize_deletion_lengths(deletion_lengths, deletion_rates_weights):
    # Normalize weights
    total_weight = sum(deletion_rates_weights)
    normalized_weights = [weight / total_weight for weight in deletion_rates_weights]

    # Generate new deletion lengths based on weights
    new_deletion_lengths = random.choices(deletion_lengths, weights=normalized_weights, k=len(deletion_lengths))

    return new_deletion_lengths


def apply_insertion(line, insertion_lengths, insertion_rates):
    mutated_line_with_insertions = []
    for base, insertion_rate in zip(line, insertion_rates):
        if base in ['A', 'T', 'G', 'C']:
            mutated_line_with_insertions.append(base)
            if random.random() < insertion_rate:
                optimized_insertion_lengths = optimize_insertion_lengths(insertion_lengths, insertion_rates)
                insertion_length = random.choice(optimized_insertion_lengths)
                insertion_sequence = ''.join(random.choices('ATGC', k=insertion_length))
                mutated_line_with_insertions.append(insertion_sequence)

    return ''.join(mutated_line_with_insertions)


def mutate_genome(line, point_mutation_rate, frame_shift_rate, insertion_lengths, insertion_rates, deletion_lengths, deletion_rates):
    mutated_line = []
    for base in line:
        if base in ['A', 'T', 'G', 'C']:
            # Apply point mutations
            if random.random() < point_mutation_rate:
                mutated_base = random.choice(['A', 'T', 'G', 'C'])
                mutated_line.append(mutated_base)
            else:
                mutated_line.append(base)

            # Apply frame shifts
            if random.random() < frame_shift_rate:
                mutated_line.append(random.choice(['A', 'T', 'G', 'C']))

    return ''.join(mutated_line)


def mutate_genomes(input_directory, output_directory, point_mutation_rate, frame_shift_rate, insertion_lengths, insertion_rates, deletion_lengths, deletion_rates):
    os.makedirs(output_directory, exist_ok=True)  # Creating the output directory

    genome_files = [file_name for file_name in os.listdir(input_directory) if file_name.endswith('.fna')]

    for file_name in genome_files:
        input_file = os.path.join(input_directory, file_name)

        with open(input_file, 'r', encoding='latin-1') as file:
            original_genome_lines = [line.strip() for line in file.readlines()]

        mutated_genome_lines = []
        mutated_genome_lines_with_insertions = []

        for line in original_genome_lines:
            mutated_line = mutate_genome(line, point_mutation_rate, frame_shift_rate, insertion_lengths, insertion_rates, deletion_lengths, deletion_rates)
            mutated_line_with_insertions = apply_insertion(mutated_line, insertion_lengths, insertion_rates)

            mutated_genome_lines.append(mutated_line)
            mutated_genome_lines_with_insertions.append(mutated_line_with_insertions)

        output_file = os.path.join(output_directory, "mutated_" + file_name)
        with open(output_file, 'w') as file:
            file.write('\n'.join(mutated_genome_lines))

        output_file_with_insertions = os.path.join(output_directory, "mutated_insertion_" + file_name)
        with open(output_file_with_insertions, 'w') as file:
            file.write('\n'.join(mutated_genome_lines_with_insertions))

        print(f"The mutated genome has been successfully saved to '{output_file}'.")
        print(f"The mutated genome with insertions has been successfully saved to '{output_file_with_insertions}'.\n")


# Test the function
input_directory = 'input_genomes'  # Replace with the actual input directory path
output_directory = 'output_genomes'  # Replace with the actual output directory path
point_mutation_rate = 0.01
frame_shift_rate = 0.01
insertion_lengths = [1, 2, 3]
insertion_rates = [0.2, 0.3, 0.5]
deletion_lengths = [1, 2, 3]
deletion_rates = [0.2, 0.3, 0.5]

mutate_genomes(input_directory, output_directory, point_mutation_rate, frame_shift_rate, insertion_lengths, insertion_rates, deletion_lengths, deletion_rates)
