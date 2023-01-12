'''
@author Ricardo Sosa Melo
'''
import os
import glob
from uuid import uuid4 as uuid
from pathlib import Path
from argparse import ArgumentParser
from random import randint, choice
import cv2
import random


# Create and parse cli arguments #------------------

parser = ArgumentParser()
parser.add_argument(
    "--num_maps",
    action="store",
    dest="num_maps",
    default=10,
    help="How many maps do you want to create",
    required=False,
)

parser.add_argument(
    "--num_settings",
    action="store",
    dest="num_settings",
    default=1,
    help="How many different simulation settings you want to run on each map",
    required=False,
)

parser.add_argument(
    "--maps_path",
    action="store",
    dest="maps_path",
    default="../../../arena-rosnav/simulator_setup/maps",
    help="The path where the maps are stored.",
    required=False,
)

parser.add_argument(
    "--records_path",
    action="store",
    dest="records_path",
    default="../../arena-evaluation/01_recording/project_recordings",
    help="The path where the recordings of the simulations ran on the maps are stored.",
    required=False,
)


args = parser.parse_args()

num_maps = int(args.num_maps)
num_settings = int(args.num_settings)
maps_path = args.maps_path
records_path = args.records_path

#---------------------------------------------------
# Create necessary directories #--------------------

dirname = os.path.dirname(__file__)

# Create local maps folder if it does not exist
local_maps = Path(dirname) / "maps"
local_maps.mkdir(parents=True, exist_ok=True)

# Create local records folder if it does not exist
local_records = Path(dirname) / "sims_data_records"
local_records.mkdir(parents=True, exist_ok=True)

# Create local dnn input data folder if it does not exist
dnn_input = Path(dirname) / "dnn_input_data"
dnn_input.mkdir(parents=True, exist_ok=True)

#---------------------------------------------------
# Pipeline loop #-----------------------------------

for i in range(num_maps):
# Generate maps #-----------------------------------------

    mapSize = random.choice([50,70,90])

    if mapSize == 50:
        num_dyn_obs = random.choice([0,3,6,9])
        num_static_obs = random.choice([0,3,6,9])
    
    if mapSize == 70:
        num_dyn_obs = random.choice([0,4,8,12])
        num_static_obs = random.choice([0,4,8,12])

    if mapSize == 90:
        num_dyn_obs = random.choice([0,5,10,15])
        num_static_obs = random.choice([0,5,10,15])

        num_dyn_obs = random.choice(range(0,16,5))
        num_static_obs = random.choice(range(0,16,5))
    
    map_name = str(uuid())
    width = mapSize
    height = mapSize
    map_type = "indoor"
    num_maps_to_generate = 1
    map_res = 0.5
    iterations = random.choice([5,10,15,30,45,70]) 
    num_obstacles = 45
    obstacle_size = 10
    corridor_width = 3

    #TODO remove, just for testing
    mapSize = 70
    width = mapSize
    height = mapSize
    num_static_obs = 12
    num_dyn_obs = 12   
    iterations = 40

    generate_maps_command = f"python3 cliMapGenerator.py --map_name {map_name} --width {width} --height {height} --map_type {map_type} --num_maps {num_maps_to_generate} --map_res {map_res} --save_path {maps_path} --iterations {iterations} --num_obstacles {num_obstacles} --obstacle_size {obstacle_size} --corridor_width {corridor_width}"
    os.system(generate_maps_command)
    
    #---------------------------------------------------------
    # Run simulations and record data #-----------------------

    planner = random.choice(["rosnav"])    
    robot = random.choice(["burger"])
    dyn_obs_velocity = 0.5
    dyn_obs_radius = 0.5
    static_obs_vertices = 5

    num_dyn_obs 
    num_static_obs 
    roslaunch_command = f""" roslaunch arena_bringup start_arena_flatland.launch model:={robot} num_dynamic_obs:={num_dyn_obs} num_static_obs:={num_static_obs} min_dyn_vel:={dyn_obs_velocity} max_dyn_vel:={dyn_obs_velocity} min_dyn_radius:={dyn_obs_radius} max_dyn_radius:={dyn_obs_radius} min_static_num_vertices:={static_obs_vertices} max_static_num_vertices:={static_obs_vertices} local_planner:={planner} map_file:={map_name} task_mode:="project_eval" scenario_file:="project_eval/scenario_1.json" use_recorder:="true" show_rviz:="false" use_rviz:="false" """
    os.system(roslaunch_command)


    # Copy new generated map to local maps folder
    os.system(f"mv {maps_path}/{map_name} maps")
    
    # Copy recorded data for the new map to local sims_data_records folder
    os.system(f"mv {records_path}/{map_name} sims_data_records")
        
    #---------------------------------------------------------
    # Data cleaning, analysis and map complexity calculation #
    os.system("python3 createAverage_changed.py --csv_name /{}/{}*.csv --map_iterations {}" .format(map_name,map_name,iterations))
    
    #----------------------------------------------------------