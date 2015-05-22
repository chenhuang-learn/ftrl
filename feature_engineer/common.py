import math, os, subprocess

def open_with_first_line_skipped(path, skip=True):
    f = open(path)
    if not skip:
        return f
    next(f)
    return f

# lines of data must >> nr_thread, get nr_thread new files
def split(path, nr_thread, has_header):

    # new file: path.__tmp__.idx
    def open_with_header_witten(path, idx, header):
        f = open(path+'.__tmp__.{0}'.format(idx), 'w')
        if not has_header:
            return f
        f.write(header)
        return f

    # ceil(data_lines/nr_thread) lines per thread
    def calc_nr_lines_per_thread():
        nr_lines = int(list(subprocess.Popen('wc -l {0}'.format(path), shell=True
            , stdout=subprocess.PIPE).stdout)[0].split()[0])
        if has_header:
            nr_lines -= 1
        return math.ceil(float(nr_lines)/nr_thread)

    # idx [0,>nr_thread-1]
    header = open(path).readline()
    nr_lines_per_thread = calc_nr_lines_per_thread()
    idx = 0
    f = open_with_header_witten(path, idx, header)
    for i, line in enumerate(open_with_first_line_skipped(path, has_header), start=1):
        if i > nr_lines_per_thread * (idx + 1):
            f.close()
            idx += 1
            f = open_with_header_witten(path, idx, header)
        f.write(line)
    f.close()

# equals 'command[0] ... command[n-1] arg_paths[0].__tmp__.idx ... arg_paths[n-1].__tmp__.idx'
def parallel_convert(commands, arg_paths, nr_thread):
    workers = []
    for i in range(nr_thread):
        cmd = ' '.join(commands)
        for path in arg_paths:
            cmd += ' {0}'.format(path+'.__tmp__.{0}'.format(i))
        worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        workers.append(worker)
    for worker in workers:
        worker.communicate()

# cat all subfiles to file
def cat(path, nr_thread):
    if os.path.exists(path):
        os.remove(path)
    for i in range(nr_thread):
        cmd = 'cat {svm}.__tmp__.{idx} >> {svm}'.format(svm=path, idx=i)
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()

def delete(path, nr_thread):
    for i in range(nr_thread):
        os.remove('{0}.__tmp__.{1}'.format(path, i))

