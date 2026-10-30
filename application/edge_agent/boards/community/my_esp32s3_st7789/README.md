# my_esp32s3_st7789 — 自定义 ESP32-S3 + 2.4" ST7789 屏幕板型

针对裸 **ESP32-S3 + 2.4 英寸 ST7789（240×320）SPI 屏** 定制的最小板型，只包含一块显示屏。

## 接线（推荐默认引脚）

| 屏引脚 | GPIO |
|---|---|
| SCLK（时钟） | GPIO12 |
| MOSI（数据） | GPIO11 |
| CS（片选） | GPIO10 |
| DC（数据/命令） | GPIO9 |
| RST（复位） | GPIO8 |
| BL（背光） | GPIO7（也可接 3.3V 常亮） |
| VCC | 3.3V |
| GND | GND |

> SPI 使用 SPI2_HOST。接线如与默认不同，请修改 `board_peripherals.yaml`（sclk/data0）和 `board_devices.yaml`（cs/dc/reset）中的引脚号。

## 云编译时如何选用本板

在 `application/edge_agent` 目录执行：

```bash
idf.py set-target esp32s3
idf.py bmgr -c ./boards -b my_esp32s3_st7789
idf.py build
```

`bmgr` 会生成板支持代码并把本目录（含 `setup_device.c` 的 ST7789 驱动初始化）编入固件。

## 说明

- 屏幕分辨率 240×320（竖屏），`invert_color: true`（常见 ST7789 需反转）。
- `setup_device.c` 提供 `lcd_panel_factory_entry_t`，包含标准 ST7789 初始化时序（0x11 睡眠退出、0x3A 像素格式 RGB565、伽马校正等）。
- `sdkconfig.defaults.board` 默认按 ESP32-S3 N8R8（8MB Flash + 8MB Octal PSRAM）配置；若你的模块 Flash/PSRAM 不同，需相应调整。
- edge_agent 框架需要 **ESP-IDF v5.5+**。
