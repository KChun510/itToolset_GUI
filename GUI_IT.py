# Multi-frame tkinter application v2.3
import tkinter as tk
import requests
from tkinterdnd2 import DND_FILES, TkinterDnD

# Global token (bearer token) used across classes. "Variable Defined in Auth() function"
Jamf_token = ''

# The first class is our "SampleApp" this opens up app window/ is root
class SampleApp(tk.Tk): # tk.Tk, "SampleApp" is the room frame inheritce tk.Tk
	def __init__(self, title, size):
		tk.Tk.__init__(self)
		self._frame = None
		self.title(title)
		self.geometry(f"{size[0]}x{size[1]}")
		self.minsize(size[0], size[1])
		self.switch_frame(StartPage)

	def switch_frame(self, frame_class):
		"""Destroys current frame and replaces it with a new one."""
		new_frame = frame_class(self)
		if self._frame is not None:
		    self._frame.destroy()
		self._frame = new_frame
		self._frame.pack()

class StartPage(tk.Frame): # tk.Frame, "start_page" inheritce a frame class of tk
    def __init__(self, master): # The construcotr of startpage
        tk.Frame.__init__(self, master) # The frame is a child of the master class

        # Define our widgets
        start_label = tk.Label(self, text="Sign-In (Jamf Authorization)")		
        to_page_one = tk.Button(self, text="Open page one",command=lambda: master.switch_frame(PageOne))
        to_page_two = tk.Button(self, text="Open page two",command=lambda: master.switch_frame(PageTwo))

        username_box = tk.Entry(self, text='')
        password_box = tk.Entry(self, text='', show="*")
        sumbit_button = tk.Button(self, text="Get_user_input", command=lambda: self.Auth(username_box, password_box, master))
        
        # Define placement grid
        self.columnconfigure((0,1,2), weight = 1 , uniform = 'a')
        self.rowconfigure((0,1,2,3,4), weight = 1, uniform = 'a')

        # Place widgets on grid
        # Frame Label
        start_label.grid(row = 0, column = 1, sticky = 'nswe')

        # Username box
        tk.Label(self, text="User Name:").grid(row = 1, column = 0, sticky = 'nswe', padx=(100,0))
        username_box.grid(row = 1, column = 1, sticky = 'nswe')


        # Password box
        tk.Label(self, text="Password:").grid(row = 2, column = 0, sticky = 'nswe', padx=(100,0))
        password_box.grid(row = 2, column = 1, sticky = 'nswe')


        sumbit_button.grid(row = 3, column = 1 ,sticky = 'nswe')
        

    def Auth(self, username_box, password_box, master) -> int:
    	global Jamf_token
    	print("function was called")
    	user_name = username_box.get()
    	pass_word = password_box.get()

    	url = "https://creditkarmastaging.jamfcloud.com/api/v1/auth/token" # End point to generate bearer token
    	header = {"accept": "application/json"}
    	response = requests.post(url=url, headers=header, auth=(user_name, pass_word), timeout=10)

    	if response.status_code == 200:
    		user_name = ''
    		pass_word = ''
    		response_json = response.json() # Get the respoce and format it into json
    		bearer_token = response_json['token']
    		print("Auth succefull")
    		master.switch_frame(PageOne)
    		token = bearer_token
    		return 0
    	else:
    		print(f"Error: {response.status_code} Failed to authenticate.")
    		return 0 

   



class PageOne(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		# Define our widegts
		Page_label = tk.Label(self, text = "Available Tools")
		Jamf_label = tk.Label(self, text = "Jamf Tools")
		Jamf_func_button = tk.Button(self, text = "Get system OS version", command=lambda: master.switch_frame(get_os_vers))
		
		Jira_label = tk.Label(self, text = "Jira Tools" )
		Jira_func_button = tk.Button(self, text = "Coming Soon")


		self.columnconfigure((0,1,2), weight = 1 , uniform = 'a')
		self.rowconfigure((0,1,2,3,4), weight = 1, uniform = 'a')

		Page_label.grid(row = 0, column = 1, sticky = 'nswe')
		
		Jamf_label.grid(row = 1, column = 1, sticky = 'nswe', pady=(25,0))
		Jamf_func_button.grid(row = 2, column = 1, sticky = 'nswe')

		Jira_label.grid(row = 3, column = 1, sticky = 'nswe', pady=(25,0))
		Jira_func_button.grid(row = 4, column = 1, sticky = 'nswe')

	

class get_os_vers(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)


	

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = SampleApp("IT Internal Tools", (600, 600))
    app.mainloop()
