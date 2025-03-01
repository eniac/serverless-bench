import time
IMPORT_START_TIME = time.time()
import igraph
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
def graph_ops(size):
    graph = igraph.Graph.Barabasi(size, 10)
    return graph.pagerank()[0]

def handler(event, context=None):
    sleep_time = event.get("sleep_time", 0)
    size = event.get("size", 1000)
    result = graph_ops(size)

    time.sleep(sleep_time)
    return {
        "result": "{} size graph BFS finished!".format(size),
        "import_time": IMPORT_END_TIME - IMPORT_START_TIME
    }


if __name__ == "__main__":
    event = {
        "size": 1000
    }
    print(handler(event))