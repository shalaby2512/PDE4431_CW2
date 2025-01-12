# Type help("robodk.robolink") or help("robodk.robomath") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/robodk.html
# Note: It is not required to keep a copy of this file, your Python script is saved with your RDK project

# You can also use the new version of the API:
from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
import time
from robodk import *      # RoboDK API
from robolink import *    # Robot toolbox

RDK = robolink.Robolink()
coursework_bot = RDK.Item('Epson VT6')
coursework_bot.setSpeed(100)

# variables and location teaching start

# programs

gripper_open_function = RDK.Item('gripper_open', itemtype=ITEM_TYPE_PROGRAM)
gripper_close_function = RDK.Item('gripper_close', itemtype=ITEM_TYPE_PROGRAM)
gripper_grip_function = RDK.Item('gripper_grip', itemtype=ITEM_TYPE_PROGRAM)
attach_to_tool = RDK.Item('attach_to_tool', itemtype=ITEM_TYPE_PROGRAM)
detach_from_tool = RDK.Item('detach_from_tool', itemtype=ITEM_TYPE_PROGRAM)
replace_all_cones = RDK.Item('replace_all_cones', itemtype=ITEM_TYPE_PROGRAM)

# frames for pickup and drop
feed_frame = RDK.Item('feed_frame')
outfeed_frame = RDK.Item('drop_frame')
gripper_tool = coursework_bot.Childs()[0]

# Cone pick up station locations
cone1_pickup_loc = RDK.Item('cone1_pickup_point')
cone2_pickup_loc = cone1_pickup_loc.Pose() * transl(0,-120, 0)
cone3_pickup_loc = cone1_pickup_loc.Pose() * transl(0,-240, 0)
cone4_pickup_loc = cone1_pickup_loc.Pose() * transl(0,0, 120)
cone5_pickup_loc = cone1_pickup_loc.Pose() * transl(0,-120, 120)
cone6_pickup_loc = cone1_pickup_loc.Pose() * transl(0,-240, 120)

# cone drop locations
cone1_drop_loc = RDK.Item('cone1_drop_position', itemtype=ITEM_TYPE_TARGET)
cone2_drop_loc = RDK.Item('cone2_drop_position', itemtype=ITEM_TYPE_TARGET)
cone3_drop_loc = RDK.Item('cone3_drop_position', itemtype=ITEM_TYPE_TARGET)
cone4_drop_loc = RDK.Item('cone4_drop_position', itemtype=ITEM_TYPE_TARGET)
cone5_drop_loc = RDK.Item('cone5_drop_position', itemtype=ITEM_TYPE_TARGET)
cone6_drop_loc = RDK.Item('cone6_drop_position', itemtype=ITEM_TYPE_TARGET)


# points for movement
home_pos = RDK.Item('Home_pos')
cone_pickup_approach_point = RDK.Item('cone_pickup_approach_pt')
safe_point = RDK.Item('safe_point')
filling_station_approach_point = RDK.Item('filling_station_approach_point')
filling_curve_approach = RDK.Item('filling_curve_approach')
filling_station_exit = RDK.Item('filling_station_exit')
filling_station_exit_high = RDK.Item('filling_station_exit_high')
drop_station_approach_high = RDK.Item('drop_station_approach_high')

# curve points for filling station
filling_station_first_curve = RDK.Item('filling_station_first_curve')
filling_station_first_curve_end = RDK.Item('filling_station_first_curve_end')
filling_station_second_curve_mid = RDK.Item('filling_station_second_curve_mid')
filling_station_second_curve_end = RDK.Item('filling_station_second_curve_end')

# variables and location teaching end

# main execution starts here

pickup_positions = [cone1_pickup_loc, cone2_pickup_loc, cone3_pickup_loc, cone4_pickup_loc, cone5_pickup_loc, cone6_pickup_loc]
drop_locations = [cone1_drop_loc, cone2_drop_loc, cone3_drop_loc, cone4_drop_loc, cone5_drop_loc, cone6_drop_loc]
cone_list = ['Cone1', 'Cone2', 'Cone3', 'Cone4', 'Cone5', 'Cone6']
replace_all_cones.RunCode()
for i in range(6):
    coursework_bot.MoveJ(home_pos)
    gripper_open_function.RunCode()
    coursework_bot.MoveJ(cone_pickup_approach_point)
    coursework_bot.MoveL(pickup_positions[i])
    gripper_grip_function.RunCode()
    # attach_to_tool.RunCode()
    attach_object = RDK.Item(cone_list[i])
    curr_pose = attach_object.PoseAbs()
    attach_object.setParent(gripper_tool)
    attach_object.setPoseAbs(curr_pose)
    coursework_bot.MoveL(cone_pickup_approach_point)
    coursework_bot.MoveJ(safe_point)
    coursework_bot.MoveJ(filling_station_approach_point)
    coursework_bot.MoveJ(filling_curve_approach)
    coursework_bot.MoveC(filling_station_first_curve, filling_station_first_curve_end)
    coursework_bot.MoveC(filling_station_second_curve_mid, filling_station_second_curve_end)
    coursework_bot.MoveL(filling_station_exit)
    coursework_bot.MoveL(filling_station_exit_high)
    coursework_bot.MoveJ(safe_point)
    coursework_bot.MoveJ(drop_station_approach_high)
    # if i == 4 or i == 5:
    #     coursework_bot.MoveJ(drop_locations[i])
    # else:
    coursework_bot.MoveJ(drop_locations[i])
    detach_from_tool.RunCode()
    print(cone_list[i])
    detach_object = RDK.Item(cone_list[i])
    drop_pose = detach_object.PoseAbs()
    print(drop_pose)
    detach_object.setParent(outfeed_frame)
    detach_object.setPoseAbs(drop_pose)
    gripper_open_function.RunCode()
    coursework_bot.MoveJ(drop_station_approach_high)
    gripper_close_function.RunCode()
    coursework_bot.MoveJ(home_pos)