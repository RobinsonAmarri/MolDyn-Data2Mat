from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QComboBox, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import matplotlib.pyplot as plt
import sys
import time 

# class
class Home(QWidget):
    # Initializes the Home class (Constructor)
    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings()
        self.button_clicked()


    # App object and design. 
    #I want to ask for the data file, then convert it to 
    def initUI(self):
        self.browse_button = QPushButton("Select File", self)
        self.filetype = QComboBox(self)
        self.filetype.addItems(["XVG", "CSV", "JSON"])
        self.inputfile = QTextEdit(self)
        self.inputfile.setPlaceholderText("Selected file path...")
        self.inputfile.setReadOnly(True)  # Make the input file read-only
        self.graphtitle = QTextEdit(self)
        self.graphtitle.setPlaceholderText("Enter graph title...")
        self.xaxis = QTextEdit(self)
        self.xaxis.setPlaceholderText("Enter X-axis label...")
        self.yaxis = QTextEdit(self)
        self.yaxis.setPlaceholderText("Enter Y-axis label...")
        self.submit_button = QPushButton("Graph")
        self.reset_button = QPushButton("Reset")
        self.title = QLabel("Data2Graph!", self)
        self.title.setFont(QFont("Courier New", 20))

        #gives a variable to the figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        # creating a Vertical Box layout
         
       
         
        # setting layout to the main window




        self.master = QHBoxLayout()
        layout = QVBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

         # adding tool bar to the layout
        layout.addWidget(self.toolbar)
         
        # adding canvas to the layout
        layout.addWidget(self.canvas)
         
         
        # setting layout to the main window

        col1.addWidget(self.title)
        col1.addWidget(self.browse_button)
        col1.addWidget(self.inputfile)
        col1.addWidget(self.filetype)
        col1.addWidget(self.graphtitle)
        col1.addWidget(self.xaxis)
        col1.addWidget(self.yaxis)
        col1.addWidget(self.submit_button)
        col1.addWidget(self.reset_button)

        #col2.addWidget(QLabel(""))
        #col2.addWidget(self.submit_button)
        #col2.addWidget(self.reset_button)






        self.master.addLayout(col1, 30)
        #self.master.addLayout(col2, 10)
        self.master.addLayout(layout, 70)


        self.setLayout(self.master)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                color: #333;
            }
            QPushButton {
                background-color: #ADD8E6;
                color: #333;
                border: 1px solid #fff;
                border-radius: 10px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #3399ff;
            }
        """)

      
        pass

    def settings(self):
        self.setWindowTitle("Data2Graph")
        self.setGeometry(250, 250, 800, 600)  # Set the window size and position
        pass

    def button_clicked(self):
        self.submit_button.clicked.connect(self.submit_button_clicked)
        self.reset_button.clicked.connect(self.reset)
        self.browse_button.clicked.connect(self.choose_file)
        pass

    def choose_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Data File", "", "All Files (*)")
        if filename:
            self.inputfile.setText(filename)

    def reset(self):
        self.inputfile.clear()
        self.graphtitle.clear()
        self.xaxis.clear()
        self.yaxis.clear()
        self.figure.clear()  # Clear the figure
        self.canvas.draw()  # Redraw the canvas
        pass

    def submit_button_clicked(self):
        filename = self.inputfile.toPlainText().strip()
        print(f"Selected file: {filename}")
        filetype = self.filetype.currentText().strip()
        print(f"Selected file type: {filetype}")
        title = self.graphtitle.toPlainText().strip()
        print(f"Graph title: {title}")
        xlabel = self.xaxis.toPlainText().strip()
        print(f"X-axis label: {xlabel}")
        ylabel = self.yaxis.toPlainText().strip()
        print(f"Y-axis label: {ylabel}")
       
        if not filename:
            print("No file selected.")
            return
        
        if filetype == "XVG":
            data = []
            with open(filename) as f:
                for line in f:
                    if line.startswith(('@', '#')):
                        continue
                    data.append([float(x) for x in line.split()])
            data = np.array(data)
            if data.shape[1] >= 2:
                ax = self.figure.add_subplot(111)
                ax.plot(data[:, 0], data[:, 1])
                ax.set_title(title)
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                ax.grid()
                ax.legend()
                self.canvas.draw()
            else:
                print("XVG file does not have enough columns to plot.")
        else:
            print("Only XVG plotting is implemented.")
       

        

       


if __name__ == '__main__': # Main function to run the application
    app = QApplication([])
    home = Home()
    home.show()
    app.exec_()
