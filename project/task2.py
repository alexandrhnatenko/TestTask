import time
from multiprocessing import Pool, Queue


def uploading(file):
    # print('Start upload file "{}"'.format(file))
    if file.endswith('2'):
        return 0
    time.sleep(5)
    # print('finish upload file "{}"'.format(file, 1))
    return 1


class Uploader:
    def __init__(self, files, process_count, queue):
        self.workers = None
        self.files_list = files
        self.queue = queue
        self.pool = Pool(process_count)

    def start(self):
        self.workers = self.pool.map_async(uploading, self.files_list)

    def is_active(self):
        time.sleep(1)
        # result = self.workers.get(1)
        # self.queue.put((result.count(1), result.count(0),
        #                 len(result)))
        if not self.workers.ready():
            return True


def main(files_list, processes_count=1):
    work_queue = Queue()
    uploader = Uploader(files_list, processes_count, work_queue)
    work_queue.put((0, 0, len(files_list)))
    try:
        uploader.start()
        while uploader.is_active():
            print('active')
            # if not work_queue.empty():
            #     progress = work_queue.get()
            #     print('Done: {}, Error: {}, Total: {}'.format(*progress))
    except KeyboardInterrupt:
        uploader.pool.terminate()
    else:
        uploader.pool.close()
    uploader.pool.join()
    # while not work_queue.empty():
    #     progress = work_queue.get()
    #     print('Done: {}, Error: {}, Total: {}'.format(*progress))


if __name__ == '__main__':
    files_list = ['link1', 'link2', 'link3', 'link4', 'link5']
    main(files_list, 4)
