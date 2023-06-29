import sys
import requests
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

app = QApplication(sys.argv)

image_url = "https://panela-cheia.s3.amazonaws.com/YhbsXRYzTaMsLLAH-profile-2.png"

# Cria um QLabel para exibir a imagem
label = QLabel()

# Define a escala da imagem para se ajustar ao tamanho do QLabel
label.setScaledContents(True)

# Carrega a imagem da URL
response = requests.get(image_url)
pixmap = QPixmap()
pixmap.loadFromData(response.content)

# Define a imagem no QLabel
label.setPixmap(pixmap)

# Cria um layout vertical e adiciona o QLabel a ele
layout = QVBoxLayout()
layout.addWidget(label)

# Cria um widget para ser a janela principal
window = QWidget()
window.setWindowTitle("Imagem Renderizada")
window.setWindowFlag(Qt.WindowStaysOnTopHint)  # Mantém a janela sempre no topo
window.setLayout(layout)
window.show()

sys.exit(app.exec_())