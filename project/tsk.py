import time
from multiprocessing import Process, Queue


class Uploader:
    def __init__(self, ):
        self.workers = []
        self._queue = Queue()
        self._progress_queue = None
        self._processes_count = 0

    def _build_workers(self, ):
        for i in range(self._processes_count):
            worker = Upload(self._queue, self._progress_queue)
            worker.start()
            self.workers.append(worker)

    def start(self, files_list, processes_count, progress_queue):
        self._progress_queue = progress_queue

        if self._progress_queue.empty():
            progress = (0, 0, len(files_list))
            print('Done: {}, Error: {}, Total:{}'.format(*progress))
            self._progress_queue.put(progress)
        else:
            progress = self._progress_queue.get()
            update_progress = (
                progress[0],
                progress[1],
                progress[2] + len(files_list))
            print('Done: {}, Error: {}, Total:{}'.format(*update_progress))
            self._progress_queue.put(update_progress)

        for file in files_list:
            self._queue.put(file)
        self._processes_count = processes_count
        self._build_workers()

    def terminate(self, process_id):
        process_name = 'Upload-{}'.format(process_id)
        process = list(
            filter(lambda x: x.name == process_name, self.workers))
        if process and process[0].is_alive():
            process[0].terminate()

            progress = self._progress_queue.get()
            update_progress = (progress[0], progress[1] + 1, progress[2])
            print('Done: {}, Error: {}, Total:{}'.format(*update_progress))
            self._progress_queue.put(update_progress)
        else:
            print('Process "{}" not exist'.format(process_name))

    def terminate_all(self):
        stop_files = 0
        while not self._queue.empty():
            self._queue.get()
            stop_files += 1
        for process in self.workers:
            if process.is_alive():
                process.terminate()
                stop_files += 1

        progress = self._progress_queue.get()
        update_progress = (progress[0], progress[1] + stop_files, progress[2])
        print('Done: {}, Error: {}, Total:{}'.format(*update_progress))
        self._progress_queue.put(update_progress)


class Upload(Process):
    def __init__(self, queue, progress_queue):
        super(Process, self).__init__()
        self._queue = queue
        self._progress_queue = progress_queue

    def run(self):
        while not self._queue.empty():
            content = self._queue.get()
            self.uploading(content)

            progress = self._progress_queue.get()
            update_progress = (progress[0] + 1, progress[1], progress[2])
            print('Done: {}, Error: {}, Total:{}'.format(*update_progress))
            self._progress_queue.put(update_progress)

    def uploading(self, content):
        print('Start upload file "{}" in process "{}"'.format(
            content, self.name))
        time.sleep(5)


def validate_command(input_string):
    supported_commands = ['upload', 'exit', 'stop']
    command_string = input_string.split(' ')
    if len(command_string) == 0 or len(command_string) > 2:
        print('Invalid command')
        raise Exception
    if command_string[0] not in supported_commands:
        print('Command not supported')
        raise Exception
    if len(command_string) == 1:
        param = None
    else:
        try:
            param = int(command_string[1])
        except ValueError:
            print('Invalid type of parameter')
            raise Exception
    return command_string[0], param


if __name__ == '__main__':
    """
    Command 'upload' to uploading files by several processes,
        has 'parameter processes_count', default = 1
    Example:
        upload 4
        upload
    Command 'stop' to stop  process of uploading files,
        has parameter  process_id, without parameter will stop all processes
    Example:
        stop 4
        stop
    Command 'exit' to exit from program
    Example:
        exit
    """
    default_processes_count = 1
    files_list = ['link1', 'link2', 'link3', 'link4', 'link5', 'link6',
                  'link7', 'link8', 'link9', 'link10', 'link11', 'link12',
                  'link13', 'link14', 'link15', 'link16', 'link17', 'link18',
                  'link19', 'link20']
    uploader = Uploader()
    progress_queue = Queue()
    while True:
        print('Enter command :')
        input_string = input()
        try:
            command, param = validate_command(input_string)
        except:
            continue
        if command == 'upload':
            if param:
                uploader.start(files_list, param, progress_queue)
            else:
                uploader.start(files_list, default_processes_count,
                               progress_queue)
            continue
        if command == 'exit':
            uploader.terminate_all()
            break
        if command == 'stop':
            if param:
                uploader.terminate(param)
            else:
                uploader.terminate_all()
    print('Exit')
