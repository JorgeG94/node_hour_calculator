# node_hour_calculator
A tool to calculate node hour budgets for random grants. 

## How to use 

The program needs a `json` file that contains the experiment details that are to 
be carried out. The overall skeleton is:

```
{
"machines": [
{
  "machine": {
  "name": "frontier",
  "node_hours": true,
  "node_hours_conversion_factor": 1,
  "experiments": [
    {
      "title": "Set of single point energies",
      "note": "string of string",
      "time_per_experiment_seconds": 2,
      "number_of_runs": 1250,
      "nodes_to_use": 1280
    },
    {
      "title": "Ab initio MD runs",
      "note": "string of string",
      "aimd": {
        "timestep_latency_seconds": 1,
        "timestep_size_ps": 0.1,
        "simulation_target_time_ps": 100
      },
      "number_of_runs": 10,
      "nodes_to_use": 1280
    },
    {
      "title": "Strong scaling",
      "note": "string of string",
      "strong": {
        "nodes_to_use": [
          1,
          2
        ],
        "time_for_smallest_seconds": 1200,
        "efficiencies": [
          1,
          0.95
        ]
      }
    },
    {
      "title": "Weak scaling",
      "note": "string of string",
      "weak": {
        "nodes_to_use": [
          1,
          2
        ],
        "expected_time_seconds": 1200,
        "efficiencies": [
          1,
          0.95
        ]
      }
    }
  ]
}
},
{
  "machine": {
  "name": "gadi",
  "node_hours": true,
  "node_hours_conversion_factor": 128,
  "experiments": [
    {
      "title": "Set of single point energies",
      "note": "string of string",
      "time_per_experiment_seconds": 2,
      "number_of_runs": 1250,
      "nodes_to_use": 1280
    },
    {
      "title": "Ab initio MD runs",
      "note": "string of string",
      "aimd": {
        "timestep_latency_seconds": 1,
        "timestep_size_ps": 0.1,
        "simulation_target_time_ps": 100
      },
      "number_of_runs": 10,
      "nodes_to_use": 1280
    },
    {
      "title": "Strong scaling",
      "note": "string of string",
      "strong": {
        "nodes_to_use": [
          1,
          2
        ],
        "time_for_smallest_seconds": 1200,
        "efficiencies": [
          1,
          0.95
        ]
      }
    },
    {
      "title": "Weak scaling",
      "note": "string of string",
      "weak": {
        "nodes_to_use": [
          1,
          2
        ],
        "expected_time_seconds": 1200,
        "efficiencies": [
          1,
          0.95
        ]
      }
    }
  ]
}
}
]
}
```

Basically, you can have a set of `machines` you wish to calculate your node hours
on. And per machine you can have a set of experiments. The options are built
on top of what Jorge usually does, in this case: strong, weak scaling; ab initio
md calculations, and simple one of a time calculations. 

The code can take an arbitrary number of machines and experiments. The couple of options
are:

## How to use:

Simply: `python3 calculate_node_hours.py experiments.json` if you want to generate a skeleton, you can use 
`python3 create_experiment_json.py --n_machines=n` and it will create and prepopulate an experiment json. 
