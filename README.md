# #Slack Chat App
It is a real time online messaging service similar to 'slack' based on Flask-SocketIO with features including private as well as group messaging. A user will be remembered by his unique username. After logging in, user can join into an already created channel by selecting from channels list or can create a new one. User can now chat with others in that channel. 
## Login Page
![alt text](https://github.com/rodeketan/chat_app/blob/main/Images/Screenshot%20from%202021-06-16%2004-17-58.png)
## Chat Window
![alt text](https://github.com/rodeketan/chat_app/blob/main/Images/Screenshot%20from%202021-06-16%2004-13-52.png)
## Private Chat Feature
![alt text](https://github.com/rodeketan/chat_app/blob/main/Images/Screenshot%20from%202021-06-16%2004-16-12.png)


I have added an additional feature in this chat application where by a user can chat privately with another user in the same channel. This chat will not be shown in group chat window.

1. **application.py**- This is the main application file.

2. **templates folder**- This folder contains 5 html files, they all inherit layout.html file which is also contained in this folder.

3. **static folder**- This folder contains channel.js file which is linked to channel.html file contained in templates. A style.css file is also there which is linked to layout.html.
