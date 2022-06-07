from pynput.mouse import Button, Controller as mouse_controller
from pynput.keyboard import Key, Controller as key_controller
import PIL.ImageGrab,os,time,math

mouse = mouse_controller()
keyboard = key_controller()

wait_before_next_page = 3
good = False

while not good:
	try:
		unit_num,clicks,reverse =list(map(int,input("Enter unit,pages and reverse state (ex: 5 26 1):").split(' ')))
	except ValueError:
		print('One of your inputs is missing or invalid')
	else:
		good =True

try:
	path = f"C:/Users/user/Desktop/Units/{unit_num}/"
	os.mkdir(path) # create a directory with the given unit number
except FileExistsError:
	pass

time.sleep(3)

x,y = mouse.position # get current mouse position
keyboard.press(Key.f11) # get in full screen mode
keyboard.release(Key.f11) # release the key
time.sleep(2)

def check_duplicated(location):
	'''loop through images and delete the '_more' ones if they have the same size of the original image'''
	for filename in os.listdir(location):
		if '_more' in filename:
			file_size =math.floor(os.path.getsize(location+filename)/1024) # get the file size of the _more version
			origin_size= math.floor(os.path.getsize(location+filename.split('_')[0]+'.png')/1024) # get the file size of the original version
			if file_size ==origin_size or abs(file_size - origin_size) <=4:
				os.remove(location+filename) # remove the _more file
	keyboard.press(Key.f11) # exit full screen mode
	keyboard.release(Key.f11) # release the key

def scroll(x,y):
	'''get the mouse up and click it then a space bar press to scroll down and return the shot image'''
	mouse.position = (x, y) # go up with the mouse
	mouse.click(Button.left, 1) # click to enable scrollling
	keyboard.press(Key.space) # press space to scroll down
	keyboard.release(Key.space) # release the key
	time.sleep(1)
	img = PIL.ImageGrab.grab() # get a screenshot (scrolled)
	return img

if reverse ==1: # if the order of the pages is reversed
	for num in range(1,clicks +1,1):
		img = PIL.ImageGrab.grab() # get a screenshot (original) 
		img.save(path+f"{clicks+1 -num}.png") # save the image in the directory
		if num != 1: # if this isn't the first iteration
			img = scroll(x-5,y-50)
			img.save(path+f"{str(clicks+1 -num)+ '_more'}.png") # add _more to distinguish the image later 
			mouse.position = (x -50, y) # revert to the original position
			mouse.click(Button.left, 1) # go to next page
		else: # for first iteration
			mouse.click(Button.left, 1) 
			mouse.position = (x -50, y)
		time.sleep(wait_before_next_page)

else: # if the order of the pages is normal
	for num in range(1,clicks +1,1):
		img = PIL.ImageGrab.grab()
		img.save(path +f"{num}.png")
		img = scroll(x,y-50)
		img.save(path+f"{str(num)+ '_more'}.png")
		mouse.position = (x, y)
		mouse.click(Button.left, 1)
		time.sleep(wait_before_next_page)

check_duplicated(path)
