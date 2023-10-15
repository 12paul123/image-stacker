import os, sys
from PIL import Image, ImageOps
import shutil

def average():
	frames_folder = "cropped"

	# prepare files & folders
	del_folders("prepared")
	shutil.copytree(frames_folder, "prepared")

	# list images in directory
	os.chdir('prepared')
	images = os.listdir()

	# Set amount images
	amount = len(images)
	# Set stack amount
	span = len(images)

	print("\nstart stacking images...")
	# loop through images and extract RGB channels as separate lists
	red_data = []
	green_data = []
	blue_data = []

	num, file_num = 0, 0
	while num < amount:
		image = images.pop()
		with Image.open(image) as img:
			if num == 0: # get size of 1st cropped image
				img_size = img.size # width-height tuple to use later
			red_data.append(list(img.getdata(0)))
			green_data.append(list(img.getdata(1)))
			blue_data.append(list(img.getdata(2)))

		print(num)

		num += 1
		if num % span == 0:
			file_num += 1
			print("JPEG _{} Created".format(file_num))

			ave_red = [round(sum(x) / len(red_data)) for x in zip(*red_data)]
			ave_green = [round(sum(x) / len(green_data)) for x in zip(*green_data)]
			ave_blue = [round(sum(x) / len(blue_data)) for x in zip(*blue_data)]

			del red_data
			del green_data
			del blue_data

			red_data = []
			green_data = []
			blue_data = []
			
			merged_data = [(x) for x in zip(ave_red, ave_green, ave_blue)]
			stacked = Image.new('RGB', (img_size))
			stacked.putdata(merged_data)

			file_name = 'prepared_{}.tif'.format(file_num)
			stacked.save(file_name, 'TIFF')

		elif span == amount and num % (span-1) == 0:

			ave_red = [ x[int(len(x)/2)] for x in zip(*red_data)]
			ave_blue = [ x[int(len(x)/2)] for x in zip(*blue_data)]
			ave_green = [ x[int(len(x)/2)] for x in zip(*green_data)]

			merged_data = [(x) for x in zip(ave_red, ave_green, ave_blue)]
			stacked = Image.new('RGB', (img_size))
			stacked.putdata(merged_data)
			stacked.show()

			os.chdir('..')
			stacked.save('jupiter_average.tif', 'TIFF')

	clean_folder(prefix_to_save="prepared")
	images = os.listdir()

	del red_data
	del green_data
	del blue_data

	red_data = []
	green_data = []
	blue_data = []

	for image in images:
		with Image.open(image) as img:
			if image == images[0]:
				img_size = img.size
			red_data.append(list(img.getdata(0)))
			green_data.append(list(img.getdata(1)))
			blue_data.append(list(img.getdata(2)))

	ave_red = [round(sum(x) / len(red_data)) for x in zip(*red_data)]
	ave_blue = [round(sum(x) / len(blue_data)) for x in zip(*blue_data)]
	ave_green = [round(sum(x) / len(green_data)) for x in zip(*green_data)]

	merged_data = [(x) for x in zip(ave_red, ave_green, ave_blue)]
	stacked = Image.new('RGB', (img_size))
	stacked.putdata(merged_data)
	stacked.show()

	os.chdir('..')
	stacked.save('jupiter_stacked.tif', 'TIFF')

def median():
	frames_folder = "cropped"

	# prepare files & folders
	del_folders("prepared")
	shutil.copytree(frames_folder, "prepared")

	# list images in directory
	os.chdir('prepared')
	images = os.listdir()

	# Set amount images
	amount = len(images)
	# set stack amount
	span = 8

	print("\nstart stacking images...")
	# loop through images and extract RGB channels as separate lists
	red_data = []
	green_data = []
	blue_data = []

	num, file_num = 0, 0
	while num < amount:
		image = images.pop()
		with Image.open(image) as img:
			if num == 0: # get size of 1st cropped image
				img_size = img.size # width-height tuple to use later
			red_data.append(list(img.getdata(0)))
			green_data.append(list(img.getdata(1)))
			blue_data.append(list(img.getdata(2)))

		num += 1
		if num % span == 0:
			file_num += 1
			print("JPEG _{} Created".format(file_num))

			ave_red = [ x[int(len(x)/2)] for x in zip(*red_data)]
			ave_blue = [ x[int(len(x)/2)] for x in zip(*blue_data)]
			ave_green = [ x[int(len(x)/2)] for x in zip(*green_data)]

			del red_data
			del green_data
			del blue_data

			red_data = []
			green_data = []
			blue_data = []

			merged_data = [(x) for x in zip(ave_red, ave_green, ave_blue)]
			stacked = Image.new('RGB', (img_size))
			stacked.putdata(merged_data)

			file_name = 'prepared_{}.tif'.format(file_num)
			stacked.save(file_name, 'TIFF')

		elif span == amount and num % span-1 == 0:

			ave_red = [ x[int(len(x)/2)] for x in zip(*red_data)]
			ave_blue = [ x[int(len(x)/2)] for x in zip(*blue_data)]
			ave_green = [ x[int(len(x)/2)] for x in zip(*green_data)]

			merged_data = [(x) for x in zip(ave_red, ave_green, ave_blue)]
			stacked = Image.new('RGB', (img_size))
			stacked.putdata(merged_data)
			stacked.show()

			os.chdir('..')
			stacked.save('jupiter_median.tif', 'TIFF')

	clean_folder(prefix_to_save="prepared")
	images = os.listdir()

	del red_data
	del green_data
	del blue_data

	red_data = []
	green_data = []
	blue_data = []

	for image in images:
		with Image.open(image) as img:
			if image == images[0]:
				img_size = img.size
			red_data.append(list(img.getdata(0)))
			green_data.append(list(img.getdata(1)))
			blue_data.append(list(img.getdata(2)))

	ave_red = [ x[int(len(x)/2)] for x in zip(*red_data)]
	ave_blue = [ x[int(len(x)/2)] for x in zip(*blue_data)]
	ave_green = [ x[int(len(x)/2)] for x in zip(*green_data)]

	merged_data = [(x) for x in zip(ave_red, ave_green, ave_blue)]
	stacked = Image.new('RGB', (img_size))
	stacked.putdata(merged_data)
	stacked.show()

	os.chdir('..')
	stacked.save('jupiter_median.tif', 'TIFF')

def del_folders(name):
	"""If a folder with a named prefix exists in directory, delete it."""
	contents = os.listdir()
	for item in contents:
		if os.path.isdir(item) and item.startswith(name):
			answer = input("Do you want to delete {} folder: ".format(item)).lower()
			if answer == "yes":
				shutil.rmtree(item)

def clean_folder(prefix_to_save):
	"""Delete all files in folder except those with a names prefix."""
	files = os.listdir()
	for file in files:
		if not file.startswith(prefix_to_save):
			os.remove(file)

average()