# my_esp32s3_st7789 — 自定义 ESP32-S3 + 2.4" ST7789 屏幕 + 麦克风/功放板型

针对裸 **ESP32-S3 + 2.4 英寸 ST7789（240×320）SPI 屏 + INMP441 麦克风 + MAX98357A 功放** 定制的最小板型，无外部编解码芯片，音频走纯 I2S。

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

## 音频接线（INMP441 麦克风 + MAX98357A 功放，纯 I2S）

| I2S 信号 | GPIO | 接到 |
|---|---|---|
| BCLK（位时钟） | GPIO4 | INMP441.SCK 与 MAX98357A.BCLK |
| WS（字选择/LRCK） | GPIO5 | INMP441.WS 与 MAX98357A.LRCK |
| DOUT（功放数据输出） | GPIO6 | MAX98357A.DIN |
| DIN（麦克风数据输入） | GPIO3 | INMP441.SD |

**INMP441 麦克风**：SCK→GPIO4、WS→GPIO5、SD→GPIO3；**L/R 接地**（选左声道）、VDD→3.3V、GND→GND。

**MAX98357A 功放**：BCLK→GPIO4、LRCK→GPIO5、DIN→GPIO6；**SD（关断）接 3.3V 常开**、GAIN 接地（默认增益）、VIN→5V、GND→GND，扬声器接 SPK+/SPK-。

> MCLK 未使用（MAX98357A 与 INMP441 都无需 MCLK）。音频端口为 I2S0、采样率 16000Hz、立体声。

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
- 音频设备 `audio_dac`/`audio_adc` 用 `chip: internal`（映射到 esp_codec_dev 的 dummy codec），配合 `CONFIG_CODEC_DUMMY_SUPPORT=y` 与 `CONFIG_ESP_BOARD_PERIPH_I2S_SUPPORT=y`；无需 `setup_device.c` 额外代码。
- `sdkconfig.defaults.board` 默认按 ESP32-S3 N8R8（8MB Flash + 8MB Octal PSRAM）配置；若你的模块 Flash/PSRAM 不同，需相应调整。
- edge_agent 框架需要 **ESP-IDF v5.5+**。
