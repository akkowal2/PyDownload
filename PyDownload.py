#!/usr/bin/python

import Http
import uuid
import time
from multiprocessing.pool import ThreadPool


file_url = 'http://speedtest.tele2.net/100MB.zip'
file_name = '100MB.zip'

if not Http.supports_partial_download(file_url):
	print('Does not support partial downloading')
	sys.exit(0)

print(file_url + ' supports partial downloads!')

start_time = time.time()
Http.get_file(file_name + '.full', file_url)
end_time = time.time()
print('Downloaded file with 1 thread in {} seconds'.format(end_time - start_time))

start_time = time.time()
size = int(Http.get_file_size(file_url))
num_threads = 5

increment_size = int(size / num_threads)
ranges = []
for i in range(num_threads):
	if i == 0:
		start_byte = i * increment_size
	else:
		start_byte = (i * increment_size) + 1

	end_byte = (i * increment_size) + increment_size
	if end_byte > size:
		end_byte = size
	ranges.append((start_byte, end_byte))

pool = ThreadPool(processes=num_threads)
threads = []

for i in range(len(ranges)):
	threads.append(pool.apply_async(Http.get_partial_file, (file_url, ranges[i][0], ranges[i][1])))

f = open(file_name + '.parallel', 'w')
data = ""
for thread in threads:
	data += thread.get()

f.write(data)
end_time = time.time()
f.close()

print('Downloaded file with {} threads in {} seconds'.format(num_threads, end_time - start_time))