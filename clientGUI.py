import tkinter as tk
import tkinter.ttk as ttk
import main as m

FONT = ("Verdana",12)
TITLE_FONT = ("Verdana",16)
# Based off of my own application in Tkinter previously
class bakerClient(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        # Set title and good inital window size
        tk.Tk.wm_title(self, "BakerAI")
        self.geometry("1000x700")

        # Container is parent frame, containing all frames
        parent = tk.Frame(self)
        parent.pack(side="top",fill="both",expand=True)
        # Format: min size, weight is z index
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        # Main frame layout: where content is stored 
        mainFrame = tk.Frame(parent)
        mainFrame.pack(side="top",fill="both",expand=True)
        for i in range(9):
            mainFrame.grid_rowconfigure(index=i, weight=1)
            mainFrame.grid_columnconfigure(index=i, weight=1)
        self.loaded_clf = m.load_sentiment_analysis()[0]
        
        # Elements of the main frame #
        # Title
        title = tk.Label(mainFrame, text="Welcome to Sakura's very own BakerAI!", font=TITLE_FONT)
        title.grid(row=1,column=1,columnspan=7)
        # What we will change to show output
        self.outputBox = tk.Text(mainFrame, font=FONT)
        self.outputBox.grid(row=3, column=1, columnspan=7, rowspan=1, sticky="")
        self.outputBox.insert(tk.END,"BakerAI: Hey there! How can I help you? \n")
        self.outputBox.configure(state="disabled")
        scrollbar = tk.Scrollbar(self)
        scrollbar.config(command = self.outputBox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.outputBox.config(yscrollcommand=scrollbar.set)

        # Input related items
        entryLabel = tk.Label(mainFrame, text="Enter your text below!", font=FONT)
        entryLabel.grid(row=4, column=2, columnspan=2, sticky="")
        self.userInput = tk.Entry(mainFrame)
        self.userInput.grid(row=5, column=1, columnspan=4, sticky="EW")
        sendButton = tk.Button(mainFrame, text="Send message", command=lambda: self.getResponse())
        sendButton.grid(row=5, column=6, columnspan=1, sticky="EW")
        self.userInput.bind("<Return>", lambda x: self.getResponse())

    def getResponse(self):
        # Get user message
        userMessage = self.userInput.get()
        # Ignore empty messages
        if userMessage == "":
            return
        # Clear the user input
        self.userInput.delete(0, "end")
        # Get our reply
        reply = "BakerAI: " + m.getFinalOutput(self.loaded_clf,userMessage) + "\n"
        # Send reply to client
        storedUserMessage = "You: " + userMessage + "\n"
        self.outputBox.configure(state="normal")
        self.outputBox.insert(tk.END, storedUserMessage) 
        self.outputBox.insert(tk.END, reply) 
        self.outputBox.configure(state="disabled")


if __name__ == '__main__':
    client = bakerClient()
    client.mainloop()

