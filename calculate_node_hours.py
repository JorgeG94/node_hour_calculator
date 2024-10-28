import json
import sys

def read_machine_info(json_file):
    # Open and read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract the machine groups (list of machines)
    machines = data.get('machines', [])
    if not machines:
        print("No machines found in the JSON file.")
        sys.exit(1)

    # Loop through each machine and display its characteristics
    for i, machine in enumerate(machines):
        machine_info = machine.get('machine', {})
        machine_name = machine_info.get('name', 'Unknown')
        node_hours_enabled = machine_info.get('node_hours', False)
        node_hours_conversion_factor = machine_info.get('node_hours_conversion_factor', 1)

        # Display the machine characteristics
        print(f"\nMachine {i + 1}: {machine_name}")
        print(f"Node Hours Enabled: {node_hours_enabled}")
        if node_hours_conversion_factor != 1:
            print(f"Node Hours Conversion Factor to SUs: {node_hours_conversion_factor}")

    # Return the machines data for further processing
    return machines


def check_experiment_groups(experiment):
    # Check for the presence of the "aimd", "strong", or "weak" groups
    aimd_present = 'aimd' in experiment
    strong_present = 'strong' in experiment
    weak_present = 'weak' in experiment
    
    # Count how many of these groups are present
    groups_present = sum([aimd_present, strong_present, weak_present])
    
    # Raise an error if more than one group is present
    if groups_present > 1:
        raise ValueError(f"Experiment '{experiment.get('title', 'Unknown')}' contains multiple groups ('aimd', 'strong', 'weak'). Only one is allowed.")
    
    # Return the group that is present
    if aimd_present:
        return 'aimd'
    elif strong_present:
        return 'strong'
    elif weak_present:
        return 'weak'
    else:
        return None

def calculate_node_hours(experiment_time, nodes, number_of_runs):
    node_hours_per_run = experiment_time * nodes
    node_hours_for_experiment = node_hours_per_run * number_of_runs
    print(f"        The amount of node hours per run is: {node_hours_per_run}")
    print("         \033[92m ------------->\033[0m")
    print(f"            The amount of node hours for the experiment is: {node_hours_for_experiment}")
    return node_hours_for_experiment

def calculate_time_per_node(nodes_to_use, time_for_smallest_seconds=None, expected_time_seconds=None, efficiencies=None, scaling_type='strong'):
    node_hours = 0
    if scaling_type == 'strong' and time_for_smallest_seconds is not None:
        print(f"Calculating time per node for Strong Scaling:")
        for i, nodes in enumerate(nodes_to_use):
            efficiency = efficiencies[i]
            # Time for this configuration
            time_per_node = (time_for_smallest_seconds / efficiency) * (nodes_to_use[0] / nodes)
            node_hours += (time_per_node / 3600) * nodes
            print(f"  Nodes: {nodes}, Efficiency: {efficiency}, Time per Node: {time_per_node:.2f} seconds")

    elif scaling_type == 'weak' and expected_time_seconds is not None:
        print(f"Calculating time per node for Weak Scaling:")
        for i, nodes in enumerate(nodes_to_use):
            efficiency = efficiencies[i]
            # Time for this configuration
            time_per_node = expected_time_seconds / efficiency
            node_hours += (time_per_node / 3600) * nodes
            print(f"  Nodes: {nodes}, Efficiency: {efficiency}, Time per Node: {time_per_node:.2f} seconds")

    else:
        raise ValueError("Invalid scaling type or missing required parameters.")
    print("         \033[92m ------------->\033[0m")
    print(f"        Node hours for {scaling_type} are : {node_hours}")
    return node_hours

def process_aimd(experiment):
    print(f"  Processing AIMD group for experiment '{experiment.get('title')}'")
    # Implement the logic for handling AIMD experiments here
    # Example: timestep_latency_seconds, timestep_size_fs, simulation_target_time_ps
    aimd_info = experiment['aimd']
    timestep_latency_seconds = aimd_info.get('timestep_latency_seconds', 0)
    timestep_size_ps = aimd_info.get('timestep_size_ps', 0)
    simulation_target_time_ps = aimd_info.get('simulation_target_time_ps', 0)
    number_of_runs = experiment.get('number_of_runs',0)
    nodes_to_use = experiment.get('nodes_to_use', 0)

    n_timesteps = simulation_target_time_ps / timestep_size_ps
    calculation_time = n_timesteps * timestep_latency_seconds
    calculation_time_hours = calculation_time / 3600
    experiment_time = calculation_time_hours 

    
    # Print or calculate based on these values
    print(f"    Timestep Latency (seconds): {timestep_latency_seconds}")
    print(f"    Timestep Size (ps): {timestep_size_ps}")
    print(f"    Number of total timesteps : {n_timesteps}")
    print(f"    Simulation Target Time (ps): {simulation_target_time_ps}")
    print(f"    Experiment Time (hours): {experiment_time}")
    print(f"    Nodes to use : {nodes_to_use}")
    print(f"    Number of runs : {number_of_runs}")
    node_hours_total = calculate_node_hours(experiment_time, nodes_to_use, number_of_runs) 
    return node_hours_total

def process_strong(experiment):
    print(f"  Processing Strong Scaling group for experiment '{experiment.get('title')}'")
    # Implement the logic for handling strong scaling experiments here
    strong_info = experiment['strong']
    nodes_to_use = strong_info.get('nodes_to_use', [])
    time_for_smallest_seconds = strong_info.get('time_for_smallest_seconds', 0)
    efficiencies = strong_info.get('efficiencies', [])
    
    # Print or calculate based on these values
    print(f"    Nodes to Use: {nodes_to_use}")
    print(f"    Time for Smallest (seconds): {time_for_smallest_seconds}")
    print(f"    Efficiencies: {efficiencies}")
    node_hours = calculate_time_per_node(nodes_to_use, time_for_smallest_seconds=time_for_smallest_seconds, efficiencies=efficiencies, scaling_type='strong')
    return node_hours

def process_weak(experiment):
    print(f"  Processing Weak Scaling group for experiment '{experiment.get('title')}'")
    # Implement the logic for handling weak scaling experiments here
    weak_info = experiment['weak']
    nodes_to_use = weak_info.get('nodes_to_use', [])
    expected_time_seconds = weak_info.get('expected_time_seconds', 0)
    efficiencies = weak_info.get('efficiencies', [])
    
    # Print or calculate based on these values
    print(f"    Nodes to Use: {nodes_to_use}")
    print(f"    Expected Time (seconds): {expected_time_seconds}")
    print(f"    Efficiencies: {efficiencies}")
    node_hours = calculate_time_per_node(nodes_to_use, expected_time_seconds=expected_time_seconds, efficiencies=efficiencies, scaling_type='weak')
    return node_hours

def process_single_point(experiment):
    print(f"  Processing single point experiment '{experiment.get('title')}'")

    time_per_experiment_seconds = experiment.get('time_per_experiment_seconds',0)
    number_of_runs = experiment.get('number_of_runs',0)
    nodes_to_use = experiment.get('nodes_to_use', 0)

    time_in_hours = time_per_experiment_seconds / 3600
    time_in_hours = time_in_hours * number_of_runs 
    node_hours = time_in_hours * nodes_to_use 
    print("         \033[92m ------------->\033[0m")
    print(f"            Node hours for single point experiment are: {node_hours}")
    return node_hours

def print_experiment_info(machine_info):
    # Extract machine characteristics
    machine_name = machine_info.get('name', 'Unknown')
    node_hours_enabled = machine_info.get('node_hours', False)
    node_hours_conversion_factor = machine_info.get('node_hours_conversion_factor', 1)

    # Extract experiments
    experiments = machine_info.get('experiments', [])

    # Count the number of experiments
    num_experiments = len(experiments)
    print("*******************************************************************************")
    print(f"\nMachine: {machine_name}")
    print(f"Number of Experiments: {num_experiments}\n")

    # Initialize node hour counters for this machine
    node_hours_aimd = 0
    node_hours_strong = 0
    node_hours_weak = 0
    node_hours_single_point = 0

    # Loop through each experiment and print the title, note, and process group info
    for i, experiment in enumerate(experiments):
        title = experiment.get('title', 'No title')
        note = experiment.get('note', 'No note')
        print("------------------------------------------------------------------------")
        print(f"Experiment {i + 1}:")
        print(f"  Title: {title}")
        print(f"  Note: {note}")

        # Check which group is present and process accordingly
        group = check_experiment_groups(experiment)
        if group == 'aimd':
            node_hours_aimd += process_aimd(experiment)
        elif group == 'strong':
            node_hours_strong += process_strong(experiment)
        elif group == 'weak':
            node_hours_weak += process_weak(experiment)
        else:
            node_hours_single_point += process_single_point(experiment)

    # Calculate total node hours for the machine
    total_node_hours = node_hours_aimd + node_hours_strong + node_hours_weak + node_hours_single_point
    charge_type = "node hours"
    if node_hours_conversion_factor != 1:
        charge_type = "SUs"
        total_node_hours *= node_hours_conversion_factor
    print("------------------------------------------------------------------------")
    print(f"\033[92m  Total {charge_type} for machine '{machine_name}' = {total_node_hours}\033[0m")
    return total_node_hours



if __name__ == "__main__":
    # Check if the user provided a JSON file as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 calculate_node_hours.py <file.json>")
        sys.exit(1)
    
    # Get the JSON file from the command-line arguments
    json_file = sys.argv[1]

    # Read machine info and experiments from the provided JSON file
    machines = read_machine_info(json_file)
        # Initialize a dictionary to store node hours per machine
    machine_node_hours = {}

    # Process each machine and store the node hours in the dictionary
    for machine in machines:
        machine_info = machine.get('machine', {})
        machine_name = machine_info.get('name', 'Unknown')  # Extract machine name
        
        # Get the node hours from print_experiment_info
        node_hours = print_experiment_info(machine_info)  

        # Check the conversion factor
        node_hours_conversion_factor = machine_info.get('node_hours_conversion_factor', 1)

        # Determine charge type
        charge_type = "node hours"
        if node_hours_conversion_factor != 1:
            charge_type = "SUs"

        # Store machine name and node hours/SUs
        machine_node_hours[machine_name] = (node_hours, charge_type)

    # Output the node hours or SUs for each machine
    print("***********************************************************************")
    print("Per machine totals: ")
    for machine_name, (node_hours, charge_type) in machine_node_hours.items():
        print(f"\033[92m Machine: {machine_name}, Total k{charge_type}: {node_hours/1000}\033[0m")

