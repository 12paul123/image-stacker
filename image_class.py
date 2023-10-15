import os
import sys
import shutil
from multiprocessing import Process, Queue, cpu_count
from PIL import Image, ImageOps
import time, math
import numpy as np

class Image_api():

	def __init__(self):
		self.current_path = os.getcwd()
		self.frames_path = os.path.join(self.current_path, "video_frames")
		self.video_path = os.path.join(self.current_path, "video")
		self.prepared_path = os.path.join(self.current_path, "prepared")
		self.finished_path = os.path.join(self.current_path, "finished")

		self.width = 1280
		self.height = 1280

		self.processes = cpu_count()
		self.queue = Queue()

	def change_size(self, width, height):
		self.width = width
		self.height = height

	def create_folders(self):
		if not os.path.exists(self.frames_path):
			os.makedirs(self.frames_path)
		if not os.path.exists(self.video_path):
			os.makedirs(self.video_path)
		if not os.path.exists(self.prepared_path):
			os.makedirs(self.prepared_path)
		if not os.path.exists(self.finished_path):
			os.makedirs(self.finished_path)

	def crop(self, files, start):
		for file_num, file in enumerate(files, start=start):
			file_path = os.path.join(self.frames_path, file)
			with Image.open(file_path) as img:
				gray = img.convert('L')
				bw = gray.point(lambda x: 0 if x < 90 else 255)
				box = bw.getbbox()
				padded_box = (box[0]-20, box[1]-20, box[2]+20, box[3]+20)
				cropped = img.crop(padded_box)
				file_name = 'cropped_{}.jpg'.format(file_num)
				file_path = os.path.join(self.prepared_path, file_name)
				cropped.save(file_path, "JPEG")

	def crop_images(self):
		files = os.listdir(self.frames_path)
		if not files:
			print("No Frames")
		num = math.ceil(len(files)/self.processes)

		start = 1
		chunks = [files[x:x+num] for x in range(0, len(files), num)]
		for chunk in chunks:
			p = Process(target=self.crop, args=(chunk, start,))
			p.start()
			start += len(chunk)
		p.join()
		time.sleep(1)
		self.clean_folder("cropped")

	def scale(self, files, start):
		for file_num, file in enumerate(files, start=start):
			file_path = os.path.join(self.prepared_path, file)
			with Image.open(file_path) as img:
				scaled = ImageOps.fit(img, (self.width, self.height),
									Image.LANCZOS, 0, (0.5, 0.5))
				file_name = "scaled_{}.jpg".format(file_num)
				file_path = os.path.join(self.prepared_path, file_name)
				scaled.save(file_path, "JPEG")

	def scale_images(self):
		files = os.listdir(self.prepared_path)
		if not files:
			print("No Images")
		num = math.ceil(len(files)/self.processes)

		start = 1
		chunks = [files[x:x+num] for x in range(0, len(files), num)]
		for chunk in chunks:
			p = Process(target=self.scale, args=(chunk, start,))
			p.start()
			start += len(chunk)
		p.join()
		time.sleep(1)
		self.clean_folder("scaled")

	def quad_average_image(self, image):
		img = []
		for x in range(self.width):
			for y in range(self.height):
				try:
					pix_xy = image[x][y]
					pix_x1 = image[x-1][y]
					pix_x2 = image[x+1][y]
					pix_y1 = image[x][y-1]
					pix_y2 = image[x][y+1]

					pixel_ave = int((pix_x1+pix_x2+pix_y1+pix_y2+pix_xy) / 5)
					img.append(pixel_ave)
				except: img.append(0)
		self.queue.put(img)

	def quad_median_image(self, image):
		img = []
		for x in range(self.height):
			for y in range(self.width):
				try:
					pix_xy = image[x][y]
					pix_x1 = image[x-1][y]
					pix_x2 = image[x+1][y]
					pix_y1 = image[x][y-1]
					pix_y2 = image[x][y+1]

					pixel_ave = sorted([pix_x1,pix_x2,pix_y1,pix_y2,pix_xy])
					pixel_ave = pixel_ave[int(len(pixel_ave)/2)]
					img.append(pixel_ave)
				except: img.append(0)
		self.queue.put(img)

	def quad_noise_image(self, image):
		img = []
		thres = 1
		for x in range(self.width):
			for y in range(self.height):
				try:
					xy = image[x][y]
					x1 = image[x-1][y]
					x2 = image[x+1][y]
					y1 = image[x][y-1]
					y2 = image[x][y+1]

					pixel_ave = float((x1+x2+y1+y2) / 4)
					med = [xy,x1,x2,y1,y2]
					pixel_med =  med[int(len(med)/2)]
					if int(pixel_ave+thres) > xy and int(pixel_ave-thres) < xy:
						img.append(xy)
					else: img.append(0)
				except: img.append(0)
		self.queue.put(img)

	def quad_images(self, func, num=0):
		images = os.listdir(self.prepared_path)

		amount = 5
		while num < amount:
			image = images.pop()
			image_path = os.path.join(self.prepared_path, image)
			with Image.open(image_path) as img:
				red_data = np.array(img.getdata(0)).reshape((self.width, self.height))
				green_data = np.array(img.getdata(1)).reshape((self.width, self.height))
				blue_data = np.array(img.getdata(2)).reshape((self.width, self.height))

				print("Start, {}".format(image))
				if func.lower() == "average":
					Process(target=self.quad_average_image, args=(red_data,)).start()
					Process(target=self.quad_average_image, args=(green_data,)).start()
					Process(target=self.quad_average_image, args=(blue_data,)).start()
				elif func.lower() == "median":
					Process(target=self.quad_median_image, args=(red_data,)).start()
					Process(target=self.quad_median_image, args=(green_data,)).start()
					Process(target=self.quad_median_image, args=(blue_data,)).start()
				elif func.lower() == "noise":
					Process(target=self.quad_noise_image, args=(red_data,)).start()
					Process(target=self.quad_noise_image, args=(green_data,)).start()
					Process(target=self.quad_noise_image, args=(blue_data,)).start()

				try:
					r_data = self.queue.get()
					g_data = self.queue.get()
					b_data = self.queue.get()
				except: sys.exit()
				print("Done")

			merged_data = [(x) for x in zip(r_data, g_data, b_data)]
			new_img = Image.new('RGB', (self.width, self.height)) # RGB
			new_img.putdata(merged_data)
			file_name = 'quad_{}.jpg'.format(num+1)
			file_path = os.path.join(self.finished_path, file_name)
			new_img.save(file_path, "JPEG")
			num += 1

	def quad_median_images(self):
		self.quad_images("median")

	def quad_average_images(self):
		self.quad_images("average")

	def quad_noise_images(self):
		self.quad_images("noise")

	def average_image(self, data):
		data = [int(sum(x)/len(x)) for x in zip(*data)]
		self.queue.put(data)

	def median_image(self, data):
		data = [sorted(x)[int(len(x)/2)] for x in zip(*data)]
		self.queue.put(data)

	def images(self, func, amount, span=5):
		images = os.listdir(self.prepared_path)

		red_data = []
		green_data = []
		blue_data = []

		amount = len(images)
		file_num, num = 0, 0
		while num < amount:
			image = images.pop()
			image_path = os.path.join(self.prepared_path, image)
			print(image)
			with Image.open(image_path) as img:
				red_data.append(list(img.getdata(0)))
				green_data.append(list(img.getdata(1)))
				blue_data.append(list(img.getdata(2)))

			num += 1
			if num % span == 0:
				file_num += 1

				print("Start")
				if func.lower() == "average":
					Process(target=self.average_image, args=(red_data,)).start()
					Process(target=self.average_image, args=(green_data,)).start()
					Process(target=self.average_image, args=(blue_data,)).start()
				elif func.lower() == "median":
					Process(target=self.median_image, args=(red_data,)).start()
					Process(target=self.median_image, args=(green_data,)).start()
					Process(target=self.median_image, args=(blue_data,)).start()

				try:
					ave_red = self.queue.get()
					ave_green = self.queue.get()
					ave_blue = self.queue.get()
				except: sys.exit()
				print("Done")

				del red_data
				del green_data
				del blue_data

				red_data = []
				green_data = []
				blue_data = []

				merged_data = [(x) for x in zip(ave_red, ave_green, ave_blue)]
				stacked = Image.new('RGB', (self.width, self.height))
				stacked.putdata(merged_data)
				file_name = 'prepared_{}.JPG'.format(file_num)
				file_path = os.path.join(self.finished_path, file_name)
				stacked.save(file_path, 'JPEG')

	def median_images(self, amount=1, span=5):
		self.images("median",amount, span)

	def average_images(self, amount=1, span=5):
		self.images("average",amount, span)

	def clean_folder(self, prefix):
		files = os.listdir(self.prepared_path)
		for file in files:
			if not file.startswith(prefix):
				file_path = os.path.join(self.prepared_path, file)
				os.remove(file_path)

	def exit(self):
		self.queue.close()
		sys.exit()

if __name__ == "__main__":
	t = Image_api()
	t.change_size(3264, 1836)
	#t.crop_images()
	#t.scale_images()
	t.median_images(amount=4,span=4)
	#t.average_images(amount=4, span=4)
	t.exit()