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
import time

class SmallTrend(QtGui.QGraphicsView):
	def __init__(self, parent = None):
		self.bkgColor = QtGui.QColor(0x000000)
		self.axisColor = QtGui.QColor(0xffcc66)
		self.crvColor = QtGui.QColor(0x99ccff)
		
		QtGui.QGraphicsView.__init__(self,parent)
		
		self.maxDataSize = 20000
		self.xSpan = 100.0
		self.ySpan = 2.0
		self.xScale = (self.size().width() - 50) / self.xSpan		
		self.yScale = (self.size().height() - 50) / self.ySpan
		
		self.xData = np.zeros(self.maxDataSize)
		self.yData = np.zeros(self.maxDataSize)
		self.xData[0] = time.time()
		self.paintPath = QtGui.QPainterPath(QtCore.QPointF((self.xData[0]-self.xData[0])*self.xScale, self.yData[0]))
		self.dataPoly = QtGui.QPolygonF()
		self.dataPoly.append(QtCore.QPointF(0.01,0.0))
		self.dataPoly.append(QtCore.QPointF(self.xSpan,0))
		print self.dataPoly.at(0)
		print self.dataPoly.at(1)
		self.xPos = 0
		self.xNum = 1	
# 		self.xData[self.xPos]=time.time()	
# 		for p in range(self.xNum):
# 			index = p + self.xPos
# 			self.paintPath.lineTo((self.xData[self.xPos+p]-self.xData[0])*self.xScale, self.yData[self.xPos+p])
			
		self.curvePen = QtGui.QPen(self.crvColor)
		self.curvePen.setWidthF(0.1)
		crvFillColor = self.crvColor
#		crvFillColor = QtGui.QColor(0x3399ff)
		crvFillColor.setAlphaF(0.5)
		self.curveBrush = QtGui.QBrush(crvFillColor)
		self.curveBrush.setStyle = QtCore.Qt.SolidPattern
		self.axisPen = QtGui.QPen(self.axisColor)
		self.axisPen.setWidthF(1.5)
		self.axisBrush = QtGui.QBrush()
		self.axisBrush.setStyle = QtCore.Qt.NoBrush
		self.axisFont = QtGui.QFont('Segoe UI', 8)
		self.axisFont = QtGui.QFont('calibri', 8)
		self.axisFontHeight = QtGui.QFontMetricsF(self.axisFont).height()
		
		self.setMinimumWidth(50)
		self.setMinimumHeight(40)
		self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
 		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
 		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		
		self.axisRect = QtCore.QRectF(10.0, 10.0, self.size().width(), self.size().height())		
		self.viewRect = QtCore.QRectF(0,-0.01,self.xSpan,2*self.ySpan)
		
		self.graphicsScene = QtGui.QGraphicsScene()
		self.graphicsScene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(self.bkgColor)))
		self.scale(1,-1)
		self.scenePoly = self.graphicsScene.addPolygon(self.dataPoly, pen=self.curvePen, brush=self.curveBrush)
		self.scenePoly.setBrush(self.curveBrush)
		
		p2 = QtCore.QRectF(0,0,50,50)
#		self.graphicsScene.addRect(p2, pen=self.curvePen, brush = self.curveBrush)
	
		self.setScene(self.graphicsScene)
		self.fitInView(self.viewRect)
		
		
		print self.sceneRect()	
		
				
			
	def updateData(self, xNew, yNew):
		self.xPos += 1
		if self.xPos >= self.maxDataSize:
			self.xPos = 0
		self.xData[self.xPos]=xNew	
		self.yData[self.xPos]=yNew

		self.xNum += 1	
		if self.xNum > self.maxDataSize:
			self.xNum = self.maxDataSize

		poly = self.scenePoly.polygon()
		poly.replace(poly.count()-1, QtCore.QPointF(xNew - self.xData[0], yNew))
		poly.append(QtCore.QPointF(xNew - self.xData[0], 0))
		self.graphicsScene.removeItem(self.scenePoly)
		self.scenePoly = self.graphicsScene.addPolygon(poly, pen = self.curvePen, brush = self.curveBrush)
# 		p3 = QtGui.QPolygonF()
# 		p3.append(QtCore.QPointF(0.01,0.0))
# 		p3.append(QtCore.QPointF(0.01,50.0))
# 		p3.append(QtCore.QPointF(50.01,50.0))
# 		p3.append(QtCore.QPointF(50.01,0.0))
# 		self.graphicsScene.addPolygon(p3, pen=self.curvePen, brush=self.curveBrush)


		self.update()

# 		for ind in range(poly.count()):
# 			print poly.at(ind)

	def drawForeground(self, painter, rect):
		print "In drawForeground:"
		print rect.x(), rect.y()
 		axisOffset = 10
 		right = self.width()-2*axisOffset
 		bottom = self.height()-2*axisOffset
  		painter.setWorldMatrixEnabled(False)
  		painter.setRenderHint(QtGui.QPainter.Antialiasing)
  		painter.setPen(self.axisPen)
  		painter.setFont(self.axisFont)
  		painter.drawRect(axisOffset, axisOffset, right, bottom)
  		painter.drawText(axisOffset+2, bottom+axisOffset-2, str(self.xSpan))
  		s = str(self.ySpan)
  		painter.drawText(right-QtGui.QFontMetricsF(self.axisFont).width(s)+8, axisOffset+self.axisFontHeight-3, s)
 		
		
	
	def resizeEvent(self, e):
		self.xScale = self.size().width() / self.xSpan
		self.yScale = self.size().height() / self.ySpan
		print 'In resizeEvent: scale ', self.xScale, self.yScale
		print 'Extents: ', self.size().width(), self.size().height() 
		self.fitInView(self.viewRect)
		QtGui.QGraphicsView.resizeEvent(self, e)
		

		
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
		
		self.timer = QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateData)
		self.timer.start(500)
		
	def updateData(self):
		self.trendWidget.updateData(time.time(), np.random.rand())
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	myapp = TrendTest()
	myapp.show()
	sys.exit(app.exec_())	
