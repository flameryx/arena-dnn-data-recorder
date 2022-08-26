# Evaluation run guide

## Objective

The goal of this evaluation run is to create performance data of a robot in a simulated enviroment. This data will be used for traning a neural network 
for predicting map performance. A pipeline script creates a random map and a robot has to preform a certain task. After 25 iterations the performance and 
map metrics are calcualted a saved and a new map with a new task is created.

## Prerequisites
- Python 3.8.10

## Installation 

To be able to execute the pipeline script which creates the nessesary data you have to be on the navprediction branch of arena-rosnav.

1. If Arena-Rosnav is not installed: Install Arena-Rosnav by following the installtion guide the arena-rosnav [readme](https://github.com/ignc-research/arena-rosnav) of arena-rosnav
2. Access rosnav env: `workon rosnav`
3. Navigate to `/arena_ws/src/arena-rosnav`
4. Pull the current state: `git pull`
5. Checkout to the navpredriction branch by running the command: `git checkout navprediction`
6. Update your workspace by running the command: `rosws update`
7. Build workspace by running the command: `catkin_make`

## Running the script and upload to cloud

1. Access rosnav env: `workon rosnav`
2. Navigate to the arena-dnn-data-recorder directory via the path: `arena_ws/src/forks/arena-dnn-data-recorder`
3. Intall the requirements: `pip install -r requirements.txt`
4. Run the pipeline script: `python3 pipeline_script.py [--num_maps NUM_MAPS]` NUM_MAPS specifies the number of maps you want to generate and run simulations on. Default value is 10.

After following these steps the pipeline script will start the simulation and create output data in the directorys: sims_data_records, maps, and 
dnn_input_data. After the script has ended please zip the dnn_input_data directory and upload it to the [cloud](https://tubcloud.tu-berlin.de/s/M9NYDab8rNmW6fo) 
following the naming convention: firstname_lastname_dnn_input_data.zip. In case you are uploading several zip folders you can add a number at the end. 

## Please Note

- The pipeline script can be stopped and continued at any time.
- Ros collects large amounts of log files in background which can clog your disk space. If you are having disk space issues please run 
  `sudo du -h --max-depth=1` in your Terminal to check where the disk issue arrises and if it is ideed from ros logs you can run
  `rosclean purge`
  
  
## Further Information
- [README arena-dnn-data-recorder](https://github.com/flameryx/arena-dnn-data-recorder/blob/master/README.md)
- [CreateAverages documentation](https://github.com/flameryx/arena-dnn-data-recorder/blob/master/CreateAverages_documentation.md)


