"""
single: 55.65580487251282s for 120 images
concurrent: 11.968398094177246s for 120 images, 8.73671007156372s for 123 images with 16 threads
parallel: 12.376783847808838s for 123 images
redis: 79s for 130 images with 1 rqworker, 29s for 130 images with 3 rqworkers

In concurrent(), threads execute concurrently, but not in parallel, because the global interpreter lock (GIL) prevents threads from executing in parallel in cpython (unlink jython and other implementations). Because this is an IO heavy task, the majority of the time is spent waiting for the network, and not for the processor to write the image to the download directory. Using threads ensures that the CPU doesn't have to wait for the network. Increasing the number of threads to 16 improves the execution time considerably.

In parallel(), processes are spawned. Processes consume more resources than threads, buy they are not subject to the GIL, which means the code executes in parallel. Increasing the parallelism from 8 to 16 processes slightly degrades the performance.

In redis(), tasks are pushed to a redis queue.
"""

import logging
from queue import Queue
from threading import Thread
import os, sys
from time import time
from functools import partial
from multiprocessing.pool import Pool

from redis import Redis
import rq

from download import setup_download_dir, get_links, download_link

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

def single():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")

    download_dir = setup_download_dir('./images')
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    for link in links:
        download_link(download_dir, link)
    print('Took {}s'.format(time() - ts))

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # get the task from the queue and unpack the tuple
            directory, link = self.queue.get()
            download_link(directory, link)
            # signal to main thread that this task was dequeued. if this is not called,
            # Queue.join() will block the main thread from exiting indefinitely
            self.queue.task_done()

def concurrent(num_threads=8):
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir('./images')
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    # create a thread-safe queue to communicate with the worker threads
    queue = Queue()
    # create worker threads
    for x in range(int(num_threads)):
        worker = DownloadWorker(queue)
        # setting daemon to true will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # put the tasks into the queue as tuples
    for link in links:
        logger.info('Queueing {}'.format(link))
        queue.put((download_dir, link))
    # causes the main thread to wait for the queue to finish processing all the tasks before exiting
    queue.join()
    print('Took {}'.format(time() - ts))

def parallel(num_processes=8):
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir('./images')
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    download = partial(download_link, download_dir)
    with Pool(int(num_processes)) as p:
        p.map(download, links)
    print('Took {}s'.format(time() - ts))

def redis():
    """Start redis and then run `rqworker` from the command line from within the
    directory containing this script. This will spawn a worker listening on the
    default queue. Then, when this script is run, it will connect to redis and load
    tasks onto the queue, along with the pickled download_link function so that
    the queue knows which function it needs to run for each task in the queue."""
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir('./images')
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    q = rq.Queue(connection=Redis(host='localhost', port=6379))
    for link in links:
        q.enqueue(download_link, download_dir, link)


if __name__ == '__main__':
    mode = sys.argv[1]
    if sys.argv[2:]:
        concurrency = sys.argv[2]

    if mode == 'single':
        single()
    elif mode == 'thread':
        concurrent(concurrency)
    elif mode == 'process':
        parallel(concurrency)
    elif mode == 'redis':
        redis()



