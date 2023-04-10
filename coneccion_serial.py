import sys
import serial
import serial.tools.list_ports
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
import time

class SerialGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('R.ico'))
        self.setWindowTitle("T01_Remote_Switch_Controller")
        self.serialPort = None
        self.setFixedSize(350,480)

        # Creamos estilos de fuentes para las labels
        titlesFont = QFont("Arial",12)
        titlesFont.setBold(True)
        
        serialStatusFont = QFont("Arial",10)
        serialStatusFont.setBold(True)
        
        checkboxFont = QFont("Arial",10)
        checkboxFont.setBold(False)
        
        # Creamos una label fixeada para la seleccion del puerto serial
        self.selectPort = QLabel("Select a Serial Port:")
        self.selectPort.setFont(titlesFont)
        
        # Crear una lista desplegable para los puertos serie
        self.portList = QComboBox()
        self.portList.setFont(checkboxFont)
        self.refresh_ports()
        
        # Crear un botón para conectar al puerto serie seleccionado
        self.connectButton = QPushButton("Connect")
        self.connectButton.clicked.connect(self.connect_serial)
        self.connectButton.setFont(checkboxFont)

        # Crear un botón para desconectar el puerto serie actualmente conectado
        self.disconnectButton = QPushButton("Disconnect")
        self.disconnectButton.clicked.connect(self.disconnect_serial)
        self.disconnectButton.setFont(checkboxFont)

        # Deshabilitar el botón de desconectar
        self.disconnectButton.setEnabled(False)

        # Crear un label para mostrar el estado de la conexión
        
        self.statusLabelFiexd = QLabel("Connection status:")
        self.statusLabelFiexd.setFont(serialStatusFont)
        self.statusLabel = QLabel("Disconnected")
        self.statusLabel.setFont(serialStatusFont)
        self.statusLabel.setStyleSheet("color: red")

        # Crear checkboxes para seleccionar los switches
        self.checkbox0 = QCheckBox('V_BAT Switch')
        self.checkbox0.stateChanged.connect(lambda checked: self.send_message(checked, "0") )
        self.checkbox0.setFont(checkboxFont)
        
        self.checkbox1 = QCheckBox('IGNITION Switch')
        self.checkbox1.stateChanged.connect(lambda checked: self.send_message(checked, "1") )
        self.checkbox1.setFont(checkboxFont)
        
        self.checkbox2 = QCheckBox('ACCESS Switch')
        self.checkbox2.stateChanged.connect(lambda checked: self.send_message(checked, "2") )
        self.checkbox2.setFont(checkboxFont)
        
        self.checkbox3 = QCheckBox('Switch PCAN Channel')
        self.checkbox3.stateChanged.connect(lambda checked: self.send_message(checked, "3") )
        self.checkbox3.setFont(checkboxFont)
        
        # Crear un label para mostrar en que canal esta el PCAN
        self.pcan_channel = QLabel("PCAN Connected to Channel 0")
        self.pcan_channel.setEnabled(False)
        
        self.checkbox4 = QCheckBox('SHORT FOR CAN BUS 0')
        self.checkbox4.stateChanged.connect(lambda checked: self.send_message(checked, "4") )
        self.checkbox4.setFont(checkboxFont)
        
        self.checkbox5 = QCheckBox('SHORT FOR CAN BUS 1')
        self.checkbox5.stateChanged.connect(lambda checked: self.send_message(checked, "5") )
        self.checkbox5.setFont(checkboxFont)
        
        self.checkbox0.setEnabled(False)
        self.checkbox1.setEnabled(False)
        self.checkbox2.setEnabled(False)
        self.checkbox3.setEnabled(False)                        
        self.checkbox4.setEnabled(False)
        self.checkbox5.setEnabled(False)

        

        # Crear un layout vertical y agregar los widgets
        outerLayout = QVBoxLayout()
        
        # Crear un layout para la seleccion del puerto Serial a conectar
        serialConnectionGB = QGroupBox()
        serialConnectionLayout = QVBoxLayout()        
        serialConnectionGB.setLayout(serialConnectionLayout)
        
        serialConnectionLayout.addWidget(self.selectPort)
        serialConnectionLayout.addWidget(self.portList)
        serialConnectionLayout.addWidget(self.connectButton)
        serialConnectionLayout.addWidget(self.disconnectButton)
        serialConnectionLayout.addWidget(self.statusLabelFiexd)
        serialConnectionLayout.addWidget(self.statusLabel)
        
        # Crear un layout para las checkboxes
        checkboxesGB = QGroupBox()
        checkboxesLayout = QVBoxLayout()
        checkboxesGB.setLayout(checkboxesLayout)
        
        checkboxesLayout.addWidget(self.checkbox0)
        checkboxesLayout.addSpacing(10)
        checkboxesLayout.addWidget(self.checkbox1)
        checkboxesLayout.addSpacing(10)
        checkboxesLayout.addWidget(self.checkbox2)
        checkboxesLayout.addSpacing(10)
        checkboxesLayout.addWidget(self.checkbox4)
        checkboxesLayout.addSpacing(10)
        checkboxesLayout.addWidget(self.checkbox5)
        
        #Crear un layout solo para seleccionar a que canal se conecta el PCAN
        checkboxesPcanGB = QGroupBox()
        checkboxesPcanLayout = QVBoxLayout()
        checkboxesPcanGB.setLayout(checkboxesPcanLayout)
        checkboxesPcanLayout.addWidget(self.checkbox3)
        checkboxesPcanLayout.addWidget(self.pcan_channel)
        checkboxesPcanLayout.addSpacing(10)
        
        # Acomodar todas las layout en el outerlayout
        outerLayout.addWidget(serialConnectionGB)
        outerLayout.addSpacing(5)
        outerLayout.addWidget(checkboxesPcanGB)
        outerLayout.addSpacing(5)
        outerLayout.addWidget(checkboxesGB)
        
        self.setContentsMargins(10,10,10,10)
        self.setLayout(outerLayout)     
        
        # Crear un temporizador para actualizar la lista de puertos cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_ports)
        self.timer.start(1000)

    def send_message(self, state, id_rel):
        message = ''
        if (id_rel == "0"):
            if state == Qt.Checked:
                message = '0'
            else:
                message = '6'
                
        if (id_rel == "1"):
            if state == Qt.Checked:
                message = '1'
            else:
                message = '7'
                
        if (id_rel == "2"):
            if state == Qt.Checked:
                message = '2'
            else:
                message = '8'  
                  
        if (id_rel == "3"):
            if state == Qt.Checked:
                message = '3'
                self.pcan_channel.setText("PCAN Connected to Channel 1")
            else:
                message = '9'
                self.pcan_channel.setText("PCAN Connected to Channel 0")
        
        if (id_rel == "4"):
            if state == Qt.Checked:
                message = '4'
            else:
                message = ':'
                
        if (id_rel == "5"):
            if state == Qt.Checked:
                message = '5'
            else:
                message = ';'  
                
                
        # Envío del mensaje al dispositivo serial
        self.serialPort.write(message.encode('utf-8'))

        
    def refresh_ports(self):
        
        # Obtener la lista de puertos serie disponibles
        ports = serial.tools.list_ports.comports()

        # Obtener los puertos actualmente en la lista desplegable
        current_ports = [self.portList.itemText(i) for i in range(self.portList.count())]

        # Verificar si ha habido cambios en la lista de puertos
        if set(current_ports) != set([port.device for port in ports]):
            # Limpiar la lista desplegable
            self.portList.clear()

            # Agregar los puertos a la lista desplegable
            for port in ports:
                self.portList.addItem(port.device)

    def connect_serial(self):
        # Obtener el puerto serie seleccionado
        self.port = self.portList.currentText()

        # Conectar al puerto serie seleccionado
        try:
            self.serialPort = serial.Serial(self.port)
            self.statusLabel.setText("Connected to the port {}".format(self.port))
            self.statusLabel.setStyleSheet("color: green")
            # Habilitar el botón de desconectar y deshabilitar el botón de conectar
            self.disconnectButton.setEnabled(True)
            self.connectButton.setEnabled(False)
            
            time.sleep(2)
            
            self.checkbox0.setEnabled(True)
            self.checkbox1.setEnabled(True)
            self.checkbox2.setEnabled(True)
            self.checkbox3.setEnabled(True)                        
            self.checkbox4.setEnabled(True)
            self.checkbox5.setEnabled(True)
            
            self.pcan_channel.setEnabled(True)

        except serial.SerialException:
            self.statusLabel.setText("Could not connect to port {}".format(self.port))
            self.statusLabel.setStyleSheet("color: red")

    def disconnect_serial(self):
        # Desconectar el puerto serie actualmente conectado
        self.checkbox0.setEnabled(False)
        self.checkbox1.setEnabled(False)
        self.checkbox2.setEnabled(False)
        self.checkbox3.setEnabled(False)                        
        self.checkbox4.setEnabled(False)
        self.checkbox5.setEnabled(False)
        self.pcan_channel.setEnabled(False)
        
        self.checkbox0.setCheckState(0)
        self.checkbox1.setCheckState(0)
        self.checkbox2.setCheckState(0)
        self.checkbox3.setCheckState(0)
        self.checkbox4.setCheckState(0)
        self.checkbox5.setCheckState(0)
        
        if self.serialPort is not None:
            self.serialPort.close()
            self.serialPort = None
            self.statusLabel.setText("Disconnected")
            self.statusLabel.setStyleSheet("color: red")
            
            # Habilitar el botón de conectar y deshabilitar el botón de desconectar
            self.connectButton.setEnabled(True)
            self.disconnectButton.setEnabled(False)
            
            

    def closeEvent(self, event):
        # Cerrar el puerto serie si está conectado antes de salir de la aplicación
        if self.serialPort is not None:
            self.disconnect_serial()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SerialGUI()
    gui.show()
    sys.exit(app.exec_())