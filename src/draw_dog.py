import time
import logging
from cad_controller import CADController
from typing import Tuple, List

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dog_drawer')

class DogDrawer:
    def __init__(self):
        self.controller = CADController()
        # 启动CAD
        if not self.controller.is_running():
            logger.info("启动CAD...")
            success = self.controller.start_cad()
            if not success:
                logger.error("CAD启动失败")
                raise Exception("无法启动CAD")
            time.sleep(2)  # 等待CAD完全启动

    def create_layer_if_not_exists(self, layer_name: str):
        """创建图层（如果不存在）"""
        try:
            # 检查图层是否已存在
            for layer in self.controller.doc.Layers:
                if layer.Name == layer_name:
                    logger.info(f"图层 {layer_name} 已存在")
                    return True

            # 创建新图层
            new_layer = self.controller.doc.Layers.Add(layer_name)
            logger.info(f"已创建图层: {layer_name}")
            return True
        except Exception as e:
            logger.error(f"创建图层 {layer_name} 失败: {str(e)}")
            return False

    def draw_dog(self):
        """绘制一个简单的小狗图形"""
        try:
            # 设置绘图参数
            layer = "DOG_LAYER"
            color = 1  # 红色
            lineweight = 5

            # 创建图层
            self.create_layer_if_not_exists(layer)

            # 绘制身体（椭圆）
        body_center = (100, 100, 0)
        body_major_axis = 40
        body_minor_axis = 30
        self.controller.draw_ellipse(
            body_center, body_major_axis, body_minor_axis, rotation=0,
            layer=layer, color=color, lineweight=lineweight
        )

        # 绘制头部（圆）
        head_center = (140, 120, 0)
        head_radius = 20
        self.controller.draw_circle(
            head_center, head_radius, layer=layer, color=color, lineweight=lineweight
        )

        # 绘制耳朵（两个三角形）
        left_ear_points = [(130, 140, 0), (140, 155, 0), (150, 140, 0)]
        right_ear_points = [(150, 140, 0), (160, 155, 0), (170, 140, 0)]
        self.controller.draw_polyline(
            left_ear_points, closed=True, layer=layer, color=color, lineweight=lineweight
        )
        self.controller.draw_polyline(
            right_ear_points, closed=True, layer=layer, color=color, lineweight=lineweight
        )

        # 绘制眼睛（两个小圆）
        left_eye_center = (135, 125, 0)
        right_eye_center = (145, 125, 0)
        eye_radius = 2
        self.controller.draw_circle(
            left_eye_center, eye_radius, layer=layer, color=7, lineweight=lineweight
        )
        self.controller.draw_circle(
            right_eye_center, eye_radius, layer=layer, color=7, lineweight=lineweight
        )

        # 绘制鼻子（椭圆）
        nose_center = (140, 115, 0)
        nose_major_axis = 8
        nose_minor_axis = 5
        self.controller.draw_ellipse(
            nose_center, nose_major_axis, nose_minor_axis, rotation=0,
            layer=layer, color=7, lineweight=lineweight
        )

        # 绘制嘴巴（弧线）
        mouth_center = (140, 110, 0)
        mouth_radius = 8
        self.controller.draw_arc(
            mouth_center, mouth_radius, 0, 180, layer=layer, color=color, lineweight=lineweight
        )

        # 绘制腿（四条直线）
        leg_length = 15
        leg_width = 5

        # 前左腿
        front_left_leg_start = (90, 85, 0)
        front_left_leg_end = (90, 85 - leg_length, 0)
        self.controller.draw_line(
            front_left_leg_start, front_left_leg_end, layer=layer, color=color, lineweight=lineweight
        )

        # 前右腿
        front_right_leg_start = (110, 85, 0)
        front_right_leg_end = (110, 85 - leg_length, 0)
        self.controller.draw_line(
            front_right_leg_start, front_right_leg_end, layer=layer, color=color, lineweight=lineweight
        )

        # 后左腿
        back_left_leg_start = (70, 85, 0)
        back_left_leg_end = (70, 85 - leg_length, 0)
        self.controller.draw_line(
            back_left_leg_start, back_left_leg_end, layer=layer, color=color, lineweight=lineweight
        )

        # 后右腿
        back_right_leg_start = (130, 85, 0)
        back_right_leg_end = (130, 85 - leg_length, 0)
        self.controller.draw_line(
            back_right_leg_start, back_right_leg_end, layer=layer, color=color, lineweight=lineweight
        )

        # 绘制尾巴（多段线）
        tail_points = [(60, 100, 0), (40, 110, 0), (30, 105, 0)]
        self.controller.draw_polyline(
            tail_points, closed=False, layer=layer, color=color, lineweight=lineweight
        )

        # 缩放视图以显示所有对象
        self.controller.zoom_extents()

        print("小狗绘制完成！")
        return True

if __name__ == "__main__":
    try:
        drawer = DogDrawer()
        success = drawer.draw_dog()
        if success:
            logger.info("小狗绘制完成！")
        else:
            logger.error("小狗绘制失败")
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}", exc_info=True)