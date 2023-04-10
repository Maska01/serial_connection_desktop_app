import sys
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QLabel, QVBoxLayout, QCheckBox
import time

class SerialGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Serial GUI")
        self.serial_port = None

        # Crear una lista desplegable para los puertos serie
        self.port_list = QComboBox()
        self.refresh_ports()
        
        # Crear un botón para conectar al puerto serie seleccionado
        self.connect_button = QPushButton("Conectar")
        self.connect_button.clicked.connect(self.connect_serial)

        # Crear un botón para desconectar el puerto serie actualmente conectado
        self.disconnect_button = QPushButton("Desconectar")
        self.disconnect_button.clicked.connect(self.disconnect_serial)

        # Deshabilitar el botón de desconectar
        self.disconnect_button.setEnabled(False)

        self.checkbox_0 = QCheckBox('Relevador 0')
        self.checkbox_0.stateChanged.connect(lambda checked: self.send_message(checked, "0") )
        
        self.checkbox_1 = QCheckBox('Relevador 1')
        self.checkbox_1.stateChanged.connect(lambda checked: self.send_message(checked, "1") )
        
        self.checkbox_2 = QCheckBox('Relevador 2')
        self.checkbox_2.stateChanged.connect(lambda checked: self.send_message(checked, "2") )
        
        self.checkbox_3 = QCheckBox('Relevador 3')
        self.checkbox_3.stateChanged.connect(lambda checked: self.send_message(checked, "3") )
        
        self.checkbox_4 = QCheckBox('Relevador 4')
        self.checkbox_4.stateChanged.connect(lambda checked: self.send_message(checked, "4") )
        
        self.checkbox_5 = QCheckBox('Relevador 5')
        self.checkbox_5.stateChanged.connect(lambda checked: self.send_message(checked, "5") )
        
        self.checkbox_0.setEnabled(False)
        self.checkbox_1.setEnabled(False)
        self.checkbox_2.setEnabled(False)
        self.checkbox_3.setEnabled(False)                        
        self.checkbox_4.setEnabled(False)
        self.checkbox_5.setEnabled(False)

        # Crear un label para mostrar el estado de la conexión
        self.status_label = QLabel("Desconectado")

        # Crear un layout vertical y agregar los widgets
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Selecciona el puerto serie:"))
        layout.addWidget(self.port_list)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.disconnect_button)
        layout.addWidget(QLabel("Estado de la conexión:"))
        layout.addWidget(self.status_label)
        layout.addWidget(self.checkbox_0)
        layout.addWidget(self.checkbox_1)
        layout.addWidget(self.checkbox_2)
        layout.addWidget(self.checkbox_3)
        layout.addWidget(self.checkbox_4)
        layout.addWidget(self.checkbox_5)
        self.setLayout(layout)     
        
        # Crear un temporizador para actualizar la lista de puertos cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_ports)
        self.timer.start(1000)

    def send_message(self, state, id_rel):
        message = ''
        if (id_rel == "0"):
            if state == Qt.Checked:
                message = '2'
            else:
                message = '8'
                
        if (id_rel == "1"):
            if state == Qt.Checked:
                message = '3'
            else:
                message = '9'
                
        if (id_rel == "2"):
            if state == Qt.Checked:
                message = '4'
            else:
                message = ':'  
                  
        if (id_rel == "3"):
            if state == Qt.Checked:
                message = '5'
            else:
                message = ';'
        
        if (id_rel == "4"):
            if state == Qt.Checked:
                message = '6'
            else:
                message = '<'
                
        if (id_rel == "5"):
            if state == Qt.Checked:
                message = '7'
            else:
                message = '='  
                
                
        # Envío del mensaje al dispositivo serial
        self.serial_port.write(message.encode('utf-8'))
        print("ID: " + id_rel + "Message: " + message)

        
    def refresh_ports(self):
        
        # Obtener la lista de puertos serie disponibles
        ports = serial.tools.list_ports.comports()

        # Obtener los puertos actualmente en la lista desplegable
        current_ports = [self.port_list.itemText(i) for i in range(self.port_list.count())]

        # Verificar si ha habido cambios en la lista de puertos
        if set(current_ports) != set([port.device for port in ports]):
            # Limpiar la lista desplegable
            self.port_list.clear()

            # Agregar los puertos a la lista desplegable
            for port in ports:
                self.port_list.addItem(port.device)

    def connect_serial(self):
        # Obtener el puerto serie seleccionado
        self.port = self.port_list.currentText()

        # Conectar al puerto serie seleccionado
        try:
            self.serial_port = serial.Serial(self.port)
            self.status_label.setText("Conectado al puerto {}".format(self.port))

            # Habilitar el botón de desconectar y deshabilitar el botón de conectar
            self.disconnect_button.setEnabled(True)
            self.connect_button.setEnabled(False)
            
            time.sleep(2)
            
            self.checkbox_0.setEnabled(True)
            self.checkbox_1.setEnabled(True)
            self.checkbox_2.setEnabled(True)
            self.checkbox_3.setEnabled(True)                        
            self.checkbox_4.setEnabled(True)
            self.checkbox_5.setEnabled(True)

        except serial.SerialException:
            self.status_label.setText("No se pudo conectar al puerto {}".format(self.port))

    def disconnect_serial(self):
        # Desconectar el puerto serie actualmente conectado
        if self.serial_port is not None:
            self.serial_port.close()
            self.serial_port = None
            self.status_label.setText("Desconectado")

            # Habilitar el botón de conectar y deshabilitar el botón de desconectar
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            
            self.checkbox_0.setEnabled(False)
            self.checkbox_1.setEnabled(False)
            self.checkbox_2.setEnabled(False)
            self.checkbox_3.setEnabled(False)                        
            self.checkbox_4.setEnabled(False)
            self.checkbox_5.setEnabled(False)
            


    def closeEvent(self, event):
        # Cerrar el puerto serie si está conectado antes de salir de la aplicación
        if self.serial_port is not None:
            self.disconnect_serial()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SerialGUI()
    gui.show()
    sys.exit(app.exec_())