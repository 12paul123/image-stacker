import sys
sys.path.append('C:\\Users\\paul1\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\cv2')
import cv2
import PIL.Image
from PIL import ImageFilter

def main():
	video_folder = "video"

	#del_folders("video_f")
	#shutil.copytree(video_folder, "video_f")

	# run cropping function
	print("start cutting and framing...")
	#os.chdir("video_f")
	frame_images()
	#clean_folder(prefix_to_save="frame") # delete uncropped originals

def del_folders(name):
	"""If a folder with a named prefix exists in directory, delete it."""
	contents = os.listdir()
	for item in contents:
		if os.path.isdir(item) and item.startswith(name):
			answer = input("Do you want to delete {} folder.").lower()
			if answer == "yes":
				shutil.rmtree(item)

def clean_folder(prefix_to_save):
	"""Delete all files in folder except those with a names prefix."""
	files = os.listdir()
	for file in files:
		if not file.startswith(prefix_to_save):
			os.remove(file)

def frame_images():
	"""Frame images based on the cut"""
	video = cv2.VideoCapture("video.mp4")

	Frames = []

	for n, image in video.read():
		print(n, image)

if __name__ == '__main__':
	main()