import urllib2

def supports_partial_download(url):
	header = get_http_response_header(url)
	return 'Accept-Ranges' in header

def get_http_response_header(url):
	request = urllib2.urlopen(url)
	return request.info()

def get_file_size(url):
	request = urllib2.urlopen(url)
	return request.info().getheaders('Content-Length')[0]

def get_file(file_name, url):
	request = urllib2.urlopen(url)
	with open(file_name, 'w') as f:
		f.write(request.read())

def get_partial_file(url, start_byte, end_byte):
	http_request = urllib2.Request(url, headers={"Range": "bytes={}-{}".format(start_byte, end_byte)})
	request = urllib2.urlopen(http_request)
	data = request.read()
	return data
