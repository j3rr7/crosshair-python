__author__ = 'Jere'

import sys
import time
import threading
from typing import Tuple

import theme
from config import Config
import pymeow as pm
import dearpygui.dearpygui as dpg

config = Config()


def gui():
    dpg.create_context()
    dpg.create_viewport(title="Config Editor", width=480, height=320, resizable=False, decorated=True)
    dpg.setup_dearpygui()

    # Menu Item Callback
    def callback_menu_overlayUpdate(src: any) -> None:
        config.settings()["overlay"]["updating"] = dpg.get_value(src)

    def callback_menu_overayDelay(src: any) -> None:
        config.settings()["overlay"]["delay"] = dpg.get_value(src)

    # Crosshair Settings
    def callback_crosshair_enabled(src: any) -> None:
        config.settings()["crosshair"]["enabled"] = dpg.get_value(src)

    def callback_crosshair_lineWidth(src: any) -> None:
        config.settings()["crosshair"]["lineWidth"] = dpg.get_value(src)

    def callback_crosshair_radius(src: any) -> None:
        config.settings()["crosshair"]["length"] = dpg.get_value(src)

    def callback_crosshair_color(src: any) -> None:
        config.settings()["crosshair"]["color"] = norm_color_to_float(dpg.get_value(src))

    # Utility Functions
    def norm_color_to_float(color: Tuple = (0, 0, 0, 0)) -> Tuple:
        return color[0] / 255, color[1] / 255, color[2] / 255

    def norm_color_to_int(color=None) -> list:
        if color is None:
            color = [0, 0, 0]
        return [int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)]

    light_theme = theme.create_theme_imgui_light()
    dpg.bind_theme(light_theme)

    with dpg.window(tag="Config Editor"):
        with dpg.menu_bar():
            with dpg.menu(label="Menu"):
                dpg.add_menu_item(label="Save", callback=lambda: config.save())
                dpg.add_menu_item(label="Load", callback=lambda: config.load())
                dpg.add_menu_item(label="Exit", callback=lambda: sys.exit(1))
            with dpg.menu(label="Overlay"):
                dpg.add_checkbox(label="Update (Don't Disable May Crash!!!)",
                                 default_value=bool(config.settings()["overlay"]["updating"]),
                                 callback=callback_menu_overlayUpdate)
                dpg.add_slider_int(label="delay",
                                   default_value=int(config.settings()["overlay"]["delay"]),
                                   min_value=0, max_value=120, callback=callback_menu_overayDelay)

        with dpg.collapsing_header(label="Crosshair"):
            dpg.add_checkbox(label="Enabled", default_value=True, callback=callback_crosshair_enabled)
            dpg.add_slider_float(label="Line Width",
                                 default_value=config.settings()["crosshair"]["lineWidth"],
                                 min_value=0.01, max_value=10,
                                 callback=callback_crosshair_lineWidth)
            dpg.add_slider_float(label="Length",
                                 default_value=config.settings()["crosshair"]["length"],
                                 min_value=0.1, max_value=1000,
                                 callback=callback_crosshair_radius)
            dpg.add_color_picker(label="Color", no_alpha=True,
                                 default_value=norm_color_to_int(config.settings()["crosshair"]["color"]),
                                 no_tooltip=True, no_label=True, no_inputs=True,
                                 picker_mode=dpg.mvColorPicker_wheel,
                                 display_type=dpg.mvColorEdit_float,
                                 callback=callback_crosshair_color)
    dpg.set_primary_window("Config Editor", True)
    dpg.show_viewport()
    # dpg.start_dearpygui()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    config.set_running(False)
    dpg.destroy_context()


def main():
    overlay = pm.overlay_init(exitKey=0x23)
    font = pm.font_init(10, "Tahoma")
    pm.overlay_set_title(str(config.settings()["overlay"]["title"]))

    x, y = overlay["midX"], overlay["midY"]

    while pm.overlay_loop(overlay,
                          update=config.settings()["overlay"]["updating"],
                          delay=config.settings()["overlay"]["delay"]):
        if pm.key_pressed(config.get_toggle_key()):
            pm.overlay_hide()
            time.sleep(0.1)

        if pm.key_pressed(config.get_exit_key()) or not config.is_running():
            break

        if config.settings()["crosshair"]["enabled"]:
            pm.line(x - config.settings()["crosshair"]["length"], y,
                    x + config.settings()["crosshair"]["length"], y,
                    lineWidth=config.settings()["crosshair"]["lineWidth"],
                    color=config.settings()["crosshair"]["color"]
                    )
            pm.line(x, y - config.settings()["crosshair"]["length"],
                    x, y + config.settings()["crosshair"]["length"],
                    lineWidth=config.settings()["crosshair"]["lineWidth"],
                    color=config.settings()["crosshair"]["color"]
                    )
        time.sleep(0.01)
    pm.overlay_deinit(overlay)


if __name__ == '__main__':
    gui_thread = threading.Thread(target=gui)
    gui_thread.start()
    main_thread = threading.Thread(target=main)
    main_thread.start()
