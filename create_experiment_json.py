import json
import argparse

def create_skeleton_json(n_machines):
    skeleton = {"machines": []}

    # Populate each machine
    for i in range(n_machines):
        machine = {
            "machine": {
                "name": f"machine_{i+1}",
                "node_hours": True,
                "node_hours_conversion_factor": 1,
                "experiments": [
                    {
                        "title": f"experiment_{i+1}_single_point",
                        "note": "This is a single point calculation",
                        "time_per_experiment_seconds": 1,
                        "number_of_runs": 1,
                        "nodes_to_use": 1
                    },
                    {
                        "title": f"experiment_{i+1}_aimd",
                        "note": "This is an AIMD experiment.",
                        "aimd": {
                            "timestep_latency_seconds": 1,
                            "timestep_size_fs": 1,
                            "simulation_target_time_ps": 1
                        }
                    },
                    {
                        "title": f"experiment_{i+1}_strong",
                        "note": "This is a strong scaling experiment.",
                        "strong": {
                            "nodes_to_use": [1, 2],
                            "time_for_smallest_seconds": 1,
                            "efficiencies": [1, 1]
                        }
                    },
                    {
                        "title": f"experiment_{i+1}_weak",
                        "note": "This is a weak scaling experiment.",
                        "weak": {
                            "nodes_to_use": [1, 2],
                            "expected_time_seconds": 1,
                            "efficiencies": [1, 1]
                        }
                    }
                ]
            }
        }
        skeleton["machines"].append(machine)

    return skeleton

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Create a skeleton JSON file for experiments.")
    parser.add_argument("--n_machines", type=int, required=True, help="Number of machines to create")
    args = parser.parse_args()

    # Create the skeleton JSON structure
    skeleton = create_skeleton_json(args.n_machines)

    # Write the skeleton JSON to a file
    output_filename = "experiment_skeleton.json"
    with open(output_filename, 'w') as json_file:
        json.dump(skeleton, json_file, indent=4)

    print(f"Skeleton JSON created: {output_filename}")

if __name__ == "__main__":
    main()

