# 图片查看工具

这是一款能够对 常见格式的图片和 YUV 格式的图片进行查看、分析和对比的工具

## 背景

1. 经常需要抓取 yuv，又没有比较好的工具，能够打开比较多的格式，并且保存成 jpg
2. 多张 yuv 之间的对比也比较麻烦
3. 缺乏 yuv 的分析工具

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
