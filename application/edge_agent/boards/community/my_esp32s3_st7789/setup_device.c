/*
 * ST7789 panel factory entry used by the board manager generated code.
 */
#include "esp_lcd_panel_st7789.h"

esp_err_t lcd_panel_factory_entry_t(esp_lcd_panel_io_handle_t io,
                                    const esp_lcd_panel_dev_config_t *panel_dev_config,
                                    esp_lcd_panel_handle_t *ret_panel)
{
    return esp_lcd_new_panel_st7789(io, panel_dev_config, ret_panel);
}
