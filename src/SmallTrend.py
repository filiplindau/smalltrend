# -*- coding:utf-8 -*-
"""
Created on Aug 26, 2013

@author: Filip
"""
import numpy as np
import PyTango as pt
import pyqtgraph as pq
from PyQt4 import QtGui, QtCore
import sys

class SmallTrend(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self,parent)
		
		self.maxDataSize = 2000
		self.xSpan = 200.0
		self.ySpan = 30.0
		self.xScale = self.size().width() / self.xSpan
		self.yScale = self.size().height() / self.ySpan
		
		self.xData = np.zeros(self.maxDataSize)
		self.yData = np.zeros(self.maxDataSize)
		self.paintPath = QtGui.QPainterPath(QtCore.QPointF(self.xData[0], self.yData[0]))
		self.xPos = 1		
		for p in range(self.xPos):
			self.paintPath.lineTo(self.xData[p], self.yData[p])
			
		self.curvePen = QtGui.QPen(QtGui.QColor(0x99ccff))
		self.curvePen.setWidthF(1.3)
		self.axisPen = QtGui.QPen(QtGui.QColor(0xffcc66))
		self.axisPen.setWidthF(1.0)
		
		self.setMinimumWidth(200)
		self.setMinimumHeight(200)
				
			
	def updateData(self, xNew, yNew):
		pass
		
	def paintEvent(self, e):
		qp = QtGui.QPainter()
		qp.begin(self)
		qp.setRenderHint(QtGui.QPainter.Antialiasing)
		qp.setPen(QtCore.Qt.blue)
		qp.drawPath(self.paintPath)
		qp.end()
		
class TrendTest(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)

		self.deviceName = 'testfel/gunlaser/finesse'
	
		self.deviceFinesse = pt.DeviceProxy(self.deviceName)

		layout = QtGui.QVBoxLayout(self)
		self.trendWidget = SmallTrend()
		label = QtGui.QLabel(''.join(('Trending ', self.deviceName)))
		layout.addWidget(label)
		layout.addWidget(self.trendWidget)
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	myapp = TrendTest()
	myapp.show()
	sys.exit(app.exec_())	
