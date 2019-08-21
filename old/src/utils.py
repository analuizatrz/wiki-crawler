from datetime import datetime
import csv

def read_first_column(csv_filepath):
	with open(csv_filepath) as csvfile:
		return [row[0] for row in list(csv.reader(csvfile))]

def file_name_with_out_extension(file_path):
	return file_path.split("/")[-1].split(".")[0]

class Clock(object):
	def __init__(self):
		self.time = datetime.now()
		self.sum_time = 0
		self.cont_deltas = 0

	def finish_time(self):
			delta = datetime.now()-self.time
			self.time = datetime.now()
			return delta

	def print_delta(self, task):
		delta = self.finish_time()
		self.sum_time += delta.total_seconds()
		self.cont_deltas += 1
		print(task+" done in "+str(delta.total_seconds())+" average: "+str(self.sum_time/self.cont_deltas))
