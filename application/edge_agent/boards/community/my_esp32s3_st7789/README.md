# my_esp32s3_st7789 — ESP32-S3 + 2.4" ST7789（7pin）+ INMP441 + MAX98357A

裸 ESP32-S3 开发板外接 2.4 英寸 ST7789 SPI 屏（240×320，7 引脚、无 BL 背光调节脚）、
INMP441 I2S 麦克风、MAX98357A I2S 功放，无编解码芯片，音频走纯 I2S。

## 屏幕接线（SPI2_HOST）

| 屏引脚 | GPIO |
|---|---|
| SCLK | GPIO12 |
| MOSI / SDA | GPIO11 |
| CS | GPIO10 |
| DC | GPIO9 |
| RST | GPIO8 |
| BL 背光 | 直接接 3.3V（常亮，固件不控制） |

## 音频接线

MAX98357A（喇叭，I2S 端口 1，ESP 为主时钟）：

| 信号 | GPIO |
|---|---|
| BCLK | GPIO15 |
| LRCK / WS | GPIO16 |
| DIN | GPIO7 |

INMP441（麦克风，I2S 端口 0，ESP 为主时钟）：

| 信号 | GPIO |
|---|---|
| SCK / BCLK | GPIO4 |
| WS | GPIO5 |
| SD | GPIO3 |

> 麦克风和功放必须挂在**不同的 I2S 控制器**上，因此 BCLK/WS 不能共用。
> INMP441 的 L/R 接地（选左声道），VDD 接 3.3V；MAX98357A 的 SD 接 3.3V 常开、GAIN 接地。

## 编译

```bash
cd application/edge_agent
idf.py bmgr -c ./boards -b my_esp32s3_st7789
idf.py build
```

`bmgr` 会自动选定 esp32s3 目标、生成板级代码并写入 sdkconfig 选项（不需要 `idf.py set-target`）。

## 说明

- 默认按 Flash 8MB + 8MB Octal PSRAM（N8R8）配置。若模块是 N8R2 或没有 PSRAM，请改
  `sdkconfig.defaults.board`：`CONFIG_SPIRAM_MODE_OCT=y` → `CONFIG_SPIRAM_MODE_QUAD=y`；
  没有 PSRAM 则删掉三行 `CONFIG_SPIRAM*`。
- 屏幕 240×320 竖屏，`invert_color: true`。
- `setup_device.c` 只提供 `lcd_panel_factory_entry_t`，初始化时序由 `esp_lcd_panel_st7789` 驱动完成。
