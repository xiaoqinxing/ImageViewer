# 图片查看工具

这是一款能够对 常见格式的图片和 YUV 格式的图片进行查看、分析和对比的工具。支持任意组图片对比，可以随意增删画面对比窗口，支持统计信息的查看。

## 特色

1. 支持任意组图片对比，可以随意增删画面对比窗口
2. 支持统计信息的查看，有直方图信噪比等专业信息，同时通过框选，调整统计信息区域
3. 支持 YUV 格式的图片查看，和 jpg 一样的体验，同时可以转换成 jpg 格式，方便他人查看
4. 支持按照时间先后顺序，查看前后两张图片的跳转，方便图像细节的对比。即使新增文件，也能立刻识别。

## 使用方法

1. 可以通过点击打开图像的按钮或者拖动图片到图像显示框里进行显示
2. 通过保存按钮可以保存当前的图像(可是是图像处理前后的)
3. 通过 YUV 图像格式设置按钮，可以设置 YUV 的图像格式，用于正常显示图片
4. 通过点击图像统计分析按钮可以获取到整幅图像的统计信息，包括直方图，RGB 均值与信噪比，转成 YUV 之后的均值和信噪比，窗口大小，以及 RGB 增益
5. 统计信息窗口不关闭的情况下，框选图像中的任意一块区域，都可以显示这块区域的统计信息
6. 统计信息窗口中的直方图，显示了 RGB 和 Y 通道的直方图，可以通过复选框选择是否显示该通道的直方图
7. 点击增加和减少对比窗口可以增加或减少对比窗口，每个窗口可以独立操作和移动

## 界面

1. 右侧有四个按钮，分为为：打开图像，保存图像，设置 YUV 图像格式，删除图片，查看统计数据，查看上一张图片，查看下一章图片，向右翻转，增加对比窗口，减少对比窗口
2. 左下角会显示当前图像鼠标位置像素点的信息，包括 RGB 值以及缩放比例
3. 点击右侧按钮，查看统计信息，会跳出统计信息窗口，可以通过框选，调整显示区域
4. 点击增加和减少对比窗口可以增加或减少对比窗口，如图，创建了 3 个对比窗口

![yuv查看工具](https://github.com/xiaoqinxing/ImageViewer/raw/main/test/resource/8.png)

![统计信息窗口](https://github.com/xiaoqinxing/ImageViewer/raw/main/test/resource/7.png)

## 将要实现的功能点

- [x] 能够支持常见的 yuv 格式
- [x] 打开或者拖动的时候，会提示选取 yuv 格式，并保存最近一次格式
- [x] 能够保存成 jpg 格式
- [x] 能够通过鼠标对图片放大和缩小
- [x] 能够通过鼠标对像素点的信息进行显示
- [x] 能够通过直方图等统计分析对选中区域进行分析
- [x] 能够支持多张图片对比，按+号，可以添加图片窗口
- [ ] 多张图片拖动与放大应该保持一致
- [ ] 能够支持批量 yuv 图片转换成 jpg 的功能
- [x] 能够按上下键去查看上下的 yuv
- [ ] 能够支持多帧 yuv 的解析，通过数字或者滑动条去选择相应帧的图片显示
- [ ] 支持多张图片的偏移调整
