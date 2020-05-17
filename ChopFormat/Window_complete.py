from untitled import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from Custom_widgets import PainterLabel
import types
from Crop_handler import *
from PIL import Image

class CMWindow(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        super().__init__(MainWindow)
        self.UI_obj = Ui_MainWindow()
        self.UI_obj.setupUi(MainWindow)
        self.color_dict = {'Blue': (0, 0, 255), 'Red': (255, 0, 0), 'Orange': (255, 127, 25)}
        self.UI_obj.fullimg = PainterLabel(5)
        self.UI_obj.patch_group = {}
        self.UI_obj.HR_group ={}
        self.UI_obj.set_root.clicked.connect(self.setRoot)
        self.UI_obj.show_Fullimg.clicked.connect(self.show_Full_img)
        self.UI_obj.set_Saveroot_bt.clicked.connect(self.setSave)
        self.UI_obj.crop_viewbt.clicked.connect(self.cropView)
        self.UI_obj.save_finalbt.clicked.connect(self.saveAll_results)
        self.UI_obj.patchTab.currentChanged['int'].connect(self.add_Tab)
        self.UI_obj.tab_1 = QtWidgets.QScrollArea(self.UI_obj.patchTab)
        self.UI_obj.tab_2 = QtWidgets.QScrollArea(self.UI_obj.patchTab)
        self.UI_obj.patchTab.addTab(self.UI_obj.tab_1, 'Patch Group 1')
        self.UI_obj.patchTab.addTab(self.UI_obj.tab_2, '+')
        self.UI_obj.fullimg.installEventFilter(self)
        self.UI_obj.patchTab.installEventFilter(self)
        self.UI_obj.fullimg.drawRecFlag = False

    def setRoot(self):
        dir_root_path = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                              "choose directory",
                                                              "E:/Workplace/visuals/AIM")
        if dir_root_path:
            self.UI_obj.imgDirRoot.addItem(dir_root_path)
            self.UI_obj.imgDirRoot.setFont(QtGui.QFont('Times', 11))
            self.UI_obj.imgDirRoot.setCurrentText(dir_root_path)
            self.subdirs = os.listdir(dir_root_path)
            # subdirs_with_index = \
            #     [str(i+1) + '-' + subdirs[i] for i in range(len(subdirs))]
            self.UI_obj.sub_dir_list.clear()
            self.UI_obj.sub_dir_list.addItems(self.subdirs)
            self.UI_obj.sub_dir_list.setFont(QtGui.QFont('Times', 11))
            img_list = os.listdir(os.path.join(dir_root_path, 'HR'))
            self.UI_obj.img_list.clear()
            self.UI_obj.img_list.addItems(img_list)
            self.UI_obj.img_list.setFont(QtGui.QFont('Times', 11))


    def show_Full_img(self):
        s = os.path.join(str(self.UI_obj.imgDirRoot.currentText()),
                         str(self.UI_obj.sub_dir_list.currentText()),
                         str(self.UI_obj.img_list.currentText()))
        self.HR_path = os.path.join(self.UI_obj.imgDirRoot.currentText(), 'HR', self.UI_obj.img_list.currentText())
        if self.UI_obj.img_list.currentText():
            self.pixmap = QtGui.QPixmap(s)
            self.UI_obj.fullimg.setPixmap(self.pixmap)
            self.UI_obj.fullimg.adjustSize()
            self.UI_obj.fullimg_window.setBackgroundRole(QtGui.QPalette.Dark)
            self.UI_obj.fullimg_window.setWidget(self.UI_obj.fullimg)
            self.UI_obj.fullimg.setMouseTracking(True)
            self.UI_obj.fullimg.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        else:
            QtWidgets.QMessageBox.warning(self,
                                          "Warning", "Please choose the Image Dir root first",
                                          QtWidgets.QMessageBox.Cancel)

    def setSave(self):
        dir_root_path = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                                   "choose directory",
                                                                   "E:/Workplace/visuals/Cropped_for_paper")
        if dir_root_path:
                self.UI_obj.saveDirRoot.addItem(dir_root_path)
                self.UI_obj.saveDirRoot.setFont(QtGui.QFont('Times', 11))



    def cropView(self):
        left, upper, h, w = self.UI_obj.fullimg.getRect()

        resize_flag = self.UI_obj.resize_combobox.currentText()

        cropped_img_dict = {}
        for subdir in self.subdirs:
            cropped_imgs, resize = crop(self.UI_obj.imgDirRoot.currentText(), subdir, self.UI_obj.img_list.currentText(),
                                left, upper, h, w,
                                self.color_dict[self.UI_obj.edge_colorcbox.currentText()], self.UI_obj.edgeWidthLine.text(),
                                resize_flag)
            cropped_img_dict[subdir] = cropped_imgs


        HR_wRect = draw_HRrec(self.HR_path,
                              left, upper, h, w, self.color_dict[self.UI_obj.edge_colorcbox.currentText()], self.UI_obj.edgeWidthLine.text())


        content_widget = QtWidgets.QWidget()
        flay = QtWidgets.QGridLayout(content_widget)
        layout_idx, caption_idx = 0, 0
        tp_subdir = []
        for subdir in self.subdirs:
            p = cropped_img_dict[subdir]
            object = QtWidgets.QLabel('Text')
            object_label = QtWidgets.QLabel(subdir)
            object.setFixedSize(resize[0], resize[1])
            object_label.setFixedWidth(resize[1])
            object_label.setAlignment(QtCore.Qt.AlignCenter)
            qImg = QtGui.QImage(p.data, p.shape[1], p.shape[0], p.shape[1] * 3, QtGui.QImage.Format_RGB888)
            img = QtGui.QPixmap.fromImage(qImg).scaled(resize[0], resize[1])
            object.setPixmap(img)
            flay.addWidget(object, layout_idx // 3, layout_idx % 3)
            flay.addWidget(object_label, (layout_idx // 3) + 1, layout_idx % 3)
            tp_subdir.append(subdir)
            layout_idx += 1
            if (layout_idx // 3) % 2 == 1:
                layout_idx += 3

        showCrop_Position = QtWidgets.QPushButton(self.UI_obj.patchTab.currentWidget())
        showCrop_Position.setFixedSize(resize[0], resize[1])
        showCrop_Position.setText('Show crop positions \n in HR size')
        flay.addWidget(showCrop_Position, layout_idx // 3, layout_idx % 3)

        cropped_img_dict['HR_rect'] = HR_wRect
        self.UI_obj.patchTab.currentWidget().setWidget(content_widget)
        showCrop_Position.clicked.connect(self.show_crop_Pos)
        self.UI_obj.patch_group[self.UI_obj.patchTab.tabText(self.UI_obj.patchTab.currentIndex())] = cropped_img_dict
        self.UI_obj.HR_group[self.UI_obj.patchTab.tabText(self.UI_obj.patchTab.currentIndex())] = \
            {'Crop_position': (left, upper, h, w), 'Color_digits': self.color_dict[self.UI_obj.edge_colorcbox.currentText()],
             'Edge_width': self.UI_obj.edgeWidthLine.text(), 'Color_text': self.UI_obj.edge_colorcbox.currentText()}



    def show_crop_Pos(self):
        HR_wRect = self.UI_obj.patch_group[self.UI_obj.patchTab.tabText(self.UI_obj.patchTab.currentIndex())]['HR_rect']
        HR_window = QtWidgets.QDialog(self.UI_obj.patchTab)
        HR_img = QtWidgets.QLabel(HR_window)
        qImg = QtGui.QImage(HR_wRect.data, HR_wRect.shape[1], HR_wRect.shape[0], HR_wRect.shape[1] * 3, QtGui.QImage.Format_RGB888)
        img = QtGui.QPixmap.fromImage(qImg).scaled(HR_wRect.shape[1]/4, HR_wRect.shape[0]/4)
        HR_img.setPixmap(img)
        HR_window.setFixedSize(HR_wRect.shape[1]/4, HR_wRect.shape[0]/4)
        HR_window.show()


    def add_Tab(self):
        num_tab = self.UI_obj.patchTab.currentIndex()

        if self.UI_obj.patchTab.tabText(num_tab) == '+':
            self.UI_obj.new_tab = QtWidgets.QScrollArea()
            self.UI_obj.new_tab.setObjectName('tab_{}'.format(num_tab - 1))

            self.UI_obj.new_tab.setGeometry(self.UI_obj.tab_1.geometry())
            self.UI_obj.new_tab.setWidgetResizable(True)
            self.UI_obj.patchTab.insertTab(num_tab, self.UI_obj.new_tab, 'Patch Group {}'.format(num_tab+1))
            self.UI_obj.patchTab.setCurrentIndex(num_tab)


    def saveAll_results(self):

        if self.UI_obj.saveDirRoot:

            HR_img = np.array(Image.open(self.HR_path))
            img_name = os.path.basename(self.HR_path).split('.')[0]
            save_path_root = self.UI_obj.saveDirRoot.currentText()
            for hr_info in self.UI_obj.HR_group:
                left, upper, h, w = self.UI_obj.HR_group[hr_info]['Crop_position']
                color, edge_width = self.UI_obj.HR_group[hr_info]['Color_digits'], self.UI_obj.HR_group[hr_info]['Edge_width']
                HR_img = cv2.rectangle(HR_img, (left, upper), (left + h, upper + w), color, thickness=int(edge_width))


            pil = Image.fromarray(HR_img)
            img_name_format = '{}_{}_{}.png'.format(img_name, 'HR', 'Full_img')
            pil.save(os.path.join(save_path_root, img_name_format))

            for pg in self.UI_obj.patch_group:
                color_text = self.UI_obj.HR_group[pg]['Color_text']
                for subdir in self.UI_obj.patch_group[pg]:
                    if subdir != 'HR_rect':
                        pil = Image.fromarray(self.UI_obj.patch_group[pg][subdir])
                        img_name_format = '{}_{}_{}.png'.format(img_name, subdir, color_text)
                        pil.save(os.path.join(save_path_root, img_name_format))
        else:

            QtWidgets.QMessageBox.warning(self,
                                          "Warning", "Please choose the Save Dir root first",
                                          QtWidgets.QMessageBox.Cancel)




    def eventFilter(self, QObject, QEvent):
        if QObject == self.UI_obj.fullimg:
            if QEvent.type() == QtGui.QMouseEvent.MouseMove:
                self.UI_obj.statusBar.showMessage(
                    'Image size: {}, {}, current position: {}, {}'
                    .format(self.UI_obj.fullimg.frameGeometry().height(),
                            self.UI_obj.fullimg.frameGeometry().width(),
                            QEvent.y(),
                            QEvent.x()))
                return False
        return False








# class MouseTracker(QtWidgets.QWidget):
#     def __init__(self, img, pl):
#         super().__init__()
#         self.label = QtWidgets.QLabel(self)
#         self.label.resize(200, 40)
#         self.setMouseTracking(True)
#
#
#     def mouseMoveEvent(self, event):
#         self.label.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))
#         # return 1