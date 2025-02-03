import multiprocessing
import objaverse
processes = multiprocessing.cpu_count()
processes

import json

# Open and load JSON file
with open("./data_lists/lvis_uids_filter_by_vertex.json", "r") as file:
    random_object_uids = json.load(file)

objects = objaverse.load_objects(
    uids=random_object_uids,
    download_processes=processes
)
objects
