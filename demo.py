import URService as URS

ur=URS.urip("192.168.152.128") #robot ip 机器人IP
Dashboard=ur.UR_29999("robotmode")
send_data = f'''
def whf():
    popup("这是第一行")
    popup("这是第二行")
end
'''
ur_script=ur.UR_30003Script(send_data)
real_time=ur.UR_30003rt("Tool vector target") 